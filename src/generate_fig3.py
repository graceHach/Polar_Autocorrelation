
import numpy as np
import pandas as pd
import os
import argparse
import polarAC_utils as pAC
import stat_utils as SU
import matplotlib.pyplot as plt
from scipy.integrate import quad  # used for numerical integration

# This file does the statistical analysis, and exports results into a csv

def main():
    parser = argparse.ArgumentParser(description="Generate figure two using the data produced by generate_figure_data.sh")

    parser.add_argument('--data_directory', type=str, help='Directory with data (AC curves) to do analysis on')
    parser.add_argument('--color', type=str, help='Main color for figure, cmyk')
    parser.add_argument('--name', type=str, help='name_of_figure')
    args = parser.parse_args()
    path = args.data_directory

    # Get all csv files in input directory
    csv_paths = pAC.get_csvs_from_directories(path)

    # AC data stored in below list of lists
    arc_length, r_ac = [], []

    ac_binned = []
    if len(csv_paths) == 0:
        print("No csv files in this directory to process.")
    else:

        width_values = [0.5, .75, 2, 3]  # row in data
        CI_values = [0.9999, 0.99, .98, .97]  # col in data


        for csv in csv_paths:
            AC_df = pAC.read_csv(csv)
            correct_csv = AC_df.columns[0] == 'r_autocorreation' and AC_df.columns[1] == 'arc_length'
            # IGNORES files that don't have the correct headers
            if correct_csv:
                arc_length.append(list(AC_df['arc_length']))
                r_ac.append(list(AC_df['r_autocorreation']))
            else:
                print(csv, "has missing or incorrect headers. Headers should be: 'r_autocorreation', 'arc_length', 'num_features_sign_change'")

        fig,axs = plt.subplots(4, 4, figsize=(16, 16), sharey=True)
        upper_color, lower_color, middle_color = "#8000ff", "#029688", "#0066ff"
        color = args.color
        areas_between_curves = []

        for i, width in enumerate(width_values):
            for j, ci in enumerate(CI_values):
                # Do the analysis
                bins = np.arange(width, 360 + width, width)
                # Ac values for each bin are stored in a dict, with the key being the upper edge of the bin (2 to 360)
                # Each AC value is added to the empty list in the dict
                AC_values = {key: [] for key in bins}
                confidence_level = ci
                CI_lower_bound, CI_upper_bound = [], []  # Stores confidence intervals (lower bound/upper bound)
                # Adds each datapoint to appropriate bin of AC_values
                for dataset_tuple in zip(arc_length, r_ac):
                    for arc, r_ac_ in zip(dataset_tuple[0], dataset_tuple[1]):
                        if arc == 360:
                            key = 360
                        else:
                            key = (arc // width + 1) * width  # This rounds up. i.e., 2 becomes 4
                        AC_values[key].append(r_ac_)

                # Calcualted CI and adds to list
                x_values = []  # keeps track of which bins are occupied
                for key in list(AC_values.keys()):
                    if len(AC_values[key]) <= 1: # can't draw statistical conclusions with one sample!
                        continue
                    else:
                        lb, ub = SU.confidence_interval(AC_values[key], confidence=confidence_level)
                        CI_lower_bound.append(lb)
                        CI_upper_bound.append(ub)
                        x_values.append(key)

                # Do the plotting
                # Some bins are empty, overwriting bins with x_values, for which a confidence interval is calculable
                bins = x_values
                axs[i, j].set_title(f'Bin Width: {width}, CI: {ci*100:.2f}%')
                axs[i, j].plot(bins, CI_lower_bound, label='Lower', color=color)
                axs[i, j].plot(bins, CI_upper_bound, label='Upper', color=color)
                axs[i, j].fill_between(bins, CI_upper_bound, CI_lower_bound, color=color, alpha=0.3, interpolate=True)
                # Get area between curves
                area = SU.area_between_curves(bins, CI_lower_bound, bins, CI_upper_bound)
                #area = 12
                areas_between_curves.append(area)
                # below is for text labels of area under curve
                axs[i, j].text(350, .75, f'Area = {area:.2f}', ha='right', fontsize=14,
                               bbox=dict(facecolor='white', edgecolor='black', boxstyle='round,pad=1'))


                # Hide tick labels on middle plots
                if i != 3:
                    axs[i, j].set_xticklabels([])
                else:
                    axs[i, j].set_xlabel("Arc Length")
                if j != 0:
                    axs[i, j].set_yticklabels([])
                else:
                    axs[i, j].set_ylabel("Autocorrelation")
                    #axs[i, j].set_yticklabels(labels=[-1,0,1])

                # fixing y range and adding labels
                y_min = -1.2
                y_max = 1.2

                for ax_row in axs:
                    for ax in ax_row:
                        ax.set_ylim(y_min, y_max)

                for ax_row in axs:
                    ticks = [-1, -0.5, 0, 0.5, 1]
                    ax_row[0].set_yticks(ticks)
                    ax_row[0].set_yticklabels(ticks)

        # Adjust layout to prevent overlapping
        plt.tight_layout()
        plt.savefig(args.name)


if __name__ == '__main__':
    main()
