import json
import os
import copy
import logging as log
from nba2_interface.qradar_postgres_connector import QRadarPostgresConnector
from nba2_interface import definition


class Tokens():
    NUM_OF_ITEMS_IN_HEADER = 12  # skip items to _extract features
    EXTRA_FIELDS_LEN = 3  # 3 number at the end of the file

    # models tokens from solution.txt file
    EOS_STR = "EOS"
    ID_STR = "id"
    UUID_STR = "uuid"
    INF_STR = "inf"
    HASHED_NAME_STR = "hashedName"
    HEADER_STR = "header"
    FEATURES_STR = "features"
    NAME_STR = "name"
    DEF_STR = "def"
    WEIGHTING_FACTOR_ALLOWLIST_STR = "weighting_factor_allowlist"
    WEIGHTING_FACTOR_NUMERIC_STR = "weighting_factor_numeric"

    NEGATIVE_EPSILON_VAL = -0.00001
    NEGATIVE_EPSILON_STR = '-0.0'

    NULL_STRING = "NULL"
    OTHER_STRING = "other"

    DB_TREE_FILE_NAME = "db_tree_file.csv"
    DB_MODELS_FILE_NAME = "db_models_file.csv"


def get_converted_feature(feature_name: str) -> str:
    feature_to_flow_converter = {
        "sourceip": definition.TOKEN_SOURCE_IP,
        "destinationip": definition.TOKEN_DESTINATION_IP
    }
    if feature_name in feature_to_flow_converter:
        return feature_to_flow_converter[feature_name]  # convert the sourceip/destinationip to source_address/destination_address as i feature.json
    else:
        return feature_name


