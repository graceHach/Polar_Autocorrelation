
import numpy as np
import pandas as pd
import os
import argparse
import polarAC_utils as pAC
import glob
"""
bit = "organoid_point_clouds"
#get all csv result files 
directory = "C:\\Users\\graci\\OneDrive\\Documents\\Lab\\Polar AC\\"+bit+"\\results_arc"
csv_filepaths = glob.glob(os.path.join(directory, "*.csv")) #list of filenames/directories as strings 

# filenames is av_filepaths with directory and _PolarAC trimmed off
filenames = [x[76:-12] for x in csv_filepaths]
# Feature numbers list stores number of features 
feature_numbers = []
feature_numbers2 = []
# Result stores everything
result = pd.DataFrame()
print(filenames[0])
for i,j in enumerate(csv_filepaths):
    # read contents of csv, store individual columns 
    points = pd.read_csv(j)
    points.columns=[filenames[i]+' theta',filenames[i]+' r autocorrelation',filenames[i]+' number of features',filenames[i]+' number of features 2']
    # add only theta and r_cor to final dataframe 
    feature_numbers.append(points[filenames[i]+' number of features'][0])
    feature_numbers2.append(points[filenames[i]+' number of features 2'][0])
    result = pd.concat([result,points[[filenames[i]+' theta',filenames[i]+' r autocorrelation']]], axis=1)

# Add two new columns for filename / feature number
filenames_df = pd.DataFrame(filenames)
filenames_df2 = pd.DataFrame(filenames)
feature_num_df = pd.DataFrame(feature_numbers)
feature_num2_df = pd.DataFrame(feature_numbers2)
filenames_df.columns = ["sign change"] 
filenames_df2.columns = ["2nd deriv"] 
feature_num_df.columns=["num features sign change"]
feature_num2_df.columns=["num features 2nd deriv."]
result = pd.concat([filenames_df,filenames_df2,feature_num_df,feature_num2_df,result],axis=1)

#  Write new file to this directory 
directory = "C:\\Users\\graci\\OneDrive\\Documents\\Lab\\Polar AC\\"+bit+"\\results_arc"
os.chdir(directory)
result.to_csv("!!!!Compiled_results_otho_meta_para.csv",index=False)
"""


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
