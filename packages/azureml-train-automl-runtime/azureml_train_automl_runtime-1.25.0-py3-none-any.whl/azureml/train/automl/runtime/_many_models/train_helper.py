# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import os
import pickle


class MetadataFileHandler:
    """ This class is used for writing and reading run metadata"""
    # Metadata file names
    ARGS_FILE_NAME = "args.pkl"
    AUTOML_SETTINGS_FILE_NAME = "automl_settings.pkl"
    LOGS_FILE_NAME = "logs.pkl"
    RUN_DTO_FILE_NAME = "run_dto.pkl"

    def __init__(self, data_dir: str):
        """ This class is used for writing and reading run metadata"""
        # Directory where metadata files live
        self.data_dir = data_dir

        # Full paths to metadata files
        self._args_file_path = os.path.join(self.data_dir, self.ARGS_FILE_NAME)
        self._automl_settings_file_path = os.path.join(self.data_dir, self.AUTOML_SETTINGS_FILE_NAME)
        self._logs_file_path = os.path.join(self.data_dir, self.LOGS_FILE_NAME)
        self._run_dto_file_name = os.path.join(self.data_dir, self.RUN_DTO_FILE_NAME)

    def delete_logs_file_if_exists(self):
        if not os.path.exists(self._logs_file_path):
            return
        os.remove(self._logs_file_path)

    def load_automl_settings(self):
        return self.load_obj_from_disk(self._automl_settings_file_path)

    def load_args(self):
        return self.load_obj_from_disk(self._args_file_path)

    def load_logs(self):
        return self.load_obj_from_disk(self._logs_file_path)

    def load_run_dto(self):
        return self.load_obj_from_disk(self._run_dto_file_name)

    def write_args_to_disk(self, args):
        self.serialize_obj_to_disk(args, self._args_file_path)

    def write_automl_settings_to_disk(self, automl_settings):
        self.serialize_obj_to_disk(automl_settings, self._automl_settings_file_path)

    def write_logs_to_disk(self, logs):
        self.serialize_obj_to_disk(logs, self._logs_file_path)

    def write_run_dto_to_disk(self, run_dto):
        self.serialize_obj_to_disk(run_dto, self._run_dto_file_name)

    @classmethod
    def load_obj_from_disk(cls, file_path):
        with open(file_path, 'rb') as f:
            return pickle.load(f)

    @classmethod
    def serialize_obj_to_disk(cls, obj, file_path):
        with open(file_path, 'wb') as f:
            pickle.dump(obj, f)


class Arguments:
    def __init__(self, process_count_per_node, retrain_failed_models):
        self.process_count_per_node = process_count_per_node
        self.retrain_failed_models = retrain_failed_models