class TreeModelReConvertor(object):
    def __init__(self):
        self.score_factor = 1.0
        self.cost_round_len = 4
        self.start_line_cnt = 1
        self.line_cnt = self.start_line_cnt
        self.no_more_models = False

        self.features_to_replace_NULL_to_other = ["source_network", "destination_network"]

        self.base_range = {
            definition.TOKEN_OUT_OF_RANGE_COST: 0,
            definition.TOKEN_RANGE: {
                definition.TOKEN_AVG: 0, definition.TOKEN_STD: 0, definition.TOKEN_MAX: 0, definition.TOKEN_MIN: 0,
                definition.TOKEN_RANGE_START: 0, definition.TOKEN_RANGE_STOP: 0},
            definition.TOKEN_X_CUT_POINTS: [],
            definition.TOKEN_COST: []
        }

        self.base_2d_hist = {
            definition.TOKEN_OUT_OF_RANGE_COST: 0,
            definition.TOKEN_X_RANGE: {definition.TOKEN_AVG: 0, definition.TOKEN_STD: 0, definition.TOKEN_MAX: 0,
                                       definition.TOKEN_MIN: 0, definition.TOKEN_RANGE_START: 0, definition.TOKEN_RANGE_STOP: 0},
            definition.TOKEN_Y_RANGE: {definition.TOKEN_AVG: 0, definition.TOKEN_STD: 0, definition.TOKEN_MAX: 0,
                                       definition.TOKEN_MIN: 0, definition.TOKEN_RANGE_START: 0, definition.TOKEN_RANGE_STOP: 0},
            definition.TOKEN_X_CUT_POINTS: [],
            definition.TOKEN_Y_CUT_POINTS: [],
            definition.TOKEN_COST: []
        }

    # <header>: <id>,<uuid>,hashedName <model name> expectedOccurrence <val> normalisedLikelihood <val> len <val>
    def _extract_db_header(self, header_vec: list) -> dict:
        tokens_info = {Tokens.HASHED_NAME_STR: 5, "expectedOccurrence": 7, "normalisedLikelihood": 9, "len": 11}
        header = {}
        try:
            if header_vec[0] == Tokens.EOS_STR:
                self.no_more_models = True
                return {}  # no more models
            header[Tokens.ID_STR] = header_vec[0]
            header[Tokens.UUID_STR] = header_vec[1]
            for token in tokens_info:
                header[token] = header_vec[tokens_info[token]]
            return header
        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    # <len> [idx, val]*len "def" val
    def _extract_whitelist(self, model_name: str, feature_name: str, feature_vec: list) -> (int, dict):
        whitelist = {}
        idx = 0
        try:
            if feature_vec[idx] == '0':  # no whitelist
                return idx+1, None
            else:
                _len = int(feature_vec[idx])
                idx += 1
                for i in range(0, _len*2, 2):
                    val = feature_vec[idx]
                    if feature_name in self.features_to_replace_NULL_to_other and Tokens.NULL_STRING in val:
                        val = Tokens.OTHER_STRING
                    whitelist[val] = round(float(feature_vec[idx+1]) / self.score_factor, self.cost_round_len)
                    idx += 2
                if feature_vec[idx] != Tokens.DEF_STR:
                    log.error(f'Model {model_name}, feature: {feature_name} expect to find {Tokens.INF_STR} token but find {feature_vec[idx+1]}')
                idx += 1
                whitelist[definition.TOKEN_DEFAULT] = round(float(feature_vec[idx]) / self.score_factor, self.cost_round_len)
                return idx+1, whitelist
        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    def _extract_one_d_hist(self, model_name: str, feature_name: str, feature_vec: list) -> (int, dict):
        _type = definition.TOKEN_X_CUT_POINTS
        idx = 0
        try:
            data = copy.deepcopy(self.base_range)
            if feature_vec[idx] == '0':  # no info
                return idx + 1, None
            else:
                _len = int(feature_vec[idx])
                data[_type] = []
                # read indices
                for i in range(_len):
                    idx += 1
                    val = float(feature_vec[idx]) if feature_vec[idx] != Tokens.NEGATIVE_EPSILON_STR else Tokens.NEGATIVE_EPSILON_VAL
                    data[_type].append(val)
                idx += 1  # skip the last index: "inf"
                data[definition.TOKEN_RANGE][definition.TOKEN_RANGE_START] = data[_type][0]
                data[definition.TOKEN_RANGE][definition.TOKEN_RANGE_STOP] = data[_type][_len-1]
                # read costs
                for i in range(_len):
                    idx += 1
                    data[definition.TOKEN_COST].append(round(float(feature_vec[idx]) / self.score_factor, self.cost_round_len))
                idx += 1  # skip the last index: "inf"
                data[definition.TOKEN_OUT_OF_RANGE_COST] = data[definition.TOKEN_COST][0]
                new_feature_vec = feature_vec[idx:]
                new_idx, data = self._extract_min_max(model_name=model_name, feature_name=feature_name, data=data,
                                                      feature_vec=new_feature_vec, _type=definition.TOKEN_RANGE)
                idx += new_idx
                return idx, data
        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    def _extract_min_max(self, model_name: str, feature_name: str, data: dict, feature_vec: list, _type: str) -> (int, dict):
        idx = 0
        try:
            if feature_vec[idx + 1] != definition.TOKEN_MIN:
                log.error(
                    f'Model {model_name}, feature: {feature_name} expect to find {definition.TOKEN_MIN} token but find {feature_vec[idx + 1]}')
            idx += 2
            data[_type][definition.TOKEN_MIN] = feature_vec[idx]
            if feature_vec[idx + 1] != definition.TOKEN_MAX:
                log.error(
                    f'Model {model_name}, feature: {feature_name} expect to find {definition.TOKEN_MAX} token but find {feature_vec[idx + 1]}')
            idx += 2
            data[_type][definition.TOKEN_MAX] = feature_vec[idx]
            return idx+1, data
        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    # <x/y> <len> [<val> * len] 'min' <val> 'max' <val>
    def _extract_range_vec(self, model_name: str, feature_name: str, data: dict, feature_vec: list, range_name: str, cut_point_name: str) -> (int, dict):
        try:
            idx = 0
            idx += 1  # skip on 'x' or 'y'
            if feature_vec[idx] == '0':  # no info
                return idx + 1, data
            else:
                _len = int(feature_vec[idx])
                data[cut_point_name] = []
                for i in range(_len):
                    idx += 1
                    val = float(feature_vec[idx]) if feature_vec[idx] != Tokens.NEGATIVE_EPSILON_STR else Tokens.NEGATIVE_EPSILON_VAL
                    data[cut_point_name].append(val)
                data[range_name][definition.TOKEN_RANGE_START] = data[cut_point_name][0]
                data[range_name][definition.TOKEN_RANGE_STOP] = data[cut_point_name][_len-1]
                new_feature_vec = feature_vec[idx:]
                new_idx, data = self._extract_min_max(model_name=model_name, feature_name=feature_name, data=data, feature_vec=new_feature_vec, _type=range_name)
                idx += new_idx
                return idx, data
        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    # costs 10000.0 10000.0 10000.0 ... inf 100
    def _extract_cost_vec(self, model_name: str, feature_name: str, data: dict, feature_vec: list, _len: int) -> (int, float, dict):
        try:
            idx = 0
            data[definition.TOKEN_COST] = []
            for i in range(_len):
                data[definition.TOKEN_COST].append([])
                for j in range(_len):
                    idx += 1
                    data[definition.TOKEN_COST][i].append(round(float(feature_vec[idx]) / self.score_factor, self.cost_round_len))
            if feature_vec[idx + 1] != Tokens.INF_STR:
                log.error(
                    f'Model {model_name}, feature: {feature_name} expect to find {Tokens.INF_STR} token but find {feature_vec[idx + 1]}')
            idx += 2
            inf = feature_vec[idx]
            return idx+1, inf, data
        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    def _extract_2_d_hist(self, model_name: str, feature_name: str, feature_vec: list) -> (int, dict):
        try:
            idx = 0
            data = copy.deepcopy(self.base_2d_hist)

            new_idx, data = self._extract_range_vec(
                model_name=model_name,
                feature_name=feature_name,
                data=data,
                feature_vec=feature_vec,
                range_name=definition.TOKEN_X_RANGE,
                cut_point_name=definition.TOKEN_X_CUT_POINTS)
            idx += new_idx
            new_feature_vec = feature_vec[new_idx:]
            new_idx, data = self._extract_range_vec(
                model_name=model_name,
                feature_name=feature_name,
                data=data,
                feature_vec=new_feature_vec,
                range_name=definition.TOKEN_Y_RANGE,
                cut_point_name=definition.TOKEN_Y_CUT_POINTS)
            idx += new_idx
            new_feature_vec = feature_vec[idx:]
            _len = len(data[definition.TOKEN_X_CUT_POINTS])
            if _len > 0:
                new_idx, inf, data = self._extract_cost_vec(model_name=model_name, feature_name=feature_name,
                                                            data=data, feature_vec=new_feature_vec, _len=_len)
                idx += new_idx
                data[definition.TOKEN_OUT_OF_RANGE_COST] = data[definition.TOKEN_COST][0][0]
            return idx, data
        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    def _extract_model_features(self, idx: int, model_name: str, feature_vec: list) -> (int, dict):
        feature = {}
        try:
            feature_name = get_converted_feature(feature_name=feature_vec[idx])
            log.debug(f'Feature name: {feature_name}')
            idx += 1
            new_feature_vec = feature_vec[idx:]
            new_idx, data = self._extract_whitelist(model_name=model_name, feature_name=feature_name, feature_vec=new_feature_vec)
            idx += new_idx
            if data:
                feature[definition.TOKEN_ALLOWLIST] = copy.deepcopy(data)
            new_feature_vec = feature_vec[idx:]
            new_idx, data = self._extract_one_d_hist(model_name=model_name, feature_name=feature_name, feature_vec=new_feature_vec)
            idx += new_idx
            if data:
                feature[definition.TOKEN_1D_HIST] = copy.deepcopy(data)
            new_feature_vec = feature_vec[idx:]
            new_idx, data = self._extract_2_d_hist(model_name=model_name, feature_name=feature_name, feature_vec=new_feature_vec)
            idx += new_idx
            if len(data[definition.TOKEN_X_CUT_POINTS]) > 0:
                feature[definition.TOKEN_2D_HIST] = copy.deepcopy(data)
            #else:
            #    feature[TWO_D_HIST_STR] = None
            return idx, feature, feature_name
        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    def _get_model_features(self, model_name: str, model_vec: list) -> dict:
        _features = {}
        try:
            idx = 0
            while idx < len(model_vec)-Tokens.EXTRA_FIELDS_LEN:
                idx, feature, feature_name = self._extract_model_features(idx=idx, model_name=model_name, feature_vec=model_vec)
                _features[feature_name] = feature
        except Exception as e:
            log.error(f"Error: {e}")
        return _features

    def _reconstruct_model(self, model_name: str) -> dict:
        model = {}
        try:
            model_name = model_name.replace(" ", ",")
            data_vec = [x.strip() for x in model_name.split(",")]
            model[Tokens.HEADER_STR] = self._extract_db_header(data_vec[0:Tokens.NUM_OF_ITEMS_IN_HEADER])
            if self.no_more_models:
                return {}
            model[Tokens.FEATURES_STR] = self._get_model_features(model_name=model[Tokens.HEADER_STR][Tokens.HASHED_NAME_STR],
                                                                  model_vec=data_vec[Tokens.NUM_OF_ITEMS_IN_HEADER:])
        except Exception as e:
            log.error(f"Error: {e}")
        return model

    def _reconstruct_models(self, models_data: list) -> dict:
        models = {}
        try:
            _len = len(models_data)
            for model in models_data[self.start_line_cnt:]:
                if self.line_cnt % 1000 == 0:
                    log.info(f"Line {self.line_cnt}/{_len}")
                self.line_cnt += 1
                val = self._reconstruct_model(model_name=model)
                if self.no_more_models:
                    log.info(f"End of MODELS found, number of models: {self.line_cnt - self.start_line_cnt - 1}")
                    break
                models[val[Tokens.HEADER_STR][Tokens.HASHED_NAME_STR]] = copy.deepcopy(val)
        except Exception as e:
            log.error(f"Error: {e}")
        return models

    def _extract_models_from_db(self, models_csv_file: str) -> dict:
        models = {}
        try:
            with open(models_csv_file, "r") as f:
                _data = f.readlines()
            models = self._reconstruct_models(models_data=_data)
            log.info(f"Read total of {len(models)} models")
            log.debug(f"Models: {json.dumps(models,indent=3)}")
            return models
        except Exception as e:
            log.error(f"Error: {e}")
        return models

    def _write_db_models_to_files(self, models: dict, write_models_path: os.path = None):
        try:
            if write_models_path:
                for model in models:
                    model_file_path = os.path.join(write_models_path,
                                                   f"{models[model][Tokens.HEADER_STR][Tokens.UUID_STR]}")
                    with open(model_file_path, "w") as f:
                        json.dump(models[model][Tokens.FEATURES_STR], f, indent=3)
        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    def convert_models_to_model_manager_format(self, models_csv_file: os.path, new_models_path: os.path):
        try:
            models = self._extract_models_from_db(models_csv_file=models_csv_file)
            self._write_db_models_to_files(models=models, write_models_path=new_models_path)
        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    def _set_feature_weight(self, features: dict, feature_name: str, allowlist_val: float, range_val: float):
        if feature_name not in features:
            features[feature_name] = {}
        features[feature_name][definition.TOKEN_ALLOWLIST] = allowlist_val
        features[feature_name][definition.TOKEN_RANGE] = range_val
        features[feature_name][definition.TOKEN_1D_HIST] = range_val
        features[feature_name][definition.TOKEN_2D_HIST] = range_val

    def _read_db_features(self, db_features: list) -> dict:
        try:
            _features = {}
            for line in db_features:
                #  protocolid weighting_factor_allowlist 0.25 weighting_factor_numeric 0.0
                data = line.split(Tokens.WEIGHTING_FACTOR_ALLOWLIST_STR)
                if len(data) > 1:
                    data1 = data[0].split("\"")
                    feature_name = data1[1].strip() if len(data1) > 1 else data1[0].strip()
                    feature_name = get_converted_feature(feature_name=feature_name)
                    self._set_feature_weight(features=_features, feature_name=feature_name, allowlist_val=0, range_val=0)
                    info = (data[1].split("\""))[0].split(" ")
                    self._set_feature_weight(features=_features, feature_name=feature_name, allowlist_val=float(info[1]), range_val=float(info[3]))
            return _features
        except Exception as e:
            log.error(f"Error: {e}")
            raise e

    def get_updated_feature_struct(self, tree_csv_file: str):
        try:
            with open(tree_csv_file, "r") as f:
                db_features_data = f.readlines()
                db_features = self._read_db_features(db_features=db_features_data)
                return db_features
        except Exception as e:
            log.error(f"Error: {e}")
            raise e


