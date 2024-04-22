import polarAC_utils as pAC
import matplotlib.pyplot as plt
from matplotlib import gridspec
import matplotlib
import argparse
import numpy as np


def main ():
    parser = argparse.ArgumentParser(description="Generate figure two using the data produced by generate_figure_data.sh")
    parser.add_argument('--snapshots_directory', type=str, help='directory with AC curves of snapshots')
    parser.add_argument('--timeseries_directory', type=str, help='directory with AC curves of timeseries')
    parser.add_argument('--CI_filename', type=str, help='Csv file with confidence intervals')
    args = parser.parse_args()
    CI_filename = args.CI_filename
    s_dir, t_dir = [args.snapshots_directory, args.timeseries_directory]
    legend = False
    light_pink="#ff6e73"
    dark_purple = "#5400a5"
    dark_cyan = "#69DCDA"
    dark_orange = "#b45f3c"
    colors = {'bounds1': dark_purple, 'bounds2': "#5DBAB8", 'real': dark_cyan}
    alpha = 1
    colormap = 'RdPu'

    CI_df = pAC.read_csv(CI_filename)

    gs = gridspec.GridSpec(1, 2, width_ratios=[1, 1.2])
    #fig, (ax1, ax2) = plt.subplots(1,2, sharey=True, figsize=(11, 6))
    fig = plt.figure(layout="constrained", figsize=(13, 6))
    fig = plt.figure( figsize=(13, 6))
    ax1 = fig.add_subplot(gs[0])
    ax2 = fig.add_subplot(gs[1])
    axs = [ax1,ax2]
    ax1.set_ylim(-1.2, 1.2)  # Limit y-values
    ax2.set_ylim(-1.2, 1.2)  # Limit y-values
    arc, lowerCI, upperCI = CI_df['Arc length'], CI_df['CI lower bound'], CI_df['CI upper bound']

    simulated_bounds1, = ax1.plot(arc, lowerCI, label="Simulated Bounds", color=colors['bounds1'])
    ax1.plot(arc, upperCI, color=colors['bounds1'])
    ax1.fill_between(arc, lowerCI, upperCI, color=colors['bounds1'])


    simulated_bounds2, = ax2.plot(arc, lowerCI, label="Simulated Bounds", color=colors['bounds2'])
    ax2.plot(arc, upperCI, color=colors['bounds2'])
    ax2.fill_between(arc, lowerCI, upperCI, color=colors['bounds2'])


    snapshot_csvs = pAC.get_csvs_from_directory(s_dir)

    for csv in snapshot_csvs:
        curr_df = pAC.read_csv(csv)
        correct_csv = curr_df.columns[0] == 'r_autocorrelation' and curr_df.columns[1] == 'arc_length'
        # IGNORES files that don't have the correct headers
        if correct_csv:
            arc, ac = curr_df['arc_length'], curr_df['r_autocorrelation']

            if not legend:
                legend = True
                line, = ax1.plot(arc, ac, color=colors['real'], alpha=alpha)
            else:
                ax1.plot(arc, ac, color=colors['real'], alpha=alpha)

        else:
            print(csv, "has missing or incorrect headers. Headers should be: 'r_autocorrelation', etc")


    ax1.legend([line, simulated_bounds1], ["Individual organoids", "Simulated bounds"], loc='upper right')
    ax1.set_xlabel("Arc length parameterization")
    ax1.set_ylabel("Radial coordinate autocorrelation")
    ax1.set_title("Snapshots")

    timeseries_csvs = pAC.get_csvs_from_directory(t_dir)
    num_timepoints = len(timeseries_csvs)
    sm = plt.cm.ScalarMappable(cmap=colormap, norm=plt.Normalize(vmin=0, vmax=64))
    #timepoints = np.linspace(1, num_timepoints, num=num_timepoints)
    timepoints = range(0,65,1)
    sm.set_array(timepoints)

    for index, csv in enumerate(timeseries_csvs):
        curr_df = pAC.read_csv(csv)
        correct_csv = curr_df.columns[0] == 'r_autocorrelation' and curr_df.columns[1] == 'arc_length'
        # IGNORES files that don't have the correct headers
        if correct_csv:
            arc, ac = curr_df['arc_length'], curr_df['r_autocorrelation']
            ax2.plot(arc, ac, color=sm.to_rgba(index), alpha=0.8)
        else:
            print(csv, "has missing or incorrect headers. Headers should be: 'r_autocorrelation', etc")

    ax2.legend([simulated_bounds2], ["Simulated bounds"], loc='upper right')
    ax2.set_xlabel("Arc length parameterization")
    ax2.set_ylabel("Radial coordinate autocorrelation")
    ax2.set_title("Timeseries")

    cbar = fig.colorbar(sm, ax=ax2)
    cbar.set_label('Timepoint')

    plt.suptitle("Experimental data vs simulated bounds")
    #ax1.set_title("Four featured organoid data vs simulated bounds")
    plt.subplots_adjust(left=0.075, right=0.97, wspace=0.2)
    plt.savefig("..\\doc\\fig5.png")


if __name__ == "__main__":
    main()