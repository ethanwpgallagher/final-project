# used to create the messidor training/testing sets, change of dataset renders this useless

import random
import pandas as pd
import numpy as np
import os
import shutil
import tensorflow as tf
import cv2
import csv
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score
label_dict = {}
TESTING_SET_DIRECTORY = '/Users/ethan/Downloads/Messidor2/train copy/test'

# Messidor 1
def read_labels__and_make_dict_mess1(directory):
    files = os.listdir(directory)
    df = None
    for file in files:
        if file.endswith(('.xls')):
            df = pd.read_excel(os.path.join(directory, file))
    
    grades = df['Retinopathy grade'].unique()
    for grade in grades:
        os.makedirs(os.path.join(directory, str(grade)), exist_ok=True)
    
    for file in files:
        if file.endswith(('.tif')):
            row = df[df['Image name'] == str(file)]
            file_grade = row['Retinopathy grade'].values[0]
            shutil.move(os.path.join(directory, file), os.path.join(directory, str(file_grade)))

def move_classes_from_each_folder(directory):
    train_folder = None
    for folder in os.listdir(directory):
        if 'train' in folder:
            train_folder = os.path.join(directory, folder)

    for folder in os.listdir(directory):
        if 'Base' in folder:
            base_folder = os.path.join(directory, folder)
            for dr_grade in os.listdir(base_folder):
                train_class = os.path.join(train_folder, dr_grade)
                if train_class is not None:
                    base_grade_folder = os.path.join(base_folder, dr_grade)
                    if os.path.isdir(base_grade_folder):
                        for image in os.listdir(base_grade_folder):
                            if image.endswith(('.tif')):
                                image_file_source = os.path.join(base_grade_folder, image)
                                shutil.move(image_file_source, train_class)

# Messidor 2

def create_grade_folders_and_move_images(directory):
    files = os.listdir(directory)
    df = None
    for file in files:
        if file.endswith(('.csv')):
            df = pd.read_csv(os.path.join(directory, file))

    grades = df['adjudicated_dr_grade'].unique()
    for grade in grades:
        os.makedirs(os.path.join(directory, str(grade)), exist_ok=True)

    for file in files:
        if file.endswith(('.JPG', '.png')):
            file = file.replace('.JPG', '.jpg')
            row = df[df['image_id'] == str(file)]
            file_grade = row['adjudicated_dr_grade'].values[0]
            shutil.move(os.path.join(directory, file), os.path.join(directory, str(file_grade)))

def create_test_folder(directory):
    train_folder = os.path.join(directory, 'train')
    test_folder = os.path.join(directory, 'test')
    for i in range(5):
        os.makedirs(os.path.join(test_folder, str(i)), exist_ok=True)

    for i in range(5):
        class_folder = os.path.join(train_folder, str(i))
        if os.path.isdir(class_folder):
            files = os.listdir(class_folder)
            images = [file for file in files if file.endswith(('.jpeg', '.png', '.jpg'))]
            selected_images = random.sample(images, 100)
            for image in selected_images:
                source_path = os.path.join(class_folder, image)
                destination_path = os.path.join(test_folder, str(i))
                shutil.move(source_path, destination_path)


def read_csv_file(filename):
  with open(filename, 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) == 3:
                image_name, label, _ = row
                label_dict[image_name + '.jpeg'] = label
            if len(row) == 2:
              image_name, label = row
              label_dict[image_name + '.jpeg'] = label
            if len(row) == 4:
              image_name, label, _, _ = row
              label_dict[image_name] = label

def get_prediction(model, test_input):
    test_input = tf.convert_to_tensor(test_input)
    test_input = tf.expand_dims(test_input, axis=0)
    return model.predict(test_input)

def get_class_from_probabilities(probabilities):
    predicted_index = np.argmax(probabilities)
    class_labels = ['0', '1', '2', '3', '4']
    return class_labels[predicted_index]

def test_model(model):
    true_labels = []
    predicted_labels = []
    counter = 0
    for root, _, files in os.walk(TESTING_SET_DIRECTORY):
        for filename in files:
            if filename.endswith(('.jpeg', '.jpg', '.png')):
                img_path = os.path.join(root, filename)
                image = cv2.imread(img_path)
                image = cv2.resize(image, (224, 224))
                diagnosis = get_prediction(model, image).tolist()
                predicted_class = get_class_from_probabilities(diagnosis[0])
                if 'augmented' in filename:
                    parts = filename.split('_')
                    filename = '_'.join(parts[1:-1])
                actual_diagnosis = label_dict[filename]

                true_labels.append(actual_diagnosis)
                predicted_labels.append(predicted_class)

    cm = confusion_matrix(true_labels, predicted_labels)
    accuracy = accuracy_score(true_labels, predicted_labels)
    f1 = f1_score(true_labels, predicted_labels, average='weighted')

    class_counts = len(np.unique(true_labels))
    sensitivity = np.zeros(class_counts)
    specificity = np.zeros(class_counts)

    for i in range(class_counts):
        true_positives = cm[i, i]
        false_positives = np.sum(cm[:, i]) - true_positives
        false_negatives = np.sum(cm[i, :]) - true_positives
        true_negatives = np.sum(cm) - (true_positives + false_positives + false_negatives)

        sensitivity[i] = true_positives / (true_positives + false_negatives)
        specificity[i] = true_negatives / (true_negatives + false_positives)

    print("Confusion Matrix:")
    print(cm)
    print(f"Accuracy: {accuracy}")
    print(f"F1 Score: {f1}")
    print("Sensitivity for each class:", sensitivity)
    print("Specificity for each class:", specificity)


if __name__=="__main__":
    create_test_folder('/Users/ethan/Downloads/Messidor2/train copy/')