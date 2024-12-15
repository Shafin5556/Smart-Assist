import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go

# Load the dataset (update the file path as needed)
file_path = 'dummy_crop_environment_data.csv'
data = pd.read_csv(file_path)

# Convert date and time columns to a datetime format
data['datetime'] = pd.to_datetime(data['date'] + ' ' + data['time'])

# Define parameters for visualization
columns_to_plot = ['temperature', 'humidity', 'light_intensity']

# 1. Line Charts
plt.figure(figsize=(10, 6))
for column in columns_to_plot:
    plt.plot(data['datetime'], data[column], label=column.capitalize())
plt.title('Line Charts of Environmental Parameters Over Time')
plt.xlabel('Datetime')
plt.ylabel('Value')
plt.legend()
plt.grid()
plt.tight_layout()
plt.savefig('line_chart.png')
plt.show()

# 2. Bar Charts
daily_avg = data.groupby('date')[columns_to_plot].mean()
daily_avg.plot(kind='bar', figsize=(10, 6))
plt.title('Bar Charts of Daily Averages')
plt.xlabel('Date')
plt.ylabel('Average Value')
plt.tight_layout()
plt.savefig('bar_chart.png')
plt.show()

# 3. Scatter Plots
sns.pairplot(data[columns_to_plot], diag_kind='kde', height=3)
plt.savefig('scatter_plots.png')
plt.show()

# 4. Gauge Widgets
for column in columns_to_plot:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=data[column].mean(),
        title={'text': f"{column.capitalize()} Gauge"},
        gauge={'axis': {'range': [min(data[column]), max(data[column])]},
               'bar': {'color': "blue"}}
    ))
    fig.write_image(f"gauge_{column}.png")
    fig.show()

# 5. Heatmap
data['hour'] = data['datetime'].dt.hour
heatmap_data = data.pivot_table(index='hour', columns='date', values='temperature', aggfunc='mean')
plt.figure(figsize=(12, 8))
sns.heatmap(heatmap_data, cmap='coolwarm', annot=False)
plt.title('Heatmap of Temperature Trends by Hour and Date')
plt.xlabel('Date')
plt.ylabel('Hour of Day')
plt.tight_layout()
plt.savefig('heatmap_temperature.png')
plt.show()

print("All visualizations have been saved as images.")
