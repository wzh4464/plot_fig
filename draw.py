"""
Optimized plotting utilities for experiment data visualization.
Refactored for better maintainability and code reuse.
"""

import matplotlib.pyplot as plt
import numpy as np
import os
import pandas as pd
import argparse

# Configure matplotlib for consistent plot styling
plt.rcParams.update(
    {
        "text.usetex": True,
        "font.family": "Times",
        "font.size": 30,
        "legend.fontsize": 26,
    }
)


# Plot styling constants
DEFAULT_COLORS = ["orange", "red", "grey", "black", "blue", "green"]
DEFAULT_MARKERS = ["o", "^", "x", "s", "v", "1"]
DEFAULT_FIGURE_SIZE = (6, 4)
DEFAULT_DPI = 600
DEFAULT_LINEWIDTH = 2
DEFAULT_MARKERSIZE = 8

# Plot layout constants
LEGEND_BBOX_CENTER = (0.5, 1.4)
LEGEND_BBOX_LOWER = (0.1, 0)
SUBTITLE_Y_POSITION = -0.45


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


def create_plot(
    data,
    plot_type="line_with_markers",
    pic_name="plot",
    save=False,
    xlabel="X-axis",
    ylabel="Y-axis",
    ylim=None,
    xlim=None,
    labellist=None,
    ax=None,
    show_legend=True,
    y_div=1,
    y_label_unit=None,
    colorlist=None,
    markerlist=None,
    markersize=None,
    linewidth=None,
    xstep=None,
    ytick_step=None,
    k_bool=False,
    x_grid_step=None,
    subtitle=None,
    subtitle_fontsize=None,
    legend_bbox=None,
    legend_ncol=7,
    legend_fontsize=None,
    y_k_bool=False,
    **kwargs,
):
    """Unified plotting function that can handle different plot types."""

    # Set defaults
    colorlist = colorlist or DEFAULT_COLORS
    markerlist = markerlist or DEFAULT_MARKERS
    markersize = markersize or DEFAULT_MARKERSIZE
    linewidth = linewidth or DEFAULT_LINEWIDTH

    x = data[0, :]
    ynum = np.size(data, 0) - 1
    y = data[1 : ynum + 1, :]

    # Handle data transformations
    x_plot = x / 1000 if k_bool else x
    y_plot = y / y_div if y_div != 1 else y

    # Handle y-axis scaling and labeling
    if y_k_bool:
        y_plot = y / 1000
        ylim_scaled = ylim / 1000 if ylim else None
        ytick_step_scaled = ytick_step / 1000 if ytick_step else None
        ylabel_scaled = (
            f"{ylabel} {y_label_unit}" if y_label_unit else f"{ylabel} ($10^3$)"
        )
        if y_label_unit and (
            "TX" in y_label_unit or "tps" in y_label_unit or "ms" in y_label_unit
        ):
            ylabel_scaled = f"{ylabel.split(' ')[0]} ($10^3$)"
    else:
        ylim_scaled = ylim / y_div if ylim and y_div != 1 else ylim
        ytick_step_scaled = (
            ytick_step / y_div if ytick_step and y_div != 1 else ytick_step
        )
        ylabel_scaled = f"{ylabel} {y_label_unit}" if y_label_unit else ylabel

    # Create figure if not provided
    if ax is None:
        fig, leftaxis = plt.subplots(figsize=DEFAULT_FIGURE_SIZE)
    else:
        leftaxis = ax
        fig = ax.get_figure()

    # Plot data based on type
    for i in range(ynum):
        plot_params = {
            "color": colorlist[i % len(colorlist)],
            "zorder": 2,
        }

        if labellist and show_legend:
            plot_params["label"] = labellist[i]

        if plot_type == "line_with_markers":
            plot_params.update(
                {
                    "marker": markerlist[i % len(markerlist)],
                    "markersize": markersize,
                }
            )
        elif plot_type == "time_series":
            plot_params["linewidth"] = linewidth

        leftaxis.plot(x_plot, y_plot[i, :], **plot_params)

    # Configure axes
    leftaxis.set_xlabel(xlabel)
    leftaxis.set_ylabel(ylabel_scaled)

    if ylim_scaled:
        leftaxis.set_ylim(0, ylim_scaled)
    if xlim:
        leftaxis.set_xlim(0, xlim)

    # Configure ticks
    if xstep:
        x_min, x_max = x_plot.min(), x_plot.max()
        current_xstep = xstep / 1000 if k_bool else xstep
        ticks = np.arange(x_min, x_max + current_xstep * 0.5, current_xstep)
        leftaxis.set_xticks(ticks)
        if k_bool:
            leftaxis.set_xticklabels([f"{t}" for t in ticks])
    elif xlim:
        step = max(1, xlim // 5)
        leftaxis.set_xticks(np.arange(0, xlim + 1, step))
    else:
        leftaxis.set_xticks(x_plot)
        if not k_bool:
            leftaxis.set_xticklabels(x_plot.astype(int))

    if ytick_step_scaled:
        y_max = ylim_scaled if ylim_scaled else y_plot.max() * 1.1
        leftaxis.set_yticks(np.arange(0, y_max + 1, ytick_step_scaled))

    # Add grid
    leftaxis.grid(axis="both", linestyle="--", zorder=0)
    if x_grid_step:
        from matplotlib.ticker import MultipleLocator

        current_x_grid_step = x_grid_step / 1000 if k_bool else x_grid_step
        leftaxis.xaxis.set_minor_locator(MultipleLocator(current_x_grid_step))
        leftaxis.grid(which="minor", axis="x", linestyle="--")

    # Configure legend
    if show_legend and labellist:
        legend_params = {"ncol": legend_ncol}
        if legend_bbox:
            legend_params.update({"loc": "upper center", "bbox_to_anchor": legend_bbox})
        else:
            legend_params.update(
                {"loc": "upper center", "bbox_to_anchor": LEGEND_BBOX_CENTER}
            )
        if legend_fontsize:
            legend_params["fontsize"] = legend_fontsize
        leftaxis.legend(**legend_params)

    # Add subtitle
    if subtitle:
        fontsize = subtitle_fontsize if subtitle_fontsize else plt.rcParams["font.size"]
        leftaxis.set_title(subtitle, y=SUBTITLE_Y_POSITION, fontsize=fontsize)

    # Save if requested
    if ax is None and save:
        plt.savefig(get_figure_path(pic_name), dpi=DEFAULT_DPI, bbox_inches="tight")


# Legacy function wrappers for backward compatibility
def plot_beta(data, **kwargs):
    """Legacy wrapper for create_plot with beta-specific defaults."""
    defaults = {
        "plot_type": "line_with_markers",
        "pic_name": "plot_beta",
        "xlabel": "TX rate / (TXs/Sec)",
        "ylabel": "Throughput",
        "ylim": 2800,
        "labellist": ["bsize=100", "bsize=150", "bsize=80", "bsize=50"],
        "legend_bbox": LEGEND_BBOX_LOWER,
    }
    defaults.update(kwargs)
    return create_plot(data, **defaults)


def plot_line_with_markers(data, **kwargs):
    """Legacy wrapper for create_plot with line marker defaults."""
    defaults = {
        "plot_type": "line_with_markers",
        "colorlist": ["grey", "blue", "orange", "black", "red", "green"],
        "markerlist": ["x", "s", "o", "^", "v", "1"],
    }
    defaults.update(kwargs)
    return create_plot(data, **defaults)


def plot_time_series(data, **kwargs):
    """Legacy wrapper for create_plot with time series defaults."""
    defaults = {
        "plot_type": "time_series",
        "legend_bbox": (0.5, 1.25),
        "legend_ncol": 4,
        "legend_fontsize": 22,
    }
    defaults.update(kwargs)
    return create_plot(data, **defaults)


# --------------------------------------------------------------------------------
# Specific Plotting Functions
# --------------------------------------------------------------------------------


class BasePlotter:
    """Base class for all plotters with common functionality."""

    def __init__(self, save=True):
        self.save = save
        self.data_source = None
        self.plot_config = {}

    def _load_and_prepare_data(self):
        """Load data from source. Override in subclasses."""
        if self.data_source:
            try:
                # First try reading with pandas (handles CSV headers and mixed delimiters)
                import pandas as pd
                
                # Check if file looks like CSV
                with open(self.data_source, 'r') as f:
                    first_line = f.readline().strip()
                    
                if ',' in first_line:
                    # CSV format - check if first row contains headers
                    try:
                        # Try to parse first value as number
                        first_val = first_line.split(',')[0]
                        float(first_val)
                        # No header, read normally
                        df = pd.read_csv(self.data_source, header=None)
                    except ValueError:
                        # Header present, skip it
                        df = pd.read_csv(self.data_source, skiprows=1, header=None)
                else:
                    # Space-separated format
                    df = pd.read_csv(self.data_source, sep=r'\s+', header=None)
                    
                return np.transpose(df.to_numpy().astype(float)).round(1)
                
            except Exception:
                # Fallback to numpy loadtxt
                data = np.loadtxt(self.data_source)
                return np.transpose(data).round(1)
        raise NotImplementedError(
            "Subclass must implement _load_and_prepare_data or set data_source"
        )

    def plot(self, ax=None, show_legend=True, subtitle=None, subtitle_fontsize=None):
        """Generic plot method using the unified create_plot function."""
        data = self._load_and_prepare_data()

        # Merge default config with runtime parameters
        config = self.plot_config.copy()
        config.update(
            {
                "ax": ax,
                "show_legend": show_legend,
                "subtitle": subtitle,
                "subtitle_fontsize": subtitle_fontsize,
                "save": self.save and ax is None,
            }
        )

        return create_plot(data, **config)


class CrossShardTxsPlotter(BasePlotter):
    def __init__(self, save=True):
        super().__init__(save)
        self.plot_config = {
            "plot_type": "line_with_markers",
            "pic_name": "ncr-nshard",
            "xlabel": "Number of Shards",
            "ylabel": r"Num of Cross-shard TXs",
            "ylim": 1100000,
            "xlim": 1000000,
            "labellist": ["Random", "X-shard", "cross-shard tx"],
            "y_div": 100,
            "y_label_unit": r"($10^2$)",
            "legend_bbox": LEGEND_BBOX_LOWER,
        }

    def _load_and_prepare_data(self):
        data = np.genfromtxt("cr-tx.csv", delimiter=",")
        data = np.delete(data, 0, axis=0)
        data = np.transpose(data)
        return data.astype(int)


class ThroughputVsShardsPlotter(BasePlotter):
    def __init__(self, save=True):
        super().__init__(save)
        self.data_source = "source/result.txt"
        self.plot_config = {
            "plot_type": "line_with_markers",
            "pic_name": "throughtput",
            "xlabel": "Number of Shards",
            "ylabel": "Throughput",
            "ylim": 3500,
            "labellist": ["Overall TX", "Effective TX", "Cross-shard TX"],
            "ytick_step": 500,
            "markersize": 6,
            "y_div": 100,
            "y_label_unit": r"($10^2$ tps)",
        }


class LatencyVsShardsPlotter(BasePlotter):
    def __init__(self, save=True):
        super().__init__(save)
        self.data_source = "source/latency.csv"
        self.plot_config = {
            "plot_type": "line_with_markers",
            "pic_name": "latency",
            "xlabel": "Number of Shards",
            "ylabel": "Latency",
            "ylim": 1600,
            "labellist": ["Cross-shard TX", "Intra-shard TX", "Overall TX"],
            "ytick_step": 200,
            "colorlist": ["orange", "red", "grey"],
            "markerlist": ["o", "^", "x"],
            "y_div": 100,
            "y_label_unit": r"($10^2$ ms)",
        }


class ThroughputVsBlkSizePlotter(BasePlotter):
    def __init__(self, save=True):
        super().__init__(save)
        self.data_source = "source/blk_size.txt"
        self.plot_config = {
            "plot_type": "line_with_markers",
            "pic_name": "blk_size_throughput",
            "xlabel": "Block Size (TX)",
            "ylabel": "Throughput",
            "ylim": 4000,
            "labellist": ["Overall TX", "Effective TX", "Cross-shard TX"],
            "ytick_step": 500,
            "y_div": 100,
            "y_label_unit": r"($10^2$ tps)",
            "xstep": 100,
            "x_grid_step": 50,
        }


class LatencyVsBlkSizePlotter(BasePlotter):
    def __init__(self, save=True):
        super().__init__(save)
        self.data_source = "source/latency_blksize.csv"
        self.plot_config = {
            "plot_type": "line_with_markers",
            "pic_name": "latency-blksize",
            "xlabel": "Block Size(TX)",
            "ylabel": "Latency",
            "ylim": 1600,
            "labellist": ["Cross-shard TX", "Intra-shard TX", "Overall TX"],
            "ytick_step": 200,
            "colorlist": ["orange", "red", "grey"],
            "markerlist": ["o", "^", "x"],
            "y_div": 100,
            "y_label_unit": r"($10^2$ ms)",
            "xstep": 100,
            "x_grid_step": 50,
        }


class ThroughputVsTxArrivalPlotter(BasePlotter):
    def __init__(self, save=True):
        super().__init__(save)
        self.data_source = "source/th_txar.txt"
        self.plot_config = {
            "plot_type": "line_with_markers",
            "pic_name": "throughput-txarate",
            "xlabel": "TX Arrival Rate (tps)",
            "ylabel": "Throughput",
            "ylim": 1400,
            "labellist": ["Overall TX", "Effective TX", "Cross-shard TX"],
            "ytick_step": 200,
            "xstep": 500,
            "k_bool": True,
            "y_div": 100,
            "y_label_unit": r"($10^2$ ms)",
        }


class LatencyVsTxArrivalPlotter(BasePlotter):
    def __init__(self, save=True):
        super().__init__(save)
        self.data_source = "source/latency_txar.txt"
        self.plot_config = {
            "plot_type": "line_with_markers",
            "pic_name": "latency-txar",
            "xlabel": "TX Arrival Rate ($10^3$ tps)",
            "ylabel": "Latency",
            "ylim": 700,
            "labellist": ["Cross-shard TX", "Intra-shard TX", "Overall TX"],
            "ytick_step": 150,
            "colorlist": ["orange", "red", "grey"],
            "markerlist": ["o", "^", "x"],
            "xstep": 500,
            "k_bool": True,
            "y_div": 100,
            "y_label_unit": r"($10^2$ ms)",
        }


class QueueSizeTotalPlotter(BasePlotter):
    def __init__(self, save=True):
        super().__init__(save)
        self.plot_config = {
            "plot_type": "time_series",
            "pic_name": "qtb",
            "xlabel": "Time (sec)",
            "ylabel": "Queue Size",
            "xlim": 2100,
            "ylim": 44000,
            "labellist": [
                "50 TXs",
                "100 TXs",
                "150 TXs",
                "200 TXs",
                "250 TXs",
                "300 TXs",
                "350 TXs",
            ],
            "xstep": 500,
            "ytick_step": 5000,
            "legend_ncol": 7,
            "y_k_bool": True,
            "y_label_unit": r"($10^3$ TX)",
        }

    def _load_and_prepare_data(self):
        data = np.genfromtxt("../txrate_xshard/qtb.txt")
        data = data[:, ::10]
        # Make x-axis start from 0 instead of 1
        data[0, :] = data[0, :] - 1
        return data


class QueueSizeQ1Plotter(BasePlotter):
    def __init__(self, save=True):
        super().__init__(save)
        self.plot_config = {
            "plot_type": "time_series",
            "pic_name": "q1",
            "xlabel": "Time (sec)",
            "ylabel": "Queue Size",
            "xlim": 2100,
            "labellist": [
                "8 shards",
                "16 shards",
                "24 shards",
                "32 shards",
                "40 shards",
                "48 shards",
                "56 shards",
            ],
            "ytick_step": 15000,
            "xstep": 500,
            "y_k_bool": True,
            "y_label_unit": r"($10^3$ TX)",
        }

    def _load_and_prepare_data(self):
        data = np.genfromtxt("../txrate_xshard/q1.txt")
        # Make x-axis start from 0 instead of 1
        data[0, :] = data[0, :] - 1
        self.plot_config["ylim"] = data.max() * 1.1
        return data


class QueueSizeQ2Plotter(BasePlotter):
    def __init__(self, save=True):
        super().__init__(save)
        self.plot_config = {
            "plot_type": "time_series",
            "pic_name": "q2",
            "xlabel": "Time (sec)",
            "ylabel": "Queue Size",
            "xlim": 2100,
            "labellist": [
                "8 shards",
                "16 shards",
                "24 shards",
                "32 shards",
                "40 shards",
                "48 shards",
                "56 shards",
            ],
            "ytick_step": 15000,
            "xstep": 500,
            "y_k_bool": True,
            "y_label_unit": r"($10^3$ TX)",
        }

    def _load_and_prepare_data(self):
        data = np.genfromtxt("../txrate_xshard/q2.txt")
        # Make x-axis start from 0 instead of 1
        data[0, :] = data[0, :] - 1
        self.plot_config["ylim"] = data.max() * 1.1
        return data

    def plot(self, ax=None, show_legend=True, subtitle=None, subtitle_fontsize=None):
        # Override to force show_legend=False for this specific plotter
        return super().plot(
            ax,
            show_legend=False,
            subtitle=subtitle,
            subtitle_fontsize=subtitle_fontsize,
        )


# --------------------------------------------------------------------------------
# Combined Plotting Functions
# --------------------------------------------------------------------------------
class CombinedThroughputPlotter(BasePlotter):
    def plot(self, ax=None, show_legend=True, subtitle=None, subtitle_fontsize=None):
        fig, axes = plt.subplots(1, 3, figsize=(18, 4.5))
        # fig.suptitle("Throughput Analysis", fontsize=32, y=1.08)

        # Plot 1: Throughput vs Shards
        ThroughputVsShardsPlotter().plot(
            ax=axes[0], show_legend=False, subtitle="(a) Different Number of Shards"
        )

        # Plot 2: Throughput vs Block Size (with legend)
        ThroughputVsBlkSizePlotter().plot(
            ax=axes[1], show_legend=True, subtitle="(b) Different TX Arrival Rate"
        )

        # Plot 3: Throughput vs Tx Arrival
        ThroughputVsTxArrivalPlotter().plot(
            ax=axes[2], show_legend=False, subtitle="(c) Different Block Size"
        )

        # Increase margins to avoid clipping of y-labels and suptitle
        fig.subplots_adjust(left=0.10, right=0.98, top=0.85, bottom=0.20, wspace=0.4)

        if self.save:
            plt.savefig(
                get_figure_path("combined_throughput"), dpi=600, bbox_inches="tight"
            )


class CombinedLatencyPlotter(BasePlotter):
    def plot(self, ax=None, show_legend=True, subtitle=None, subtitle_fontsize=None):
        fig, axes = plt.subplots(1, 3, figsize=(18, 4.5))
        # fig.suptitle("Latency Analysis", fontsize=32, y=1.08)

        # Plot 1: Latency vs Shards
        LatencyVsShardsPlotter().plot(
            ax=axes[0], show_legend=False, subtitle="(a) Different Number of Shards"
        )

        # Plot 2: Latency vs Block Size (with legend)
        LatencyVsBlkSizePlotter().plot(
            ax=axes[1], show_legend=True, subtitle="(b) Different Block Size"
        )

        # Plot 3: Latency vs Tx Arrival
        LatencyVsTxArrivalPlotter().plot(
            ax=axes[2], show_legend=False, subtitle="(c) Different TX Arrival Rate"
        )

        # Increase margins to avoid clipping of y-labels and suptitle
        fig.subplots_adjust(left=0.10, right=0.98, top=0.85, bottom=0.20, wspace=0.4)

        if self.save:
            plt.savefig(
                get_figure_path("combined_latency"), dpi=600, bbox_inches="tight"
            )


class CombinedQueueSizePlotter(BasePlotter):
    def plot(self, ax=None, show_legend=True, subtitle=None, subtitle_fontsize=None):
        fig, axes = plt.subplots(1, 3, figsize=(18, 4.5))
        # fig.suptitle("Queue Size Analysis", fontsize=32, y=1.08)

        # Plot 1: Queue Size Q1
        QueueSizeQ1Plotter().plot(
            ax=axes[0], show_legend=False, subtitle="(a) Eight Shards"
        )

        # Plot 2: Queue Size Total (with legend)
        QueueSizeTotalPlotter().plot(
            ax=axes[1], show_legend=True, subtitle="(b) Different Number of Shards"
        )

        # Plot 3: Queue Size Q2 (no legend by default)
        QueueSizeQ2Plotter().plot(
            ax=axes[2], show_legend=False, subtitle="(c) Different Block Size"
        )

        # Increase margins to avoid clipping of y-labels and suptitle
        fig.subplots_adjust(left=0.10, right=0.98, top=0.85, bottom=0.20, wspace=0.4)

        if self.save:
            plt.savefig(get_figure_path("combined_queue"), dpi=600, bbox_inches="tight")


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
        print(
            "Warning: 'all' task was specified with other tasks. Only 'all' will be run."
        )
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
                print(
                    f"Warning: Directory not found at {repo_path}. Skipping data update."
                )

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
                print(
                    f"Warning: Directory not found at {repo_path}. Skipping data update."
                )

        else:
            print(f"Unknown task: {task_to_run}. Please choose from {available_tasks}")


if __name__ == "__main__":
    plt.close("all")
    main()
