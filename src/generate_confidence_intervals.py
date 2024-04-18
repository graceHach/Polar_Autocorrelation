
import numpy as np
import pandas as pd
import os
import argparse
import polarAC_utils as pAC
import stat_utils as SU
import matplotlib.pyplot as plt

# This file does the statistical analysis, and exports results into a csv

def main():
    parser = argparse.ArgumentParser(description="Generate figure two using the data produced by generate_figure_data.sh")

    parser.add_argument('--data_directory', type=str, help='Directory with data (AC curves) to do analysis on')
    parser.add_argument('--filename', type=str, default="Confidence_intervals", help='of csv file. Width and CI '
                                                                                     'parameters will be appended.')
    parser.add_argument('--width', type=float, default=2, help='Bin width for statistical analysis. Default 2 degrees')
    parser.add_argument('--CI', type=float, default=.95, help='confidence level for statistical analysis. Default 95%')
    args = parser.parse_args()
    path = args.data_directory

    # Get all csv files in input directory
    csv_paths = pAC.get_csvs_from_directories(path)

    # AC data stored in below list of lists
    arc_length, r_ac = [], []
    #
    ac_binned = []
    if len(csv_paths) == 0:
        print("No csv files in this directory to process.")
    else:

        width = args.width
        bins = np.arange(width, 360 + width, width)
        # Ac values for each bin are stored in a dict, with the key being the upper edge of the bin (2 to 360)
        # Each AC value is added to the empty list in the dict
        AC_values = {key: [] for key in bins}
        confidence_level = args.CI
        CI_lower_bound, CI_upper_bound = [], [] # Stores confidence intervals (lower bound/upper bound)

        for csv in csv_paths:
            AC_df = pAC.read_csv(csv)
            correct_csv = AC_df.columns[0] == 'r_autocorrelation' and AC_df.columns[1] == 'arc_length'
            # IGNORES files that don't have the correct headers
            if correct_csv:
                arc_length.append(list(AC_df['arc_length']))
                r_ac.append(list(AC_df['r_autocorrelation']))
            else:
                print(csv, "has missing or incorrect headers. Headers should be: 'r_autocorrelation', 'arc_length', 'num_features_sign_change'")


        for dataset_tuple in zip(arc_length, r_ac):
            for arc, r_ac in zip(dataset_tuple[0], dataset_tuple[1]):
                key = (arc//width+1)*width # This rounds up. i.e., 2 becomes 4
                if key>360:
                    key=360
                AC_values[key].append(r_ac)

        #print(AC_values.keys())
        for key in list(AC_values.keys()):
            """
            if len(AC_values[key]) >= 2:
                lb, ub = SU.confidence_interval(AC_values[key], confidence=confidence_level)
            else:
                continue
                
            """
            # Below throws warnings, but works
            lb, ub = SU.confidence_interval(AC_values[key], confidence=confidence_level)
            CI_lower_bound.append(lb)
            CI_upper_bound.append(ub)

        stat_df = pd.DataFrame(columns=['Arc length', 'CI lower bound', 'CI upper bound'])
        stat_df['Arc length'] = bins
        stat_df['CI lower bound'] = CI_lower_bound
        stat_df['CI upper bound'] = CI_upper_bound

        filename = args.filename +"_bin_widths-" + str(width) + "_CI-" + str(confidence_level) + ".csv"
        pAC.export_df(stat_df, filename)


if __name__ == '__main__':
    main()
