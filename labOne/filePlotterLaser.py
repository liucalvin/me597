# You can use this file to plot the loged sensor data
# Note that you need to modify/adapt it to your own files
# Feel free to make any modifications/additions here

import matplotlib.pyplot as plt
import numpy as np
from utilities import FileReader

def plot_singletimestamp(filename, timestamp):
    headers, values=FileReader(filename).read_file() 

    # Extract timestamp
    stamp = values[timestamp][-1]

    # Extract list of all angle incrementations
    angle_increment = float(values[timestamp][-2])

    # Extract which row/timestamp to plot
    selected_row = values[timestamp]

    # Extract list of all ranges detected for selected row/timestamp
    ranges = np.array(selected_row[:-2], dtype=float)

    # Remove invalid points (inf values)
    valid_points = np.isfinite(ranges)  # True for finite values, False for inf/nan
    ranges = ranges[valid_points] # only valid ranges

    # Compute angles
    angles = np.arange(0, len(selected_row[:-2]) * angle_increment, angle_increment)
    angles = angles[valid_points]  # only angles with valid ranges

    # Convert to Cartesian coordinates
    x = ranges * np.cos(angles)
    y = ranges * np.sin(angles)

    # Plot
    plt.figure(figsize=(8, 8))
    plt.scatter(x, y, s=5, label=f"Scanned Points")
    plt.scatter(0, 0, color='red', marker='s', s=100, label="Turtlebot")
    plt.xlabel("X (m)")
    plt.ylabel("Y (m)")
    plt.title(f"Laser Scan at {stamp}")
    plt.legend()
    plt.axis("equal")
    plt.grid()
    plt.show()

    
import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    parser.add_argument('--stamp', required=True, help='Timestamp to Visualize')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)
    print("\nplotting the timestamp", args.stamp)

    filenames=args.files
    stamp = int(args.stamp)

    for filename in filenames:
        plot_singletimestamp(filename, stamp)