import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def visualize_data(data):
    print("Data types:", data.dtypes) 
    print("Data summary:\n", data.describe()) 


    data = data.dropna(subset=['duration', 'distance_nm'])  


    plt.figure(figsize=(12, 6))
    sns.barplot(x='voyage_id', y='duration', data=data)
    plt.title('Duration Between Events by Voyage ID')
    plt.xlabel('Voyage ID')
    plt.ylabel('Duration (seconds)')
    plt.show()

    plt.figure(figsize=(12, 6))
    sns.lineplot(x='voyage_id', y='distance_nm', data=data, marker='o')
    plt.title('Distance Traveled Between Ports by Voyage ID')
    plt.xlabel('Voyage ID')
    plt.ylabel('Distance (Nautical Miles)')
    plt.show()

if __name__ == "__main__":
    data = pd.read_csv('processed_data.csv')
    visualize_data(data)