class ModelRetrievalInterface(object):
    def __init__(self, qradar_ip: str, qradar_user: str, qradar_password: str):
        self.qradar_ip = qradar_ip
        self.qradar_user = qradar_user
        self.qradar_password = qradar_password

    def retrieve_models_from_db(self, models_path: os.path, permission_script_path: str = None, extract: bool=True):
        try:
            if not models_path.endswith("/"):
                models_path += "/"

            db_models_file_path = os.path.join(models_path, Tokens.DB_MODELS_FILE_NAME)
            db_tree_file_path = os.path.join(models_path, Tokens.DB_TREE_FILE_NAME)

            # Retrieves models (solution.txt format) from QRadar
            if extract:
                qradar_api = QRadarPostgresConnector(permission_script_path=permission_script_path)
                qradar_api.get_models_from_qradar(
                    ip=self.qradar_ip,
                    user=self.qradar_user,
                    password=self.qradar_password,
                    db_models_file_name=Tokens.DB_MODELS_FILE_NAME,
                    db_tree_file_name=Tokens.DB_TREE_FILE_NAME,
                    db_dest_path=models_path
                )

            # Convert models to model manger json format
            m = TreeModelReConvertor()
            m.convert_models_to_model_manager_format(
                models_csv_file=db_models_file_path,
                new_models_path=models_path
            )
            features = m.get_updated_feature_struct(
                tree_csv_file=db_tree_file_path
            )
            return features
        except Exception as e:
            log.error(f"error: {e}")
            raise e
