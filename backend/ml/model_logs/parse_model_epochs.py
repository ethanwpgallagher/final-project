# Api request sent from front end, select model, training or test data, or both to overlap
# Training data, test data, both, objects or dictionaries?
# parse into preferred format then sort out requests
import os
import re

class Epoch:
    def __init__(self, epoch_num, train_loss, train_accuracy, val_loss, val_accuracy):
        self.epoch_num = epoch_num
        self.train_loss = train_loss
        self.train_acccuracy = train_accuracy
        self.val_loss = val_loss
        self.val_accuracy = val_accuracy

class EpochLogParser:
    def __init__(self, log_text):
        self.log_text = log_text
        self.pattern = re.compile('Epoch (\d+)/(\d+).*?loss: (\d+\.\d+) - accuracy: (\d+\.\d+).*?val_loss: (\d+\.\d+) - val_accuracy: (\d+\.\d+)')
        self.epochs_data = {}

    def parse_epochs(self):
        for match in re.finditer(self.pattern, self.log_text):
            epoch_num = int(match.group(1))
            total_epochs = int(match.group(2))
            loss = float(match.group(3))
            accuracy = float(match.group(4))
            val_loss = float(match.group(5))
            val_accuracy = float(match.group(6))

            epoch = Epoch(epoch_num, loss, accuracy, val_loss, val_accuracy)
            self.epochs_data[epoch_num] = epoch

    def get_epoch_data(self, epoch_num):
        return self.epochs_data.get(epoch_num, None)

def read_rtf_file(file_path):
    with open(file_path, 'r') as file:
        return file.read()    

def load_logs_from_directory(directory):
    logs_directory = os.path.join(directory, 'ml', 'model_logs', 'epoch_logs')

    log_parsers = {}
    rtf_files = [f for f in os.listdir(logs_directory) if f.endswith('.rtf')]

    for rtf_file in rtf_files:
        model_name = rtf_file.split('_')[0]
        file_path = os.path.join(logs_directory, rtf_file)
        log_text = read_rtf_file(file_path)
        parser = EpochLogParser(log_text)
        parser.parse_epochs()
        log_parsers[model_name] = parser

    return log_parsers