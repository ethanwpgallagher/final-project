import parse_model_epochs
import numpy as np
import scipy.stats as stats

epoch_log_parsers = parse_model_epochs.load_logs_from_directory('/Users/ethan/Desktop/ComputerScienceUniWork/Year 3/final-project/backend/')

model_val_accuracies = {
    'densenet': [epoch['val_accuracy'] for epoch in epoch_log_parsers['densenet'].values()],
    'inceptionv3': [epoch['val_accuracy'] for epoch in epoch_log_parsers['inceptionv3'].values()],
    'alexnet': [epoch['val_accuracy'] for epoch in epoch_log_parsers['alexnet'].values()],
    'mobilenet': [epoch['val_accuracy'] for epoch in epoch_log_parsers['mobilenet'].values()],
    'resnet': [epoch['val_accuracy'] for epoch in epoch_log_parsers['resnet'].values()]
}

def perform_t_test(model1_data, model2_data):
    t_stat, p_val = stats.ttest_ind(model1_data, model2_data, equal_var=False)
    return t_stat, p_val

model_names = list(model_val_accuracies.keys())
results = {}

for i in range(len(model_names)):
    for j in range(i + 1, len(model_names)):
        model1_name = model_names[i]
        model2_name = model_names[j]
        t_stat, p_val = perform_t_test(model_val_accuracies[model1_name], model_val_accuracies[model2_name])
        results[f'{model1_name} vs {model2_name}'] = {
            't_statistic': t_stat,
            'p_value': p_val
        }

for comparison, res in results.items():
    print(f"T-test between {comparison}:")
    print(f"  T-Statistic: {res['t_statistic']:.3f}, P-value: {res['p_value']:.4f}")
    print()