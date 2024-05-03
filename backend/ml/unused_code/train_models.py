# old code for training the models before the realisation that personal hardware wasnt powerful enough. Moved over to colab
# also contains some file processing code

import csv
from datetime import datetime
import random
import sys
import keras
import os
import shutil
import tensorflow as tf
import matplotlib.pyplot as plt
import numpy as np
from vggnet import vgg_16, vgg_19
from sklearn.utils.class_weight import compute_class_weight
from backend.ml.unused_code.preprocessing import preprocessing, kaggle_augment_training_image, kaggle_bloke_preprocessing, hopeful_preprocessing
import cv2

DATASET_DIRECTORY = "/Users/ethan/Downloads/diabetic-retinopathy-detection-2/train"
NEW_DATASET_DIRECTORY = "/Users/ethan/Downloads/diabetic-retinopathy-detection-2/new-train copy"
MESSIDOR = '/Users/ethan/Downloads/Messidor2/train copy'

def sort_dataset():
    label_dict = {}

    with open('testLabels.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) == 2:
                image_name, label = row
                label_dict[image_name + '.jpeg'] = label
            elif len(row) == 3:
                image_name, label, _ = row
                label_dict[image_name + '.jpeg'] = label

    for label in set(label_dict.values()):
        label_directory = os.path.join(DATASET_DIRECTORY, label)
        os.makedirs(label_directory, exist_ok=True)
    
    return label_dict

def make_full_training_set(label_dict):
    for filename in os.listdir(DATASET_DIRECTORY):
        if filename in label_dict:
            label = label_dict[filename]
            source_path = os.path.join(DATASET_DIRECTORY, filename)
            destination_path = os.path.join(NEW_DATASET_DIRECTORY, label, filename)
            shutil.move(source_path, destination_path)

def copy_random_images(source_directory, destination_directory, num_images_per_class=10):
    os.makedirs(destination_directory, exist_ok=True)

    for class_dir in os.listdir(source_directory):
        class_path = os.path.join(source_directory, class_dir)

        if os.path.isdir(class_path):
            dest_class_path = os.path.join(destination_directory, class_dir)
            os.makedirs(dest_class_path, exist_ok=True)
            class_files = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.jpeg'))]

            selected_images = random.sample(class_files, min(num_images_per_class, len(class_files)))

            for image in selected_images:
                source_path = os.path.join(class_path, image)
                destination_filename = f"{image}"
                destination_path = os.path.join(destination_directory, class_path, destination_filename)
                shutil.copyfile(source_path, destination_path)

def organise_left_right(source_directory):
    for class_dir in os.listdir(source_directory):
        class_path = os.path.join(source_directory, class_dir)
        if os.path.isdir(class_path):
            left_folder = os.path.join(class_path, 'left')
            right_folder = os.path.join(class_path, 'right')
            os.makedirs(left_folder, exist_ok=True)
            os.makedirs(right_folder, exist_ok=True)
            images = os.listdir(class_path)
            images = [f for f in images if f.lower().endswith(('.jpg', '.jpeg'))]
            for image in images:
                eye_side = 'left' if 'left' in image else 'right'
                dest_folder = left_folder if eye_side == 'left' else right_folder
                source_path = os.path.join(class_path, image)
                dest_path = os.path.join(dest_folder, image)
                shutil.move(source_path, dest_path)

def print_left_right_images(source_directory):
    for class_id in range(5):
        class_folder = os.path.join(source_directory, str(class_id))

        if not os.path.exists(class_folder):
            continue

        left_count = 0
        right_count = 0

        for eye_side in ['left', 'right']:
            eye_folder = os.path.join(class_folder, eye_side)
            if os.path.exists(eye_folder):
                eye_images = os.listdir(eye_folder)
                if eye_side == 'left':
                    left_count = len(eye_images)
                else:
                    right_count = len(eye_images)

        print(f"Class {class_id}: Left - {left_count}, Right - {right_count}")

def create_new_dataset(source_directory, destination_directory, target_count=5000):
    destination_train_folder = os.path.join(destination_directory, 'train')
    destination_test_folder = os.path.join(destination_directory, 'test')
    
    os.makedirs(destination_train_folder, exist_ok=True)
    os.makedirs(destination_test_folder, exist_ok=True)
    for class_id in range(5):
        class_folder = os.path.join(source_directory, str(class_id))
        destination_train_class_folder = os.path.join(destination_train_folder, str(class_id))
        destination_test_class_folder = os.path.join(destination_test_folder, str(class_id))

        if not os.path.exists(class_folder):
            continue

        os.makedirs(destination_train_class_folder, exist_ok=True)
        os.makedirs(destination_test_class_folder, exist_ok=True)

        selected_images = random.sample([file for file in os.listdir(class_folder)], min(target_count, len(os.listdir(class_folder))))
        
        test_images = selected_images[:500]
        train_images = selected_images[500:]

        for image in test_images:
            source_path = os.path.join(class_folder, image)
            destination_path = os.path.join(destination_test_class_folder, image)
            shutil.copyfile(source_path, destination_path)

        for image in train_images:
            source_path = os.path.join(class_folder, image)
            destination_path = os.path.join(destination_train_class_folder, image)
            shutil.copyfile(source_path, destination_path)

def maybe_augment_folder(directory, target_count=1017):
    for i in range(5):
        class_folder = os.path.join(directory, str(i))

        total_count = len(os.listdir(class_folder))
        if total_count < target_count:
            images_needed = target_count - total_count
            images_per_file = images_needed // total_count
            remainder = images_needed % total_count

            for image in os.listdir(class_folder):
                if 'augmented' not in image:
                    source_path = os.path.join(class_folder, image)
                    num_augmentations = images_per_file + (1 if remainder > 0 else 0)
                    remainder -= 1

                    for _ in range(num_augmentations):
                        augmented_image = kaggle_augment_training_image(cv2.imread(source_path))
                        if augmented_image is not None:
                            timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
                            augmented_destination_path = os.path.join(class_folder, f"augmented_{image.replace('.jpeg', '')}_{timestamp}.jpeg")
                            cv2.imwrite(augmented_destination_path, augmented_image)
                        if len(os.listdir(class_folder)) > target_count:
                            return

def count_left_right_images(class_folder):
    left_folder = os.path.join(class_folder, 'left')
    right_folder = os.path.join(class_folder, 'right')

    left_count = len(os.listdir(left_folder))
    right_count = len(os.listdir(right_folder))

    return left_count, right_count

def new_process_images_in_directory(directory, img_size=(224, 224)):
    for root, _, files in os.walk(directory):
        print("Processing images in folder:", root)
        for filename in files:
            if filename.endswith(('.jpeg', '.jpg', '.png', '.JPG')):
                img_path = os.path.join(root, filename)
                hopeful_preprocessing(img_path)
        

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
    return folder_counts

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
