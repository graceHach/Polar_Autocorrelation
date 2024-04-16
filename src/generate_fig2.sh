#!/bin/bash -e
#todo:

python generate_fig2.py \
--data_directories "..\data\contrived_noisy\dicrypt\results" "..\data\contrived_noisy\tricrypt\results" \
"..\data\contrived_noisy\quadcrypt\results" "..\data\contrived_noisy\pentacrypt\results"
