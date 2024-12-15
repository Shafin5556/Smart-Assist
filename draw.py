import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Load the dataset
file_path = 'dummy_crop_environment_data.csv'
data = pd.read_csv(file_path)

# Convert date and time columns to a datetime format for time-series analysis
data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['time'])

# List of numerical columns for analysis
columns_to_analyze = ['temperature', 'humidity', 'light_intensity']

# 1. Time-Series Line Graphs
for column in columns_to_analyze:
    plt.figure(figsize=(10, 6))
    plt.plot(data['datetime'], data[column], label=column.capitalize(), color='blue')
    plt.title(f'Time-Series Trend of {column.capitalize()}')
    plt.xlabel('Datetime')
    plt.ylabel(column.capitalize())
    plt.legend()
    plt.grid()
    plt.tight_layout()
    plt.savefig(f'time_series_{column}.png')
    plt.close()

# 2. Histograms
for column in columns_to_analyze:
    plt.figure(figsize=(8, 6))
    plt.hist(data[column], bins=30, color='skyblue', edgecolor='black')
    plt.title(f'Histogram of {column.capitalize()}')
    plt.xlabel(column.capitalize())
    plt.ylabel('Frequency')
    plt.tight_layout()
    plt.savefig(f'histogram_{column}.png')
    plt.close()

# 3. Box Plots
for column in columns_to_analyze:
    plt.figure(figsize=(8, 6))
    sns.boxplot(data[column], orient='h', color='lightgreen')
    plt.title(f'Box Plot of {column.capitalize()}')
    plt.xlabel(column.capitalize())
    plt.tight_layout()
    plt.savefig(f'boxplot_{column}.png')
    plt.close()

# 4. Scatter Plots (Pairwise Correlations)
for i in range(len(columns_to_analyze)):
    for j in range(i + 1, len(columns_to_analyze)):
        plt.figure(figsize=(8, 6))
        plt.scatter(data[columns_to_analyze[i]], data[columns_to_analyze[j]], alpha=0.6, c='purple')
        plt.title(f'{columns_to_analyze[i].capitalize()} vs {columns_to_analyze[j].capitalize()}')
        plt.xlabel(columns_to_analyze[i].capitalize())
        plt.ylabel(columns_to_analyze[j].capitalize())
        plt.grid()
        plt.tight_layout()
        plt.savefig(f'scatter_{columns_to_analyze[i]}_vs_{columns_to_analyze[j]}.png')
        plt.close()

# 5. Heatmap (Day-Time Trends)
# Create a pivot table to reshape the data
data['hour'] = data['datetime'].dt.hour
pivot_table = data.pivot_table(index='hour', columns='date', values='temperature', aggfunc='mean')

plt.figure(figsize=(12, 8))
sns.heatmap(pivot_table, cmap='coolwarm', annot=False)
plt.title('Heatmap of Temperature Trends by Hour and Date')
plt.xlabel('Date')
plt.ylabel('Hour of Day')
plt.tight_layout()
plt.savefig('heatmap_temperature.png')
plt.close()

print("All graphs have been generated and saved as images.")
