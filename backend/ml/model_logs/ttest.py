import parse_model_epochs
import scipy.stats as stats

# Load epoch log data from specified directory for multiple models.
epoch_log_parsers = parse_model_epochs.load_logs_from_directory('/Users/ethan/Desktop/ComputerScienceUniWork/Year 3/final-project/backend/')

# Extract validation accuracies for each model from the loaded log data.
model_val_accuracies = {
    'densenet': [epoch['val_accuracy'] for epoch in epoch_log_parsers['densenet'].values()],
    'inceptionv3': [epoch['val_accuracy'] for epoch in epoch_log_parsers['inceptionv3'].values()],
    'alexnet': [epoch['val_accuracy'] for epoch in epoch_log_parsers['alexnet'].values()],
    'mobilenet': [epoch['val_accuracy'] for epoch in epoch_log_parsers['mobilenet'].values()],
    'resnet': [epoch['val_accuracy'] for epoch in epoch_log_parsers['resnet'].values()]
}

def perform_t_test(model1_data, model2_data):
    """
    Performs an independent two-sample t-test on the validation accuracies between two models.

    Args:
        model1_data (list): Validation accuracies of the first model.
        model2_data (list): Validation accuracies of the second model.

    Returns:
        tuple: A tuple containing the t-statistic and the p-value of the t-test.
    """
    t_stat, p_val = stats.ttest_ind(model1_data, model2_data, equal_var=False)
    return t_stat, p_val

# List of model names extracted from the keys of model_val_accuracies dictionary.
model_names = list(model_val_accuracies.keys())

# Dictionary to store the results of t-tests between model pairs.
results = {}

# Iterate through all pairs of models and perform t-tests.
for i in range(len(model_names)):
    for j in range(i + 1, len(model_names)):
        model1_name = model_names[i]
        model2_name = model_names[j]
        t_stat, p_val = perform_t_test(model_val_accuracies[model1_name], model_val_accuracies[model2_name])
        results[f'{model1_name} vs {model2_name}'] = {
            't_statistic': t_stat,
            'p_value': p_val
        }

# Print the t-test results for each comparison.
for comparison, res in results.items():
    print(f"T-test between {comparison}:")
    print(f"  T-Statistic: {res['t_statistic']:.3f}, P-value: {res['p_value']:.4f}")
    print()