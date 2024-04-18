import polarAC_utils as pAC
import matplotlib.pyplot as plt
import matplotlib
import argparse
def main ():
    parser = argparse.ArgumentParser(description="Generate figure two using the data produced by generate_figure_data.sh")
    parser.add_argument('--data_directory', type=str, help='directory with csvs to plot')
    parser.add_argument('--CI_filename', type=str, help='Csv file with confidence intervals')
    args = parser.parse_args()
    CI_filename = args.CI_filename
    data_dir = args.data_directory
    legend = False
    light_pink="#ff6e73"
    dark_purple = "#5400a5"
    colors = {'bounds': 'c', 'real': "#ff6e73"}

    CI_df = pAC.read_csv(CI_filename)

    #fig (ax1, ax2) = plt.subplots(1,2,sharey=True, figsize)

    arc, lowerCI, upperCI = CI_df['Arc length'], CI_df['CI lower bound'], CI_df['CI upper bound']
    simulated_bounds, = plt.plot(arc, lowerCI, label="Simulated Bounds", color=colors['bounds'])
    plt.plot(arc, upperCI, color=colors['bounds'])
    plt.fill_between(arc, lowerCI, upperCI, color=colors['bounds'])

    data_csvs = pAC.get_csvs_from_directory(data_dir)

    for csv in data_csvs:
        curr_df = pAC.read_csv(csv)
        correct_csv = curr_df.columns[0] == 'r_autocorrelation' and curr_df.columns[1] == 'arc_length'
        # IGNORES files that don't have the correct headers
        if correct_csv:
            arc, ac = curr_df['arc_length'], curr_df['r_autocorrelation']

            if not legend:
                legend = True
                line, = plt.plot(arc, ac, color=colors['real'], alpha=0.8)
            else:
                plt.plot(arc, ac, color=colors['real'], alpha=0.8)

        else:
            print(csv,"has missing or incorrect headers. Headers should be: 'r_autocorrelation', etc")


    plt.legend([line, simulated_bounds], ["Experimental Data", "Simulated Bounds"], loc='upper right')
    plt.xlabel("Arc length parameterization")
    plt.ylabel("Radial coordinate autocorrelation")
    plt.title("Four featured organoid data vs simulated bounds")
    plt.savefig("..\\doc\\fig5.png")


if __name__ == "__main__":
    main()