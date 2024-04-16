import pandas as pd
import argparse
import polarAC_utils as pAC
import stat_utils as SU
# get all data files from a folder, for each, add



def main():
    parser = argparse.ArgumentParser(description='Combine the results of multiple files into a single file.')
    parser.add_argument('--data_directories', nargs=4, type=str, help='Directories with data to process')
    parser.add_argument('--ground_truths', nargs=4, type=int, default=[2,3,4,5], help='ground truths of feature number for the ')
    parser.add_argument('--result_directory', type=str, help='Directories  to place processed results')
    args = parser.parse_args()
    # inialize dataframe
    results_df = pd.DataFrame(columns=['Ground_truth_feature_number','num_sign_changes', 'num_1st_deriv_sign_changes',
                            'num_2nd_deriv_sign_changes', 'Abs_AUC', 'numerical_tangent'])

    paths = args.data_directories
    #POTENTIAL ISSUE:
    #paths = [r x for x in paths]
    csvs_and_paths = []  # list of tuples, ground truth feature number and csv path
    ground_truth = dict(zip(args.data_directories, args.ground_truths))
    for gt, path in zip(args.ground_truths, paths):
        tuples = [(gt, x) for x in pAC.get_csvs_from_directory(path)]
        csvs_and_paths = csvs_and_paths + tuples

    for index, gt_csv in enumerate(csvs_and_paths):
        # columns ['arc_length' 'r_autocorrelation']

        ac_df = pAC.read_csv(gt_csv[1])
        ac_curve = list(ac_df['r_autocorrelation'])
        arc_length = list(ac_df['arc_length'])
        #UN_NORMALIZED
        gt = gt_csv[0]
        num_sign_changes = pAC.count_sign_changes(ac_curve)
        num_1st_deriv = pAC.first_derivative_test(ac_curve)
        num_2nd_deriv = pAC.second_derivative_test(ac_curve)
        abs_AUC = SU.absolute_AUC(arc_length, ac_curve)
        num_tang = SU.get_numerical_tangent_x_intercept(arc_length, ac_curve)
        new_row = {
            'Ground_truth_feature_number': gt,
            'num_sign_changes': num_sign_changes,
            'num_1st_deriv_sign_changes': num_1st_deriv,
            'num_2nd_deriv_sign_changes': num_2nd_deriv,
            'Abs_AUC': abs_AUC,
            'numerical_tangent': num_tang
        }
        results_df = pd.concat([results_df, pd.DataFrame([new_row])], ignore_index=True)
        pAC.export_df(results_df, args.result_directory)

if __name__ == "__main__":
    main()

# TODO try this with and without
# get each