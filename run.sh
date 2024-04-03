#!/bin/bash -e


# generate all data for figure 1
python src/PolarAC_arc_parameterization_better_practices.py \
--data_directory "C:\Users\graci\OneDrive\Documents\Lab\Polar AC\Noisy!\dicrypt\data" \
--result_directory "C:\Users\graci\OneDrive\Documents\Lab\Polar AC\Noisy!\para_1\new_results" \
--include_ac_curve True

python src/PolarAC_process_results_better_practices.py \
--data_directory "C:\Users\graci\OneDrive\Documents\Lab\Polar AC\Noisy!\para_1\new_results" \
--result_directory "C:\Users\graci\OneDrive\Documents\Lab\Polar AC\Noisy!\para_1\new_results"