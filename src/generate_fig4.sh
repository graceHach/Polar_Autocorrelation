#!/bin/bash -e

# data for figure 4 is created by generate_fig2.sh

# extracts parameters from autocorrelation curve and saves them to a csv
python get_AC_statistics.py \
--data_directories "..\data\contrived_noisy\dicrypt\results" "..\data\contrived_noisy\tricrypt\results" \
"..\data\contrived_noisy\quadcrypt\results" "..\data\contrived_noisy\pentacrypt\results" \
--ground_truths 2 3 4 5 \
--result_directory "..\data\contrived_noisy\AC_stats.csv"

# does clustering using AC_stats.csv, and all_shape_descriptors.csv, both in ..\data\contrived_noisy\.
python generate_fig4.py