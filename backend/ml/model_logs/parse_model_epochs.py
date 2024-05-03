import os
import re

class Epoch:
    """
    Represents a training epoch with its associated metrics.

    Attributes:
        epoch_num (int): The number of the epoch.
        train_loss (float): Training loss for this epoch.
        train_accuracy (float): Training accuracy for this epoch.
        val_loss (float): Validation loss for this epoch.
        val_accuracy (float): Validation accuracy for this epoch.
    """

    def __init__(self, epoch_num, train_loss, train_accuracy, val_loss, val_accuracy):
        self.epoch_num = epoch_num
        self.train_loss = train_loss
        self.train_acccuracy = train_accuracy
        self.val_loss = val_loss
        self.val_accuracy = val_accuracy

    def __str__(self):
        """Returns a string representation of the epoch's metrics."""
        return f"Epoch {self.epoch_num}: train_loss={self.train_loss}, train_accuracy={self.train_accuracy}, val_loss={self.val_loss}, val_accuracy={self.val_accuracy}"

    def __json__(self):
        """Serialises the epoch data into a JSON-compatible dictionary."""
        return {
            'epoch_num': self.epoch_num,
            'train_loss': self.train_loss,
            'train_accuracy': self.train_accuracy,
            'val_loss': self.val_loss,
            'val_accuracy': self.val_accuracy
        }
    
class EpochLogParser:
    """
    Parses epoch logs from a given text to extract detailed epoch metrics.

    Attributes:
        log_text (str): Raw string text containing the logs for multiple epochs.
        pattern (re.Pattern): Compiled regex pattern to match the log format.
        epochs_data (dict): Dictionary of parsed epoch data, keyed by epoch number.
    """

    def __init__(self, log_text):
        self.log_text = log_text
        self.pattern = re.compile(r'Epoch (\d+)/(\d+).*?loss: (\d+\.\d+) - accuracy: (\d+\.\d+).*?val_loss: (\d+\.\d+) - val_accuracy: (\d+\.\d+)', re.DOTALL)
        self.epochs_data = self.parse_epochs()


    def parse_epochs(self):
        """Parses the log text and extracts epoch data into a dictionary."""
        result = {}
        for match in re.finditer(self.pattern, self.log_text):
            epoch_num = int(match.group(1))
            total_epochs = int(match.group(2))
            loss = float(match.group(3))
            accuracy = float(match.group(4))
            val_loss = float(match.group(5))
            val_accuracy = float(match.group(6))

            epoch = {
                'epoch_num': epoch_num,
                'total_epochs': total_epochs,
                'loss': loss,
                'accuracy': accuracy,
                'val_loss': val_loss,
                'val_accuracy': val_accuracy
            }
            result[epoch_num] = epoch
        return result

    def get_epoch_data(self, epoch_num):
        """Returns data for a specific epoch number or None if not available."""
        return self.epochs_data.get(epoch_num, None)
    
    def __str__(self) -> str:
        """Returns string representation of all parsed epoch data."""
        return f"epochs_data={self.epochs_data})"
    
    def __json__(self):
        """Serialises the parsed epoch data into a JSON-compatible dictionary."""
        return self.epochs_data

def read_rtf_file(file_path):
    """
    Reads the contents of an RTF file.

    Args:
        file_path (str): Path to the RTF file.

    Returns:
        str: The content of the file.
    """
    with open(file_path, mode='r') as file:
            return file.read()

def load_logs_from_directory(directory):
    """
    Loads and parses all .rtf log files from a specified directory within a specific subdirectory path.

    Args:
        directory (str): Base directory from which the logs will be loaded.

    Returns:
        dict: A dictionary containing model names as keys and parsed log data as values.
    """
    logs_directory = os.path.join(directory, 'ml', 'model_logs', 'epoch_logs')

    log_parsers = {}
    rtf_files = [f for f in os.listdir(logs_directory) if f.endswith('.rtf')]

    for rtf_file in rtf_files:
        model_name = rtf_file.split('.')[0]
        file_path = os.path.join(logs_directory, rtf_file)
        log_text = read_rtf_file(file_path)
        parser = EpochLogParser(log_text)
        log_parsers[model_name] = parser.epochs_data
    return log_parsers
