import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


def generate_traffic_data():
    np.random.seed(42)
    data = {
        "time": pd.date_range("2023-01-01", periods=100, freq="H"),
        "vehicle_count": np.random.poisson(50, 100),
        "average_speed": np.random.uniform(20, 80, 100),
        "traffic_density": np.random.uniform(0.1, 1.0, 100),
        "accidents": np.random.choice([0, 1], size=100, p=[0.9, 0.1]),
    }
    return pd.DataFrame(data)

def visualize_and_save(data, output_folder):

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    plt.figure(figsize=(10, 5))
    plt.plot(data['time'], data['vehicle_count'], label='Vehicle Count', color='blue')
    plt.title("Traffic Flow Over Time")
    plt.xlabel("Time")
    plt.ylabel("Vehicle Count")
    plt.legend()
    plt.grid()
    plt.show() 
    plt.savefig(f"{output_folder}/traffic_flow_over_time.png")
    plt.close()

  
    plt.figure(figsize=(10, 5))
    sns.scatterplot(x='traffic_density', y='average_speed', hue='accidents', data=data, palette='coolwarm')
    plt.title("Traffic Density vs Average Speed")
    plt.xlabel("Traffic Density")
    plt.ylabel("Average Speed")
    plt.show()  
    plt.savefig(f"{output_folder}/density_vs_speed.png")
    plt.close()

    plt.figure(figsize=(10, 5))
    sns.histplot(data['average_speed'], bins=20, kde=True, color='green')
    plt.title("Distribution of Average Speeds")
    plt.xlabel("Average Speed")
    plt.ylabel("Frequency")
    plt.show()  
    plt.savefig(f"{output_folder}/speed_distribution.png")
    plt.close()


    correlation = data[['vehicle_count', 'average_speed', 'traffic_density', 'accidents']].corr()
    plt.figure(figsize=(8, 6))
    sns.heatmap(correlation, annot=True, cmap='coolwarm', fmt='.2f')
    plt.title("Correlation Heatmap of Traffic Metrics")
    plt.show()  
    plt.savefig(f"{output_folder}/traffic_correlation_heatmap.png")
    plt.close()

    fig = px.line(data, x='time', y='vehicle_count', title='Traffic Flow Over Time (Interactive)', labels={'vehicle_count': 'Vehicle Count'})
    fig.show() 
    fig.write_image(f"{output_folder}/interactive_traffic_flow.png")

    fig = px.scatter_3d(data, x='traffic_density', y='average_speed', z='vehicle_count', color='accidents', title='3D Scatter Plot of Traffic Metrics', labels={'traffic_density': 'Density', 'average_speed': 'Speed', 'vehicle_count': 'Count'})
    fig.show()  
    fig.write_image(f"{output_folder}/3d_scatter_plot.png")

    density_bins = pd.cut(data['traffic_density'], bins=5, labels=['Very Low', 'Low', 'Medium', 'High', 'Very High'])
    density_counts = density_bins.value_counts().reset_index()
    density_counts.columns = ['Density', 'Count']

    fig = go.Figure(data=[go.Pie(labels=density_counts['Density'], values=density_counts['Count'], hole=0.4)])
    fig.update_layout(title_text="Traffic Density Distribution")
    fig.show()  
    fig.write_image(f"{output_folder}/traffic_density_pie_chart.png")


if __name__ == "__main__":
    traffic_data = generate_traffic_data()
    output_folder = "traffic_visualizations"
    visualize_and_save(traffic_data, output_folder)
    print(f"All plots have been saved to the folder: {output_folder}")
