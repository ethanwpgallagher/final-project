import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv('trainLabels.csv')
count_per_level = df.groupby('level').size()

plt.bar(count_per_level.index, count_per_level.values)
plt.xlabel('DR Grade', fontsize=15)
plt.ylabel('Number of Images', fontsize=15)
plt.xticks(count_per_level.index, fontsize=15)
plt.yticks(fontsize=15)
plt.tight_layout()
plt.savefig('kaggleTrainingDistribution.png')