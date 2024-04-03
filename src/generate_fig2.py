
import numpy as np
import pandas as pd
import os
import argparse
import polarAC_utils as pAC
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description="Generate figure two using the data produced by generate_figure_data.sh")

    parser.add_argument('--data_directories', nargs=4, type=str, help='Directories with data for figure 2')

    args = parser.parse_args()
    paths = args.data_directories

    # names of sub-figures
    names = ['Dicrypt', 'Tricrypt', 'Quadcrypt', 'Pentacrypt']
    colors = [['darkslateblue', 'mediumslateblue', 'mediumpurple'], ['darkblue','mediumblue','blue'], ['seagreen', 'mediumseagreen', 'springgreen'], ['darkgoldenrod', 'goldenrod', 'gold']]
    legend_bools = [[True, True, True], [True, True, True], [True, True, True], [True, True, True]]
    # Get all csv files in input directories
    csvs_and_paths = []  # nested lists

    for path in paths:
        csvs_and_paths.append(pAC.get_csvs_from_directories(path))

    #print("working dir:", os.getcwd())
    #print("Tricrypt paths:", csvs_and_paths[1])
    # results stored in below list of lists
    arc_length, r_ac = [], []
    if len(csvs_and_paths) == 0:
        print("No csv files in this directory to process.")
    else:
        fig, axs = plt.subplots(4, figsize=(8, 16), sharey=True)

        for index, path in enumerate(paths):  # iterates over each path
            axs[index].set_title(names[index])
            axs[index].set_ylabel('Autocorrelation of radial coordinate')

            if not index == 3:
                axs[index].xaxis.set_ticklabels([])
            else:
                axs[index].set_xlabel('Arc length parameterization')
            for csv_file in csvs_and_paths[index]:
                #print(csv_file)
                results_df = pAC.read_csv(csv_file)
                if 'arc_length' in results_df.columns and 'r_autocorreation' in results_df.columns:
                    if "results\\0.1_" in  csv_file:
                        color_index = 0
                        label = 'Low noise'
                    elif "results\\0.2_" in csv_file:
                        color_index = 1
                        label = 'Moderate noise'
                    else:
                        color_index = 2
                        label = 'High noise'
                    arc_length.append(results_df['arc_length'])
                    r_ac.append(results_df['r_autocorreation'])
                    if legend_bools[index][color_index]:  # This ensures that we don't have several hundred legend entries per subfigure
                        axs[index].plot(results_df['arc_length'], results_df['r_autocorreation'], alpha=.11,
                                        label=label, color=colors[index][color_index])
                        legend_bools[index][color_index] = False
                    else:
                        axs[index].plot(results_df['arc_length'], results_df['r_autocorreation'], alpha=.11, color=colors[index][color_index])
                else:
                    print(
                        f"CSV file {csv_file} has different or missing column headers.")
                legend = axs[index].legend()
                for line in legend.get_lines():
                    line.set_alpha(1)

        # plot all xy datasets with alpha = 0.1
        #plt.plot()
        # Save figure
        #os.chdir(args.result_directory)
        plt.tight_layout()
        plt.savefig("../doc/fig2.png")
        print("fig generated.")

if __name__ == '__main__':
    main()
