###
# File: ./plot_fig/draw.py
# Created Date: Friday, June 20th 2025
# Author: Zihan
# -----
# Last Modified: Friday, 20th June 2025 5:47:58 pm
# Modified By: the developer formerly known as Zihan at <wzh4464@gmail.com>
# -----
# HISTORY:
# Date      		By   	Comments
# ----------		------	---------------------------------------------------------
###

# %%
import matplotlib.pyplot as plt
import numpy as np
import os
import time
import pandas as pd
import argparse

plt.rcParams.update(
    {
        "text.usetex": False,
        "font.family": "Times",
        "font.size": 30,
        "legend.fontsize": 26,
    }
)

# %%

# os.environ["PATH"]='/home/wu/anaconda3/bin:/home/wu/anaconda3/condabin:/usr/local/texlive/2022/bin/x86_64-linux:/home/wu/bin:/usr/local/bin:/home/wu/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/usr/games:/usr/local/games:/snap/bin:/snap/bin'

# plt.rcParams.update({
# "text.usetex": True,
# "font.family": "sans-serif",
# "font.sans-serif": ["Helvetica"]})
plt.rcParams.update(
    {
        "text.usetex": True,
        # "font.family": "Helvetica"
    }
)


# %%
# --------------------------------------------------------------------------------
# Filename Management
# --------------------------------------------------------------------------------
def get_figure_path(pic_name):
    """Gets the standardized path for a figure, creating the 'pic' directory if it doesn't exist."""
    output_dir = "pic"
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)
    return os.path.join(output_dir, f"{pic_name}.png")


# --------------------------------------------------------------------------------
# Generic Plotting Functions
# --------------------------------------------------------------------------------


def plot_beta(
    data,
    bar_width=2,
    pic_name="plot_beta",
    save=False,
    xlabel="TX rate / (TXs/Sec)",
    ylabel="Throughput",
    text_location=50,
    ylim=2800,
    labellist=["bsize=100", "bsize=150", "bsize=80", "bsize=50"],
    ytick_k=False,
    xlim=1000000,
    xscale=5,
    ax=None,
    show_legend=True,
    y_div=1,
    y_label_unit=None,
):
    colorlist = ["orange", "red", "grey", "black", "blue", "green"]
    markerlist = ["o", "^", "x", "s"]
    x = data[0, :]
    ynum = np.size(data, 0) - 1
    y = data[1 : ynum + 1, :]

    y_plot = y / y_div if y_div != 1 else y
    ylim_plot = ylim / y_div if y_div != 1 else ylim
    ylabel_plot = f"{ylabel} {y_label_unit}" if y_label_unit else ylabel

    if ax is None:
        fig, leftaxis = plt.subplots(figsize=(6, 4))
    else:
        leftaxis = ax
        fig = ax.get_figure()

    for i in range(ynum):
        leftaxis.plot(
            x,
            y_plot[i, :],
            color=colorlist[i],
            label=labellist[i],
            zorder=2,
            marker=markerlist[i],
            markersize=8,
        )

    leftaxis.grid(axis="y", linestyle="--", zorder=0)
    leftaxis.grid(axis="x", linestyle="--", zorder=0)

    leftaxis.set_xlabel(xlabel)
    leftaxis.set_ylabel(ylabel_plot)
    leftaxis.set_ylim(0, ylim_plot)
    leftaxis.set_xticks(x, x.astype(int))
    # print(x)
    if show_legend:
        leftaxis.legend(loc="upper center", bbox_to_anchor=(0.1, 0), ncol=7)
    if ytick_k:
        plt.yticks(
            np.linspace(0, xlim, xscale + 1),
            [f"{int(y)}" for y in np.linspace(0, 10, xscale + 1)],
        )
        plt.xticks(np.linspace(8, 64, 8))
        leftaxis.set_xlim(4, 68)
    if ax is None and save:
        plt.savefig(get_figure_path(pic_name), dpi=600, bbox_inches="tight")
    # plt.show()


