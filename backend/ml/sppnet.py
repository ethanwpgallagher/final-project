import tensorflow as tf
from tensorflow_addons.layers import SpatialPyramidPooling2D
import matplotlib.pyplot as plt
from keras import datasets, layers, models, optimizers
        
def spp_net():
    sppnet = models.Sequential()

    # Conv1 and Pool1
    sppnet.add(layers.Conv2D(96, 11, strides=4, padding='same'))
    #sppnet.add(layers.Lambda(tf.nn.local_response_normalization))
    sppnet.add(layers.BatchNormalization())
    sppnet.add(layers.Activation('relu'))
    sppnet.add(layers.MaxPooling2D(3, strides=2))

    # Conv2 and Pool2
    sppnet.add(layers.Conv2D(256, 5, strides=4, padding='same'))
    #sppnet.add(layers.Lambda(tf.nn.local_response_normalization))
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

if __name__=='__main__':
    (x_train, y_train), (x_test, y_test) = datasets.mnist.load_data()

    x_train = tf.pad(x_train, [[0,0], [2,2], [2,2]]) / 255
    x_test = tf.pad(x_test, [[0,0], [2,2], [2,2]]) / 255

    x_train = tf.expand_dims(x_train, axis=-1)
    x_test = tf.expand_dims(x_test, axis=-1)

    x_train = tf.repeat(x_train, 3, axis=-1)
    x_test = tf.repeat(x_test, 3, axis=-1)

    x_val = x_train[-2000:]
    y_val = y_train[-2000:]
    x_train = x_train[:-2000]
    y_train = y_train[:-2000]

    model = spp_net()   
    model.build(input_shape=(None, 32, 32, 3))
    model.summary() 

    optimizer = optimizers.legacy.Adam(learning_rate=0.0001)  # Reduce the learning rate
    model.compile(optimizer=optimizer, loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    history = model.fit(x_train, y_train, batch_size=64, epochs=5, validation_data=(x_val, y_val))

    fig, axs = plt.subplots(2, 1, figsize=(15, 15))
    axs[0].plot(history.history['loss'])
    axs[0].plot(history.history['val_loss'])
    axs[0].set_title('Training Loss vs Validation Loss')
    axs[0].set_xlabel('Epochs')
    axs[0].set_ylabel('Loss')
    axs[0].legend(['Train', 'Val'])
    
    axs[1].plot(history.history['accuracy'])
    axs[1].plot(history.history['val_accuracy'])
    axs[1].set_title('Training Accuracy vs Validation Accuracy')
    axs[1].set_xlabel('Epochs')
    axs[1].set_ylabel('Accuracy')
    axs[1].legend(['Train', 'Val'])

    plt.show()