# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
"""This is the entry point into SDK for all remote runs"""

from typing import Any, Dict, List, Optional
from azureml.automl.core.constants import PreparationRunTypeConstants

from azureml.train.automl.runtime._entrypoints import local_managed_entrypoint
from azureml.train.automl.runtime._entrypoints import remote_batch_training_run_entrypoint
from azureml.train.automl.runtime._entrypoints import remote_explain_run_entrypoint
from azureml.train.automl.runtime._entrypoints import remote_featurization_fit_run_entrypoint
from azureml.train.automl.runtime._entrypoints import remote_featurization_run_entrypoint
from azureml.train.automl.runtime._entrypoints import remote_setup_run_entrypoint
from azureml.train.automl.runtime._entrypoints import remote_test_run_entrypoint
from azureml.train.automl.runtime._entrypoints import remote_training_run_entrypoint


def setup_wrapper(
        script_directory: Optional[str],
        dataprep_json: str,
        entry_point: str,
        automl_settings: str,
        prep_type: str = PreparationRunTypeConstants.SETUP_ONLY,
        **kwargs: Any
) -> None:
    """entry point for setup run"""
    remote_setup_run_entrypoint.execute(
        script_directory,
        dataprep_json,
        entry_point,
        automl_settings,
        prep_type,
        **kwargs)


def featurization_wrapper(
        script_directory: Optional[str],
        dataprep_json: str,
        entry_point: str,
        automl_settings: str,
        setup_container_id: str,
        featurization_json: str,
        **kwargs: Any
) -> None:
    """entry point for featurization run"""
    remote_featurization_run_entrypoint.execute(
        script_directory,
        dataprep_json,
        entry_point,
        automl_settings,
        setup_container_id,
        featurization_json,
        ** kwargs)


def driver_wrapper(
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
    """entry point for training iteration run"""
    return remote_training_run_entrypoint.execute(
        script_directory,
        automl_settings,
        run_id,
        training_percent,
        iteration,
        pipeline_spec,
        pipeline_id,
        dataprep_json,
        entry_point,
        **kwargs)


def model_exp_wrapper(
        script_directory: str,
        automl_settings: str,
        run_id: str,
        child_run_id: str,
        dataprep_json: str,
        entry_point: str,
        **kwargs: Any
) -> Dict[str, Any]:
    """entry point for expliner run"""
    return remote_explain_run_entrypoint.execute(
        script_directory,
        automl_settings,
        run_id,
        child_run_id,
        dataprep_json,
        entry_point,
        **kwargs)


def model_test_wrapper(
        script_directory: str,
        automl_settings: str,
        run_id: str,
        training_run_id: str,
        dataprep_json: str,
        entry_point: str,
        **kwargs: Any
) -> None:
    """entry point for run that does inference and evaluation"""
    remote_test_run_entrypoint.execute(
        script_directory,
        automl_settings,
        run_id,
        training_run_id,
        dataprep_json,
        entry_point,
        **kwargs)


def fit_featurizers_wrapper(
        script_directory: Optional[str],
        dataprep_json: str,
        entry_point: str,
        automl_settings: str,
        setup_container_id: str,
        featurization_json: str,
        **kwargs: Any
) -> None:
    """entry point for run that does fit on featurizer(s)"""
    remote_featurization_fit_run_entrypoint.execute(
        script_directory,
        dataprep_json,
        entry_point,
        automl_settings,
        setup_container_id,
        featurization_json,
        ** kwargs)


def batch_driver_wrapper(
        script_directory: str,
        automl_settings: str,
        dataprep_json: str,
        child_run_ids: List[str],
        **kwargs: Any
) -> None:
    """entry point for run that does batch training iterations"""
    remote_batch_training_run_entrypoint.execute(
        script_directory,
        automl_settings,
        dataprep_json,
        child_run_ids,
        **kwargs)


def local_managed_wrapper() -> None:
    local_managed_entrypoint.execute()