def plot_line_with_markers(
    data,
    pic_name,
    save,
    xlabel,
    ylabel,
    ylim,
    labellist,
    ytick_step=None,
    markersize=8,
    colorlist=["grey", "blue", "orange", "black", "red", "green"],
    markerlist=["x", "s", "o", "^", "v", "1"],
    xstep=None,
    k_bool=False,
    ax=None,
    show_legend=True,
    y_div=1,
    y_label_unit=None,
    x_grid_step=None,
):
    x = data[0, :]
    ynum = np.size(data, 0) - 1
    y = data[1 : ynum + 1, :]

    if ax is None:
        fig, leftaxis = plt.subplots(figsize=(6, 4))
    else:
        leftaxis = ax
        fig = ax.get_figure()

    x_plot = x / 1000 if k_bool else x

    y_plot = y / y_div if y_div != 1 else y
    ylim_plot = ylim / y_div if y_div != 1 else ylim
    ytick_step_plot = (
        ytick_step / y_div if ytick_step is not None and y_div != 1 else ytick_step
    )
    ylabel_plot = f"{ylabel} {y_label_unit}" if y_label_unit else ylabel

    for i in range(ynum):
        leftaxis.plot(
            x_plot,
            y_plot[i, :],
            color=colorlist[i % len(colorlist)],
            label=labellist[i],
            zorder=2,
            marker=markerlist[i % len(markerlist)],
            markersize=markersize,
        )

    leftaxis.set_xlabel(xlabel)
    leftaxis.set_ylabel(ylabel_plot)
    leftaxis.set_ylim(0, ylim_plot)

    # Set major x-axis ticks based on xstep
    if xstep:
        x_min, x_max = x_plot.min(), x_plot.max()
        current_xstep = xstep / 1000 if k_bool else xstep

        # Use a small epsilon to include the max value in the range
        ticks = np.arange(x_min, x_max + current_xstep * 0.5, current_xstep)
        leftaxis.set_xticks(ticks)

        if k_bool:
            leftaxis.set_xticklabels([f"{t}" for t in ticks])
        # For non-k_bool, the default integer representation is fine
    else:
        # If no xstep, ticks are at the data points
        leftaxis.set_xticks(x_plot)
        if not k_bool:
            leftaxis.set_xticklabels(x_plot.astype(int))

    # Enable grid. Default is major ticks.
    leftaxis.grid(which="major", axis="x", linestyle="--")
    leftaxis.grid(which="major", axis="y", linestyle="--")

    # If x_grid_step is provided, set up minor ticks and grid
    if x_grid_step:
        from matplotlib.ticker import MultipleLocator

        current_x_grid_step = x_grid_step / 1000 if k_bool else x_grid_step
        leftaxis.xaxis.set_minor_locator(MultipleLocator(current_x_grid_step))
        leftaxis.grid(which="minor", axis="x", linestyle="--")

    if ytick_step:
        leftaxis.set_yticks(np.arange(0, ylim_plot + 1, ytick_step_plot))

    if show_legend:
        leftaxis.legend(loc="upper center", bbox_to_anchor=(0.5, 1.3), ncol=7)

    if ax is None and save:
        plt.savefig(get_figure_path(pic_name), dpi=600, bbox_inches="tight")
    # plt.show()


def plot_time_series(
    data,
    pic_name,
    save,
    xlabel,
    ylabel,
    xlim,
    ylim,
    labellist,
    xstep,
    ystep,
    show_legend=True,
    linewidth=2,
    legend_fontsize=22,
    ax=None,
    legend_ncol=4,
    y_k_bool=False,
    y_label_unit=None,
):
    x = data[0, :]
    ynum = np.size(data, 0) - 1
    y = data[1 : ynum + 1, :]

    y_plot = y
    ylim_plot = ylim
    ystep_plot = ystep
    ylabel_plot = ylabel
    if y_k_bool:
        y_plot = y / 1000
        ylim_plot = ylim / 1000
        ystep_plot = ystep / 1000
        ylabel_plot = f"{ylabel} {y_label_unit}" if y_label_unit else f"{ylabel} ($10^3$)"
        # 如果 y_label_unit 包含 TX 或 tps，只保留 ($10^3$)
        if y_label_unit and ("TX" in y_label_unit or "tps" in y_label_unit or "ms" in y_label_unit):
            ylabel_plot = f"{ylabel} ($10^3$)"

    if ax is None:
        fig, leftaxis = plt.subplots(figsize=(6, 4))
    else:
        leftaxis = ax
        fig = ax.get_figure()

    for i in range(ynum):
        if show_legend:
            leftaxis.plot(x, y_plot[i, :], label=labellist[i], zorder=2, linewidth=linewidth)
        else:
            leftaxis.plot(x, y_plot[i, :], zorder=2, linewidth=linewidth)

    leftaxis.grid(axis="y", linestyle="--", zorder=0)
    leftaxis.grid(axis="x", linestyle="--", zorder=0)

    leftaxis.set_xlabel(xlabel)
    leftaxis.set_ylabel(ylabel_plot)
    leftaxis.set_xlim(0, xlim)
    leftaxis.set_ylim(0, ylim_plot)
    leftaxis.set_xticks(np.arange(0, xlim + 1, xstep))
    leftaxis.set_yticks(np.arange(0, ylim_plot + 1, ystep_plot))
    if show_legend:
        legend_params = {
            "loc": "upper center",
            "bbox_to_anchor": (0.5, 1.25),
            "ncol": legend_ncol,
        }
        if legend_fontsize:
            legend_params["fontsize"] = legend_fontsize
        leftaxis.legend(**legend_params)

    if ax is None and save:
        plt.savefig(get_figure_path(pic_name), dpi=600, bbox_inches="tight")
    # plt.show()


