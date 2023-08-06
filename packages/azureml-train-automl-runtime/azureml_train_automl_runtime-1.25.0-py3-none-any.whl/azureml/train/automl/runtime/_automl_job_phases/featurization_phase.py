# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import logging
from typing import Any, Dict, Optional, Union

from azureml.automl.runtime._data_definition import RawExperimentData
from scipy import sparse

from azureml._tracing._tracer_factory import get_tracer
from azureml.automl.core._experiment_observer import ExperimentObserver
from azureml.automl.core._run import RunType
from azureml.automl.core.automl_base_settings import AutoMLBaseSettings
from azureml.automl.core.shared import constants, logging_utilities, reference_codes
from azureml.automl.core.shared._diagnostics.contract import Contract
from azureml.automl.runtime import training_utilities
from azureml.automl.runtime._feature_sweeped_state_container import FeatureSweepedStateContainer
from azureml.automl.runtime._featurization_orchestration import orchestrate_featurization
from azureml.automl.runtime._runtime_params import ExperimentControlSettings, ExperimentDataSettings
from azureml.automl.runtime.data_context import TransformedDataContext, DataContextParams
from azureml.automl.runtime.faults_verifier import VerifierManager
from azureml.automl.runtime.shared.cache_store import CacheStore
from azureml.automl.runtime.shared.datasets import DatasetBase
from azureml.automl.runtime.streaming_data_context import StreamingTransformedDataContext
from azureml.core import Run
from azureml.train.automl._automl_feature_config_manager import AutoMLFeatureConfigManager

from azureml.train.automl.runtime import _problem_info_utils
from azureml.train.automl.runtime._automl_job_phases.utilities import PhaseUtil

logger = logging.getLogger(__name__)
tracer = get_tracer(__name__)


class FeaturizationPhase:
    """AutoML job phase that featurizes the data."""

    @staticmethod
    def run(
        parent_run_id: str,
        automl_settings: AutoMLBaseSettings,
        cache_store: CacheStore,
        current_run: RunType,
        experiment_observer: ExperimentObserver,
        feature_config_manager: AutoMLFeatureConfigManager,
        feature_sweeped_state_container: Optional[FeatureSweepedStateContainer],
        raw_experiment_data: RawExperimentData,
        subsample_cache_strategy: str,
        verifier: VerifierManager
    ) -> DatasetBase:
        """
        Run the featurization phase. This function assumes the data (raw_experiment_data) is already validated before.

        If featurization is enabled, data will be featurized. A data snapshot is taken to be used
        as input sample for inference. Problem info is set.

        Depending on the scenario, this phase will be called from a ParentRun, SetupRun, or FeaturizationRun.

        :param parent_run_id: The id of the current_run's parent.
        :param raw_experiment_data: Data inputs to the experiment.
        :param automl_settings: Object containing AutoML settings as specified by user.
        :param cache_store: The cache store.
        :param current_run: The current run.
        :param experiment_observer: The experiment observer.
        :param feature_config_manager: The feature config manager.
        :param feature_sweeped_state_container: The feature sweeped state container.
        :param subsample_cache_strategy: The SubsampleCacheStrategy to use for subsampling.
            SubsampleCacheStrategy.Classic should be used on remote, else use SubsampleCacheStrategy.Preshuffle
        :param verifier: The fault verifier manager.
        :return: The transformed data context (after the problem info has been set)
        """
        # Transform raw input and save to cache store.
        logger.info("AutoML featurization for run {}.".format(current_run.id))

        with logging_utilities.log_activity(logger=logger, activity_name="Getting transformed data context."):
            # TODO: Make the caller pass in the RawDataContext into this method.
            raw_data_context = PhaseUtil.build_raw_data_context(raw_experiment_data,
                                                                DataContextParams(automl_settings))
            logger.info("Using {} for caching transformed data.".format(type(cache_store).__name__))
            with logging_utilities.log_activity(
                logger=logger,
                activity_name="Beginning full featurization logic."
            ):
                feature_sweeping_config = feature_config_manager.get_feature_sweeping_config(
                    enable_feature_sweeping=automl_settings.enable_feature_sweeping,
                    parent_run_id=parent_run_id,
                    task_type=automl_settings.task_type
                )

                # TODO: break down featurization span more
                with tracer.start_as_current_span(
                        constants.TelemetryConstants.SPAN_FORMATTING.format(
                            constants.TelemetryConstants.COMPONENT_NAME, constants.TelemetryConstants.FEATURIZATION
                        ),
                        user_facing_name=constants.TelemetryConstants.FEATURIZATION_USER_FACING
                ):
                    td_ctx = orchestrate_featurization(
                        automl_settings.enable_streaming,
                        automl_settings.is_timeseries,
                        automl_settings.path,
                        raw_data_context,
                        cache_store,
                        verifier,
                        experiment_observer,
                        feature_sweeping_config,
                        feature_sweeped_state_container
                    )

        Contract.assert_value(
            td_ctx,
            "transformed_data_context",
            reference_code=reference_codes.ReferenceCodes._FEATURIZATION_PHASE_MISSING_TDCTX,
            log_safe=True
        )

        logger.info("Setting problem info.")
        _problem_info_utils.set_problem_info(
            td_ctx.X,
            td_ctx.y,
            enable_subsampling=automl_settings.enable_subsampling or False,
            enable_streaming=automl_settings.enable_streaming,
            current_run=current_run,
            transformed_data_context=td_ctx,
            cache_store=cache_store
        )

        return training_utilities.init_dataset(
            transformed_data_context=td_ctx,
            cache_store=cache_store,
            task_type=automl_settings.task_type,
            experiment_data_settings=ExperimentDataSettings(automl_settings),
            subsample_cache_strategy=subsample_cache_strategy,
            init_all_stats=False,
            keep_in_memory=False)
