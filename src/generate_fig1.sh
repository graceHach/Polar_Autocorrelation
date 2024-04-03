#!/bin/bash -e

python PolarAC_arc_parameterization_better_practices.py \
--data_directory "..\data\contrived_ideal" \
--result_directory "..\data\contrived_ideal\results" \
--include_ac_curve True
echo 'Data for figure 1 created.'

python generate_fig1.py \
--data_directory "..\data\contrived_ideal\results" \
--figure_destination_directory "..\doc\fig1_unannotated.png"