# --------------------------------------------------------------------------------
# Specific Plotting Functions
# --------------------------------------------------------------------------------


class BasePlotter:
    """Base class for all plotters."""

    def __init__(self, save=True):
        self.save = save

    def _load_and_prepare_data(self):
        raise NotImplementedError

    def plot(self, ax=None, show_legend=True):
        raise NotImplementedError


class CrossShardTxsPlotter(BasePlotter):
    def _load_and_prepare_data(self):
        data = np.genfromtxt("cr-tx.csv", delimiter=",")
        data = np.delete(data, 0, axis=0)
        data = np.transpose(data)
        return data.astype(int)

    def plot(self, ax=None, show_legend=True):
        data = self._load_and_prepare_data()
        plot_beta(
            data=data,
            pic_name="ncr-nshard",
            save=self.save and ax is None,
            xlabel="Number of Shards",
            ylabel=r"Num of Cross-shard TXs",
            text_location=30000,
            xlim=1000000,
            ylim=1100000,
            labellist=["Random", "X-shard", "cross-shard tx"],
            ax=ax,
            show_legend=show_legend,
            y_div=100,
            y_label_unit=r"($10^2$)",
        )


class ThroughputVsShardsPlotter(BasePlotter):
    def _load_and_prepare_data(self):
        data = np.loadtxt("source/result.txt")
        data = np.transpose(data)
        return data.round(1)

    def plot(self, ax=None, show_legend=True):
        data = self._load_and_prepare_data()
        plot_line_with_markers(
            data=data,
            pic_name="throughtput",
            save=self.save and ax is None,
            xlabel="Number of Shards",
            ylabel="Throughput",
            ylim=3500,
            labellist=["Overall TX", "Effective TX", "Cross-shard TX"],
            ytick_step=500,
            markersize=6,
            ax=ax,
            show_legend=show_legend,
            y_div=100,
            y_label_unit=r"($10^2$ tps)",
        )


class LatencyVsShardsPlotter(BasePlotter):
    def _load_and_prepare_data(self):
        df = pd.read_csv("source/latency.csv")
        data = np.transpose(df.to_numpy())
        return data.round(1)

    def plot(self, ax=None, show_legend=True):
        data = self._load_and_prepare_data()
        plot_line_with_markers(
            data=data,
            pic_name="latency",
            save=self.save and ax is None,
            xlabel="Number of Shards",
            ylabel="Latency",
            ylim=1600,
            labellist=["Cross-shard TX", "Intra-shard TX", "Overall TX"],
            ytick_step=200,
            colorlist=["orange", "red", "grey"],
            markerlist=["o", "^", "x"],
            ax=ax,
            show_legend=show_legend,
            y_div=100,
            y_label_unit=r"($10^2$ ms)",
        )


