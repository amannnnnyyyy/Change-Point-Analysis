import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import find_peaks

def change_point_analysis(data):
    data['Date'] = pd.to_datetime(data['Date'])
    data = data.sort_values(by='Date').reset_index(drop=True)

    change_points = []
    significant_change_points = []
    min_distance = 100 
    mean_diff_threshold = 10 
    significant_mean_diff_threshold = 20

    # Detect peaks (maxima) and troughs (minima)
    peaks, _ = find_peaks(data['Price'], distance=min_distance)
    troughs, _ = find_peaks(-data['Price'], distance=min_distance)  # Invert for troughs

    # Combine peaks and troughs as potential change points
    extrema = sorted(np.concatenate((peaks, troughs)))

    # Detect significant mean changes across the dataset
    for i in range(min_distance, len(data) - min_distance):
        before_data = data['Price'][:i]
        after_data = data['Price'][i:]
        
        mean_before = before_data.mean()
        mean_after = after_data.mean()
        
        if abs(mean_before - mean_after) > significant_mean_diff_threshold:
            if not significant_change_points or (i - significant_change_points[-1] >= min_distance):
                significant_change_points.append(i)
        elif abs(mean_before - mean_after) > mean_diff_threshold:
            if not change_points or (i - change_points[-1] >= min_distance):
                change_points.append(i)

    all_change_points = sorted(set(change_points + extrema))
    all_significant_change_points = sorted(set(significant_change_points + extrema))

    def plot_segment(data, start_idx, end_idx, change_points, significant_change_points):
        plt.figure(figsize=(14, 7))
        plt.plot(data['Date'][start_idx:end_idx], data['Price'][start_idx:end_idx], label='Brent Oil Price')
        
        for cp in change_points:
            if start_idx <= cp < end_idx:
                plt.axvline(x=data['Date'].iloc[cp], color='orange', linestyle='--', label='Detected Change Point')
                plt.annotate(f"{data['Date'].iloc[cp].date()}\n{data['Price'].iloc[cp]:.2f}", 
                            xy=(data['Date'].iloc[cp], data['Price'].iloc[cp]), 
                            xytext=(5, 5), textcoords='offset points', 
                            arrowprops=dict(arrowstyle='->', color='orange'),
                            fontsize=10, color='orange')

        for scp in significant_change_points:
            if start_idx <= scp < end_idx:
                plt.axvline(x=data['Date'].iloc[scp], color='red', linestyle='--', label='Significant Change Point')
                plt.annotate(f"{data['Date'].iloc[scp].date()}\n{data['Price'].iloc[scp]:.2f}", 
                            xy=(data['Date'].iloc[scp], data['Price'].iloc[scp]), 
                            xytext=(5, -15), textcoords='offset points', 
                            arrowprops=dict(arrowstyle='->', color='red'),
                            fontsize=10, color='red')

        plt.xlabel('Date')
        plt.ylabel('Price (USD)')
        plt.title(f'Brent Oil Prices from {data["Date"].iloc[start_idx]} to {data["Date"].iloc[end_idx-1]}')
        plt.legend()
        plt.show()

    segment_size = 500

    for i in range(0, len(data), segment_size):
        start_idx = i
        end_idx = min(i + segment_size, len(data))
        plot_segment(data, start_idx, end_idx, change_points, significant_change_points)

    print("Detected Change Points:")
    for cp in all_change_points:
        print(f"Date: {data['Date'].iloc[cp].date()}, Price: {data['Price'].iloc[cp]:.2f}")
        
    print("\nSignificant Change Points:")
    for scp in all_significant_change_points:
        print(f"Date: {data['Date'].iloc[scp].date()}, Price: {data['Price'].iloc[scp]:.2f}")