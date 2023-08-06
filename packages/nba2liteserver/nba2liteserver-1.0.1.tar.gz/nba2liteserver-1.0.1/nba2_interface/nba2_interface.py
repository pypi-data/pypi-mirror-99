import os
import logging as log
import json

from nba2_interface.singleton import singleton
from nba2_interface.nba1_model_retrieval import ModelRetrievalInterface


@singleton
class NBA2Interface(object):
    def __init__(self, qradar_ip: str, qradar_user: str, qradar_password: str, models_path: os.path,
                 permission_script_path: os.path = None, extract: bool = True):
        self.models_path = models_path
        self.permission_script_path = permission_script_path
        self.models_retrieval = ModelRetrievalInterface(
            qradar_ip=qradar_ip, qradar_user=qradar_user, qradar_password=qradar_password)
        self.features_weight = self.update_models_from_qradar_db()

    def get_model(self, model_id: str) -> dict:
        try:
            model_path = os.path.join(self.models_path, model_id)
            with open(model_path, "r") as f:
                model = json.load(f)
                return model
        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    def get_features_weight(self) -> dict:
        try:
            return self.features_weight
        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    def update_models_from_qradar_db(self):
        try:
            self.features_weight = self.models_retrieval.retrieve_models_from_db(
                models_path=self.models_path, permission_script_path=self.permission_script_path, extract=True)
            return self.features_weight
        except Exception as e:
            log.error(f"Error: {e}")
            raise e