class ThroughputVsBlkSizePlotter(BasePlotter):
    def _load_and_prepare_data(self):
        data = np.loadtxt("source/blk_size.txt")
        data = np.transpose(data)
        return data.round(1)

    def plot(self, ax=None, show_legend=True):
        data = self._load_and_prepare_data()
        plot_line_with_markers(
            data=data,
            pic_name="blk_size_throughput",
            save=self.save and ax is None,
            xlabel="Block Size (TX)",
            ylabel="Throughput",
            ylim=4000,
            labellist=["Overall TX", "Effective TX", "Cross-shard TX"],
            ytick_step=500,
            ax=ax,
            show_legend=show_legend,
            y_div=100,
            y_label_unit=r"($10^2$ tps)",
            xstep=100,
            x_grid_step=50,
        )


class LatencyVsBlkSizePlotter(BasePlotter):
    def _load_and_prepare_data(self):
        df = pd.read_csv("source/latency_blksize.csv")
        data = np.transpose(df.to_numpy())
        return data.round(1)

    def plot(self, ax=None, show_legend=True):
        data = self._load_and_prepare_data()
        plot_line_with_markers(
            data=data,
            pic_name="latency-blksize",
            save=self.save and ax is None,
            xlabel="Block Size(TX)",
            ylabel="Latency",
            ylim=1600,
            labellist=["Cross-shard TX", "Intra-shard TX", "Overall TX"],
            ytick_step=200,
            colorlist=["orange", "red", "grey"],
            markerlist=["o", "^", "x"],
            ax=ax,
            show_legend=show_legend,
            y_div=100,
            y_label_unit=r"($10^2$ ms)",
            xstep=100,
            x_grid_step=50,
        )


class ThroughputVsTxArrivalPlotter(BasePlotter):
    def _load_and_prepare_data(self):
        return (np.transpose(np.loadtxt("source/th_txar.txt"))).round(1)

    def plot(self, ax=None, show_legend=True):
        data = self._load_and_prepare_data()
        plot_line_with_markers(
            data=data,
            pic_name="throughput-txarate",
            save=self.save and ax is None,
            xlabel="TX Arrival Rate (tps)",
            ylabel="Throughput",
            ylim=1400,
            labellist=["Overall TX", "Effective TX", "Cross-shard TX"],
            ytick_step=200,
            xstep=500,
            k_bool=True,
            ax=ax,
            show_legend=show_legend,
            y_div=100,
            y_label_unit=r"($10^2$ ms)",
        )


class LatencyVsTxArrivalPlotter(BasePlotter):
    def _load_and_prepare_data(self):
        df = pd.read_csv("source/latency_txar.txt")
        data = np.transpose(df.to_numpy())
        return data.round(1)

    def plot(self, ax=None, show_legend=True):
        data = self._load_and_prepare_data()
        plot_line_with_markers(
            data=data,
            pic_name="latency-txar",
            save=self.save and ax is None,
            xlabel="TX Arrival Rate ($10^3$ tps)",
            ylabel="Latency",
            ylim=700,
            labellist=["Cross-shard TX", "Intra-shard TX", "Overall TX"],
            ytick_step=150,
            colorlist=["orange", "red", "grey"],
            markerlist=["o", "^", "x"],
            xstep=500,
            k_bool=True,
            ax=ax,
            show_legend=show_legend,
            y_div=100,
            y_label_unit=r"($10^2$ ms)",
        )


class QueueSizeTotalPlotter(BasePlotter):
    def _load_and_prepare_data(self):
        data = np.genfromtxt("../txrate_xshard/qtb.txt")
        return data[:, ::10]

    def plot(self, ax=None, show_legend=True):
        data = self._load_and_prepare_data()
        plot_time_series(
            data=data,
            pic_name="qtb",
            save=self.save and ax is None,
            xlabel="Time (sec)",
            ylabel="Queue Size",
            xlim=2100,
            ylim=44000,
            labellist=[
                "50 TXs",
                "100 TXs",
                "150 TXs",
                "200 TXs",
                "250 TXs",
                "300 TXs",
                "350 TXs",
            ],
            xstep=500,
            ystep=5000,
            ax=ax,
            show_legend=show_legend,
            legend_ncol=7,
            y_k_bool=True,
            y_label_unit=r"($10^3$ TX)",
        )


