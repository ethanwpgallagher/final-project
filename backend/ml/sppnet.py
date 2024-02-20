import tensorflow as tf
from tensorflow_addons.layers import SpatialPyramidPooling2D
import matplotlib.pyplot as plt
from keras import datasets, layers, models, optimizers
        
def spp_net():
    sppnet = models.Sequential()

    # Conv1 and Pool1
    sppnet.add(layers.Conv2D(96, 11, strides=4, padding='same'))
    sppnet.add(layers.BatchNormalization())
    sppnet.add(layers.Activation('relu'))
    sppnet.add(layers.MaxPooling2D(3, strides=2))

    # Conv2 and Pool2
    sppnet.add(layers.Conv2D(256, 5, strides=4, padding='same'))
    sppnet.add(layers.BatchNormalization())
    sppnet.add(layers.Activation('relu'))

    # Conv3 
    sppnet.add(layers.Conv2D(384, 3, strides=4, padding='same'))
    sppnet.add(layers.Activation('relu'))

    # Conv4
    sppnet.add(layers.Conv2D(384, 3, strides=4, padding='same'))
    sppnet.add(layers.Activation('relu'))

    #Conv5
    sppnet.add(layers.Conv2D(256, 3, strides=4, padding='same'))
    sppnet.add(layers.Activation('relu'))

    sppnet.add(SpatialPyramidPooling2D(bins=[1,2,4]))
    # Fully connected layers
    sppnet.add(layers.Flatten())
    sppnet.add(layers.Dense(4096, activation='relu'))
    sppnet.add(layers.Dropout(0.5))

    sppnet.add(layers.Dense(4096, activation='relu'))
    sppnet.add(layers.Dropout(0.5))

    sppnet.add(layers.Dense(19, activation='softmax'))
    return sppnet
