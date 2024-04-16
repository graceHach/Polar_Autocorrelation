#!/bin/bash -e


python get_AC_statistics.py \
--data_directories "..\data\contrived_noisy\dicrypt\results" "..\data\contrived_noisy\tricrypt\results" \
"..\data\contrived_noisy\quadcrypt\results" "..\data\contrived_noisy\pentacrypt\results" \
--ground_truths 2 3 4 5 \
--result_directory "..\data\contrived_noisy\AC_stats.csv"

python generate_fig4.py