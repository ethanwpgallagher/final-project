# Api request sent from front end, select model, training or test data, or both to overlap
# Training data, test data, both, objects or dictionaries?
# parse into preferred format then sort out requests
import os
import re
import numpy as np

class Result:
    def __init__(self, confusion_matrix, accuracy, f1, sensitivity, specificity):
        self.confusion_matrix = confusion_matrix
        self.accuracy = accuracy
        self.f1 = f1
        self.sensitivity = sensitivity
        self.specificity = specificity
        
    def __str__(self):
        result_str = "Confusion Matrix:\n"
        result_str += "\n".join([" ".join(map(str, row)) for row in self.confusion_matrix])
        result_str += f"\nAccuracy: {self.accuracy}\n"
        result_str += f"F1 Score: {self.f1}\n"
        result_str += f"Sensitivity for each class: {self.sensitivity}\n"
        result_str += f"Specificity for each class: {self.specificity}\n"
        return result_str
    
    def __json__(self):
        return {
            'confusion_matrix': self._convert_to_json(self.confusion_matrix),
            'accuracy': self.accuracy,
            'f1': self.f1,
            'sensitivity': self.sensitivity.tolist(),
            'specificity': self.specificity.tolist()
        }
    
    def _convert_to_json(self, value):
        if isinstance(value, np.ndarray):
            return value.tolist()  # Convert NumPy array to Python list
        else:
            return value

class ResultLogParser:
    def __init__(self, log_text):
        self.log_text = log_text
        self.result_data = {}
        self.parse_results()

    def parse_results(self):
        self.parse_confusion_matrix()
        self.parse_accuracy()
        self.parse_f1_score()
        self.parse_sensitivity()
        self.parse_specificity()

    def parse_confusion_matrix(self):
        confusion_matrix_strs = re.findall(r'Confusion Matrix:(.*?)Accuracy:', self.log_text, re.DOTALL)
        if confusion_matrix_strs:
            confusion_matrix_str = confusion_matrix_strs[0].strip()
            rows = confusion_matrix_str.split('\n')
            confusion_matrix = []
            for row in rows:
                row = row.strip()  # Remove extra whitespaces
                row = row.replace('\\', '')  # Remove backslashes
                row = row.replace('[', '').replace(']', '')  # Remove unnecessary brackets
                # Extract numerical values using regular expression
                row_values = [int(val) for val in row.split()]
                if row_values:  # Check if the row is not empty
                    confusion_matrix.append(row_values)

            # Check if all rows have the same length
            row_lengths = set(len(row) for row in confusion_matrix)
            if len(row_lengths) != 1:
                print("Error: Inconsistent row lengths in the confusion matrix.")
                return

            cm = np.array(confusion_matrix, dtype=int)
            self.result_data['Confusion Matrix'] = cm
        else:
            self.result_data['Confusion Matrix'] = None

    def parse_accuracy(self):
        accuracy_str = re.findall(r'Accuracy: (.*?)\n', self.log_text)[0]
        self.result_data['Accuracy'] = accuracy_str

    def parse_f1_score(self):
        f1_score_str = re.findall(r'F1 Score: (.*?)\n', self.log_text)[0]
        self.result_data['F1 Score'] = f1_score_str

    def parse_sensitivity(self):
        sensitivity_str = re.findall(r'Sensitivity for each class: \[(.*?)\]', self.log_text)[0]
        sensitivity_str_arr = np.array([float(val) for val in sensitivity_str.split()])
        self.result_data['Sensitivity'] = sensitivity_str_arr

    def parse_specificity(self):
        specificity_str = re.findall(r'Specificity for each class: \[(.*?)\]', self.log_text)[0]
        specificity_str_arr = np.array([float(val) for val in specificity_str.split()])
        self.result_data['Specificity'] = specificity_str_arr

    def __str__(self):
        result_str = ""
        for key, value in self.result_data.items():
            if key == 'Confusion Matrix':
                result_str += f"{key}:\n{value}\n"
            else:
                result_str += f"{key}: {value}\n"
        return result_str
    
    def __json__(self):
        return self.result_data
        
def read_rtf_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()    

def load_logs_from_directory(directory):
    logs_directory = os.path.join(directory, 'ml', 'model_logs', 'test_logs')

    result_parsers = {}
    rtf_files = [f for f in os.listdir(logs_directory) if f.endswith('.rtf')]

    for rtf_file in rtf_files:
        model_name = rtf_file.split('_')[0]
        file_path = os.path.join(logs_directory, rtf_file)
        log_text = read_rtf_file(file_path)
        parser = ResultLogParser(log_text)
        result_parsers[model_name] = parser
    return result_parsers
