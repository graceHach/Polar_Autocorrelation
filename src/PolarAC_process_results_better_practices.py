
import numpy as np
import pandas as pd
import os
import argparse
import polarAC_utils as pAC
import glob


def main():
    parser = argparse.ArgumentParser(description='Combine the results of multiple files into a single file.')
    parser.add_argument('--data_directory', type=str, help='Directory with data files to perform polar autocorrelation')
    parser.add_argument('--result_directory', type=str, help='Directory to '
                                                             'place results')
    parser.add_argument('--name_of_result_file', type=str, help='Name of compiled results', default='PolarAC_Results_Compiled.csv')

    args = parser.parse_args()

    # Get all csv files in input directory
    csvs_and_paths = pAC.get_csvs_from_directory(args.data_directory)
    # trims off _PolarAC.csv
    csv_file_names = [os.path.basename(file)[:-12] for file in csvs_and_paths]

    # results appended to this in the same order as the filenames stored in csv_file_names
    num_features_sign_change, num_features_2nd_deriv = [], []
    processed_results_df = pd.DataFrame(columns=['filename','num_features_sign_change', 'num_features_2nd_deriv'])
    if len(csvs_and_paths)==0:
        print("No csv files in this directory to process.")
    else:
        for csv_file in csvs_and_paths:
            results_df = pAC.read_csv(csv_file)
            if 'num_features_sign_change' in results_df.columns and 'num_features_2nd_deriv' in results_df.columns:
                num_features_sign_change.append(
                    results_df['num_features_sign_change'][0])
                num_features_2nd_deriv.append(
                    results_df['num_features_2nd_deriv'][0])
            else:
                print(
                    f"CSV file {csv_file} has different or missing column headers.")

        processed_results_df['filename'] = csv_file_names
        processed_results_df['num_features_sign_change'] = num_features_sign_change
        processed_results_df['num_features_2nd_deriv'] = num_features_2nd_deriv
        os.chdir(args.result_directory)
        pAC.export_df(processed_results_df, args.name_of_result_file)
        print("Results processed, exported.")

if __name__ == '__main__':
    main()
