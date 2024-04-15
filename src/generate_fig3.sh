#!/bin/bash -e


python generate_fig3.py \
--data_directory "..\data\contrived_noisy\tricrypt\results" \
--color '#de6064' \
--name "..\doc\fig3-2.png"




# create fig3 for dicrypt
python generate_fig3.py \
--data_directory "..\data\contrived_noisy\dicrypt\results" \
--color '#D57047' \
--name "..\doc\fig3-1.png"



# create fig3 for quadcrypt
python generate_fig3.py \
--data_directory "..\data\contrived_noisy\quadcrypt\results" \
--color '#aa2494' \
--name "..\doc\fig3-3.png"


# create fig3 for pentacrypt
python generate_fig3.py \
--data_directory "..\data\contrived_noisy\pentacrypt\results" \
--color '#5c00a5' \
--name "..\doc\fig3-4.png"


# create fig3 for tricrypt



