###
# File: ./plot_fig/draw.py
# Created Date: Friday, June 20th 2025
# Author: Zihan
# -----
# Last Modified: Friday, 20th June 2025 5:39:45 pm
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

plt.rcParams.update(
    {
        "text.usetex": False,
        "font.family": "Times",
        "font.size": 24,
        "legend.fontsize": 16,
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
        "text.usetex": False,
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
    pic_name=1,
    save=False,
    xlabel="TX rate / (TXs/Sec)",
    ylabel="Throughput (tps)",
    text_location=50,
    ylim=2800,
    labellist=["bsize=100", "bsize=150", "bsize=80", "bsize=50"],
    ytick_k=False,
    xlim=1000000,
    xscale=5,
):
    colorlist = ["orange", "red", "grey", "black", "blue", "green"]
    markerlist = ["o", "^", "x", "s"]
    x = data[0, :]
    ynum = np.size(data, 0) - 1
    y = data[1 : ynum + 1, :]
    fig, leftaxis = plt.subplots(figsize=(6, 4))
    for i in range(ynum):
        leftaxis.plot(
            x,
            y[i, :],
            color=colorlist[i],
            label=labellist[i],
            zorder=2,
            marker=markerlist[i],
            markersize=8,
        )

    leftaxis.grid(axis="y", linestyle="--", zorder=0)
    leftaxis.grid(axis="x", linestyle="--", zorder=0)

    leftaxis.set_xlabel(xlabel)
    leftaxis.set_ylabel(ylabel)
    leftaxis.set_ylim(0, ylim)
    leftaxis.set_xticks(x, x.astype(int))
    # print(x)
    leftaxis.legend(loc=0)
    if ytick_k:
        plt.yticks(np.linspace(0, xlim, xscale + 1), np.linspace(0, 10, xscale + 1))
        plt.xticks(np.linspace(8, 64, 8))
        leftaxis.set_xlim(4, 68)
    if save:
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
):
    x = data[0, :]
    ynum = np.size(data, 0) - 1
    y = data[1 : ynum + 1, :]
    fig, leftaxis = plt.subplots(figsize=(6, 4))
    for i in range(ynum):
        leftaxis.plot(
            x,
            y[i, :],
            color=colorlist[i % len(colorlist)],
            label=labellist[i],
            zorder=2,
            marker=markerlist[i % len(markerlist)],
            markersize=markersize,
        )

    leftaxis.grid(axis="y", linestyle="--", zorder=0)
    leftaxis.grid(axis="x", linestyle="--", zorder=0)

    leftaxis.set_xlabel(xlabel)
    leftaxis.set_ylabel(ylabel)
    leftaxis.set_ylim(0, ylim)
    leftaxis.set_xticks(x, x.astype(int))
    if ytick_step:
        leftaxis.set_yticks(np.arange(0, ylim + 1, ytick_step))

    leftaxis.legend(loc=0)

    if save:
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
    legend=True,
    linewidth=2,
):
    x = data[0, :]
    ynum = np.size(data, 0) - 1
    y = data[1 : ynum + 1, :]
    fig, leftaxis = plt.subplots(figsize=(6, 4))
    for i in range(ynum):
        if legend:
            leftaxis.plot(x, y[i, :], label=labellist[i], zorder=2, linewidth=linewidth)
        else:
            leftaxis.plot(x, y[i, :], zorder=2, linewidth=linewidth)

    leftaxis.grid(axis="y", linestyle="--", zorder=0)
    leftaxis.grid(axis="x", linestyle="--", zorder=0)

    leftaxis.set_xlabel(xlabel)
    leftaxis.set_ylabel(ylabel)
    leftaxis.set_xlim(0, xlim)
    leftaxis.set_ylim(0, ylim)
    leftaxis.set_xticks(np.arange(0, xlim + 1, xstep))
    leftaxis.set_yticks(np.arange(0, ylim + 1, ystep))
    if legend:
        leftaxis.legend()

    if save:
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

    def plot(self):
        raise NotImplementedError


class CrossShardTxsPlotter(BasePlotter):
    def _load_and_prepare_data(self):
        data = np.genfromtxt("cr-tx.csv", delimiter=",")
        data = np.delete(data, 0, axis=0)
        data = np.transpose(data)
        return data.astype(int)

    def plot(self):
        data = self._load_and_prepare_data()
        plot_beta(
            data=data,
            pic_name="ncr-nshard",
            save=self.save,
            xlabel="Number of Shards",
            ylabel=r"Num of Cross-shard TXs",
            text_location=30000,
            xlim=1000000,
            ylim=1100000,
            labellist=["Random", "X-shard", "cross-shard tx"],
        )


class ThroughputVsShardsPlotter(BasePlotter):
    def _load_and_prepare_data(self):
        data = np.loadtxt("source/result.txt")
        data = np.transpose(data)
        return data.round(1)

    def plot(self):
        data = self._load_and_prepare_data()
        plot_line_with_markers(
            data=data,
            pic_name="throughtput",
            save=self.save,
            xlabel="Number of Shards",
            ylabel="Throughput (tps)",
            ylim=3500,
            labellist=["Overall TX", "Effective TX", "Cross-shard TX"],
            ytick_step=500,
            markersize=6,
        )


