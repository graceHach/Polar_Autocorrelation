#import pandas as pd
import os
import argparse
import polarAC_utils as pAC


def main():
    parser = argparse.ArgumentParser(description='Generate fire and GDP data for a specific country.')
    parser.add_argument('--data_directory', type=str, help='Directory with data files to perform polar autocorrelation')
    parser.add_argument('--result_directory', type=str, help='Directory to '
                                                             'place results')
    parser.add_argument('--include_ac_curve', type=bool, help='Include autocorrelation curve in output', default=True)

    args = parser.parse_args()

    # Get all csv files in input directory
    csvs_and_paths = pAC.get_csvs_from_directory(args.data_directory)
    csv_file_names = [os.path.basename(file)[:-4] for file in csvs_and_paths]

    # results appended to this in the same order as the filenames stored in data_csvs
    results_dfs = []
    # Iterate over each csv, creating dataframes with the results
    for index, csv_file in enumerate(csvs_and_paths):
        points_df = pAC.read_csv(csv_file)
        if points_df.shape[1] == 2:
            points_df.columns = ['x', 'y']
            points_tuples = list(zip(points_df['x'], points_df['y']))
            points_tuples_sorted = pAC.sort_CCW(points_tuples)
            points_df['x'], points_df['y'] = [x for x, y in points_tuples_sorted], [y for x, y in points_tuples_sorted]
            points_df = pAC.add_radial_distance(points_df)
            points_df = pAC.add_arc_length_parameterization(points_df)
            points_df = pAC.arc_length_remapping(points_df)
            results_df = pAC.create_export_df(args.include_ac_curve, points_df)
            results_dfs.append(results_df)
            print("Processed ", csv_file_names[index])
        else:
            print("Data file should have two columns , corresponding to x and "
                  "y coordinates. ",csv_file_names[index], " has ",
                  points_df.shape[1], "columns.")
            csv_file_names.remove(csv_file_names[index])

    # Export all csvs
    os.chdir(args.result_directory)
    for df, filename in zip(results_dfs, csv_file_names):
        pAC.export_df(df, filename+"_PolarAC.csv")

    print("Exported all processed files.")


if __name__ == '__main__':
    main()
