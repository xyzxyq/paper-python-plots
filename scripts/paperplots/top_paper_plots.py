"""Reusable top-paper inspired plot primitives and demos."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.gridspec import GridSpec
from matplotlib.patches import ConnectionPatch, Patch, Rectangle
import numpy as np
import pandas as pd

from .styles import SOFT_EDGE_EDGES, SOFT_EDGE_FILLS, TOP_PAPER_PALETTES


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


def _soft_fill(index: int) -> str:
    colors = SOFT_EDGE_FILLS[2::4] or SOFT_EDGE_FILLS
    return colors[index % len(colors)]


def _soft_edge(index: int) -> str:
    colors = SOFT_EDGE_EDGES[2::4] or SOFT_EDGE_EDGES
    return colors[index % len(colors)]


def _synthetic_image(seed: int, size: int = 72) -> np.ndarray:
    rng = np.random.default_rng(seed)
    yy, xx = np.mgrid[0:size, 0:size]
    cx, cy = rng.uniform(20, 52, size=2)
    blob = np.exp(-((xx - cx) ** 2 + (yy - cy) ** 2) / rng.uniform(260, 520))
    wave = 0.25 * np.sin(xx / rng.uniform(4.5, 8.0) + seed) + 0.2 * np.cos(yy / rng.uniform(6.0, 10.0))
    img = blob + wave + rng.normal(0, 0.035, size=(size, size))
    img = (img - img.min()) / max(img.max() - img.min(), 1e-9)
    return np.dstack((img, np.roll(img, 5, axis=0), np.roll(img, -7, axis=1)))


def _method_variant(base: np.ndarray, method: str, seed: int) -> np.ndarray:
    """Create deterministic method-result variants from one synthetic scene."""

    rng = np.random.default_rng(seed)
    if method.lower() == "input":
        gray = base.mean(axis=2, keepdims=True)
        return np.clip(np.repeat(gray, 3, axis=2) * 0.82 + rng.normal(0, 0.045, base.shape), 0, 1)
    if method.lower() == "baseline":
        blurred = (
            base
            + np.roll(base, 1, axis=0)
            + np.roll(base, -1, axis=0)
            + np.roll(base, 1, axis=1)
            + np.roll(base, -1, axis=1)
        ) / 5.0
        return np.clip(blurred * 0.9 + rng.normal(0, 0.035, base.shape), 0, 1)
    if method.lower() == "ours":
        sharpened = np.clip(base + 0.55 * (base - np.roll(base, 2, axis=0)), 0, 1)
        return np.clip(sharpened * 0.96 + 0.025, 0, 1)
    return np.clip(base, 0, 1)


def qualitative_result_grid(
    images: Sequence[Sequence[np.ndarray]],
    row_labels: Sequence[str],
    col_labels: Sequence[str],
    *,
    title: str = "Qualitative Comparison",
    style_name: str = "cvpr_qualitative",
) -> plt.Figure:
    """Draw CVPR-style qualitative result grids with method columns and callouts."""

    look = get_top_paper_look(style_name)
    rows, cols = len(images), len(images[0])
    fig = plt.figure(figsize=(1.62 * cols + 1.05, 1.34 * rows + 1.05), layout=None)
    gs = GridSpec(rows, cols, figure=fig, left=0.082, right=0.99, top=0.835, bottom=0.08, wspace=0.035, hspace=0.085)
    metric_rng = np.random.default_rng(314)
    for r in range(rows):
        for c in range(cols):
            ax = fig.add_subplot(gs[r, c])
            ax.imshow(images[r][c])
            ax.set_xticks([])
            ax.set_yticks([])
            for spine in ax.spines.values():
                spine.set_color("#FFFFFF")
                spine.set_linewidth(1.25)
            if r == 0:
                ax.set_title(col_labels[c], fontsize=8.8, pad=4, color=look.text_color)
            if c == 0:
                ax.text(
                    -0.085,
                    0.5,
                    row_labels[r],
                    transform=ax.transAxes,
                    ha="right",
                    va="center",
                    fontsize=8.0,
                    color=look.muted_text,
                    rotation=90,
                )
            if c > 0:
                score = 24.0 + 5.6 * c + metric_rng.normal(0, 0.35)
                badge_color = _soft_edge(c)
                ax.text(
                    0.04,
                    0.955,
                    f"{score:.1f} dB",
                    transform=ax.transAxes,
                    ha="left",
                    va="top",
                    fontsize=6.7,
                    color="white",
                    bbox={"boxstyle": "round,pad=0.18", "facecolor": badge_color, "edgecolor": "white", "linewidth": 0.6},
                    zorder=5,
                )
            if c == max(0, cols - 2):
                rect = Rectangle((0.58, 0.55), 0.28, 0.28, transform=ax.transAxes, fill=False, edgecolor="#FFD166", linewidth=1.35)
                ax.add_patch(rect)
                inset = ax.inset_axes([0.56, 0.05, 0.34, 0.34])
                inset.imshow(images[r][c])
                inset.set_xlim(images[r][c].shape[1] * 0.52, images[r][c].shape[1] * 0.86)
                inset.set_ylim(images[r][c].shape[0] * 0.86, images[r][c].shape[0] * 0.52)
                inset.set_xticks([])
                inset.set_yticks([])
                for spine in inset.spines.values():
                    spine.set_edgecolor("#FFD166")
                    spine.set_linewidth(1.1)
    fig.suptitle(title, fontsize=12.0, y=0.982, fontweight="bold")
    fig.text(0.082, 0.892, "aligned method columns, metric badges, and local zoom callouts", fontsize=7.4, color=look.muted_text)
    return fig


def metric_suite_dashboard(
    metrics: Sequence[str],
    methods: Sequence[str],
    values: np.ndarray,
    *,
    title: str = "Benchmark Metric Suite",
    style_name: str = "icml_dense",
) -> plt.Figure:
    """Draw dense ICML-style multi-metric result dashboard."""

    look = get_top_paper_look(style_name)
    arr = np.asarray(values, dtype=float)
    fig = plt.figure(figsize=(2.55 * len(metrics), 3.25), layout=None)
    gs = fig.add_gridspec(1, len(metrics), left=0.072, right=0.986, top=0.78, bottom=0.27, wspace=0.32)
    axes = np.asarray([fig.add_subplot(gs[0, i]) for i in range(len(metrics))])
    axes = np.atleast_1d(axes)
    edges = [_soft_edge(i) for i in range(len(methods))]
    fills = [_soft_fill(i) for i in range(len(methods))]
    for ax, metric, column in zip(axes, metrics, arr.T):
        order = np.argsort(column)[::-1]
        bars = ax.bar(
            np.arange(len(methods)),
            column[order],
            color=[mcolors.to_rgba(fills[i], 0.82) for i in order],
            edgecolor=[edges[i] for i in order],
            linewidth=1.05,
            zorder=3,
        )
        _style_axis(ax, look)
        ax.set_title(metric, fontsize=9.2, pad=8)
        ax.set_xticks(np.arange(len(methods)), [methods[i] for i in order], rotation=35, ha="right", fontsize=7.2)
        ax.set_ylim(max(0, float(np.nanmin(column)) - 0.12), max(column) * 1.12)
        ax.axhline(float(np.nanmean(column)), color="#7F7F7F", linestyle="--", linewidth=0.75, alpha=0.65, zorder=1)
        for bar, value in zip(bars, column[order]):
            is_best = np.isclose(value, np.nanmax(column))
            if is_best:
                bar.set_linewidth(1.55)
                bar.set_edgecolor("#111111")
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                value + max(column) * 0.027,
                f"{value:.2f}",
                ha="center",
                va="bottom",
                fontsize=6.9,
                fontweight="bold" if is_best else "normal",
            )
    handles = [Patch(facecolor=fills[i], edgecolor=edges[i], linewidth=1.0, label=method) for i, method in enumerate(methods)]
    fig.legend(handles=handles, loc="lower center", ncol=len(methods), frameon=False, bbox_to_anchor=(0.5, 0.04), fontsize=7.8)
    fig.suptitle(title, fontsize=12.0, y=0.962, fontweight="bold")
    fig.text(0.075, 0.845, "shared method ordering with direct values and mean baselines", fontsize=7.5, color=look.muted_text)
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
    """Draw a dense ablation heatmap/table with values and best-cell emphasis."""

    look = get_top_paper_look(style_name)
    arr = np.asarray(matrix, dtype=float)
    im = ax.imshow(arr, cmap=cmap, aspect="auto")
    ax.set_facecolor(look.panel_face)
    ax.set_title(title, fontsize=10.6, pad=10, fontweight="bold")
    ax.set_xticks(np.arange(len(col_labels)), col_labels, rotation=30, ha="right")
    ax.set_yticks(np.arange(len(row_labels)), row_labels)
    baseline = arr[0]
    best_rows = np.nanargmax(arr, axis=0)
    for r in range(arr.shape[0]):
        for c in range(arr.shape[1]):
            color = "white" if arr[r, c] > np.nanmean(arr) else "#202020"
            delta = arr[r, c] - baseline[c]
            label = f"{arr[r, c]:.2f}\n{delta:+.2f}" if r > 0 else f"{arr[r, c]:.2f}"
            ax.text(c, r, label, ha="center", va="center", fontsize=6.8, color=color, linespacing=0.9)
            if best_rows[c] == r:
                ax.add_patch(Rectangle((c - 0.48, r - 0.48), 0.96, 0.96, fill=False, edgecolor="#111111", linewidth=1.35))
    ax.set_xticks(np.arange(arr.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(arr.shape[0] + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="white", linewidth=1.15)
    ax.tick_params(which="minor", bottom=False, left=False)
    for spine in ax.spines.values():
        spine.set_visible(False)
    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.046, pad=0.03)
    cbar.set_label("Score", labelpad=4)
    cbar.outline.set_linewidth(0.6)


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
    size_span = max(float(np.nanmax(sizes) - np.nanmin(sizes)), 1e-9)
    scaled_sizes = 54 + 132 * (sizes - np.nanmin(sizes)) / size_span
    colors = [_soft_edge(i) for i in range(len(xs))]
    fills = [_soft_fill(i) for i in range(len(xs))]
    order = np.argsort(xs)
    frontier: list[int] = []
    best_y = -np.inf
    for idx in order:
        if ys[idx] >= best_y:
            frontier.append(int(idx))
            best_y = float(ys[idx])
    frontier = sorted(frontier, key=lambda idx: xs[idx])
    x_pad = (float(np.nanmax(xs)) - float(np.nanmin(xs))) * 0.10
    y_pad = (float(np.nanmax(ys)) - float(np.nanmin(ys))) * 0.18
    ax.set_xlim(float(np.nanmin(xs)) - x_pad, float(np.nanmax(xs)) + x_pad * 1.55)
    ax.set_ylim(float(np.nanmin(ys)) - y_pad * 0.45, float(np.nanmax(ys)) + y_pad * 0.55)
    if len(frontier) >= 2:
        ax.plot(xs[frontier], ys[frontier], color="#222222", linewidth=1.45, linestyle="--", alpha=0.84, zorder=2)
        ax.scatter(xs[frontier], ys[frontier], s=24, facecolors="white", edgecolors="#222222", linewidths=0.8, zorder=3)
    frontier_set = set(frontier)
    edge_colors = [colors[idx] if idx in frontier_set else "#9CA3AF" for idx in range(len(xs))]
    face_colors = [fills[idx] if idx in frontier_set else "#E5E7EB" for idx in range(len(xs))]
    ax.scatter(
        xs,
        ys,
        s=scaled_sizes,
        facecolors=face_colors,
        edgecolors=edge_colors,
        alpha=[0.96 if idx in frontier_set else 0.70 for idx in range(len(xs))],
        linewidth=[1.45 if idx in frontier_set else 0.85 for idx in range(len(xs))],
        zorder=4,
    )
    offset_pattern = [(6, 7), (7, -11), (7, 6), (7, -11), (8, 7), (-44, -2), (7, 9), (7, -13), (-46, 7), (8, 6)]
    label_offsets = {
        "Ours-S": (9, 16),
        "Ours-B": (10, -20),
        "Ours-L": (-62, 9),
        "MoE": (-58, -2),
        "Dense": (10, -12),
        "Aug": (9, -18),
        "Base": (9, 8),
    }
    for idx, (xi, yi, label) in enumerate(zip(xs, ys, labels)):
        is_frontier = idx in frontier
        dx, dy = label_offsets.get(str(label), offset_pattern[idx % len(offset_pattern)])
        ax.annotate(
            label,
            (xi, yi),
            xytext=(dx, dy),
            textcoords="offset points",
            fontsize=7.1,
            color="#111111" if is_frontier else "#4B5563",
            fontweight="bold" if is_frontier else "normal",
            bbox={"facecolor": "white", "edgecolor": "none", "alpha": 0.70, "pad": 0.7},
            arrowprops={
                "arrowstyle": "-",
                "color": "#9CA3AF",
                "linewidth": 0.55,
                "shrinkA": 2,
                "shrinkB": 2,
            }
            if is_frontier and label.startswith("Ours")
            else None,
        )
    if frontier:
        best_idx = max(frontier, key=lambda idx: ys[idx])
        ax.scatter([xs[best_idx]], [ys[best_idx]], s=scaled_sizes[best_idx] * 1.12, facecolors="#FFF2B2", edgecolors="#B45309", linewidth=1.65, zorder=5)
        ax.annotate(
            "better",
            xy=(0.08, 0.90),
            xytext=(0.19, 0.79),
            xycoords="axes fraction",
            textcoords="axes fraction",
            arrowprops={"arrowstyle": "->", "linewidth": 0.85, "color": "#6B7280"},
            fontsize=7.1,
            color="#6B7280",
            ha="center",
            va="center",
        )
    if size is not None:
        legend_sizes = [float(np.nanpercentile(sizes, 25)), float(np.nanpercentile(sizes, 75))]
        handles = [
            ax.scatter([], [], s=54 + 132 * (v - np.nanmin(sizes)) / size_span, facecolors="#F3F4F6", edgecolors="#777777", label=f"{v:g}M")
            for v in legend_sizes
        ]
        ax.legend(handles=handles, title="Params", frameon=False, loc="lower right", fontsize=6.8, title_fontsize=7.0, borderpad=0.2, handletextpad=0.8)
    ax.set_xlabel(xlabel)
    ax.set_ylabel(ylabel)
    ax.set_title(title, fontweight="bold", fontsize=11.2, pad=8)
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
    levels = np.linspace(float(np.nanmin(arr)), float(np.nanmax(arr)), 5)
    ax.contour(arr, levels=levels[1:-1], colors="white", linewidths=0.55, alpha=0.62)
    ax.set_title(title, fontsize=10.2, pad=8, fontweight="bold")
    ax.set_xticks([])
    ax.set_yticks([])
    for spine in ax.spines.values():
        spine.set_color("#D1D5DB")
        spine.set_linewidth(1.0)
    ax.add_patch(Rectangle((0.05, 0.86), 0.24, 0.055, transform=ax.transAxes, facecolor="white", edgecolor="#111111", linewidth=0.65, alpha=0.88))
    ax.text(0.07, 0.887, "region", transform=ax.transAxes, fontsize=6.2, va="center", ha="left", color="#111111")
    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.045, pad=0.025)
    cbar.set_label(colorbar_label)
    cbar.outline.set_linewidth(0.6)
    ax.set_facecolor(look.panel_face)


def demo_qual_grid() -> plt.Figure:
    rows = ["Scene A", "Scene B", "Scene C"]
    cols = ["Input", "Baseline", "Ours", "GT"]
    images = []
    for r in range(len(rows)):
        base = _synthetic_image(100 + r * 9)
        images.append([_method_variant(base, col, 300 + r * 11 + c) for c, col in enumerate(cols)])
    return qualitative_result_grid(images, rows, cols, title="Qualitative Result Grid")


def demo_metric_suite() -> plt.Figure:
    rng = np.random.default_rng(11)
    methods = ["Base", "Aug", "Ours-S", "Ours-L"]
    metrics = ["Acc.", "Robust", "Speed", "Calib."]
    base = np.array([[0.72, 0.61, 0.83, 0.68], [0.76, 0.66, 0.74, 0.73], [0.82, 0.71, 0.69, 0.79], [0.86, 0.78, 0.62, 0.84]])
    values = np.clip(base + rng.normal(0, 0.015, size=base.shape), 0, 1)
    return metric_suite_dashboard(metrics, methods, values, title="Metric Suite")


def demo_ablation_matrix() -> plt.Figure:
    rows = ["No pretrain", "+ data", "+ loss", "+ scale"]
    cols = ["Small", "Base", "Large", "XL"]
    values = np.array([[0.61, 0.65, 0.67, 0.68], [0.67, 0.72, 0.75, 0.76], [0.70, 0.76, 0.80, 0.82], [0.72, 0.79, 0.84, 0.87]])
    fig, ax = plt.subplots(figsize=(4.75, 3.25), layout="constrained")
    ablation_matrix_plot(ax, values, rows, cols)
    return fig


def demo_pareto_scatter() -> plt.Figure:
    labels = ["Tiny", "Fast", "Base", "Aug", "Dense", "MoE", "Ours-S", "Ours-B", "Ours-L"]
    x = np.array([7.2, 10.4, 15.8, 18.9, 31.5, 27.0, 13.4, 20.5, 24.8])
    y = np.array([0.61, 0.70, 0.735, 0.765, 0.805, 0.835, 0.812, 0.858, 0.888])
    sizes = np.array([38, 52, 86, 96, 160, 142, 74, 112, 138])
    fig, ax = plt.subplots(figsize=(5.05, 3.15), layout="constrained")
    pareto_scatter_plot(ax, x, y, labels, size=sizes, xlabel="Latency (ms)", ylabel="Score")
    return fig


def demo_uncertainty_map() -> plt.Figure:
    rng = np.random.default_rng(19)
    yy, xx = np.mgrid[-2:2:90j, -3:3:120j]
    signal = np.exp(-(xx**2 + yy**2)) + 0.45 * np.exp(-((xx - 1.3) ** 2 + (yy + 0.8) ** 2) / 0.7)
    uncertainty = np.clip(1.0 - signal + rng.normal(0, 0.035, size=signal.shape), 0, 1)
    residual = np.abs(signal - np.roll(signal, 6, axis=1))
    fig, axes = plt.subplots(1, 3, figsize=(8.25, 2.85), layout="constrained")
    uncertainty_map_plot(axes[0], signal, title="Trait Prediction", colorbar_label="Trait", cmap="YlGn")
    uncertainty_map_plot(axes[1], uncertainty, title="Predictive Uncertainty", colorbar_label="Std.", cmap="magma")
    uncertainty_map_plot(axes[2], residual, title="Residual Hotspots", colorbar_label="Abs. err.", cmap="YlOrRd")
    return fig
