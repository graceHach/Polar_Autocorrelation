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

    colors = plt.cm.viridis(np.linspace(0, 1, len(csvs_and_paths)))

    for index, csv_file in enumerate(csvs_and_paths):
        points_df = pAC.read_csv(csv_file)
        r_autocorrelation = points_df['r_autocorreation']
        arc_length = points_df['arc_length']
        #TODO either print these on the graph in some way, or get rid of this line
        num_features = points_df['num_features_sign_change']

        row = index // 3
        col = index % 3
        #TODO add labels
        axes[row, col].plot(arc_length, r_autocorrelation, color=colors[index])
        axes[row, col].set_title(titles[index])

    plt.tight_layout()
    plt.savefig(args.figure_destination_directory+'fig1_unannotated.png')


if __name__ == '__main__':
    main()
