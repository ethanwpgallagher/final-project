import os
import numpy as np
import pytest
from unittest.mock import patch, MagicMock
import keras
import ml.ml_app as ml_app

BASE_DIR = os.path.dirname(os.path.abspath(ml_app.__file__))

@pytest.fixture
def mock_keras_model():
    model = MagicMock(spec=keras.Model)
    model.predict.return_value = np.array([[0.1, 0.9]])
    return model

def test_get_saved_model_names():
    with patch("os.listdir") as mocked_listdir:
        mocked_listdir.return_value = ["model1.h5", "model2.h5"]
        model_names = ml_app.get_saved_model_names()
        mocked_listdir.assert_called_once_with(os.path.join(BASE_DIR, 'saved_models'))
        assert "model1.h5" in model_names
        assert "model2.h5" in model_names

def test_get_saved_model():
    model_name = "model1.h5"
    with patch("keras.models.load_model") as mocked_load_model:
        ml_app.get_saved_model(model_name)
        mocked_load_model.assert_called_once_with(os.path.join(BASE_DIR, 'saved_models', model_name))

def test_get_prediction(mock_keras_model):
    test_input = np.random.rand(224, 224, 3)
    predictions = ml_app.get_prediction(mock_keras_model, test_input)
    mock_keras_model.predict.assert_called_once()
    assert predictions.shape == (1, 2)