class QueueSizeQ1Plotter(BasePlotter):
    def _load_and_prepare_data(self):
        return np.genfromtxt("../txrate_xshard/q1.txt")

    def plot(self, ax=None, show_legend=True):
        data = self._load_and_prepare_data()
        plot_time_series(
            data=data,
            pic_name="q1",
            save=self.save and ax is None,
            xlabel="Time (sec)",
            ylabel="Queue Size",
            xlim=2100,
            ylim=data.max() * 1.1,
            labellist=[
                "8 shards",
                "16 shards",
                "24 shards",
                "32 shards",
                "40 shards",
                "48 shards",
                "56 shards",
            ],
            ystep=15000,
            xstep=500,
            ax=ax,
            show_legend=show_legend,
            y_k_bool=True,
            y_label_unit=r"($10^3$ TX)",
        )


class QueueSizeQ2Plotter(BasePlotter):
    def _load_and_prepare_data(self):
        return np.genfromtxt("../txrate_xshard/q2.txt")

    def plot(self, ax=None, show_legend=True):
        data = self._load_and_prepare_data()
        plot_time_series(
            data=data,
            pic_name="q2",
            save=self.save and ax is None,
            xlabel="Time (sec)",
            ylabel="Queue Size",
            xlim=2100,
            ylim=data.max() * 1.1,
            labellist=[
                "8 shards",
                "16 shards",
                "24 shards",
                "32 shards",
                "40 shards",
                "48 shards",
                "56 shards",
            ],
            ystep=15000,
            xstep=500,
            show_legend=False,  # This plotter specifically hides legend
            ax=ax,
            y_k_bool=True,
            y_label_unit=r"($10^3$ TX)",
        )


# --------------------------------------------------------------------------------
# Combined Plotting Functions
# --------------------------------------------------------------------------------
class CombinedThroughputPlotter(BasePlotter):
    def plot(self, ax=None, show_legend=True):
        fig, axes = plt.subplots(1, 3, figsize=(18, 4.5))
        # fig.suptitle("Throughput Analysis", fontsize=32, y=1.08)

        # Plot 1: Throughput vs Shards
        ThroughputVsShardsPlotter().plot(ax=axes[0], show_legend=False)

        # Plot 2: Throughput vs Block Size (with legend)
        ThroughputVsBlkSizePlotter().plot(ax=axes[1], show_legend=True)

        # Plot 3: Throughput vs Tx Arrival
        ThroughputVsTxArrivalPlotter().plot(ax=axes[2], show_legend=False)

        # Increase margins to avoid clipping of y-labels and suptitle
        fig.subplots_adjust(left=0.10, right=0.98, top=0.85, bottom=0.10, wspace=0.4)

        if self.save:
            plt.savefig(get_figure_path("combined_throughput"), dpi=600, bbox_inches="tight")
        # plt.show()


class CombinedLatencyPlotter(BasePlotter):
    def plot(self, ax=None, show_legend=True):
        fig, axes = plt.subplots(1, 3, figsize=(18, 4.5))
        # fig.suptitle("Latency Analysis", fontsize=32, y=1.08)

        # Plot 1: Latency vs Shards
        LatencyVsShardsPlotter().plot(ax=axes[0], show_legend=False)

        # Plot 2: Latency vs Block Size (with legend)
        LatencyVsBlkSizePlotter().plot(ax=axes[1], show_legend=True)

        # Plot 3: Latency vs Tx Arrival
        LatencyVsTxArrivalPlotter().plot(ax=axes[2], show_legend=False)

        # Increase margins to avoid clipping of y-labels and suptitle
        fig.subplots_adjust(left=0.10, right=0.98, top=0.85, bottom=0.10, wspace=0.4)

        if self.save:
            plt.savefig(get_figure_path("combined_latency"), dpi=600, bbox_inches="tight")
        # plt.show()


class CombinedQueueSizePlotter(BasePlotter):
    def plot(self, ax=None, show_legend=True):
        fig, axes = plt.subplots(1, 3, figsize=(18, 4.5))
        # fig.suptitle("Queue Size Analysis", fontsize=32, y=1.08)

        # Plot 1: Queue Size Q1
        QueueSizeQ1Plotter().plot(ax=axes[0], show_legend=False)

        # Plot 2: Queue Size Total (with legend)
        QueueSizeTotalPlotter().plot(ax=axes[1], show_legend=True)

        # Plot 3: Queue Size Q2 (no legend by default)
        QueueSizeQ2Plotter().plot(ax=axes[2], show_legend=False)

        # Increase margins to avoid clipping of y-labels and suptitle
        fig.subplots_adjust(left=0.10, right=0.98, top=0.85, bottom=0.10, wspace=0.4)

        if self.save:
            plt.savefig(get_figure_path("combined_queue"), dpi=600, bbox_inches="tight")
        # plt.show()


