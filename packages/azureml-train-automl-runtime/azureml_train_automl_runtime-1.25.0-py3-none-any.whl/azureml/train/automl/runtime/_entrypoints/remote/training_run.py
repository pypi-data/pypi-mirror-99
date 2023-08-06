# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""Methods for AutoML remote runs."""
import logging
from datetime import datetime
from typing import Any, Dict, cast

from azureml._tracing import get_tracer
from azureml.automl.core._run import run_lifecycle_utilities
from azureml.automl.core.shared.telemetry_activity_logger import TelemetryActivityLogger
from azureml.core import Run
from azureml.train.automl.runtime._automl_job_phases import TrainingIterationPhase, TrainingIterationParams
from azureml.train.automl.runtime._entrypoints import entrypoint_util, training_entrypoint_util
from azureml.train.automl.runtime._azureautomlruncontext import AzureAutoMLRunContext

logger = logging.getLogger(__name__)
activity_logger = TelemetryActivityLogger()
tracer = get_tracer(__name__)


def execute(
        script_directory: str,
        automl_settings: str,
        run_id: str,
        training_percent: float,
        iteration: int,
        pipeline_spec: str,
        pipeline_id: str,
        dataprep_json: str,
        entry_point: str,
        **kwargs: Any
) -> Dict[str, Any]:
    """
    Driver script that runs one child iteration
    using the given pipeline spec for the remote run.
    """
    current_run = Run.get_context()
    result = {}  # type: Dict[str, Any]
    try:
        print("{} - INFO - Beginning driver wrapper.".format(datetime.now().__format__('%Y-%m-%d %H:%M:%S,%f')))
        logger.info('Beginning AutoML remote driver for run {}.'.format(run_id))

        parent_run, automl_settings_obj, cache_store = entrypoint_util.init_wrapper(
            current_run, automl_settings, script_directory, **kwargs)

        if automl_settings_obj.enable_streaming:
            entrypoint_util.modify_settings_for_streaming(automl_settings_obj, dataprep_json)

        dataset = entrypoint_util.load_data_from_cache(cache_store)
        onnx_cvt = training_entrypoint_util.load_onnx_converter(automl_settings_obj, cache_store, parent_run.id)

        automl_run_context = AzureAutoMLRunContext(current_run)
        automl_run_context.set_local(False)

        fit_output = TrainingIterationPhase.run(
            automl_parent_run=parent_run,
            automl_run_context=automl_run_context,
            training_iteration_params=TrainingIterationParams(automl_settings_obj),
            dataset=dataset,
            onnx_cvt=onnx_cvt,
            pipeline_id=pipeline_id,
            pipeline_spec=pipeline_spec,
            training_percent=training_percent,
        )
        result = fit_output.get_output_dict()
        if fit_output.errors:
            for fit_exception in fit_output.errors.values():
                if fit_exception.get("is_critical"):
                    exception = cast(BaseException, fit_exception.get("exception"))
                    raise exception.with_traceback(exception.__traceback__)
    except Exception as e:
        logger.error("AutoML driver_wrapper script terminated with an exception of type: {}".format(type(e)))
        run_lifecycle_utilities.fail_run(current_run, e)
        raise

    return result
