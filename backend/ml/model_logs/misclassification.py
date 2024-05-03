import numpy as np
import pandas as pd

# DenseNet confusion matrix for example
data = np.array([
    [291, 9, 4, 3, 3],
    [15, 236, 4, 12, 5],
    [2, 5, 307, 0, 0],
    [3, 14, 1, 270, 9],
    [2, 9, 0, 11, 290]
])

labels = ["Mild", "Moderate", "No_DR", "Proliferate_DR", "Severe"]

df = pd.DataFrame(data, index=labels, columns=labels)

def find_misclassifications(confusion_matrix, class_labels):
    '''
    Function to calculate the misclassifications in a confusion matrix
    '''
    misclassifications = []
    for i in range(len(class_labels)):
        for j in range(len(class_labels)):
            if i != j and confusion_matrix.iloc[i, j] > 0:
                misclassifications.append({
                    "Actual Class": class_labels[i],
                    "Predicted Class": class_labels[j],
                    "Count": confusion_matrix.iloc[i, j]
                })
    return pd.DataFrame(misclassifications)

misclassifications_df = find_misclassifications(df, labels)
print(misclassifications_df.sort_values(by="Count", ascending=False))