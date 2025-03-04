import matplotlib.pyplot as plt
from utilities import FileReader
import os



def plot_errors(filename):
    
    headers, values=FileReader(filename).read_file()
    
    time_list=[]
    
    first_stamp=values[0][-1]
    
    for val in values:
        time_list.append(val[-1] - first_stamp)

    
    
    fig, axes = plt.subplots(1,2, figsize=(14,6))


    axes[0].plot([lin[0] for lin in values], [lin[1] for lin in values])
    axes[0].set_title("state space")
    axes[0].grid()

    
    axes[1].set_title("each individual state")
    for i in range(0, len(headers) - 1):
        axes[1].plot(time_list, [lin[i] for lin in values], label= headers[i]+ " linear")

    axes[1].legend()
    axes[1].grid()

    csv_file = args.files[0] if isinstance(args.files, list) else args.files

    # save plots as png file
    csv_dir = os.path.dirname(csv_file)
    csv_basename = os.path.splitext(os.path.basename(csv_file))[0]
    output_path = os.path.join(csv_dir, f"{csv_basename}.png")

    plt.savefig(output_path)
    
    





import argparse

if __name__=="__main__":

    parser = argparse.ArgumentParser(description='Process some files.')
    parser.add_argument('--files', nargs='+', required=True, help='List of files to process')
    
    args = parser.parse_args()
    
    print("plotting the files", args.files)

    filenames=args.files
    for filename in filenames:
        plot_errors(filename)



