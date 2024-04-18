#!bin/bash -e


#generate AC data of real organoids
python PolarAC_arc_parameterization_better_practices.py \
--data_directory "..\data\real\static_4_feature\xy_data" \
--result_directory "..\data\real\static_4_feature\results" \

confidence_level=0.9999
width=0.25
# get confidence intervals for 4 features
python generate_confidence_intervals.py \
--data_directory "..\data\contrived_noisy\quadcrypt\results" \
--filename "..\doc\quad" \
--width "$width" \
--CI "$confidence_level"

#"" + str(width) + "_CI-" + str(confidence_level) + ".csv"
filename="../doc/quad_bin_widths-${width}_CI-${confidence_level}.csv"
python generate_fig5.py \
--CI_filename "$filename" \
--data_dir "..\data\real\static_4_feature\results"
#