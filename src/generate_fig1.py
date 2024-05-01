import matplotlib.pyplot as plt
import pandas as pd
import argparse
import polarAC_utils as pAC
import numpy as np


def main():

    parser = argparse.ArgumentParser(description='Calculate polar autocorrelation of an XY dataset.')
    parser.add_argument('--data_directory', type=str, help='Directory with data files (autocorrelation already '
                        'calculated) to generate figure')
    parser.add_argument('--figure_destination_directory', type=str, help='Directory to save figure as png')
    args = parser.parse_args()

    fig, axes = plt.subplots(nrows=3, ncols=3, figsize=(12, 8))
    csvs_and_paths = pAC.get_csvs_from_directory(args.data_directory)
    titles = ['One feature', 'Two features', 'Three features', 'Four features', 'Five features', 'Six features',
              'Seven features', 'Eight features', 'Nine features']

    colors = plt.cm.plasma(np.linspace(0, 1, len(csvs_and_paths)))

    # Defining custom 'xlim' and 'ylim' values.
    custom_ylim = (-1, 1)

    # Setting the values for all axes.
    plt.setp(axes, ylim=custom_ylim)

    for index, csv_file in enumerate(csvs_and_paths):
        points_df = pAC.read_csv(csv_file)
        r_autocorrelation = points_df['r_autocorrelation']
        arc_length = points_df['arc_length']
        #TODO either print these on the graph in some way, or get rid of this line
        num_features = points_df['num_features_sign_change']

        #TODO add vector graphics
        row = index // 3
        col = index % 3

        axes[row, col].plot(arc_length, r_autocorrelation, color=colors[index])
        axes[row, col].set_title(titles[index])
        if col == 0:
            axes[row, col].set_ylabel("Autocorrelation of r coordinate")
        else:
            axes[row, col].set_yticklabels([])
        if row == 2:
            axes[row, col].set_xlabel("Parameterized arc length")
        else:
            axes[row, col].set_xticklabels([])

    plt.tight_layout()
    plt.savefig(args.figure_destination_directory)
    print("Generated figure 1 and placed into doc folder.")


if __name__ == '__main__':
    main()
