import csv
import cv2
import os
import numpy as np
import pandas as pd
from preprocessing import preprocessing
from ml_app import get_saved_model, get_prediction
import random
import shutil
from sklearn.metrics import confusion_matrix, accuracy_score, f1_score

DATASET_DIRECTORY = '/Users/ethan/Downloads/diabetic-retinopathy-detection/new_test'
label_dict = {}

def process_images_in_directory(directory_path, img_size=(224, 224)):
    for root, _, files in os.walk(directory_path):
        for filename in files:
            print(filename)
            if filename.endswith(('.jpeg', '.jpg', '.png')):
                img_path = os.path.join(root, filename)
                preprocessing(img_path, img_size)

def create_label_dict():
    with open('testLabels.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        for row in csv_reader:
            if len(row) == 3:
                image_name, label, _ = row
                label_dict[image_name + '.jpeg'] = label
    
def get_testing_count():
    df = pd.read_csv('testLabels.csv')
    level_count = df.groupby('level').size()
    level_count_dict = level_count.to_dict()
    return level_count_dict

def create_new_test_with_better_counts(source_directory, destination_directory, num_images_per_class=1206):
    os.makedirs(destination_directory, exist_ok=True)
    
    class_dict = {}
    with open('testLabels.csv', 'r') as csvfile:
        csv_reader = csv.reader(csvfile)
        next(csv_reader)
        for row in csv_reader:
            if len(row) == 3:
                image_name, label, _ = row
                class_name = f'Class_{label}'
                if class_name not in class_dict:
                    class_dict[class_name] = []
                class_dict[class_name].append(image_name + '.jpeg')

    for class_name, images in class_dict.items():
        random_sample = random.sample(images, min(num_images_per_class, len(images)))

        for img in random_sample:
            src_path = os.path.join(source_directory, img)
            dst_path = os.path.join(destination_directory, img)
            shutil.copy(src_path, dst_path)
            
def check_sample_count(directory, label_dict):
    class_counts = {}

    for filename in os.listdir(directory):
        if filename in label_dict:
            label = label_dict[filename]
            class_counts[label] = class_counts.get(label, 0) + 1

    return class_counts

def get_class_from_probabilities(probabilities):
    predicted_index = np.argmax(probabilities)
    class_labels = ['0', '1', '2', '3', '4']
    return class_labels[predicted_index]

def get_prediction_and_compare(model_name):
    true_labels = []
    predicted_labels = []
    model = get_saved_model(model_name)
    counter = 0
    for root, _, files in os.walk(DATASET_DIRECTORY):
        for filename in files:
            if filename.endswith(('.jpeg', '.jpg', '.png')):
                img_path = os.path.join(root, filename)
                image = cv2.imread(img_path)
                diagnosis = get_prediction(model, image).tolist()
                predicted_class = get_class_from_probabilities(diagnosis[0])
                actual_diagnosis = label_dict[filename]

                true_labels.append(actual_diagnosis)
                predicted_labels.append(predicted_class)
                counter += 1
                print(counter)

    cm = confusion_matrix(true_labels, predicted_labels)
    accuracy = accuracy_score(true_labels, predicted_labels)
    f1 = f1_score(true_labels, predicted_labels)

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

if __name__ == "__main__":
    create_label_dict()
    get_prediction_and_compare('Alexnet')
