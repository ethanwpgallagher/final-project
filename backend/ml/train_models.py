import csv
import keras
import os
import shutil

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

def load_dataset():
    dataset = keras.utils.image_dataset_from_directory(
        DATASET_DIRECTORY,
        labels='inferred',
        label_mode='int',
        class_names=None,
        color_mode='rgb',
        batch_size=None,
        image_size=(256, 256),
        shuffle=True
    )
    return dataset

if __name__ == "__main__":
    dataset = load_dataset()
    print(dataset)