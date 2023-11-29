# -*- coding: utf-8 -*-
"""
Created on Fri Jul 28 10:35:44 2023

@author: graci
"""

import numpy as np
import pandas as pd
import os
import time
import glob

#get all csv result files 
bit = "organoid_point_clouds"
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
    
    