# old model no longer used. Huge performance issues, vanishing gradient problem!

import tensorflow as tf
import matplotlib.pyplot as plt
from keras import datasets, layers, models, losses, applications

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

if __name__=='__main__':
    (x_train, y_train), (x_test, y_test) = datasets.mnist.load_data()

    x_train = tf.pad(x_train, [[0,0], [2,2], [2,2]])/255
    x_test = tf.pad(x_train, [[0,0], [2,2], [2,2]])/255

    x_train = tf.expand_dims(x_train, axis=3, name=None)
    x_test = tf.expand_dims(x_test, axis=3, name=None)

    x_train = tf.repeat(x_train, 3, axis=3)
    x_test = tf.repeat(x_test, 3, axis=3)

    x_val = x_train[-2000:,:,:,:]
    y_val = y_train[-2000:]
    x_train = x_train[:-2000,:,:,:]
    y_train = y_train[:-2000]

    model = vgg_16(None, 1000)
    
    model.compile(optimizer='adam', loss=losses.sparse_categorical_crossentropy, metrics=['accuracy'])
    history = model.fit(x_train, y_train, batch_size=64, epochs=5, validation_data=(x_val, y_val))

    fig, axs = plt.subplots(2, 1, figsize=(15,15))
    axs[0].plot(history.history['loss'])
    axs[0].plot(history.history['val_loss'])
    axs[0].title.set_text('Training Loss vs Validation Loss')
    axs[0].set_xlabel('Epochs')
    axs[0].set_ylabel('Loss')
    axs[0].legend(['Train', 'Val'])
    axs[1].plot(history.history['accuracy'])
    axs[1].plot(history.history['val_accuracy'])
    axs[1].title.set_text('Training Accuracy vs Validation Accuracy')
    axs[1].set_xlabel('Epochs')
    axs[1].set_ylabel('Accuracy')
    axs[1].legend(['Train', 'Val'])
