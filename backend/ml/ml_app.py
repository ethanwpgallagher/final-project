import numpy as np
import tensorflow as tf
import keras
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

def get_saved_model_names():
    return os.listdir(os.path.join(BASE_DIR, 'saved_models'))

def get_saved_model(model_name):
    return keras.models.load_model(os.path.join(BASE_DIR, 'saved_models', model_name))
    
def get_prediction(model: keras.Model, test_input):
    test_input = tf.convert_to_tensor(test_input)
    test_input = tf.expand_dims(test_input, axis=0)
    return model.predict(test_input)
