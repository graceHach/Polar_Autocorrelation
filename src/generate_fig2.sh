#!/bin/bash -e
#todo:

# generate all data for figure 2 (also required for figure 3)
python PolarAC_arc_parameterization_better_practices.py \
--data_directory "..\data\contrived_noisy\dicrypt\xy_data" \
--result_directory "..\data\contrived_noisy\dicrypt\results" \
--include_ac_curve True

python PolarAC_arc_parameterization_better_practices.py \
--data_directory "..\data\contrived_noisy\tricrypt\xy_data" \
--result_directory "..\data\contrived_noisy\tricrypt\results" \
--include_ac_curve True

python PolarAC_arc_parameterization_better_practices.py \
--data_directory "..\data\contrived_noisy\quadcrypt\xy_data" \
--result_directory "..\data\contrived_noisy\quadcrypt\results" \
--include_ac_curve True

python PolarAC_arc_parameterization_better_practices.py \
--data_directory "..\data\contrived_noisy\pentacrypt\xy_data" \
--result_directory "..\data\contrived_noisy\pentacrypt\results" \
--include_ac_curve True
echo 'Data for figure 2 created.'


python generate_fig2.py \
--data_directories "..\data\contrived_noisy\dicrypt\results" "..\data\contrived_noisy\tricrypt\results" \
"..\data\contrived_noisy\quadcrypt\results" "..\data\contrived_noisy\pentacrypt\results"
echo 'Figure 2 saved to doc folder.'