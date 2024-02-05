import csv
import random
import sys
import keras
import os
import shutil
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from alexnet import alex_net
from vggnet import vgg_16, vgg_19
from sklearn.utils.class_weight import compute_class_weight
from preprocessing import preprocessing

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

def copy_random_images(source_directory, destination_directory, num_images_per_class=10):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_directory, exist_ok=True)

    # Iterate over subdirectories in the source directory
    for class_dir in os.listdir(source_directory):
        class_path = os.path.join(source_directory, class_dir)

        # Check if it's a directory
        if os.path.isdir(class_path):
            # List all files in the class directory
            class_files = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.jpeg'))]

            # Randomly select num_images_per_class images
            selected_images = random.sample(class_files, min(num_images_per_class, len(class_files)))

            # Copy selected images to the destination directory
            for image in selected_images:
                source_path = os.path.join(class_path, image)
                # Create a unique filename in the destination directory
                destination_filename = f"{class_dir}_{image}"
                destination_path = os.path.join(destination_directory, destination_filename)
                shutil.copyfile(source_path, destination_path)


def process_images_in_directory(directory_path, img_size=(224, 224)):
    for root, _, files in os.walk(directory_path):
        for filename in files:
            print(filename)
            if filename.endswith(('.jpeg', '.jpg', '.png')):
                img_path = os.path.join(root, filename)
                preprocessing(img_path, img_size)


def load_dataset() -> tf.data.Dataset:
    train_ds, val_ds = keras.utils.image_dataset_from_directory(
        DATASET_DIRECTORY,
        labels='inferred',
        label_mode='int',
        class_names=None,
        color_mode='rgb',
        batch_size=2**5,
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

def visualise_preprocessed_images(model, dataset):
    sample_images, _ = next(iter(dataset.take(1)))
    preprocessed_images = model.get_layer("preprocessing_layer")(sample_images)
    num_images = min(preprocessed_images.shape[0], 5)
    plt.figure(figsize=(15, 3))
    for i in range(num_images):
        plt.subplot(1, num_images, i+1)
        plt.imshow(np.squeeze(preprocessed_images[i]))
        plt.title(f'Image {i+1}')
        plt.axis('off')
    plt.show()

def get_class_weights(directory):
    folder_counts = {}

    for folder_name in os.listdir(directory):
        folder_path = os.path.join(directory, folder_name)

        if os.path.isdir(folder_path):
            num_images = len([file for file in os.listdir(folder_path)])
            folder_counts[folder_name] = num_images
    classes = np.array(list(map(int, folder_counts.keys())))
    counts = np.array(list(folder_counts.values()))
    weights = compute_class_weight('balanced', classes=np.unique(classes), y=classes)  
    return weights

def apply_data_augmentation(image, label):
    data_augmentation = keras.preprocessing.image.ImageDataGenerator(
        rotation_range=20,
        width_shift_range=0.2,
        height_shift_range=0.2,
        shear_range=0.2,
        zoom_range=0.2,
        horizontal_flip=True,
        fill_mode='nearest'
    )
    image = tf.image.convert_image_dtype(image, tf.float32)
    img_shape = tf.shape(image)
    if img_shape._rank == 3:
        augmented_image = data_augmentation.random_transform(image, seed=None)
    else:
        augmented_image = image
    return augmented_image, label

if __name__ == "__main__":
    train_ds, val_ds = load_dataset()
    augmented_train_ds = train_ds.map(apply_data_augmentation)
    alexnet = alex_net(input_shape=(224, 224, 3))

    # Build the model
    alexnet.build(input_shape=(224, 224, 3))

    # Compile the model
    epochs = 20
    log_dir = './logs'
    callbacks = [
        keras.callbacks.ModelCheckpoint("alexnet_at_{epoch}.keras"),
        keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1, write_images=True),
        keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)
    ]

    alexnet.summary()
    alexnet.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    history = alexnet.fit(
        augmented_train_ds,
        epochs=epochs,
        callbacks=callbacks,
        validation_data=val_ds,
        class_weight=dict(enumerate(get_class_weights(directory=DATASET_DIRECTORY)))
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
