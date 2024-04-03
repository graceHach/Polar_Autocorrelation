#!/bin/bash -e


# generate all data for figure 1
python PolarAC_arc_parameterization_better_practices.py \
--data_directory "..\data\contrived_ideal\xy_data" \
--result_directory "..\data\contrived_ideal\results" \
--include_ac_curve True

# generate all data for figure 2
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