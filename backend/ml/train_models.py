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
from alexnet import alex_net
from vggnet import vgg_16, vgg_19
from sklearn.utils.class_weight import compute_class_weight
from preprocessing import preprocessing, kaggle_augment_training_image, kaggle_bloke_preprocessing
import cv2

DATASET_DIRECTORY = "/Users/ethan/Downloads/diabetic-retinopathy-detection-2/train"
NEW_DATASET_DIRECTORY = "/Users/ethan/Downloads/diabetic-retinopathy-detection-2/new-train copy"

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

    # for label in set(label_dict.values()):
    #     label_directory = os.path.join(DATASET_DIRECTORY, label)
    #     os.makedirs(label_directory, exist_ok=True)
    
    return label_dict

def make_full_training_set(label_dict):
    for filename in os.listdir(DATASET_DIRECTORY):
        if filename in label_dict:
            label = label_dict[filename]
            source_path = os.path.join(DATASET_DIRECTORY, filename)
            destination_path = os.path.join(NEW_DATASET_DIRECTORY, label, filename)
            shutil.move(source_path, destination_path)

def copy_random_images(source_directory, destination_directory, num_images_per_class=10):
    # Create the destination directory if it doesn't exist
    os.makedirs(destination_directory, exist_ok=True)

    # Iterate over subdirectories in the source directory
    for class_dir in os.listdir(source_directory):
        class_path = os.path.join(source_directory, class_dir)

        # Check if it's a directory
        if os.path.isdir(class_path):
            dest_class_path = os.path.join(destination_directory, class_dir)
            os.makedirs(dest_class_path, exist_ok=True)
            # List all files in the class directory
            class_files = [f for f in os.listdir(class_path) if f.lower().endswith(('.jpg', '.jpeg'))]

            # Randomly select num_images_per_class images
            selected_images = random.sample(class_files, min(num_images_per_class, len(class_files)))

            # Copy selected images to the destination directory
            for image in selected_images:
                source_path = os.path.join(class_path, image)
                # Create a unique filename in the destination directory
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

def create_new_dataset(source_directory, destination_directory, target_count_per_eye=2500):
    for class_id in range(5):
        class_folder = os.path.join(source_directory, str(class_id))
        destination_class_folder = os.path.join(destination_directory, str(class_id))

        if not os.path.exists(class_folder):
            continue

        os.makedirs(destination_class_folder, exist_ok=True)

        left_count, right_count = count_left_right_images(class_folder)

        # Get list of original images for left and right eyes
        left_images = os.listdir(os.path.join(class_folder, 'left'))
        right_images = os.listdir(os.path.join(class_folder, 'right'))

        # Sample 2500 images per eye if count exceeds 2500
        selected_left_images = random.sample(left_images, min(target_count_per_eye, left_count))
        selected_right_images = random.sample(right_images, min(target_count_per_eye, right_count))

        # Copy selected images to the destination directory
        for image in selected_left_images:
            source_path = os.path.join(class_folder, 'left', image)
            destination_path = os.path.join(destination_class_folder, image)
            shutil.copyfile(source_path, destination_path)

        for image in selected_right_images:
            source_path = os.path.join(class_folder, 'right', image)
            destination_path = os.path.join(destination_class_folder, image)
            shutil.copyfile(source_path, destination_path)

def maybe_augment_folder(directory):
    class_folder = os.path.join(directory, str(4))
    
    # Create a subset of the directory containing only original images
    original_images = [image for image in os.listdir(class_folder) if 'augmented' not in os.path.join(class_folder, image)]
    for image in original_images:
        source_path = os.path.join(class_folder, image)
        augmented_image = kaggle_augment_training_image(cv2.imread(source_path))
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        augmented_destination_path = os.path.join(class_folder, f"augmented_{image}_{timestamp}.jpeg")
        cv2.imwrite(augmented_destination_path, augmented_image)
        if len(os.listdir(class_folder)) >= 5000:
            break

def count_left_right_images(class_folder):
    left_folder = os.path.join(class_folder, 'left')
    right_folder = os.path.join(class_folder, 'right')

    left_count = len(os.listdir(left_folder))
    right_count = len(os.listdir(right_folder))

    return left_count, right_count

def random_sample_with_unique_ids(folder, sample_size):
    images_by_patient = {}
    unique_ids = set()

    for image in os.listdir(folder):
        patient_id = image.split('_')[0]
        images_by_patient.setdefault(patient_id, []).append(image)

    selected_images = []
    while len(selected_images) < sample_size:
        remaining_sample_size = sample_size - len(selected_images)
        for patient_id, images in images_by_patient.items():
            if remaining_sample_size <= 0:
                break
            selected = min(len(images), remaining_sample_size)
            selected_images.extend(random.sample(images, selected))
            unique_ids.add(patient_id)
            remaining_sample_size -= selected

    return selected_images


def new_process_images_in_directory(directory, img_size=(224, 224)):
    for root, _, files in os.walk(directory):
        for filename in files:
            if filename.endswith(('.jpeg', '.jpg', '.png')):
                img_path = os.path.join(root, filename)
                kaggle_bloke_preprocessing(img_path)
                print(filename)

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

if __name__ == "__main__":
    # new_process_images_in_directory(NEW_DATASET_DIRECTORY)
    # testing_set = '/Users/ethan/Desktop/ComputerScienceUniWork/Year 3/FinalProject/final-project/backend/ml/testing_images'
    # for root, dirs, files in os.walk(testing_set):
    #     for file in files:
    #         file_path = os.path.join(root, file)
    #         if file_path.endswith(('.jpeg', '.jpg', '.png')):
    #             kaggle_bloke_preprocessing(file_path)
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

