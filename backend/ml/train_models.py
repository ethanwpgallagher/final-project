import csv
import datetime
import cv2
import math
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
from googlenet import google_net
from sppnet import spp_net
from sklearn.utils.class_weight import compute_class_weight
from preprocessing import preprocessing, data_augmentation
from config import NUM_EPOCHS, DATASET_DIRECTORY, TRAINING_SET_DIRECTORY

MODELS_DICT = {
    "alexnet": [alex_net(), (224, 224, 3)],
    "vgg_19": [vgg_19(), (None, 224, 224, 3)],
    "vgg_16": [vgg_16(), (None, 224, 224, 3)],
    "googlenet": [google_net(), (None, 224, 224, 3)],
    "sppnet": [spp_net(), (None, 32, 32, 3)]
}

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
    os.makedirs(destination_directory, exist_ok=True)

    for class_dir in os.listdir(source_directory):
        class_path = os.path.join(source_directory, class_dir)

        if os.path.isdir(class_path):
            class_files = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.jpeg'))]

            selected_images = random.sample(class_files, min(num_images_per_class, len(class_files)))

            for image in selected_images:
                source_path = os.path.join(class_path, image)
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
        TRAINING_SET_DIRECTORY,
        labels='inferred',
        label_mode='int',
        class_names=None,
        color_mode='rgb',
        batch_size=2**5,
        image_size=(224, 224),
        shuffle=True,
        validation_split=0.18,
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

def train_model(model_name, model, input_shape, train_ds, val_ds):
    model.build(input_shape)
    epochs = NUM_EPOCHS
    log_dir = './logs'
    callbacks = [
        keras.callbacks.ModelCheckpoint((f"{model_name}_at_{{epoch}}.keras"), save_best_only=True, monitor=['val_loss']),
        keras.callbacks.TensorBoard(log_dir=log_dir, histogram_freq=1, write_images=True),
        keras.callbacks.ReduceLROnPlateau(monitor='val_loss', factor=0.2, patience=3, min_lr=1e-6)
    ]
    model.summary()
    model.compile(optimizer='adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])

    history = model.fit(
        train_ds,
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
    plt.savefig(model_name)

def sample_dataset():
    csv_file = 'trainLabels.csv'
    with open(csv_file, newline='') as csvfile:
        csv_reader = csv.DictReader(csvfile)
        data = list(csv_reader)
        
    level_counts = {}
    for row in data:
        level = int(row['level'])
        level_counts[level] = level_counts.get(level, 0) + 1

    # Print the results
    for level, count in sorted(level_counts.items()):
        print(f"Level {level}: {count} images")

def create_new_balanced_dataset(source_directory, destination_directory):
    average_count = 7025
    class_counts = {class_label: len(os.listdir(os.path.join(source_directory, str(class_label)))) for class_label in range(5)}
    os.makedirs(destination_directory, exist_ok=True)

    for class_label, count in class_counts.items():
        source_class_directory = os.path.join(source_directory, str(class_label))
        destination_class_directory = os.path.join(destination_directory, str(class_label))
        os.makedirs(destination_class_directory, exist_ok=True)

        if count > average_count:
            class_images = os.listdir(source_class_directory)
            selected_images = random.sample(class_images, average_count-1)
            for image in selected_images:
                source_path = os.path.join(source_class_directory, image)
                destination_path = os.path.join(destination_class_directory, image)
                shutil.copyfile(source_path, destination_path)
        else:
            class_images = os.listdir(source_class_directory)
            selected_images = []
            augment_and_save_images(class_images, source_class_directory, destination_class_directory, average_count)
                

def augment_and_save_images(class_images, source_class_directory, destination_class_directory, average_count):
    counter = 0
    for image in class_images:
        source_path = os.path.join(source_class_directory, image)
        destination_path = os.path.join(destination_class_directory, image)
        shutil.copyfile(source_path, destination_path)
    total_count = len(class_images)
    while total_count < average_count:
        for i in range(len(class_images)):
            source_path = os.path.join(source_class_directory, class_images[i])
            destination_path = os.path.join(destination_class_directory, class_images[i])
            
            augmented_image = data_augmentation(source_path)
            augmented_filename = "augmented_" + str(datetime.datetime.now()) + "_" + class_images[i]
            augmented_destination_path = os.path.join(destination_class_directory, augmented_filename)
            cv2.imwrite(augmented_destination_path, augmented_image)

            total_count += 1
            if total_count >= average_count:
                break

def count_images_per_folder(path):
    folder_counts = {}

    for folder in os.listdir(path):
        folder_path = os.path.join(path, folder)

        if os.path.isdir(folder_path):
            image_count = len([file for file in os.listdir(folder_path) if file.lower().endswith(('.jpg', '.jpeg', '.png'))])
            folder_counts[folder] = image_count

    return folder_counts

if __name__ == "__main__":
    # train_ds, val_ds = load_dataset()
    # arg = sys.argv[1]
    #train_model(arg, MODELS_DICT[arg][0], MODELS_DICT[arg][1], train_ds, val_ds)
    create_new_balanced_dataset(DATASET_DIRECTORY, "/Users/ethan/Downloads/diabetic-retinopathy-detection/new_train")
