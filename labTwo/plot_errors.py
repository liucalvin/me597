import matplotlib.pyplot as plt
from utilities import FileReader
import os
import argparse
from PIL import Image  # Import Pillow for image cropping


# Define units for known variables
UNITS = {
    "e": "m",
    "e_dot": "m/s",
    "x": "m",
    "y": "m"
}


def plot_errors(filename):
    
    headers, values = FileReader(filename).read_file()
    
    time_list = []
    first_stamp = values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)

    if "angular" in filename:
        xlabel = "Time (s)"
        ylabel = "Angular Error Metrics"
        legend_suffix = " angular"
    elif "linear" in filename:
        xlabel = "Time (s)"
        ylabel = "Linear Error Metrics"
        legend_suffix = " linear"
    elif "robot_pose" in filename:
        xlabel = "Time (s)"
        ylabel = "Robot Pose"
        legend_suffix = " pose"
    else:
        print(f"Skipping {filename}: Unrecognized filename pattern.")
        return

    fig, axes = plt.subplots(1, 2, figsize=(14, 6))

    # Get units for first two headers (for state space plot)
    x_label = f"{headers[0]} ({UNITS.get(headers[0], headers[0])})"
    y_label = f"{headers[1]} ({UNITS.get(headers[1], headers[1])})"

    axes[0].plot([lin[0] for lin in values], [lin[1] for lin in values])
    axes[0].set_title("State Space")
    axes[0].set_xlabel(x_label)
    axes[0].set_ylabel(y_label)
    axes[0].grid()

    axes[1].set_title("Each Individual State")
    axes[1].set_xlabel(xlabel)
    axes[1].set_ylabel(ylabel)

    for i in range(0, len(headers) - 1):
        header_name = headers[i]
        unit_label = UNITS.get(header_name, header_name)
        axes[1].plot(time_list, [lin[i] for lin in values], label=f"{header_name} ({unit_label}){legend_suffix}")

    axes[1].legend()
    axes[1].grid()

    csv_dir = os.path.dirname(filename)
    csv_basename = os.path.splitext(os.path.basename(filename))[0]
    output_path = os.path.join(csv_dir, f"{csv_basename}.png")

    plt.savefig(output_path)
    plt.close()

    print(f"Plot saved to {output_path}")

    # Crop the image after saving
    crop_image(output_path)


def crop_image(image_path):
    """Crop 7% from left, 7% from right, and 5% from top."""
    img = Image.open(image_path)
    width, height = img.size

    # Compute crop boundaries
    left = int(0.07 * width)  # 7% from left
    right = width - int(0.07 * width)  # 7% from right
    top = int(0.05 * height)  # 5% from top
    bottom = height  # Keep full height (no crop from bottom)

    # Crop and overwrite the original image
    img_cropped = img.crop((left, top, right, bottom))
    img_cropped.save(image_path)

    print(f"Cropped image saved to {image_path}")


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')

    args = parser.parse_args()

    print("Plotting the files", args.files)

    filenames = args.files
    for filename in filenames:
        plot_errors(filename)