class LatencyVsShardsPlotter(BasePlotter):
    def _load_and_prepare_data(self):
        df = pd.read_csv("source/latency.csv")
        data = np.transpose(df.to_numpy())
        return data.round(1)

    def plot(self):
        data = self._load_and_prepare_data()
        plot_line_with_markers(
            data=data,
            pic_name="latency",
            save=self.save,
            xlabel="Number of Shards",
            ylabel="Latency (ms)",
            ylim=1600,
            labellist=["Cross-shard TX", "Intra-shard TX", "Overall TX"],
            ytick_step=200,
        )


class ThroughputVsBlkSizePlotter(BasePlotter):
    def _load_and_prepare_data(self):
        data = np.loadtxt("source/blk_size.txt")
        data = np.transpose(data)
        return data.round(1)

    def plot(self):
        data = self._load_and_prepare_data()
        plot_line_with_markers(
            data=data,
            pic_name="blk_size_throughput",
            save=self.save,
            xlabel="Block Size (TX)",
            ylabel="Throughput (tps)",
            ylim=4000,
            labellist=["Overall TX", "Effective TX", "Cross-shard TX"],
            ytick_step=500,
            markersize=None,
        )


class LatencyVsBlkSizePlotter(BasePlotter):
    def _load_and_prepare_data(self):
        df = pd.read_csv("source/latency_blksize.csv")
        data = np.transpose(df.to_numpy())
        return data.round(1)

    def plot(self):
        data = self._load_and_prepare_data()
        plot_line_with_markers(
            data=data,
            pic_name="latency-blksize",
            save=self.save,
            xlabel="Block Size(TX)",
            ylabel="Latency (ms)",
            ylim=1600,
            labellist=["Cross-shard TX", "Intra-shard TX", "Overall TX"],
            ytick_step=200,
            colorlist=["orange", "red", "grey"],
            markerlist=["o", "^", "x"],
        )


class ThroughputVsTxArrivalPlotter(BasePlotter):
    def _load_and_prepare_data(self):
        return (np.transpose(np.loadtxt("source/th_txar.txt"))).round(1)

    def plot(self):
        data = self._load_and_prepare_data()
        plot_line_with_markers(
            data=data,
            pic_name="throughput-txarate",
            save=self.save,
            xlabel="TX Arrival Rate (tps)",
            ylabel="Throughput (tps)",
            ylim=1400,
            labellist=["Overall TX", "Effective TX", "Cross-shard TX"],
            ytick_step=200,
        )


class LatencyVsTxArrivalPlotter(BasePlotter):
    def _load_and_prepare_data(self):
        df = pd.read_csv("source/latency_txar.txt")
        data = np.transpose(df.to_numpy())
        return data.round(1)

    def plot(self):
        data = self._load_and_prepare_data()
        plot_line_with_markers(
            data=data,
            pic_name="latency-txar",
            save=self.save,
            xlabel="TX Arrival Rate (tps)",
            ylabel="Latency (ms)",
            ylim=700,
            labellist=["Cross-shard TX", "Intra-shard TX", "Overall TX"],
            ytick_step=150,
            colorlist=["orange", "red", "grey"],
            markerlist=["o", "^", "x"],
        )


class QueueSizeTotalPlotter(BasePlotter):
    def _load_and_prepare_data(self):
        data = np.genfromtxt("../txrate_xshard/qtb.txt")
        return data[:, ::10]

    def plot(self):
        data = self._load_and_prepare_data()
        plot_time_series(
            data=data,
            pic_name="qtb",
            save=self.save,
            xlabel="Time (sec)",
            ylabel="Queue Size (TX)",
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
            xstep=300,
            ystep=5000,
        )


class QueueSizeQ1Plotter(BasePlotter):
    def _load_and_prepare_data(self):
        return np.genfromtxt("../txrate_xshard/q1.txt")

    def plot(self):
        data = self._load_and_prepare_data()
        plot_time_series(
            data=data,
            pic_name="q1",
            save=self.save,
            xlabel="Time (sec)",
            ylabel="Queue Size (TX)",
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
            xstep=300,
        )


class QueueSizeQ2Plotter(BasePlotter):
    def _load_and_prepare_data(self):
        return np.genfromtxt("../txrate_xshard/q2.txt")

    def plot(self):
        data = self._load_and_prepare_data()
        plot_time_series(
            data=data,
            pic_name="q2",
            save=self.save,
            xlabel="Time (sec)",
            ylabel="Queue Size (TX)",
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
            xstep=300,
            legend=False,
        )


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

    plot_configs = {
        "cross_shard_txs": True,
        "throughput_vs_shards": True,
        "latency_vs_shards": True,
        "throughput_vs_blk_size": True,
        "latency_vs_blk_size": True,
        "throughput_vs_tx_arrival": True,
        "latency_vs_tx_arrival": True,
    }

    for name, save_flag in plot_configs.items():
        plotter = plot_factory.create_plotter(name, save=save_flag)
        plotter.plot()

    # Update data from git repo
    # Assuming txrate_xshard is in a specific path relative to home
    print("Updating data from git repo...")
    os.system("cd ~/codes/txrate_xshard && git pull")
    print("Data updated.")

    queue_plot_configs = {
        "queue_size_total": False,
        "queue_size_q1": False,
        "queue_size_q2": True,
    }

    for name, save_flag in queue_plot_configs.items():
        plotter = plot_factory.create_plotter(name, save=save_flag)
        plotter.plot()


if __name__ == "__main__":
    main()
