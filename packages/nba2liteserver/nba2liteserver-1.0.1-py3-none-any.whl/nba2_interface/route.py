from flask import Flask, request, jsonify, Blueprint
from flask_cors import CORS
from furl import furl

from nba2_interface.nba2_interface import NBA2Interface

app = Blueprint("mold", __name__)
CORS(app)


class Tokens:
    GET_MODEL_BY_ID_PATH = "get_model"
    GET_FEATURES_WEIGHT_PATH = "get_features_weight"
    UPDATE_MODELS_PATH = "update_models"

    MODEL_ID_TOKEN = "model_id"

    OPERATION_STATUS_TOKEN = "operation"

    GET_STR = "GET"
    POST_STR = "POST"
    RESP_DATA_VAL = 200
    RESP_SERVER_ERROR_VAL = 500


@app.route(Tokens.GET_MODEL_BY_ID_PATH, methods=[Tokens.GET_STR])
def get_model_by_id():
    resp = {}
    try:
        f = furl(request.url)
        model = NBA2Interface().get_model(model_id=f.args[Tokens.MODEL_ID_TOKEN])
        resp = jsonify(model)
        resp.status_code = Tokens.RESP_DATA_VAL
    except Exception as e:
        print(f"error: {e}")
        resp = jsonify({"Error": e})
        resp.status_code = Tokens.RESP_SERVER_ERROR_VAL
    finally:
        print(f"response {resp}")
        return resp


@app.route(Tokens.GET_FEATURES_WEIGHT_PATH, methods=[Tokens.GET_STR])
def get_features_weight():
    resp = {}
    try:
        features_weight = NBA2Interface().get_features_weight()
        resp = jsonify(features_weight)
        resp.status_code = Tokens.RESP_DATA_VAL
    except Exception as e:
        print(f"error: {e}")
        resp = jsonify({"Error": e})
        resp.status_code = Tokens.RESP_SERVER_ERROR_VAL
    finally:
        print(f"response {resp}")
        return resp


@app.route(Tokens.UPDATE_MODELS_PATH, methods=[Tokens.GET_STR])
def update_models_from_qradar_db():
    resp = {}
    try:
        NBA2Interface().update_models_from_qradar_db()
        resp = jsonify({Tokens.OPERATION_STATUS_TOKEN: "Done"})
        resp.status_code = Tokens.RESP_DATA_VAL
    except Exception as e:
        print(f"error: {e}")
        resp = jsonify({"Error": e})
        resp.status_code = Tokens.RESP_SERVER_ERROR_VAL
    finally:
        print(f"response {resp}")
        return resp
