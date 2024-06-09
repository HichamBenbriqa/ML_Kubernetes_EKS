"""
Module: prediction_client.py

Description:
This module provides a client script for sending ride details to a Flask web service
for predicting ride durations. The script sends a POST request to the specified URL
containing ride details in JSON format and prints the predicted response.
"""

import json
import requests

ride = {"PULocationID": 19, "DOLocationID": 70, "trip_distance": 500}

URL = "http://0.0.0.0:8001/predict"
TIMEOUT = 10

try:
    predicted_response = requests.post(URL, json=ride, timeout=TIMEOUT).json()
    print("Predicted response:")
    print(json.dumps(predicted_response, indent=2))
except requests.Timeout:
    print("The request timed out. Please check the server or try again later.")
except requests.RequestException as e:
    print(f"An error occurred: {e}")
