import tensorflow as tf
import keras

def alex_net(input_shape=(224, 224, 3)):
    alexnet = keras.models.Sequential()

    # Conv1 and Pool1
    alexnet.add(keras.layers.Conv2D(96, 11, strides=4, padding='same', input_shape=input_shape))
    alexnet.add(keras.layers.BatchNormalization())
    alexnet.add(keras.layers.Activation('relu'))
    alexnet.add(keras.layers.MaxPooling2D(3, strides=2))

    # Conv2 and Pool2
    alexnet.add(keras.layers.Conv2D(256, 5, strides=4, padding='same'))
    alexnet.add(keras.layers.BatchNormalization())
    alexnet.add(keras.layers.Activation('relu'))
    alexnet.add(keras.layers.MaxPooling2D(3, strides=2))

    # Conv3 
    alexnet.add(keras.layers.Conv2D(384, 3, strides=4, padding='same'))
    alexnet.add(keras.layers.Activation('relu'))

    # Conv4
    alexnet.add(keras.layers.Conv2D(384, 3, strides=4, padding='same'))
    alexnet.add(keras.layers.Activation('relu'))

    #Conv5
    alexnet.add(keras.layers.Conv2D(256, 3, strides=4, padding='same'))
    alexnet.add(keras.layers.Activation('relu'))

    # Fully connected layers
    alexnet.add(keras.layers.Flatten())
    alexnet.add(keras.layers.Dense(4096, activation='relu'))
    alexnet.add(keras.layers.Dropout(0.5))

    alexnet.add(keras.layers.Dense(4096, activation='relu'))
    alexnet.add(keras.layers.Dropout(0.5))

    alexnet.add(keras.layers.Dense(5, activation='softmax'))
    alexnet.build(input_shape=(224, 224, 3))
    return alexnet