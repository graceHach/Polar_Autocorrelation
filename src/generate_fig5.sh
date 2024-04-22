#!bin/bash -e

':
#generate AC data of real organoids (snapshots)
python PolarAC_arc_parameterization_better_practices.py \
--data_directory "..\data\real\static_4_feature\xy_data" \
--result_directory "..\data\real\static_4_feature\results"

#generate AC data of real organoids (snapshots)
python PolarAC_arc_parameterization_better_practices.py \
--data_directory "..\data\real\timeseries_4_feature\xy_data" \
--result_directory "..\data\real\timeseries_4_feature\results"
'


confidence_level=0.9999
width=0.25
# get confidence intervals for 4 features
python -W ignore generate_confidence_intervals.py \
--data_directory "..\data\contrived_noisy\quadcrypt\results" \
--filename "..\doc\quad" \
--width "$width" \
--CI "$confidence_level"

#"" + str(width) + "_CI-" + str(confidence_level) + ".csv"
filename="../doc/quad_bin_widths-${width}_CI-${confidence_level}.csv"

#generate the figure
python generate_fig5.py \
--CI_filename "$filename" \
--snapshots_directory "..\data\real\static_4_feature\results" \
--timeseries_directory "..\data\real\timeseries_4_feature\results"
#