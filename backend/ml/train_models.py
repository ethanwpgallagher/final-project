import csv
import keras
import os
import shutil
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from alexnet import alex_net
from keras import losses, optimizers

DATASET_DIRECTORY = "/Users/ethan/Downloads/diabetic-retinopathy-detection/train"

def sort_dataset():
    label_dict = {}

    with open('trainLabels.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) == 2:
                image_name, label = row
                label_dict[image_name + '.jpeg'] = label

    for label in set(label_dict.values()):
        label_directory = os.path.join(DATASET_DIRECTORY, label)
        os.makedirs(label_directory, exist_ok=True)

    for filename in os.listdir(DATASET_DIRECTORY):
        if filename in label_dict:
            label = label_dict[filename]
            source_path = os.path.join(DATASET_DIRECTORY, filename)
            destination_path = os.path.join(DATASET_DIRECTORY, label, filename)
            shutil.move(source_path, destination_path)

def load_dataset() -> tf.data.Dataset:
    train_ds, val_ds = keras.utils.image_dataset_from_directory(
        DATASET_DIRECTORY,
        labels='inferred',
        label_mode='int',
        class_names=None,
        color_mode='rgb',
        batch_size=128,
        image_size=(224, 224),
        shuffle=True,
        validation_split=0.2,
        subset='both',
        seed=1337
    )
    return train_ds, val_ds

def visualise_first_few(dataset):
    plt.figure(figsize=(10, 10))
    for images, labels in dataset.take(1):
        print("Labels shape:", labels.shape)
        print("Labels values:", labels.numpy())
        
        if len(labels.shape) == 0:
            labels = [labels]

        for i in range(min(9, len(labels))):
            ax = plt.subplot(3, 3, i + 1)
            plt.imshow(np.array(images[i]).astype("uint8"))
            plt.title(int(labels[i]))
            plt.axis("off")
    plt.show()


if __name__ == "__main__":
    train_ds, val_ds = load_dataset()
    # Create an instance of your model
    alexnet = alex_net(input_shape=(224, 224, 3))

    # Build the model
    alexnet.build(input_shape=(224, 224, 3))

    # Compile the model
    epochs = 1

    callbacks = [
        keras.callbacks.ModelCheckpoint("alexnet_at_{epoch}.keras"),
        keras.callbacks.TensorBoard(log_dir="./logs", histogram_freq=1)
    ]

    alexnet.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    history = alexnet.fit(
        train_ds,
        epochs=epochs,
        callbacks=callbacks,
        validation_data=val_ds,
    )    
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
