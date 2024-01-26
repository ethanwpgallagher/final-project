import tensorflow as tf
from preprocessing import PreprocessingLayer
from keras import layers, models

def alex_net(input_shape=(224, 224, 3)):
    alexnet = models.Sequential()

    alexnet.add(PreprocessingLayer(input_shape=input_shape))
    # Conv1 and Pool1
    alexnet.add(layers.Conv2D(96, 11, strides=4, padding='same', input_shape=input_shape))
    alexnet.add(layers.Lambda(tf.nn.local_response_normalization))
    alexnet.add(layers.Activation('relu'))
    alexnet.add(layers.MaxPooling2D(3, strides=2))

    # Conv2 and Pool2
    alexnet.add(layers.Conv2D(256, 5, strides=4, padding='same'))
    alexnet.add(layers.Lambda(tf.nn.local_response_normalization))
    alexnet.add(layers.Activation('relu'))
    alexnet.add(layers.MaxPooling2D(3, strides=2))

    # Conv3 
    alexnet.add(layers.Conv2D(384, 3, strides=4, padding='same'))
    alexnet.add(layers.Activation('relu'))

    # Conv4
    alexnet.add(layers.Conv2D(384, 3, strides=4, padding='same'))
    alexnet.add(layers.Activation('relu'))

    #Conv5
    alexnet.add(layers.Conv2D(256, 3, strides=4, padding='same'))
    alexnet.add(layers.Activation('relu'))

    # Fully connected layers
    alexnet.add(layers.Flatten())
    alexnet.add(layers.Dense(4096, activation='relu'))
    alexnet.add(layers.Dropout(0.5))

    alexnet.add(layers.Dense(4096, activation='relu'))
    alexnet.add(layers.Dropout(0.5))

    alexnet.add(layers.Dense(5, activation='softmax'))
    alexnet.build(input_shape=(224, 224, 3))
    return alexnet