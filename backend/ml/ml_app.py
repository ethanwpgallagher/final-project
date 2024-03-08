import numpy as np
import tensorflow as tf
import keras
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODELS = {
    'Alexnet': os.path.join(BASE_DIR, 'saved_models', 'alexnet.keras'),
    'VGG16': os.path.join(BASE_DIR, 'saved_models', 'vgg_16.keras')
}

def get_saved_model(model_name):
    model = MODELS[model_name]
    if model is not None:
        return keras.models.load_model(model)
    
def get_prediction(model: keras.Model, test_input):
    test_input = tf.convert_to_tensor(test_input)
    test_input = tf.expand_dims(test_input, axis=0)
    return model.predict(test_input)
