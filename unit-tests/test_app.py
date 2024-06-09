import sys
from joblib import load
import pytest
from unittest.mock import patch, MagicMock

# Import the methods to be tested
sys.path.append("/home/hicham/Desktop/personal/ML_Kubernetes_EKS/")
from app import prepare_features, predict

# Sample test data
ride_data = {"PULocationID": 1, "DOLocationID": 2, "trip_distance": 10}
features_data = {"PU_DO": "1_2", "trip_distance": 10}
MODEL_PATH = "model.joblib"


def test_prepare_features():
    """
    Test the prepare_features function.

    This function tests whether the prepare_features function correctly prepares
    the features for prediction based on the input ride data.
    """
    # Call the function
    features = prepare_features(ride_data)

    # Assertions
    assert features == features_data


def test_predict_with_existing_model():
    """
    Test the predict function with an existing model.

    This function mocks the os.path.exists method to simulate the existence of
    a locally stored model. It then asserts that the prediction is made correctly.
    """
    # Mock os.path.exists
    with patch("app.os.path.exists") as mock_exists:
        # Mock load method
        with patch("app.load") as mock_load:
            mock_exists.return_value = True
            mock_model = MagicMock()
            mock_load.return_value = mock_model
            mock_model.predict.return_value = [20]

            # Call the function
            prediction = predict(features_data)

            # Assertions
            assert prediction == 20


def test_predict_with_downloaded_model():
    """
    Test the predict function with a downloaded model.

    This function mocks the os.path.exists method to simulate the absence of
    a locally stored model. It then simulates downloading and loading the model,
    and asserts that the prediction is made correctly.
    """
    # Mock os.path.exists
    with patch("app.os.path.exists") as mock_exists:
        # Mock download_production_ready_model method
        with patch("app.download_production_ready_model") as mock_download:
            # Mock load method
            with patch("app.load") as mock_load:
                mock_exists.return_value = False
                mock_download.return_value = MagicMock()
                mock_model = MagicMock()
                mock_load.return_value = mock_model
                mock_model.predict.return_value = [20]

                # Call the function
                prediction = predict(features_data)

                # Assertions
                assert prediction == 20