class PlotFactory:
    def __init__(self):
        self._plotters = {
            "cross_shard_txs": CrossShardTxsPlotter,
            "throughput_vs_shards": ThroughputVsShardsPlotter,
            "latency_vs_shards": LatencyVsShardsPlotter,
            "throughput_vs_blk_size": ThroughputVsBlkSizePlotter,
            "latency_vs_blk_size": LatencyVsBlkSizePlotter,
            "throughput_vs_tx_arrival": ThroughputVsTxArrivalPlotter,
            "latency_vs_tx_arrival": LatencyVsTxArrivalPlotter,
            "queue_size_total": QueueSizeTotalPlotter,
            "queue_size_q1": QueueSizeQ1Plotter,
            "queue_size_q2": QueueSizeQ2Plotter,
            "combined_throughput": CombinedThroughputPlotter,
            "combined_latency": CombinedLatencyPlotter,
            "combined_queue": CombinedQueueSizePlotter,
        }

    def create_plotter(self, plot_type, save=True):
        plotter_class = self._plotters.get(plot_type)
        if not plotter_class:
            raise ValueError(f"Unknown plot type: {plot_type}")
        return plotter_class(save=save)


# %%
def main():
    """Main function to run all plotting tasks."""
    plot_factory = PlotFactory()
    all_tasks = list(plot_factory._plotters.keys())
    available_tasks = all_tasks + ["update_data", "all"]

    parser = argparse.ArgumentParser(description="Generate plots from experiment data.")
    parser.add_argument(
        "tasks",
        nargs="+",
        default=["all"],
        help=f"The task(s) to run. Choose from: {', '.join(available_tasks)}. "
        'If no task is specified, "all" will be executed.',
    )
    args = parser.parse_args()
    tasks_to_run = args.tasks

    if "all" in tasks_to_run and len(tasks_to_run) > 1:
        print("Warning: 'all' task was specified with other tasks. Only 'all' will be run.")
        tasks_to_run = ["all"]

    for task_to_run in tasks_to_run:
        if task_to_run == "all":
            # The original "run all" logic
            plot_configs = {
                "cross_shard_txs": False,
                "throughput_vs_shards": True,
                "latency_vs_shards": True,
                "throughput_vs_blk_size": True,
                "latency_vs_blk_size": True,
                "throughput_vs_tx_arrival": True,
                "latency_vs_tx_arrival": True,
            }
            for name, save_flag in plot_configs.items():
                print(f"Running task: {name}...")
                plotter = plot_factory.create_plotter(name, save=save_flag)
                plotter.plot()
                print(f"Finished task: {name}")

            print("Updating data from git repo...")
            repo_path = os.path.expanduser("~/codes/txrate_xshard")
            if os.path.isdir(repo_path):
                os.system(f"cd {repo_path} && git pull")
                print("Data updated.")
            else:
                print(f"Warning: Directory not found at {repo_path}. Skipping data update.")

            queue_plot_configs = {
                "queue_size_total": True,
                "queue_size_q1": True,
                "queue_size_q2": True,
            }
            for name, save_flag in queue_plot_configs.items():
                print(f"Running task: {name}...")
                plotter = plot_factory.create_plotter(name, save=save_flag)
                plotter.plot()
                print(f"Finished task: {name}")

        elif task_to_run in all_tasks:
            print(f"Running task: {task_to_run}...")
            plotter = plot_factory.create_plotter(task_to_run, save=True)
            plotter.plot()
            print(f"Finished task: {task_to_run}")

        elif task_to_run == "update_data":
            print("Updating data from git repo...")
            repo_path = os.path.expanduser("~/codes/txrate_xshard")
            if os.path.isdir(repo_path):
                os.system(f"cd {repo_path} && git pull")
                print("Data updated.")
            else:
                print(f"Warning: Directory not found at {repo_path}. Skipping data update.")

        else:
            print(f"Unknown task: {task_to_run}. Please choose from {available_tasks}")


if __name__ == "__main__":
    plt.close("all")
    main()
