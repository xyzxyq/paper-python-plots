"""figures4papers-inspired Matplotlib helpers.

The source repository ships project-specific plotting scripts plus a skill
contract, not a reusable Python package. This module turns the reusable parts
of that contract into deterministic helpers for paper-python-plots.
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Sequence

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
import numpy as np


FIGURES4PAPERS_PALETTE = {
    "blue_main": "#0F4D92",
    "blue_secondary": "#3775BA",
    "green_1": "#DDF3DE",
    "green_2": "#AADCA9",
    "green_3": "#8BCF8B",
    "red_1": "#F6CFCB",
    "red_2": "#E9A6A1",
    "red_strong": "#B64342",
    "neutral": "#CFCECE",
    "neutral_dark": "#4D4D4D",
    "highlight": "#FFD700",
    "teal": "#42949E",
    "violet": "#9A4D8E",
}

FIGURES4PAPERS_DEFAULT_COLORS = [
    FIGURES4PAPERS_PALETTE["blue_main"],
    FIGURES4PAPERS_PALETTE["green_3"],
    FIGURES4PAPERS_PALETTE["red_strong"],
    FIGURES4PAPERS_PALETTE["teal"],
    FIGURES4PAPERS_PALETTE["violet"],
    FIGURES4PAPERS_PALETTE["neutral"],
]

SUPPORTED_FORMATS = {"pdf", "svg", "eps", "png", "jpg", "jpeg", "tif", "tiff"}


@dataclass(frozen=True)
class Figures4PapersStyle:
    """Portable style preset inferred from figures4papers project scripts."""

    font_size: int = 16
    axes_linewidth: float = 2.5
    use_tex: bool = False
    font_family: tuple[str, ...] = ("Arial", "Helvetica", "DejaVu Sans", "Noto Sans CJK SC", "sans-serif")
    big_bar: bool = False


def _as_1d(values: Sequence[float] | np.ndarray, *, name: str) -> np.ndarray:
    arr = np.asarray(values, dtype=float)
    if arr.ndim != 1:
        raise ValueError(f"{name} must be 1D, got shape {arr.shape}.")
    return arr


def _as_color_cycle(colors: Sequence[str] | None, n: int) -> list[str]:
    source = list(colors or FIGURES4PAPERS_DEFAULT_COLORS)
    if not source:
        raise ValueError("At least one color is required.")
    return [source[i % len(source)] for i in range(n)]


def apply_figures4papers_style(style: Figures4PapersStyle | None = None) -> Figures4PapersStyle:
    """Apply the figures4papers house style and return the resolved style."""

    resolved = style or Figures4PapersStyle()
    font_size = 24 if resolved.big_bar else resolved.font_size
    axes_linewidth = 3.0 if resolved.big_bar else resolved.axes_linewidth
    plt.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 300,
            "savefig.transparent": False,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.05,
            "font.family": "sans-serif",
            "font.sans-serif": list(resolved.font_family),
            "font.size": font_size,
            "axes.labelsize": font_size,
            "axes.titlesize": font_size,
            "axes.linewidth": axes_linewidth,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.major.width": max(1.0, axes_linewidth * 0.55),
            "ytick.major.width": max(1.0, axes_linewidth * 0.55),
            "xtick.major.size": 5.0,
            "ytick.major.size": 5.0,
            "legend.frameon": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "text.usetex": resolved.use_tex,
            "axes.unicode_minus": False,
        }
    )
    return resolved


def create_subplots(
    nrows: int = 1,
    ncols: int = 1,
    figsize: tuple[float, float] | None = None,
    **kwargs,
) -> tuple[plt.Figure, np.ndarray]:
    """Create subplots and return a flattened axes array."""

    fig, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize, squeeze=False, **kwargs)
    return fig, axes.ravel()


def finalize_figure(
    fig: plt.Figure,
    out_path: str | Path,
    *,
    formats: Sequence[str] | None = None,
    dpi: int = 300,
    close: bool = True,
    pad: float = 0.05,
    **kwargs,
) -> list[Path]:
    """Save to one or more formats with lightweight blank-output checks."""

    base = Path(out_path)
    if formats is None:
        formats = [base.suffix.lower().lstrip(".")] if base.suffix else ["pdf", "svg", "png"]
        if base.suffix:
            base = base.with_suffix("")
    normalized = [ext.lower().lstrip(".") for ext in formats]
    unsupported = [ext for ext in normalized if ext not in SUPPORTED_FORMATS]
    if unsupported:
        raise ValueError(f"Unsupported export format(s): {', '.join(unsupported)}")

    base.parent.mkdir(parents=True, exist_ok=True)
    fig.canvas.draw()
    paths: list[Path] = []
    for ext in normalized:
        path = base.with_suffix(f".{ext}")
        save_kwargs = {"dpi": dpi, "bbox_inches": "tight", "pad_inches": pad, **kwargs}
        if ext in {"pdf", "png", "svg"}:
            save_kwargs["metadata"] = {"Creator": "paper-python-plots figures4papers helper"}
        fig.savefig(path, **save_kwargs)
        if path.stat().st_size < 1024:
            raise RuntimeError(f"Export looks too small and may be blank: {path}")
        paths.append(path)

    for path in paths:
        if path.suffix.lower() == ".png":
            arr = mpimg.imread(path)
            if arr.size == 0 or float(np.nanstd(arr)) < 1e-5:
                raise RuntimeError(f"PNG export appears blank: {path}")
    if close:
        plt.close(fig)
    return paths


def annotate_bars(ax: plt.Axes, bars, fmt: str = "{:.2f}", fontsize: float = 10, padding: float = 3) -> None:
    """Add value labels above a Matplotlib BarContainer."""

    for bar in bars:
        value = bar.get_height()
        if not np.isfinite(value):
            continue
        ax.annotate(
            fmt.format(value),
            xy=(bar.get_x() + bar.get_width() / 2, value),
            xytext=(0, padding),
            textcoords="offset points",
            ha="center",
            va="bottom",
            fontsize=fontsize,
        )


def make_grouped_bar(
    ax: plt.Axes,
    categories: Sequence[str],
    series: Sequence[Sequence[float]],
    labels: Sequence[str],
    *,
    ylabel: str = "Value",
    colors: Sequence[str] | None = None,
    annotate: bool = False,
    hatches: Sequence[str] | None = None,
    value_fmt: str = "{:.2f}",
) -> list:
    """Render figures4papers-style grouped bars with strong edges."""

    arr = np.asarray(series, dtype=float)
    if arr.ndim != 2:
        raise ValueError(f"series must be 2D: one row per label, got shape {arr.shape}.")
    if arr.shape[0] != len(labels):
        raise ValueError("labels length must match number of series rows.")
    if arr.shape[1] != len(categories):
        raise ValueError("categories length must match number of series columns.")

    x = np.arange(len(categories))
    width = min(0.82 / max(len(labels), 1), 0.28)
    color_cycle = _as_color_cycle(colors, len(labels))
    hatch_cycle = list(hatches or [""] * len(labels))
    bars_out = []
    for idx, (values, label) in enumerate(zip(arr, labels)):
        offset = (idx - (len(labels) - 1) / 2) * width
        bars = ax.bar(
            x + offset,
            values,
            width=width,
            label=label,
            color=color_cycle[idx],
            edgecolor="black",
            linewidth=1.5,
            hatch=hatch_cycle[idx % len(hatch_cycle)] if hatch_cycle else "",
            zorder=3,
        )
        if annotate:
            annotate_bars(ax, bars, fmt=value_fmt, fontsize=max(8, plt.rcParams["font.size"] * 0.55))
        bars_out.append(bars)

    finite = arr[np.isfinite(arr)]
    if finite.size:
        ymin = min(0.0, float(finite.min()))
        ymax = float(finite.max())
        span = max(ymax - ymin, abs(ymax), 1.0)
        ax.set_ylim(ymin - 0.04 * span, ymax + 0.16 * span)
    ax.set_xticks(x, categories)
    ax.set_ylabel(ylabel)
    ax.grid(axis="y", color="#E6E6E6", linewidth=0.8, zorder=0)
    ax.legend(frameon=False)
    return bars_out


def make_trend(
    ax: plt.Axes,
    x: Sequence[float],
    y_series: Sequence[Sequence[float]],
    labels: Sequence[str],
    *,
    colors: Sequence[str] | None = None,
    yerr_series: Sequence[Sequence[float]] | None = None,
    ylabel: str | None = None,
    xlabel: str | None = None,
    show_shadow: bool = True,
) -> list:
    """Plot multi-series trends with optional uncertainty bands."""

    x_arr = _as_1d(x, name="x")
    color_cycle = _as_color_cycle(colors, len(y_series))
    if len(y_series) != len(labels):
        raise ValueError("labels length must match y_series length.")
    if yerr_series is not None and len(yerr_series) != len(y_series):
        raise ValueError("yerr_series length must match y_series length.")

    lines = []
    for idx, (values, label) in enumerate(zip(y_series, labels)):
        y_arr = _as_1d(values, name=f"y_series[{idx}]")
        if y_arr.size != x_arr.size:
            raise ValueError("Each y series must have the same length as x.")
        color = color_cycle[idx]
        (line,) = ax.plot(x_arr, y_arr, label=label, color=color, linewidth=2.5, marker="o", markersize=4.5)
        lines.append(line)
        if show_shadow:
            if yerr_series is None:
                err = np.full_like(y_arr, np.nanstd(y_arr) * 0.08)
            else:
                err = _as_1d(yerr_series[idx], name=f"yerr_series[{idx}]")
                if err.size != x_arr.size:
                    raise ValueError("Each uncertainty series must have the same length as x.")
            ax.fill_between(x_arr, y_arr - err, y_arr + err, color=color, alpha=0.16, linewidth=0)

    if ylabel:
        ax.set_ylabel(ylabel)
    if xlabel:
        ax.set_xlabel(xlabel)
    ax.grid(axis="y", color="#E6E6E6", linewidth=0.8)
    ax.legend(frameon=False)
    return lines


def make_heatmap(
    ax: plt.Axes,
    matrix: Sequence[Sequence[float]],
    *,
    x_labels: Sequence[str] | None = None,
    y_labels: Sequence[str] | None = None,
    cmap: str = "magma",
    cbar_label: str | None = None,
    annotate: bool = False,
) -> plt.AxesImage:
    """Render a labeled heatmap with optional readable cell annotations."""

    arr = np.asarray(matrix, dtype=float)
    if arr.ndim != 2:
        raise ValueError(f"matrix must be 2D, got shape {arr.shape}.")
    im = ax.imshow(arr, cmap=cmap, aspect="auto")
    if x_labels is not None:
        if len(x_labels) != arr.shape[1]:
            raise ValueError("x_labels length must match matrix columns.")
        ax.set_xticks(np.arange(arr.shape[1]), x_labels, rotation=35, ha="right")
    if y_labels is not None:
        if len(y_labels) != arr.shape[0]:
            raise ValueError("y_labels length must match matrix rows.")
        ax.set_yticks(np.arange(arr.shape[0]), y_labels)
    if annotate:
        norm = im.norm
        cmap_obj = im.cmap
        for row in range(arr.shape[0]):
            for col in range(arr.shape[1]):
                rgba = cmap_obj(norm(arr[row, col]))
                luminance = 0.2126 * rgba[0] + 0.7152 * rgba[1] + 0.0722 * rgba[2]
                ax.text(col, row, f"{arr[row, col]:.2f}", ha="center", va="center", color="black" if luminance > 0.58 else "white")
    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.035)
    if cbar_label:
        cbar.set_label(cbar_label)
    return im


def make_scatter(
    ax: plt.Axes,
    x: Sequence[float],
    y: Sequence[float],
    *,
    label: str | None = None,
    color: str | None = None,
    size: float = 50,
    alpha: float = 0.72,
) -> None:
    """Draw a single scatter series with light fill and saturated edge."""

    x_arr = _as_1d(x, name="x")
    y_arr = _as_1d(y, name="y")
    if x_arr.size != y_arr.size:
        raise ValueError("x and y must have the same length.")
    edge = color or FIGURES4PAPERS_PALETTE["blue_main"]
    fill = mcolors.to_hex(np.asarray(mcolors.to_rgb(edge)) * 0.25 + 0.75)
    ax.scatter(x_arr, y_arr, s=size, facecolor=fill, edgecolor=edge, linewidth=1.2, alpha=alpha, label=label, zorder=3)
    if label:
        ax.legend(frameon=False)


def make_sphere_illustration(
    ax: plt.Axes,
    *,
    light_dir: tuple[float, float, float] = (-0.5, 0.5, 0.8),
    resolution: int = 128,
    alpha: float = 0.6,
    cmap: str = "Blues",
) -> None:
    """Draw a shaded 2D disk that mimics a 3D sphere for conceptual panels."""

    yy, xx = np.mgrid[-1:1:complex(0, resolution), -1:1:complex(0, resolution)]
    rr = xx**2 + yy**2
    mask = rr <= 1.0
    zz = np.zeros_like(xx)
    zz[mask] = np.sqrt(1.0 - rr[mask])
    light = np.asarray(light_dir, dtype=float)
    light = light / max(np.linalg.norm(light), 1e-9)
    shade = xx * light[0] + yy * light[1] + zz * light[2]
    shade = np.where(mask, np.clip((shade + 1.0) / 2.0, 0, 1), np.nan)
    ax.imshow(shade, extent=(-1, 1, -1, 1), origin="lower", cmap=cmap, alpha=alpha)
    ax.contour(xx, yy, rr, levels=[1.0], colors=[FIGURES4PAPERS_PALETTE["blue_main"]], linewidths=1.6)
    ax.set_aspect("equal")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_visible(False)


def demo_figures4papers_house_style() -> plt.Figure:
    """Build a compact demo covering bars, trends, heatmaps, and concept panels."""

    apply_figures4papers_style(Figures4PapersStyle(font_size=12, axes_linewidth=1.6))
    fig, axes = create_subplots(2, 2, figsize=(9.5, 6.4), layout="constrained")

    make_grouped_bar(
        axes[0],
        ["AUROC", "AUPRC", "PPVn"],
        [[0.54, 0.22, 0.21], [0.69, 0.46, 0.34], [0.79, 0.70, 0.45]],
        ["Baseline", "Strong", "Ours"],
        colors=[FIGURES4PAPERS_PALETTE["red_2"], FIGURES4PAPERS_PALETTE["green_3"], FIGURES4PAPERS_PALETTE["blue_main"]],
        ylabel="Score",
        annotate=True,
    )
    axes[0].set_title("Grouped comparison")

    x = np.arange(1, 7)
    make_trend(
        axes[1],
        x,
        [
            0.42 + 0.36 * (1 - np.exp(-x / 2.4)),
            0.38 + 0.28 * (1 - np.exp(-x / 3.0)),
        ],
        ["Ours", "Baseline"],
        colors=[FIGURES4PAPERS_PALETTE["blue_main"], FIGURES4PAPERS_PALETTE["red_strong"]],
        ylabel="Accuracy",
        xlabel="Epoch",
    )
    axes[1].set_title("Trend with uncertainty")

    matrix = np.array([[0.71, 0.74, 0.79], [0.76, 0.81, 0.85], [0.83, 0.87, 0.91]])
    make_heatmap(
        axes[2],
        matrix,
        x_labels=["Task A", "Task B", "Task C"],
        y_labels=["Base", "+Data", "+Loss"],
        cmap="YlGnBu",
        cbar_label="Score",
        annotate=True,
    )
    axes[2].set_title("Ablation heatmap")

    make_sphere_illustration(axes[3], resolution=180, alpha=0.78)
    axes[3].set_title("Concept panel")

    fig.suptitle("figures4papers-inspired house style", fontsize=14, fontweight="bold")
    return fig
