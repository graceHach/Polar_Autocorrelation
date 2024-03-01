#!/bin/bash -e

python src/PolarAC_arc_parameterization_better_practices.py \
--data_directory "data\contrived_ideal" \
--result_directory "data\contrived_ideal\results" \
--include_ac_curve True

python src/generate_fig1.py \
--data_directory "data\contrived_ideal\results" \
--figure_destination_directory "data\contrived_ideal\results"