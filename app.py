"""
Module: duration_prediction_service.py

Description:
This module provides a Flask web service for predicting ride durations. It downloads
the production-ready machine learning model from Neptune and serves predictions via an
API endpoint.
"""

import os
from joblib import load
from flask import Flask, jsonify, request  # pylint: disable=0E401
from neptune_utils import download_production_ready_model

MODEL_LOCAL_PATH = "model.joblib"


def prepare_features(ride):
    """_summary_

    :param ride: _description_
    :type ride: _type_
    :return: _description_
    :rtype: _type_
    """
    features = {}
    features["PU_DO"] = "%s_%s" % (ride["PULocationID"], ride["DOLocationID"])
    features["trip_distance"] = ride["trip_distance"]
    return features


def predict(features):
    """_summary_

    :param features: _description_
    :type features: _type_
    :return: _description_
    :rtype: _type_
    """
    if os.path.exists(MODEL_LOCAL_PATH):
        model = load(MODEL_LOCAL_PATH)
    else:
        download_production_ready_model()
        model = load(MODEL_LOCAL_PATH)
    preds = model.predict(features)
    return float(preds[0])


def main():
    """
    Initialize and configure the Flask application.

    python

    Returns:
        Flask: Configured Flask application.
    """
    app = Flask("duration-prediction")

    @app.route("/predict", methods=["POST"])
    def predict_endpoint():
        """_summary_

        :return: _description_
        :rtype: _type_
        """
        ride = request.get_json()

        features = prepare_features(ride)
        pred = predict(features)

        result = {"ride": ride, "duration": pred}

        return jsonify(result)

    return app
