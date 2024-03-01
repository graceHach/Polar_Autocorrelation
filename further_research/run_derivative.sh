#!/bin/bash -e

python PolarAC_arc_parameterization_successive_derivatives.py \
--data_directory "C:\Users\graci\OneDrive\Documents\Lab\Polar AC\!real brightfield organoids\Kaustav Data - patterned\Cropped\csvs" \
--result_directory "C:\Users\graci\OneDrive\Documents\Lab\Polar AC\!real brightfield organoids\Kaustav Data - patterned\Cropped\results" \
--include_ac_curve True

python PolarAC_process_results_successive_derivatives.py \
--data_directory "C:\Users\graci\OneDrive\Documents\Lab\Polar AC\!real brightfield organoids\Kaustav Data - patterned\Cropped\results" \
--result_directory "C:\Users\graci\OneDrive\Documents\Lab\Polar AC\!real brightfield organoids\Kaustav Data - patterned\Cropped\results"