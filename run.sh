#!/bin/bash -e

python PolarAC_arc_parameterization_better_practices.py \
--data_directory "C:\Users\graci\OneDrive\Documents\Lab\Polar AC\Noisy!\The Ideals" \
--result_directory "C:\Users\graci\OneDrive\Documents\Lab\Polar AC\Noisy!\The Ideals\result" \
--include_ac_curve True

python PolarAC_process_results_better_practices.py \
--data_directory "C:\Users\graci\OneDrive\Documents\Lab\Polar AC\Noisy!\The Ideals\result" \
--result_directory "C:\Users\graci\OneDrive\Documents\Lab\Polar AC\Noisy!\The Ideals\result"