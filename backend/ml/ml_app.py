import numpy as np
import tensorflow as tf
import keras
import os

# Determine the base directory relative to the current file. This is used to locate saved models.
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_saved_model_names():
    """
    Lists all saved model directories in the 'saved_models' subdirectory of the BASE_DIR.

    Returns:
        list: A list of directory names, each representing a saved model.
    """
    return os.listdir(os.path.join(BASE_DIR, 'saved_models'))

def get_saved_model(model_name):
    """
    Loads a Keras model from a specified subdirectory within the 'saved_models' directory.

    Args:
        model_name (str): The name of the directory containing the model to load.

    Returns:
        keras.Model: The model loaded from the specified directory.
    """
    return keras.models.load_model(os.path.join(BASE_DIR, 'saved_models', model_name))
    
def get_prediction(model: keras.Model, test_input):
    """
    Generates a prediction from a given model using the provided input.

    Args:
        model (keras.Model): The model to use for making the prediction.
        test_input (np.ndarray): The input data for the model. This should match the input shape that the model expects.

    Returns:
        np.ndarray: The output from the model prediction.
    """
    test_input = tf.convert_to_tensor(test_input)
    test_input = tf.expand_dims(test_input, axis=0)
    return model.predict(test_input)
