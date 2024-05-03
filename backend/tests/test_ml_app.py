import os
import numpy as np
import pytest
from unittest.mock import patch, MagicMock
import keras
import ml.ml_app as ml_app
import sys

BASE_DIR = os.path.dirname(os.path.abspath(ml_app.__file__))

@pytest.fixture
def mock_keras_model():
    """Fixture to create a mock Keras model for testing."""
    model = MagicMock(spec=keras.Model)
    model.predict.return_value = np.array([[0.1, 0.9]])
    return model

def test_get_saved_model_names():
    """Test to verify that the correct saved model names are retrieved."""
    expected_files = ["alexnet.keras", "densenet.keras", "inceptionv3.keras", "mobilenet.keras", "resnet.keras"]
    model_names = ml_app.get_saved_model_names()
    assert sorted(model_names) == sorted(expected_files), "The model names list does not match expected"

def test_get_saved_model():
    """Test to verify that a model can be successfully loaded given its name."""
    model_name = "alexnet.keras"
    model_path = os.path.join(BASE_DIR, 'saved_models', model_name)
    assert os.path.exists(model_path), "Model file does not exist."

    model = ml_app.get_saved_model(model_name)
    assert isinstance(model, keras.models.Model), "The loaded object is not a Keras model."

def test_get_prediction(mock_keras_model):
    """Test the prediction functionality of the ML model using a mock model."""
    mock_keras_model = ml_app.get_saved_model("alexnet.keras")
    test_input = np.random.rand(224, 224, 3)
    predictions = ml_app.get_prediction(mock_keras_model, test_input)
    assert predictions.shape == (1, 5)
