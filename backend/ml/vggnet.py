import tensorflow as tf
import matplotlib.pyplot as plt
from keras import datasets, layers, models, losses

def vgg_16(weights=None, classes=1000):
    vgg16 = models.Sequential()

    # Layer 1
    vgg16.add(layers.Conv2D(64, (3,3), activation='relu', padding='same'))
    vgg16.add(layers.Conv2D(64, (3,3), activation='relu', padding='same'))
    vgg16.add(layers.MaxPooling2D((2,2), strides=(2,2)))

    # Layer 2
    vgg16.add(layers.Conv2D(128, (3,3), activation='relu', padding='same'))
    vgg16.add(layers.Conv2D(128, (3,3), activation='relu', padding='same'))
    vgg16.add(layers.MaxPooling2D((2,2), strides=(2,2)))

    # Layer 3
    vgg16.add(layers.Conv2D(256, (3,3), activation='relu', padding='same'))
    vgg16.add(layers.Conv2D(256, (3,3), activation='relu', padding='same'))
    vgg16.add(layers.Conv2D(256, (3,3), activation='relu', padding='same'))
    vgg16.add(layers.MaxPooling2D((2,2), strides=(2,2)))

    # Layer 4
    vgg16.add(layers.Conv2D(512, (3,3), activation='relu', padding='same'))
    vgg16.add(layers.Conv2D(512, (3,3), activation='relu', padding='same'))
    vgg16.add(layers.Conv2D(512, (3,3), activation='relu', padding='same'))
    vgg16.add(layers.MaxPooling2D((2,2), strides=(2,2)))

    # Layer 5
    vgg16.add(layers.Conv2D(512, (3,3), activation='relu', padding='same'))
    vgg16.add(layers.Conv2D(512, (3,3), activation='relu', padding='same'))
    vgg16.add(layers.Conv2D(512, (3,3), activation='relu', padding='same'))
    vgg16.add(layers.MaxPooling2D((2,2), strides=(2,2)))

    # Fully connected layers 
    vgg16.add(layers.Flatten())
    vgg16.add(layers.Dense(4096, activation='relu'))
    vgg16.add(layers.Dense(4096, activation='relu'))
    vgg16.add(layers.Dense(classes, activation='softmax'))

    if weights is not None:
        vgg16.load_weights(weights)
    return vgg16

def vgg_19(weights=None, classes=1000):
    vgg19 = models.Sequential()

    # Layer 1
    vgg19.add(layers.Conv2D(64, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.Conv2D(64, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.MaxPooling2D((2,2), strides=(2,2)))

    # Layer 2
    vgg19.add(layers.Conv2D(128, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.Conv2D(128, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.MaxPooling2D((2,2), strides=(2,2)))

    # Layer 3
    vgg19.add(layers.Conv2D(256, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.Conv2D(256, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.Conv2D(256, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.Conv2D(256, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.MaxPooling2D((2,2), strides=(2,2)))

    # Layer 4
    vgg19.add(layers.Conv2D(512, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.Conv2D(512, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.Conv2D(512, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.Conv2D(512, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.MaxPooling2D((2,2), strides=(2,2)))

    # Layer 5
    vgg19.add(layers.Conv2D(512, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.Conv2D(512, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.Conv2D(512, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.Conv2D(512, (3,3), activation='relu', padding='same'))
    vgg19.add(layers.MaxPooling2D((2,2), strides=(2,2)))

    # Fully connected layers
    vgg19.add(layers.Flatten())
    vgg19.add(layers.Dense(4096, activation='relu'))
    vgg19.add(layers.Dense(4096, activation='relu'))
    vgg19.add(layers.Dense(classes, activation='softmax'))
    
    if weights is not None:
        vgg19.load_weights(weights)
    
    return vgg19

