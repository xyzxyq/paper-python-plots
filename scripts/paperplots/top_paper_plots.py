"""Reusable top-paper inspired plot primitives and demos."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.gridspec import GridSpec
import numpy as np
import pandas as pd

from .styles import TOP_PAPER_PALETTES


@dataclass(frozen=True)
class TopPaperLook:
    """Small style bundle for result-figure families."""

    name: str
    palette: Sequence[str]
    panel_face: str = "#F7F7F7"
    grid_color: str = "#E1E1E1"
    text_color: str = "#202020"
    muted_text: str = "#6B7280"
    edge: str = "#303030"


def get_top_paper_look(name: str = "cvpr_qualitative") -> TopPaperLook:
    palette = TOP_PAPER_PALETTES.get(name, TOP_PAPER_PALETTES["cvpr_qualitative"])
    panel_face = "#F8FAFC"
    if name == "eccv_lowlevel":
        panel_face = "#F5F7FA"
    elif name == "icml_dense":
        panel_face = "#FBFBF7"
    elif name == "aaai_geo":
        panel_face = "#F3F7F5"
    return TopPaperLook(name=name, palette=palette, panel_face=panel_face)


def _style_axis(ax: plt.Axes, look: TopPaperLook, *, grid: bool = True) -> None:
    ax.set_facecolor(look.panel_face)
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#B8B8B8")
    ax.spines["bottom"].set_color("#B8B8B8")
    ax.tick_params(colors=look.text_color, width=0.7, length=2.5, pad=2)
    if grid:
        ax.grid(True, color=look.grid_color, linewidth=0.6, zorder=0)


def _synthetic_image(seed: int, size: int = 72) -> np.ndarray:
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:size, 0:size]
    cx, cy = rng.uniform(20, 52, size=2)
    blob = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / rng.uniform(260, 520))
    wave = 0.25 * np.sin(xx / rng.uniform(4.5, 8.0) + seed) + 0.2 * np.cos(yy / rng.uniform(6.0, 10.0))
    img = blob + wave + rng.normal(0, 0.035, size=(size, size))
    img = (img - img.min()) / max(img.max() - img.min(), 1e-9)
    return np.dstack((img, np.roll(img, 5, axis=0), np.roll(img, -7, axis=1)))


def qualitative_result_grid(
    images: Sequence[Sequence[np.ndarray]],
    row_labels: Sequence[str],
    col_labels: Sequence[str],
    *,
    title: str = "Qualitative Comparison",
    style_name: str = "cvpr_qualitative",
) -> plt.Figure:
    """Draw CVPR-style qualitative result grids with method columns."""

    look = get_top_paper_look(style_name)
    rows, cols = len(images), len(images[0])
    fig = plt.figure(figsize=(1.34 * cols + 0.75, 1.18 * rows + 0.55), layout=None)
    gs = GridSpec(rows, cols, figure=fig, left=0.075, right=0.992, top=0.88, bottom=0.055, wspace=0.035, hspace=0.075)
    for r in range(rows):
        for c in range(cols):
            ax = fig.add_subplot(gs[r, c])
            ax.imshow(images[r][c])
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_color("#FFFFFF")
                spine.set_linewidth(1.1)
            if r == 0:
                ax.set_title(col_labels[c], fontsize=8.5, pad=3)
            if c == 0:
                ax.text(
                    -0.08,
                    0.5,
                    row_labels[r],
                    transform=ax.transAxes,
                    ha="right",
                    va="center",
                    fontsize=8.0,
                    color=look.muted_text,
                    rotation=90,
                )
    fig.suptitle(title, fontsize=10.5, y=0.985)
    return fig


def metric_suite_dashboard(
    metrics: Sequence[str],
    methods: Sequence[str],
    values: np.ndarray,
    *,
    title: str = "Benchmark Metric Suite",
    style_name: str = "icml_dense",
) -> plt.Figure:
    """Draw dense ICML-style multi-metric bar/line result dashboard."""

    look = get_top_paper_look(style_name)
    arr = np.asarray(values, dtype=float)
    fig, axes = plt.subplots(1, len(metrics), figsize=(2.25 * len(metrics), 2.35), layout="constrained")
    axes = np.atleast_1d(axes)
    colors = [look.palette[i % len(look.palette)] for i in range(len(methods))]
    for ax, metric, column in zip(axes, metrics, arr.T):
        order = np.argsort(column)[::-1]
        bars = ax.bar(
            np.arange(len(methods)),
            column[order],
            color=[mcolors.to_rgba(colors[i], 0.78) for i in order],
            edgecolor=[colors[i] for i in order],
            linewidth=0.9,
            zorder=3,
        )
        _style_axis(ax, look)
        ax.set_title(metric, fontsize=8.8)
        ax.set_xticks(np.arange(len(methods)), [methods[i] for i in order], rotation=35, ha="right", fontsize=7.2)
        ax.set_ylim(0, max(column) * 1.16)
        for bar, value in zip(bars, column[order]):
            ax.text(bar.get_x() + bar.get_width() / 2, value + max(column) * 0.025, f"{value:.2f}", ha="center", va="bottom", fontsize=6.7)
    fig.suptitle(title, fontsize=10.5)
    return fig


def ablation_matrix_plot(
    ax: plt.Axes,
    matrix: Sequence[Sequence[float]],
    row_labels: Sequence[str],
    col_labels: Sequence[str],
    *,
    title: str = "Ablation Matrix",
    style_name: str = "icml_dense",
    cmap: str = "YlGnBu",
) -> None:
    """Draw a dense ablation heatmap with readable cell values."""

    look = get_top_paper_look(style_name)
    arr = np.asarray(matrix, dtype=float)
    im = ax.imshow(arr, cmap=cmap, aspect="auto")
    ax.set_facecolor(look.panel_face)
    ax.set_title(title, fontsize=9.5, pad=7)
    ax.set_xticks(np.arange(len(col_labels)), col_labels, rotation=30, ha="right")
    ax.set_yticks(np.arange(len(row_labels)), row_labels)
    for r in range(arr.shape[0]):
        for c in range(arr.shape[1]):
            color = "white" if arr[r, c] > np.nanmean(arr) else "#202020"
            ax.text(c, r, f"{arr[r, c]:.2f}", ha="center", va="center", fontsize=7.2, color=color)
    ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.03, label="Score")


def pareto_scatter_plot(
    ax: plt.Axes,
    x: Sequence[float],
    y: Sequence[float],
    labels: Sequence[str],
    *,
    size: Sequence[float] | None = None,
    xlabel: str = "Cost",
    ylabel: str = "Performance",
    title: str = "Pareto Trade-off",
    style_name: str = "icml_dense",
) -> None:
    """Draw direct-label Pareto scatter for accuracy/cost/latency tradeoffs."""

    look = get_top_paper_look(style_name)
    xs = np.asarray(x, dtype=float)
    ys = np.asarray(y, dtype=float)
    sizes = np.asarray(size if size is not None else np.full_like(xs, 85), dtype=float)
    colors = [look.palette[i % len(look.palette)] for i in range(len(xs))]
    ax.scatter(xs, ys, s=sizes, c=colors, alpha=0.86, edgecolor="white", linewidth=0.8, zorder=3)
    for xi, yi, label in zip(xs, ys, labels):
        ax.annotate(label, (xi, yi), xytext=(4, 3), textcoords="offset points", fontsize=7.4)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    _style_axis(ax, look)


def uncertainty_map_plot(
    ax: plt.Axes,
    values: Sequence[Sequence[float]],
    *,
    title: str = "Uncertainty Map",
    colorbar_label: str = "Uncertainty",
    style_name: str = "aaai_geo",
    cmap: str = "viridis",
) -> None:
    """Draw map-like calibrated heatmap panels for geospatial/social-impact results."""

    look = get_top_paper_look(style_name)
    arr = np.asarray(values, dtype=float)
    im = ax.imshow(arr, cmap=cmap, interpolation="bilinear")
    ax.set_title(title, fontsize=9.5)
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#D1D5DB")
    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.045, pad=0.025)
    cbar.set_label(colorbar_label)
    ax.set_facecolor(look.panel_face)


def demo_qual_grid() -> plt.Figure:
    rows = ["Scene A", "Scene B", "Scene C"]
    cols = ["Input", "Baseline", "Ours", "GT"]
    images = [[_synthetic_image(100 + r * 7 + c) for c in range(len(cols))] for r in range(len(rows))]
    return qualitative_result_grid(images, rows, cols, title="CVPR-style Qualitative Result Grid")


def demo_metric_suite() -> plt.Figure:
    rng = np.random.default_rng(11)
    methods = ["Base", "Aug", "Ours-S", "Ours-L"]
    metrics = ["Acc.", "Robust", "Speed"]
    base = np.array([[0.72, 0.61, 0.83], [0.76, 0.66, 0.74], [0.82, 0.71, 0.69], [0.86, 0.78, 0.62]])
    values = np.clip(base + rng.normal(0, 0.015, size=base.shape), 0, 1)
    return metric_suite_dashboard(metrics, methods, values)


def demo_ablation_matrix() -> plt.Figure:
    rows = ["No pretrain", "+ data", "+ loss", "+ scale"]
    cols = ["Small", "Base", "Large", "XL"]
    values = np.array([[0.61, 0.65, 0.67, 0.68], [0.67, 0.72, 0.75, 0.76], [0.70, 0.76, 0.80, 0.82], [0.72, 0.79, 0.84, 0.87]])
    fig, ax = plt.subplots(figsize=(4.2, 3.0), layout="constrained")
    ablation_matrix_plot(ax, values, rows, cols)
    return fig


def demo_pareto_scatter() -> plt.Figure:
    labels = ["Base", "Fast", "Dense", "Ours-S", "Ours-L"]
    x = np.array([18, 10, 34, 15, 26])
    y = np.array([0.71, 0.66, 0.78, 0.81, 0.86])
    sizes = np.array([95, 70, 150, 105, 135])
    fig, ax = plt.subplots(figsize=(4.2, 3.0), layout="constrained")
    pareto_scatter_plot(ax, x, y, labels, size=sizes, xlabel="Latency (ms)", ylabel="Score")
    return fig


def demo_uncertainty_map() -> plt.Figure:
    rng = np.random.default_rng(19)
    yy, xx = np.mgrid[-2:2:90j, -3:3:120j]
    signal = np.exp(-(xx**2 + yy**2)) + 0.45 * np.exp(-((xx - 1.3) ** 2 + (yy + 0.8) ** 2) / 0.7)
    uncertainty = np.clip(1.0 - signal + rng.normal(0, 0.035, size=signal.shape), 0, 1)
    fig, axes = plt.subplots(1, 2, figsize=(5.9, 2.75), layout="constrained")
    uncertainty_map_plot(axes[0], signal, title="Trait Prediction", colorbar_label="Trait", cmap="YlGn")
    uncertainty_map_plot(axes[1], uncertainty, title="Predictive Uncertainty", colorbar_label="Std.", cmap="magma")
    return fig
