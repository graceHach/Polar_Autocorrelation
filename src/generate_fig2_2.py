import numpy as np
import pandas as pd
import os
import argparse
import polarAC_utils as pAC
import matplotlib.pyplot as plt

def main():
    parser = argparse.ArgumentParser(description='Combine the results of multiple files into a single file.')

    # TODO do the actual data processing to generate the AC curves of the noisy organoids

    parser.add_argument('--data_directories', nargs=4, type=str, help='Directories with data files to perform polar autocorrelation')

    parser.add_argument('--result_directory', nargs=4, type=str, help='Directory to place polar autocorrelation results')



    args = parser.parse_args()
    paths = args.data_directories

    # names of sub-figures
    names = ['Dicrypt', 'Tricrypt', 'Quadcrypt', 'Pentacrypt']
    colors = ['']
    # Get all csv files in input directories
    csvs_and_paths = []  # nested lists

    print("working dir:", os.getcwd())
    for path in paths:
        csvs_and_paths.append(pAC.get_csvs_from_directories(path))

    print("Paths:", csvs_and_paths[1])
    # results stored in below list of lists
    arc_length, r_ac = [], []
    if len(csvs_and_paths) == 0:
        print("No csv files in this directory to process.")
    else:
        fig, axs = plt.subplots(4)

        for index, path in enumerate(paths):  # iterates over each path
            print(path)
            for csv_file in csvs_and_paths[index]:
                results_df = pAC.read_csv(path+"\\"+csv_file)
                if path==paths[1]:
                    print(results_df)
                if 'arc_length' in results_df.columns and 'r_autocorreation' in results_df.columns:
                    arc_length.append(results_df['arc_length'])
                    r_ac.append(results_df['r_autocorreation'])
                    axs[index].plot(results_df['arc_length'], results_df['r_autocorreation'], alpha=0.08, color='m')
                else:
                    print(
                        f"CSV file {csv_file} has different or missing column headers.")

        # plot all xy datasets with alpha = 0.1
        #plt.plot()
        # Save figure
        #os.chdir(args.result_directory)
        plt.savefig("fig2.png")
        print("fig generated.")

if __name__ == '__main__':
    main()
