import tensorflow as tf
import matplotlib.pyplot as plt

from keras import datasets, layers, models, losses

def alex_net():
    alexnet = models.Sequential()

    alexnet.add(layers.experimental.preprocessing.Resizing(224,224, interpolation='bilinear', input_shape=x_train.shape[1:]))
    # Conv1 and Pool1
    alexnet.add(layers.Conv2D(96, 11, strides=4, padding='same'))
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

    alexnet.add(layers.Dense(19, activation='softmax'))
    return alexnet


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


alexnet = alex_net()
alexnet.summary()
alexnet.compile(optimizer='adam', loss=losses.sparse_categorical_crossentropy, metrics=['accuracy'])
history = alexnet.fit(x_train, y_train, batch_size=64, epochs=5, validation_data=(x_val, y_val))

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