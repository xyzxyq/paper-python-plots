#!/usr/bin/env python3
"""Publication-ready scientific plotting helpers.

Core path intentionally uses only matplotlib, numpy, and pandas. Optional
scientific packages can be layered on by callers, but this module should keep
working in a lean Python environment.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import math
from pathlib import Path
from typing import Iterable, Sequence

import matplotlib

matplotlib.use("Agg")

import matplotlib.image as mpimg
import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.collections import PolyCollection
from matplotlib.patches import Patch
from matplotlib.ticker import MaxNLocator
import numpy as np
import pandas as pd

from paperplots import (
    SOFT_EDGE_EDGES,
    SOFT_EDGE_FILLS,
    SOFT_EDGE_PALETTES,
    TOP_PAPER_PALETTES,
    WEB_INSPIRED_PALETTES,
    ablation_matrix_plot,
    demo_ablation_matrix,
    demo_metric_suite,
    demo_pareto_scatter,
    demo_qual_grid,
    demo_uncertainty_map,
    metric_suite_dashboard,
    pareto_scatter_plot,
    qualitative_result_grid,
    uncertainty_map_plot,
)


@dataclass(frozen=True)
class FigureStyle:
    """Matplotlib style preset for paper figures."""

    name: str
    base_font_size: float = 16.0
    axes_linewidth: float = 2.4
    tick_width: float = 2.0
    tick_size: float = 6.0
    line_width: float = 2.4
    marker_size: float = 6.0
    bar_edge_width: float = 1.8
    grid: bool = False
    cjk: bool = True


STYLE_PRESETS = {
    "compact": FigureStyle("compact", 8.0, 0.8, 0.7, 3.0, 1.4, 4.0, 0.8, True),
    "rl_benchmark": FigureStyle("rl_benchmark", 7.4, 0.68, 0.58, 2.3, 1.05, 3.7, 0.78, True, False),
    "ai_conference": FigureStyle("ai_conference", 11.5, 1.35, 1.15, 4.2, 1.9, 5.0, 1.25, False),
    "nature_minimal": FigureStyle("nature_minimal", 9.0, 0.9, 0.8, 3.5, 1.5, 4.0, 0.9, False),
    "bio_stats": FigureStyle("bio_stats", 10.0, 1.1, 0.9, 3.8, 1.7, 4.5, 1.0, True),
    "cvpr_qualitative": FigureStyle("cvpr_qualitative", 9.4, 0.8, 0.7, 2.8, 1.4, 4.0, 0.8, False),
    "eccv_lowlevel": FigureStyle("eccv_lowlevel", 9.2, 0.9, 0.75, 3.0, 1.5, 4.0, 0.85, True),
    "icml_dense": FigureStyle("icml_dense", 8.8, 0.95, 0.8, 3.0, 1.45, 4.2, 0.85, True),
    "aaai_geo": FigureStyle("aaai_geo", 9.4, 0.9, 0.8, 3.2, 1.55, 4.2, 0.9, True),
    "paper_showcase": FigureStyle("paper_showcase", 9.6, 0.92, 0.78, 3.0, 1.65, 4.4, 0.95, True),
}


AI_SEMANTIC = {
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

AI_SEMANTIC_ORDER = [
    AI_SEMANTIC["blue_main"],
    AI_SEMANTIC["green_3"],
    AI_SEMANTIC["red_strong"],
    AI_SEMANTIC["teal"],
    AI_SEMANTIC["violet"],
    AI_SEMANTIC["neutral"],
    AI_SEMANTIC["blue_secondary"],
    AI_SEMANTIC["green_2"],
]

RL_PASTEL = {
    "MR.Q": {"fill": "#c7deef", "edge": "#1f77b4", "marker": "o"},
    "DreamerV3": {"fill": "#fee0c1", "edge": "#ff7f0e", "marker": "s"},
    "TD-MPC2": {"fill": "#cdeec9", "edge": "#2ca02c", "marker": "^"},
    "PPO": {"fill": "#ffd2cf", "edge": "#d62728", "marker": "P"},
    "TD7": {"fill": "#eadcff", "edge": "#9467bd", "marker": "p"},
    "DrQ-v2": {"fill": "#e8d6d0", "edge": "#8c564b", "marker": "D"},
    "Rainbow": {"fill": "#f6c7e7", "edge": "#e377c2", "marker": "v"},
    "DQN": {"fill": "#d8d8d8", "edge": "#7f7f7f", "marker": "X"},
}

RL_METHOD_ORDER = ["MR.Q", "DreamerV3", "TD-MPC2", "PPO", "TD7", "DrQ-v2", "Rainbow", "DQN"]
RL_PASTEL_FILLS = [RL_PASTEL[name]["fill"] for name in RL_METHOD_ORDER]
RL_PASTEL_EDGES = [RL_PASTEL[name]["edge"] for name in RL_METHOD_ORDER]

SCREENSHOT_PALETTES = [
    {
        "fill": ["#eef3f8", "#e0eff2", "#c0daf0", "#9dabd0"],
        "edge": ["#b9d8f7", "#90b8f1", "#6182cc", "#424d95"],
    },
    {
        "fill": ["#e5f5e0", "#c7e9c0", "#a1d99b", "#74c476"],
        "edge": ["#a1d99b", "#74c476", "#41ab5d", "#238b45"],
    },
    {
        "fill": ["#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a"],
        "edge": ["#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d"],
    },
    {
        "fill": ["#f2f0f7", "#dadaeb", "#bcbddc", "#9e9ac8"],
        "edge": ["#bcbddc", "#9e9ac8", "#807dba", "#6a51a3"],
    },
    {
        "fill": ["#feedde", "#fdd0a2", "#fdae6b", "#fd8d3c"],
        "edge": ["#fdae6b", "#fd8d3c", "#f16913", "#d94801"],
    },
    {
        "fill": ["#f0f0f0", "#d9d9d9", "#bdbdbd", "#969696"],
        "edge": ["#bdbdbd", "#969696", "#737373", "#525252"],
    },
]

OKABE_ITO = [
    "#0072B2",
    "#E69F00",
    "#009E73",
    "#D55E00",
    "#CC79A7",
    "#56B4E9",
    "#F0E442",
    "#000000",
]

JOURNAL_MUTED = [
    "#4C78A8",
    "#F58518",
    "#54A24B",
    "#B279A2",
    "#E45756",
    "#72B7B2",
    "#9D755D",
    "#BAB0AC",
]

NATURE_SOFT = [
    "#9ecae1",
    "#a1d99b",
    "#fdae6b",
    "#bcbddc",
    "#fdd0a2",
    "#bdbdbd",
    "#f2b6c6",
    "#c7e9c0",
]

PALETTES = {
    "rl_pastel": RL_PASTEL_EDGES,
    "ai_semantic": AI_SEMANTIC_ORDER,
    "screenshot": [color for block in SCREENSHOT_PALETTES for color in block["edge"]],
    "soft_edge": SOFT_EDGE_EDGES,
    **WEB_INSPIRED_PALETTES,
    "okabe_ito": OKABE_ITO,
    "journal_muted": JOURNAL_MUTED,
    "nature_soft": NATURE_SOFT,
    **TOP_PAPER_PALETTES,
}


def _optional_palette_adapters() -> dict[str, list[str]]:
    """Expose palette names from optional libraries when they are installed."""

    adapters: dict[str, list[str]] = {}
    try:
        import seaborn as sns  # type: ignore

        for name in ("deep", "muted", "bright", "pastel", "dark", "colorblind"):
            adapters[f"seaborn_{name}"] = [mcolors.to_hex(color) for color in sns.color_palette(name, 8)]
    except Exception:
        pass

    try:
        import cmasher as cmr  # type: ignore

        for name in ("amber", "ember", "fusion", "rainforest", "ocean"):
            cmap = cmr.get_sub_cmap(f"cmr.{name}", 0.08, 0.92)
            adapters[f"cmasher_{name}"] = [mcolors.to_hex(cmap(v)) for v in np.linspace(0.12, 0.88, 8)]
    except Exception:
        pass

    try:
        import colorcet as cc  # type: ignore

        if hasattr(cc, "glasbey"):
            adapters["colorcet_glasbey"] = list(cc.glasbey[:8])
        if hasattr(cc, "fire"):
            cmap = mcolors.LinearSegmentedColormap.from_list("cc_fire", cc.fire)
            adapters["colorcet_fire"] = [mcolors.to_hex(cmap(v)) for v in np.linspace(0.12, 0.88, 8)]
    except Exception:
        pass
    return adapters


PALETTES.update(_optional_palette_adapters())

HATCHES = ["", "//", "\\\\", "..", "xx", "--", "++", "oo"]


def _cycle(values: Sequence[str], n: int) -> list[str]:
    return [values[i % len(values)] for i in range(n)]


def palette(name: str = "ai_semantic", n: int = 6, kind: str = "edge") -> list[str]:
    """Return a deterministic categorical palette."""

    if name in {"screenshot", "soft_edge"}:
        if name == "soft_edge":
            source = SOFT_EDGE_FILLS if kind == "fill" else SOFT_EDGE_EDGES
            colors = source[2::4] or source
            return _cycle(colors, n)
        colors = [color for block in SCREENSHOT_PALETTES for color in block.get(kind, block["edge"])]
    elif name == "rl_pastel":
        colors = RL_PASTEL_FILLS if kind == "fill" else RL_PASTEL_EDGES
    else:
        colors = PALETTES.get(name, PALETTES["ai_semantic"])
    return _cycle(colors, n)


def rl_method_style(method: str, index: int = 0) -> dict[str, str]:
    """Return fill/edge/marker style for a method name."""

    if method in RL_PASTEL:
        return RL_PASTEL[method]
    fill = palette("rl_pastel", index + 1, "fill")[index]
    edge = palette("rl_pastel", index + 1, "edge")[index]
    marker = ["o", "s", "^", "P", "p", "D", "v", "X"][index % 8]
    return {"fill": fill, "edge": edge, "marker": marker}


def blend_with_white(color: str, amount: float = 0.55) -> str:
    rgb = np.array(mcolors.to_rgb(color))
    return mcolors.to_hex(rgb * (1 - amount) + np.ones(3) * amount)


def setup_theme(style: str | FigureStyle = "rl_benchmark") -> FigureStyle:
    """Apply paper-like Matplotlib defaults and return the resolved style."""

    resolved = STYLE_PRESETS.get(style, STYLE_PRESETS["rl_benchmark"]) if isinstance(style, str) else style
    if resolved.name == "rl_benchmark":
        font_fallbacks = [
            "Times New Roman",
            "Times",
            "DejaVu Serif",
            "Noto Serif CJK SC",
            "SimSun",
            "serif",
        ]
        font_family = "serif"
    else:
        font_fallbacks = [
            "Arial",
            "Helvetica",
            "DejaVu Sans",
            "Noto Sans CJK SC",
            "Microsoft YaHei",
            "SimHei",
            "sans-serif",
        ]
        font_family = "sans-serif"
    if not resolved.cjk:
        font_fallbacks = font_fallbacks[:4]

    plt.rcParams.update(
        {
            "figure.dpi": 150,
            "savefig.dpi": 450,
            "savefig.transparent": False,
            "savefig.bbox": "tight",
            "savefig.pad_inches": 0.05,
            "font.family": font_family,
            "font.sans-serif": font_fallbacks,
            "font.serif": font_fallbacks,
            "font.size": resolved.base_font_size,
            "axes.labelsize": resolved.base_font_size,
            "axes.titlesize": resolved.base_font_size + 1,
            "xtick.labelsize": max(resolved.base_font_size - 1, 6),
            "ytick.labelsize": max(resolved.base_font_size - 1, 6),
            "legend.fontsize": max(resolved.base_font_size - 2, 6),
            "axes.linewidth": resolved.axes_linewidth,
            "axes.spines.top": False,
            "axes.spines.right": False,
            "xtick.major.width": resolved.tick_width,
            "ytick.major.width": resolved.tick_width,
            "xtick.major.size": resolved.tick_size,
            "ytick.major.size": resolved.tick_size,
            "lines.linewidth": resolved.line_width,
            "lines.markersize": resolved.marker_size,
            "patch.linewidth": resolved.bar_edge_width,
            "legend.frameon": False,
            "pdf.fonttype": 42,
            "ps.fonttype": 42,
            "svg.fonttype": "none",
            "axes.unicode_minus": False,
        }
    )
    return resolved


def sem(values: Sequence[float]) -> float:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size <= 1:
        return float("nan")
    return float(np.std(arr, ddof=1) / math.sqrt(arr.size))


def describe_groups(data: pd.DataFrame, group: str, value: str) -> pd.DataFrame:
    rows = []
    for name, sub in data.groupby(group, dropna=False):
        vals = pd.to_numeric(sub[value], errors="coerce").dropna().to_numpy()
        rows.append(
            {
                group: name,
                "n": int(vals.size),
                "mean": float(np.mean(vals)) if vals.size else np.nan,
                "sd": float(np.std(vals, ddof=1)) if vals.size > 1 else np.nan,
                "sem": sem(vals),
                "median": float(np.median(vals)) if vals.size else np.nan,
                "q1": float(np.percentile(vals, 25)) if vals.size else np.nan,
                "q3": float(np.percentile(vals, 75)) if vals.size else np.nan,
            }
        )
    return pd.DataFrame(rows)


def compare_oneway(data: pd.DataFrame, group: str, value: str) -> dict[str, object]:
    """Run lightweight one-way checks when SciPy is available."""

    groups = [
        pd.to_numeric(sub[value], errors="coerce").dropna().to_numpy()
        for _, sub in data.groupby(group, dropna=False)
    ]
    groups = [g for g in groups if g.size > 0]
    result: dict[str, object] = {"descriptives": describe_groups(data, group, value)}
    try:
        from scipy import stats
    except Exception as exc:  # pragma: no cover - depends on environment
        result["warning"] = f"SciPy unavailable; skipped inferential tests: {exc}"
        return result

    if len(groups) < 2:
        result["warning"] = "Need at least two nonempty groups for one-way comparison."
        return result

    result["shapiro"] = [
        stats.shapiro(g)._asdict() if 3 <= g.size <= 5000 else {"statistic": np.nan, "pvalue": np.nan}
        for g in groups
    ]
    if all(g.size >= 2 for g in groups):
        result["levene"] = stats.levene(*groups)._asdict()
    result["anova"] = stats.f_oneway(*groups)._asdict()
    result["kruskal"] = stats.kruskal(*groups)._asdict()
    return result


def read_table(path: str | Path) -> pd.DataFrame:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".csv":
        return pd.read_csv(path)
    if suffix in {".tsv", ".tab", ".txt"}:
        return pd.read_csv(path, sep="\t")
    if suffix in {".xlsx", ".xls"}:
        return pd.read_excel(path)
    raise ValueError(f"Unsupported data file extension: {path.suffix}")


def dynamic_ylim(values: Sequence[float], lower_floor: float | None = None, pad_fraction: float = 0.12) -> tuple[float, float]:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return (0.0, 1.0)
    lo = float(arr.min())
    hi = float(arr.max())
    span = hi - lo if hi > lo else max(abs(hi), 1.0)
    lo = lo - span * pad_fraction
    hi = hi + span * pad_fraction
    if lower_floor is not None:
        lo = max(lower_floor, lo)
    return lo, hi


def annotate_bars(ax: plt.Axes, bars, fmt: str = "{:.2f}", fontsize: float | None = None, padding: float = 0.012) -> None:
    """Place value labels above vertical bars."""

    ymin, ymax = ax.get_ylim()
    offset = (ymax - ymin) * padding
    for bar in bars:
        height = bar.get_height()
        if not np.isfinite(height):
            continue
        ax.text(
            bar.get_x() + bar.get_width() / 2,
            height + offset,
            fmt.format(height),
            ha="center",
            va="bottom",
            fontsize=fontsize,
        )


def _finish_axis(ax: plt.Axes, grid: bool = False) -> None:
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    if grid:
        ax.grid(axis="y", color="#E8E8E8", linewidth=0.8, zorder=0)


def _paper_panel_axis(ax: plt.Axes, *, grid: bool = True, face: str = "#F6F6F4") -> None:
    """Apply a stronger top-paper result-panel axis treatment."""

    ax.set_facecolor(face)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.spines["left"].set_color("#B8B8B8")
    ax.spines["bottom"].set_color("#B8B8B8")
    ax.spines["left"].set_linewidth(1.05)
    ax.spines["bottom"].set_linewidth(1.05)
    ax.tick_params(axis="both", width=0.9, length=3.2, pad=2.2, colors="#202020")
    if grid:
        ax.grid(True, color="#DDDDDD", linewidth=0.72, zorder=0)


def _soft_pair(index: int) -> tuple[str, str]:
    return SOFT_EDGE_FILLS[index % len(SOFT_EDGE_FILLS)], SOFT_EDGE_EDGES[index % len(SOFT_EDGE_EDGES)]


def bar_scatter_sem(
    data: pd.DataFrame,
    group: str,
    value: str,
    *,
    ax: plt.Axes | None = None,
    order: Sequence[str] | None = None,
    fill: Sequence[str] | None = None,
    edge: Sequence[str] | None = None,
    ylabel: str | None = None,
    seed: int = 7,
    style: str | FigureStyle = "compact",
) -> plt.Axes:
    """Draw light bars, SEM error bars, and every raw sample."""

    resolved = STYLE_PRESETS.get(style, STYLE_PRESETS["compact"]) if isinstance(style, str) else style
    if ax is None:
        _, ax = plt.subplots(figsize=(3.3, 2.5), layout="constrained")
    order = list(order or pd.unique(data[group].dropna()))
    edges = list(edge or palette("screenshot", len(order), "edge"))
    fills = list(fill or [blend_with_white(c, 0.62) for c in edges])
    rng = np.random.default_rng(seed)
    x = np.arange(len(order))

    means = []
    errors = []
    for label in order:
        vals = pd.to_numeric(data.loc[data[group] == label, value], errors="coerce").dropna().to_numpy()
        means.append(np.mean(vals) if vals.size else np.nan)
        errors.append(sem(vals))

    ax.bar(
        x,
        means,
        yerr=errors,
        width=0.62,
        color=fills,
        edgecolor=edges,
        linewidth=resolved.bar_edge_width,
        error_kw={"ecolor": "#333333", "elinewidth": 0.9, "capsize": 3, "capthick": 0.9},
        zorder=2,
    )
    for i, label in enumerate(order):
        vals = pd.to_numeric(data.loc[data[group] == label, value], errors="coerce").dropna().to_numpy()
        jitter = rng.normal(0, 0.055, size=vals.size)
        ax.scatter(
            np.full(vals.size, i) + jitter,
            vals,
            s=24,
            facecolors="white",
            edgecolors=edges[i],
            linewidths=0.9,
            alpha=0.92,
            zorder=3,
        )

    ax.set_xticks(x, order)
    ax.set_ylabel(ylabel or value)
    _finish_axis(ax, grid=True)
    return ax


def violin_box_points(
    data: pd.DataFrame,
    group: str,
    value: str,
    *,
    ax: plt.Axes | None = None,
    order: Sequence[str] | None = None,
    colors: Sequence[str] | None = None,
    ylabel: str | None = None,
    seed: int = 11,
) -> plt.Axes:
    """Draw a compact horizontal raincloud distribution panel."""

    if ax is None:
        _, ax = plt.subplots(figsize=(4.0, 2.85), layout="constrained")
    order = list(order or pd.unique(data[group].dropna()))
    edge_colors = list(colors or palette("soft_edge", len(order), "edge"))
    fill_colors = palette("soft_edge", len(order), "fill")
    rng = np.random.default_rng(seed)
    values = [
        pd.to_numeric(data.loc[data[group] == label, value], errors="coerce").dropna().to_numpy()
        for label in order
    ]
    positions = np.arange(len(order))[::-1]

    parts = ax.violinplot(values, positions=positions, widths=0.74, vert=False, showmeans=False, showextrema=False, showmedians=False)
    for pos, body, fill_color, edge_color in zip(positions, parts["bodies"], fill_colors, edge_colors):
        for path in body.get_paths():
            vertices = path.vertices
            vertices[:, 1] = np.maximum(vertices[:, 1], pos + 0.045)
        body.set_facecolor(mcolors.to_rgba(fill_color, 0.66))
        body.set_edgecolor(edge_color)
        body.set_linewidth(1.1)
        body.set_zorder(2)

    ax.boxplot(
        values,
        vert=False,
        positions=positions - 0.01,
        widths=0.17,
        patch_artist=True,
        showfliers=False,
        medianprops={"color": "#1F2937", "linewidth": 1.35},
        boxprops={"facecolor": mcolors.to_rgba("white", 0.88), "edgecolor": "#2F2F2F", "linewidth": 0.95},
        whiskerprops={"color": "#2F2F2F", "linewidth": 0.9},
        capprops={"color": "#2F2F2F", "linewidth": 0.9},
    )
    for i, (pos, vals) in enumerate(zip(positions, values)):
        jitter = rng.normal(0, 0.035, size=vals.size)
        ax.scatter(
            vals,
            np.full(vals.size, pos - 0.25) + jitter,
            s=20,
            facecolors="white",
            edgecolors=edge_colors[i],
            linewidths=0.74,
            alpha=0.95,
            zorder=4,
        )
        if vals.size:
            mean_val = float(np.mean(vals))
            ax.scatter(
                [mean_val],
                [pos - 0.01],
                marker="D",
                s=27,
                facecolors=fill_colors[i],
                edgecolors="#111111",
                linewidths=0.78,
                zorder=5,
            )

    ax.set_yticks(positions, order)
    ax.set_xlabel(ylabel or value)
    ax.set_ylabel("")
    finite_values = [v for v in values if v.size]
    if finite_values:
        xlim = dynamic_ylim(np.concatenate(finite_values), pad_fraction=0.10)
        ax.set_xlim(xlim)
        span = xlim[1] - xlim[0]
        for pos, vals in zip(positions, values):
            if vals.size:
                ax.text(
                    xlim[1] - span * 0.018,
                    pos + 0.24,
                    f"n={vals.size}",
                    ha="right",
                    va="center",
                    fontsize=6.8,
                    color="#6B7280",
                )
    ax.set_ylim(float(np.min(positions)) - 0.58, float(np.max(positions)) + 0.58)
    _paper_panel_axis(ax, grid=False, face="#FBFBFA")
    ax.grid(axis="x", color="#E5E5E5", linewidth=0.72, zorder=0)
    ax.grid(axis="y", visible=False)
    return ax


def grouped_bar(
    ax: plt.Axes,
    categories: Sequence[str],
    series: Sequence[Sequence[float]],
    labels: Sequence[str],
    *,
    ylabel: str = "Value",
    colors: Sequence[str] | None = None,
    annotate: bool = False,
    hatches: Sequence[str] | None = None,
    hide_xticks: bool = False,
    style: FigureStyle | None = None,
) -> list:
    """Render grouped benchmark bars for multi-metric comparisons."""

    style = style or STYLE_PRESETS["ai_conference"]
    arr = np.asarray(series, dtype=float)
    if arr.ndim != 2:
        raise ValueError("series must be a 2D array-like object: n_series x n_categories.")
    if arr.shape[1] != len(categories):
        raise ValueError("Each series must have the same length as categories.")
    if arr.shape[0] != len(labels):
        raise ValueError("labels length must match number of series.")

    n_series, n_categories = arr.shape
    colors = list(colors or palette("ai_semantic", n_series))
    hatches = list(hatches or _cycle(HATCHES, n_series))
    x = np.arange(n_categories)
    width = min(0.78 / n_series, 0.16)
    offset = (np.arange(n_series) - (n_series - 1) / 2) * width
    containers = []

    for idx, label in enumerate(labels):
        bars = ax.bar(
            x + offset[idx],
            arr[idx],
            width=width,
            label=label,
            color=colors[idx],
            edgecolor="black",
            linewidth=style.bar_edge_width,
            hatch=hatches[idx],
            zorder=3,
        )
        containers.append(bars)
        if annotate:
            annotate_bars(ax, bars, fmt="{:.2f}", fontsize=max(style.base_font_size - 5, 7))

    ax.set_ylabel(ylabel)
    if hide_xticks:
        ax.set_xticks([])
    else:
        ax.set_xticks(x, categories)
    ax.set_ylim(dynamic_ylim(arr.ravel(), lower_floor=0.0))
    _finish_axis(ax, grid=False)
    return containers


def leaderboard_bar(
    ax: plt.Axes,
    labels: Sequence[str],
    values: Sequence[float],
    *,
    ylabel: str = "Score",
    colors: Sequence[str] | None = None,
    annotate: bool = True,
    sort: bool = True,
    style: FigureStyle | None = None,
) -> None:
    """Draw a sorted single-metric benchmark bar chart with direct labels."""

    style = style or STYLE_PRESETS["ai_conference"]
    vals = np.asarray(values, dtype=float)
    order = np.argsort(vals)[::-1] if sort else np.arange(len(vals))
    vals = vals[order]
    labels = [labels[i] for i in order]
    colors = list(colors or [AI_SEMANTIC["blue_main"]] + [AI_SEMANTIC["red_2"]] * max(len(vals) - 1, 0))
    colors = [colors[i % len(colors)] for i in order]
    x = np.arange(len(vals))
    bars = ax.bar(x, vals, color=_cycle(colors, len(vals)), edgecolor="black", linewidth=style.bar_edge_width, zorder=3)
    if annotate:
        annotate_bars(ax, bars, fmt="{:.2f}", fontsize=max(style.base_font_size - 4, 8))
    ax.set_xticks(x, labels, rotation=25, ha="right")
    ax.set_ylabel(ylabel)
    ax.set_ylim(dynamic_ylim(vals, lower_floor=0.0, pad_fraction=0.16))
    _finish_axis(ax, grid=False)


def composition_bar(
    ax: plt.Axes,
    categories: Sequence[str],
    components: Sequence[Sequence[float]],
    labels: Sequence[str],
    *,
    ylabel: str = "Composition",
    normalize: bool = True,
    colors: Sequence[str] | None = None,
    style: FigureStyle | None = None,
) -> None:
    """Draw stacked composition bars."""

    style = style or STYLE_PRESETS["ai_conference"]
    arr = np.asarray(components, dtype=float)
    if arr.ndim != 2:
        raise ValueError("components must be n_components x n_categories.")
    if arr.shape[1] != len(categories):
        raise ValueError("Each component must have the same length as categories.")
    if normalize:
        totals = arr.sum(axis=0)
        totals[totals == 0] = 1
        arr = arr / totals
    colors = list(colors or palette("ai_semantic", arr.shape[0]))
    bottom = np.zeros(arr.shape[1])
    x = np.arange(arr.shape[1])
    for idx, label in enumerate(labels):
        ax.bar(
            x,
            arr[idx],
            bottom=bottom,
            label=label,
            color=colors[idx],
            edgecolor="black",
            linewidth=style.bar_edge_width * 0.75,
            zorder=3,
        )
        bottom += arr[idx]
    ax.set_xticks(x, categories)
    ax.set_ylabel(ylabel)
    ax.set_ylim(0, 1.0 if normalize else max(bottom) * 1.08)
    _finish_axis(ax, grid=False)


def _rl_panel_base(ax: plt.Axes) -> None:
    ax.set_facecolor("#F1F1F1")
    ax.grid(axis="y", color="#D9D9D9", linewidth=0.55, zorder=0)
    ax.grid(axis="x", color="#E0E0E0", linewidth=0.5, zorder=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    ax.tick_params(axis="both", width=0.55, length=2.2, pad=1.5)


def _rl_panel_title(ax: plt.Axes, title: str, subtitle: str | None = None) -> None:
    ax.set_title("")
    ax.text(
        0.5,
        1.13,
        title,
        transform=ax.transAxes,
        ha="center",
        va="bottom",
        fontsize=8.2,
        color="black",
        clip_on=False,
    )
    if subtitle:
        ax.text(
            0.5,
            1.055,
            subtitle,
            transform=ax.transAxes,
            ha="center",
            va="bottom",
            fontsize=7.0,
            color="#777777",
        )


def rl_vertical_bar_panel(
    ax: plt.Axes,
    methods: Sequence[str],
    values: Sequence[float],
    *,
    errors: Sequence[float] | None = None,
    title: str = "",
    subtitle: str | None = None,
    ylabel: str = "",
    ylim: tuple[float, float] | None = None,
    show_ylabel: bool = True,
    show_method_labels: bool = True,
) -> None:
    """Reference-style vertical benchmark bars with in-bar labels."""

    _rl_panel_base(ax)
    vals = np.asarray(values, dtype=float)
    errs = np.zeros_like(vals) if errors is None else np.asarray(errors, dtype=float)
    x = np.arange(len(methods))
    fills = [rl_method_style(method, i)["fill"] for i, method in enumerate(methods)]
    edges = [rl_method_style(method, i)["edge"] for i, method in enumerate(methods)]
    bars = ax.bar(
        x,
        vals,
        width=0.68,
        color=fills,
        edgecolor=edges,
        linewidth=0.8,
        yerr=errs,
        error_kw={"elinewidth": 0.75, "capsize": 2.2, "capthick": 0.75},
        zorder=3,
    )
    yrange = ylim if ylim is not None else dynamic_ylim(vals + errs, lower_floor=0.0, pad_fraction=0.18)
    if ylim is None and np.nanmin(vals) >= 0:
        yrange = (0.0, yrange[1])
    if show_method_labels:
        ymin, ymax = yrange
        yspan = ymax - ymin
        label_y = ymin + yspan * 0.07
        for method, bar, err in zip(methods, bars, errs):
            value = float(bar.get_height())
            label_span = yspan * max(0.17, min(0.48, len(method) * 0.055))
            is_short_bar = (value - ymin) < label_span
            if is_short_bar:
                text_y = min(value + float(err) + yspan * 0.025, ymax - yspan * 0.08)
                fontsize = 5.7 if len(method) > 5 else 6.2
                rotation = 0
                ha = "center"
                va = "bottom"
            else:
                text_y = label_y
                fontsize = 5.9 if len(method) > 5 else 6.8
                rotation = 90
                ha = "center"
                va = "bottom"
            ax.text(
                bar.get_x() + bar.get_width() / 2,
                text_y,
                method,
                rotation=rotation,
                ha=ha,
                va=va,
                fontsize=fontsize,
                color="black",
                zorder=4,
                clip_on=False,
            )
    ax.set_xticks([])
    ax.set_ylabel(ylabel if show_ylabel else "")
    ax.set_ylim(yrange)
    _rl_panel_title(ax, title, subtitle)
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))


def rl_horizontal_resource_panel(
    ax: plt.Axes,
    methods: Sequence[str],
    values: Sequence[float],
    *,
    display_values: Sequence[str] | None = None,
    title: str = "",
    subtitle: str | None = None,
    xlabel: str = "",
    xlim: tuple[float, float] | None = None,
) -> None:
    """Reference-style horizontal bars for parameters/FPS/cost resources."""

    _rl_panel_base(ax)
    vals = np.asarray(values, dtype=float)
    y = np.arange(len(methods))[::-1]
    fills = [rl_method_style(method, i)["fill"] for i, method in enumerate(methods)]
    edges = [rl_method_style(method, i)["edge"] for i, method in enumerate(methods)]
    ax.barh(y, vals, height=0.58, color=fills, edgecolor=edges, linewidth=0.75, zorder=3)
    right = xlim[1] if xlim is not None else max(float(np.nanmax(vals)) * 1.12, 1.0)
    ax.set_xlim(xlim or (0, right))
    display_values = list(display_values or [f"{value:g}" for value in vals])
    for yy, method, value, text in zip(y, methods, vals, display_values):
        small_bar = float(value) < right * 0.18
        method_x = min(float(value) + right * 0.035, right * 0.78) if small_bar else right * 0.05
        ax.text(
            method_x,
            yy,
            method,
            ha="left",
            va="center",
            fontsize=7.0,
            color="black",
            zorder=4,
        )
        ax.annotate(
            f"({text})",
            xy=(method_x, yy),
            xytext=(len(method) * 4.1 + 3.0, 0),
            textcoords="offset points",
            ha="left",
            va="center",
            fontsize=6.8,
            color="#808080",
            clip_on=False,
            zorder=4,
        )
    ax.set_yticks([])
    ax.set_xlabel(xlabel)
    _rl_panel_title(ax, title, subtitle)
    ax.xaxis.set_major_locator(MaxNLocator(nbins=5))


def rl_shared_legend(
    ax: plt.Axes,
    methods: Sequence[str],
    *,
    ncol: int | None = None,
    kind: str = "bar",
) -> None:
    """Bottom strip legend with RL benchmark colors.

    Use square patches for bar grids and marker handles for line/curve figures.
    """

    ax.set_axis_off()
    handles = []
    for idx, method in enumerate(methods):
        style = rl_method_style(method, idx)
        if kind == "marker":
            handles.append(
                plt.Line2D(
                    [0],
                    [0],
                    marker=style["marker"],
                    linestyle="",
                    markerfacecolor=style["fill"],
                    markeredgecolor=style["edge"],
                    markeredgewidth=0.8,
                    markersize=5.0,
                    label=method,
                )
            )
        else:
            handles.append(
                Patch(
                    facecolor=style["fill"],
                    edgecolor=style["edge"],
                    linewidth=0.85,
                    label=method,
                )
            )
    ax.legend(
        handles=handles,
        loc="center",
        ncol=ncol or min(len(methods), 8),
        frameon=True,
        fancybox=False,
        facecolor="#F1F1F1",
        edgecolor="none",
        columnspacing=0.9,
        handlelength=0.9,
        handleheight=0.8,
        handletextpad=0.4,
        fontsize=7.6,
    )


def rl_benchmark_grid(
    panels: Sequence[dict[str, object]],
    *,
    methods_for_legend: Sequence[str] | None = None,
    include_legend: bool = True,
    legend_kind: str = "bar",
) -> plt.Figure:
    """Build a mixed 2-row RL benchmark grid from panel dictionaries."""

    n_panels = len(panels)
    ncols = max(1, math.ceil(n_panels / 2))
    height = 4.15 if include_legend else 3.85
    fig = plt.figure(figsize=(2.28 * ncols, height), layout=None)
    row_heights = [1.0, 1.0, 0.18] if include_legend else [1.0, 1.0]
    gs = fig.add_gridspec(
        3 if include_legend else 2,
        ncols,
        height_ratios=row_heights,
        left=0.058,
        right=0.992,
        top=0.875,
        bottom=0.055 if include_legend else 0.095,
        wspace=0.32,
        hspace=0.60,
    )
    all_methods: list[str] = []

    for idx, panel in enumerate(panels):
        row = 0 if idx < ncols else 1
        col = idx if row == 0 else idx - ncols
        ax = fig.add_subplot(gs[row, col])
        methods = list(panel["methods"])  # type: ignore[index]
        all_methods.extend([method for method in methods if method not in all_methods])
        values = panel["values"]  # type: ignore[index]
        orientation = str(panel.get("orientation", "vertical"))
        if orientation == "horizontal":
            rl_horizontal_resource_panel(
                ax,
                methods,
                values,  # type: ignore[arg-type]
                display_values=panel.get("display_values"),  # type: ignore[arg-type]
                title=str(panel.get("title", "")),
                subtitle=panel.get("subtitle"),  # type: ignore[arg-type]
                xlabel=str(panel.get("xlabel", "")),
                xlim=panel.get("xlim"),  # type: ignore[arg-type]
            )
        else:
            rl_vertical_bar_panel(
                ax,
                methods,
                values,  # type: ignore[arg-type]
                errors=panel.get("errors"),  # type: ignore[arg-type]
                title=str(panel.get("title", "")),
                subtitle=panel.get("subtitle"),  # type: ignore[arg-type]
                ylabel=str(panel.get("ylabel", "")),
                ylim=panel.get("ylim"),  # type: ignore[arg-type]
                show_ylabel=bool(panel.get("show_ylabel", True)),
            )

    if include_legend:
        legend_ax = fig.add_subplot(gs[2, :])
        rl_shared_legend(legend_ax, list(methods_for_legend or all_methods), kind=legend_kind)
    return fig


def line_ci(
    data: pd.DataFrame,
    x: str,
    y: str,
    *,
    group: str | None = None,
    ax: plt.Axes | None = None,
    colors: Sequence[str] | None = None,
    ylabel: str | None = None,
    xlabel: str | None = None,
    ci: float = 1.96,
) -> plt.Axes:
    if ax is None:
        _, ax = plt.subplots(figsize=(4.4, 2.8), layout="constrained")
    groups: list[tuple[str, pd.DataFrame]]
    if group:
        groups = list(data.groupby(group, dropna=False))
    else:
        groups = [("", data)]
    colors = list(colors or palette("soft_edge", len(groups), "edge"))
    fills = palette("soft_edge", len(groups), "fill")
    markers = ["o", "s", "^", "D", "P", "v", "X", "p"]

    endpoints: list[tuple[float, float, str, str]] = []
    for idx, (color, (label, sub)) in enumerate(zip(colors, groups)):
        summary = (
            sub.groupby(x, dropna=False)[y]
            .agg(mean="mean", sem=sem, n="count")
            .reset_index()
            .sort_values(x)
        )
        xs = pd.to_numeric(summary[x], errors="coerce").to_numpy()
        means = summary["mean"].to_numpy(dtype=float)
        errors = summary["sem"].to_numpy(dtype=float) * ci
        label_text = str(label) if group else None
        ax.fill_between(xs, means - errors, means + errors, color=mcolors.to_rgba(fills[idx], 0.52), linewidth=0, zorder=1)
        ax.plot(
            xs,
            means,
            marker=markers[idx % len(markers)],
            markersize=5.6,
            markerfacecolor=fills[idx],
            markeredgecolor=color,
            markeredgewidth=0.95,
            color=color,
            linewidth=2.15,
            label=label_text,
            zorder=3,
        )
        if xs.size:
            endpoints.append((float(xs[-1]), float(means[-1]), str(label), color))

    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    if group:
        xmin, xmax = ax.get_xlim()
        ax.set_xlim(xmin, xmax + (xmax - xmin) * 0.18)
        endpoints_sorted = sorted(endpoints, key=lambda item: item[1])
        min_gap = max((ax.get_ylim()[1] - ax.get_ylim()[0]) * 0.075, 1e-6)
        adjusted: list[tuple[float, float, str, str]] = []
        last_y = -np.inf
        for ex, ey, label, color in endpoints_sorted:
            y_adj = max(ey, last_y + min_gap)
            adjusted.append((ex, y_adj, label, color))
            last_y = y_adj
        ymin, ymax = ax.get_ylim()
        if adjusted and adjusted[-1][1] > ymax:
            ax.set_ylim(ymin, adjusted[-1][1] + min_gap)
        for ex, ey, label, color in adjusted:
            ax.annotate(
                label,
                (ex, ey),
                xytext=(7, 0),
                textcoords="offset points",
                ha="left",
                va="center",
                fontsize=7.6,
                color=color,
                fontweight="bold",
                clip_on=False,
            )
        ax.legend(loc="upper center", bbox_to_anchor=(0.5, -0.18), frameon=False, ncol=min(len(groups), 5), handlelength=1.7, columnspacing=1.2)
    _paper_panel_axis(ax, grid=True)
    return ax


def scatter_regression(
    data: pd.DataFrame,
    x: str,
    y: str,
    *,
    ax: plt.Axes | None = None,
    color: str = AI_SEMANTIC["blue_main"],
    xlabel: str | None = None,
    ylabel: str | None = None,
) -> plt.Axes:
    if ax is None:
        _, ax = plt.subplots(figsize=(4.0, 2.9), layout="constrained")
    xs = pd.to_numeric(data[x], errors="coerce").to_numpy()
    ys = pd.to_numeric(data[y], errors="coerce").to_numpy()
    mask = np.isfinite(xs) & np.isfinite(ys)
    xs = xs[mask]
    ys = ys[mask]

    fill = blend_with_white(color, 0.56)
    ax.scatter(xs, ys, s=76, facecolors=fill, edgecolors=color, linewidths=1.2, alpha=0.93, zorder=3)
    if xs.size >= 2:
        slope, intercept = np.polyfit(xs, ys, deg=1)
        line_x = np.linspace(xs.min(), xs.max(), 100)
        line_y = slope * line_x + intercept
        resid_std = float(np.std(ys - (slope * xs + intercept)))
        ax.plot(line_x, line_y, color="#222222", linewidth=1.55, alpha=0.72, zorder=2)
        ax.fill_between(line_x, line_y - resid_std, line_y + resid_std, color="#BDBDBD", alpha=0.15, linewidth=0)
        best = int(np.nanargmax(ys - 0.07 * xs))
        ax.scatter([xs[best]], [ys[best]], s=118, facecolors="#FFF7BC", edgecolors="#B64342", linewidths=1.5, zorder=4)
        ax.annotate(
            "highlight",
            (xs[best], ys[best]),
            xytext=(6, 5),
            textcoords="offset points",
            fontsize=7.5,
            color="#B64342",
            fontweight="bold",
        )
        ax.text(
            0.98,
            0.05,
            f"trend slope {slope:.2f}",
            transform=ax.transAxes,
            ha="right",
            va="bottom",
            fontsize=7.0,
            color="#4B5563",
        )
    ax.set_xlabel(xlabel or x)
    ax.set_ylabel(ylabel or y)
    _paper_panel_axis(ax, grid=True)
    return ax


def heatmap(
    matrix: np.ndarray | pd.DataFrame,
    *,
    ax: plt.Axes | None = None,
    cmap: str = "YlGnBu",
    colorbar_label: str = "Value",
    row_labels: Sequence[str] | None = None,
    col_labels: Sequence[str] | None = None,
    annotate: bool = False,
) -> plt.Axes:
    if ax is None:
        _, ax = plt.subplots(figsize=(3.7, 3.05), layout="constrained")
    if isinstance(matrix, pd.DataFrame):
        row_labels = list(matrix.index.astype(str)) if row_labels is None else row_labels
        col_labels = list(matrix.columns.astype(str)) if col_labels is None else col_labels
        matrix = matrix.to_numpy()

    arr = np.asarray(matrix, dtype=float)
    im = ax.imshow(arr, cmap=cmap, aspect="auto")
    if row_labels is not None:
        ax.set_yticks(np.arange(len(row_labels)), row_labels)
    if col_labels is not None:
        ax.set_xticks(np.arange(len(col_labels)), col_labels, rotation=35, ha="right")
    should_annotate = annotate or arr.size <= 64
    if should_annotate:
        cmap_obj = plt.get_cmap(cmap)
        norm = mcolors.Normalize(vmin=float(np.nanmin(arr)), vmax=float(np.nanmax(arr)))
        for i in range(arr.shape[0]):
            for j in range(arr.shape[1]):
                val = arr[i, j]
                rgb = np.asarray(cmap_obj(norm(val))[:3])
                luminance = float(np.dot(rgb, [0.2126, 0.7152, 0.0722]))
                color = "white" if luminance < 0.48 else "#202020"
                ax.text(j, i, f"{val:.2f}", ha="center", va="center", fontsize=7.3, color=color)
    ax.set_xticks(np.arange(arr.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(arr.shape[0] + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="white", linewidth=1.05)
    ax.tick_params(which="minor", bottom=False, left=False)
    cbar = ax.figure.colorbar(im, ax=ax, fraction=0.044, pad=0.025)
    cbar.set_label(colorbar_label)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    return ax


def radar_plot(
    ax: plt.Axes,
    categories: Sequence[str],
    series: Sequence[Sequence[float]],
    labels: Sequence[str],
    *,
    colors: Sequence[str] | None = None,
    fill_alpha: float = 0.14,
) -> None:
    """Draw radar/spider comparison on a polar axis."""

    arr = np.asarray(series, dtype=float)
    if arr.ndim != 2 or arr.shape[1] != len(categories):
        raise ValueError("series must be n_series x n_categories.")
    colors = list(colors or palette("ai_semantic", arr.shape[0]))
    angles = np.linspace(0, 2 * np.pi, len(categories), endpoint=False)
    angles = np.r_[angles, angles[0]]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    for idx, label in enumerate(labels):
        vals = np.r_[arr[idx], arr[idx][0]]
        ax.plot(angles, vals, color=colors[idx], label=label, linewidth=2.2)
        ax.fill(angles, vals, color=mcolors.to_rgba(colors[idx], fill_alpha), linewidth=0)
    ax.set_xticks(angles[:-1], categories)
    ax.set_ylim(0, max(1.0, float(np.nanmax(arr)) * 1.08))
    ax.grid(color="#BFBFBF", linestyle="--", linewidth=0.8)
    ax.legend(loc="upper right", bbox_to_anchor=(1.23, 1.13))


def radial_ridge_plot(
    ax: plt.Axes,
    categories: Sequence[str],
    series: Sequence[Sequence[float]],
    labels: Sequence[str],
    *,
    colors: Sequence[str] | None = None,
    inner_radius: float = 0.42,
    ridge_height: float = 0.24,
) -> None:
    """Draw a polar radial ridgeline plot for cyclic/category distributions."""

    arr = np.asarray(series, dtype=float)
    if arr.ndim != 2 or arr.shape[1] != len(categories):
        raise ValueError("series must be n_series x n_categories.")
    arr = np.nan_to_num(arr, nan=0.0)
    max_val = max(float(np.nanmax(arr)), 1e-9)
    norm = arr / max_val
    colors = list(colors or palette("soft_edge", arr.shape[0], "edge"))
    fills = palette("soft_edge", arr.shape[0], "fill")
    n = len(categories)
    theta = np.linspace(0, 2 * np.pi, n, endpoint=False)
    theta_closed = np.r_[theta, theta[0]]

    ax.set_theta_offset(np.pi / 2)
    ax.set_theta_direction(-1)
    for idx, label in enumerate(labels):
        base = inner_radius + idx * ridge_height * 1.18
        smooth = norm[idx]
        smooth = (np.roll(smooth, 1) + 2 * smooth + np.roll(smooth, -1)) / 4
        ridge = base + ridge_height * np.r_[smooth, smooth[0]]
        base_line = np.full_like(theta_closed, base)
        ax.fill_between(theta_closed, base_line, ridge, color=mcolors.to_rgba(fills[idx], 0.72), linewidth=0)
        ax.plot(theta_closed, ridge, color=colors[idx], linewidth=1.75, label=label)
        peak = int(np.nanargmax(arr[idx]))
        ax.scatter([theta[peak]], [ridge[:-1][peak]], s=18, color=colors[idx], edgecolor="white", linewidth=0.55, zorder=4)
        ax.text(theta[peak], ridge[:-1][peak] + 0.04, f"{arr[idx][peak]:.1f}", fontsize=6.8, ha="center", va="center", color=colors[idx])

    ax.set_xticks(theta, categories)
    ax.set_yticks([])
    ax.spines["polar"].set_visible(False)
    ax.grid(color="#D6D6D6", linestyle="--", linewidth=0.7)
    ax.legend(loc="center left", bbox_to_anchor=(1.05, 0.62), frameon=False, fontsize=8)


def sensitivity3d_plot(
    ax: plt.Axes,
    x: Sequence[float],
    layers: Sequence[float],
    z_matrix: Sequence[Sequence[float]],
    *,
    cmap: str = "viridis",
    line_color: str = "#263238",
    marker_values: Sequence[tuple[float, float, float]] | None = None,
) -> None:
    """Draw filled 3D sensitivity curves using Matplotlib PolyCollection."""

    xs = np.asarray(x, dtype=float)
    ys = np.asarray(layers, dtype=float)
    z = np.asarray(z_matrix, dtype=float)
    if z.shape != (len(ys), len(xs)):
        raise ValueError("z_matrix must have shape len(layers) x len(x).")

    norm = mcolors.Normalize(vmin=float(np.nanmin(ys)), vmax=float(np.nanmax(ys)))
    cmap_obj = plt.get_cmap(cmap)
    verts = []
    facecolors = []
    for layer, row in zip(ys, z):
        verts.append(list(zip(xs, row)) + [(xs[-1], 0), (xs[0], 0)])
        facecolors.append(mcolors.to_rgba(cmap_obj(norm(layer)), 0.28))
    poly = PolyCollection(verts, facecolors=facecolors, edgecolors=line_color, linewidths=1.2)
    ax.add_collection3d(poly, zs=ys, zdir="y")
    for layer, row in zip(ys, z):
        ax.plot(xs, np.full_like(xs, layer), row, color=line_color, linewidth=1.1, alpha=0.72)

    if marker_values:
        mx, my, mz = zip(*marker_values)
        ax.plot(mx, my, mz, color="black", linestyle="--", linewidth=1.1, marker="o", markersize=4)
        for xx, yy, zz in marker_values:
            ax.text(xx, yy, zz + 0.03, f"{zz:.2f}", fontsize=8, ha="center")

    ax.set_xlim(float(xs.min()), float(xs.max()))
    ax.set_ylim(float(ys.min()), float(ys.max()))
    ax.set_zlim(0, max(1.0, float(np.nanmax(z)) * 1.08))
    ax.set_xlabel("Round", labelpad=8)
    ax.set_ylabel("A1", labelpad=8)
    ax.set_zlabel("Cooperation Rate", labelpad=8)
    ax.view_init(elev=24, azim=-62)
    mappable = plt.cm.ScalarMappable(norm=norm, cmap=cmap_obj)
    mappable.set_array([])
    ax.figure.colorbar(mappable, ax=ax, shrink=0.58, pad=0.08)


def add_panel_letters(axes: Iterable[plt.Axes], letters: str = "abcdefghijklmnopqrstuvwxyz", fontsize: float = 18) -> None:
    for ax, letter in zip(axes, letters):
        ax.text(
            -0.12,
            1.06,
            letter,
            transform=ax.transAxes,
            fontsize=fontsize,
            fontweight="bold",
            va="bottom",
            ha="left",
        )


def add_legend_panel(ax: plt.Axes, labels: Sequence[str], colors: Sequence[str], title: str | None = None) -> None:
    ax.set_axis_off()
    handles = [Patch(facecolor=color, edgecolor="black", label=label) for label, color in zip(labels, colors)]
    ax.legend(handles=handles, loc="center left", title=title, frameon=False)


def save_figure(
    fig: plt.Figure,
    output_base: str | Path,
    *,
    formats: Sequence[str] = ("pdf", "svg", "png"),
    dpi: int = 450,
) -> list[Path]:
    """Save a figure and perform a lightweight nonblank check on PNG output."""

    base = Path(output_base)
    base.parent.mkdir(parents=True, exist_ok=True)
    metadata = {"Creator": "paper-python-plots"}
    paths = []
    fig.canvas.draw()
    for ext in formats:
        ext = ext.lower().lstrip(".")
        path = base.with_suffix(f".{ext}")
        kwargs = {"dpi": dpi}
        if ext in {"pdf", "png", "svg"}:
            kwargs["metadata"] = metadata
        fig.savefig(path, **kwargs)
        if path.stat().st_size < 1024:
            raise RuntimeError(f"Export looks too small and may be blank: {path}")
        paths.append(path)

    pngs = [p for p in paths if p.suffix.lower() == ".png"]
    for png in pngs:
        arr = mpimg.imread(png)
        if arr.size == 0 or float(np.nanstd(arr)) < 1e-5:
            raise RuntimeError(f"PNG export appears blank: {png}")
    return paths


def _demo_grouped(seed: int = 42) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    for i, label in enumerate(["Control", "Low", "Medium", "High"]):
        loc = [1.0, 1.25, 1.55, 1.9][i]
        scale = [0.28, 0.30, 0.34, 0.38][i]
        vals = rng.normal(loc, scale, 18)
        rows.extend({"group": label, "response": value} for value in vals)
    return pd.DataFrame(rows)


def _demo_distribution(seed: int = 66) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    specs = [
        ("Control", np.r_[rng.normal(0.92, 0.10, 16), rng.normal(1.18, 0.08, 8)]),
        ("Variant A", np.r_[rng.gamma(3.2, 0.12, 18) + 0.86, rng.normal(1.58, 0.09, 6)]),
        ("Variant B", np.r_[rng.normal(1.18, 0.08, 10), rng.normal(1.72, 0.11, 14), [2.08]]),
        ("Ours", np.r_[rng.normal(1.78, 0.12, 16), rng.normal(2.18, 0.13, 10), [2.55]]),
    ]
    rows = []
    for label, vals in specs:
        rows.extend({"group": label, "response": float(v)} for v in vals)
    return pd.DataFrame(rows)


def _demo_time(seed: int = 8) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    rows = []
    methods = [
        ("MR.Q", 0.88, 0.52),
        ("DreamerV3", 0.72, 0.40),
        ("TD-MPC2", 0.80, 0.45),
        ("TD7", 0.92, 0.48),
        ("PPO", 0.46, 0.20),
    ]
    for treatment, boost, speed in methods:
        for day in range(7):
            center = 0.20 + boost * (1 - math.exp(-day * speed)) + 0.035 * day
            for _ in range(10):
                rows.append({"day": day, "signal": rng.normal(center, 0.045 + 0.012 * day), "condition": treatment})
    return pd.DataFrame(rows)


def _demo_scatter(seed: int = 21) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    x = rng.uniform(0.2, 4.8, 48)
    y = 0.9 * x + rng.normal(0, 0.55, size=x.size) + 1.2
    return pd.DataFrame({"dose": x, "activity": y})


def _demo_heatmap(seed: int = 4) -> pd.DataFrame:
    rng = np.random.default_rng(seed)
    base = rng.normal(0, 0.25, (7, 7))
    trend = np.outer(np.linspace(-1, 1, 7), np.linspace(1, -1, 7))
    mat = base + trend
    labels = [f"G{i}" for i in range(1, 8)]
    return pd.DataFrame(mat, index=labels, columns=labels)


def _demo_ai_bars() -> tuple[list[str], list[str], np.ndarray]:
    metrics = ["AUROC", "AUPRC", "Mean PPVn"]
    methods = [
        "Prime-2.1",
        "NetMHCpan",
        "MHCnuggets",
        "MHCflurry",
        "DeepNeo",
        "BigMHC-EL",
        "BigMHC-IM",
        "ImmunoStruct",
    ]
    values = np.array(
        [
            [0.535, 0.215, 0.205],
            [0.540, 0.220, 0.225],
            [0.545, 0.245, 0.235],
            [0.575, 0.255, 0.275],
            [0.765, 0.438, 0.410],
            [0.590, 0.275, 0.290],
            [0.685, 0.460, 0.335],
            [0.790, 0.695, 0.445],
        ]
    )
    return metrics, methods, values


def _demo_radial() -> tuple[list[str], list[str], np.ndarray]:
    categories = ["DD", "CO", "MCNO", "CB", "OV", "DB", "RD"]
    labels = ["Test", "Train", "Total"]
    values = np.array(
        [
            [46.1, 20.0, 26.3, 23.0, 23.8, 15.2, 17.1],
            [48.9, 23.5, 9.4, 36.1, 23.6, 15.4, 17.1],
            [57.1, 14.5, 24.1, 32.3, 23.6, 14.8, 17.1],
        ]
    )
    return categories, labels, values


def _demo_sensitivity() -> tuple[np.ndarray, np.ndarray, np.ndarray, list[tuple[float, float, float]]]:
    x = np.arange(0, 15, 1)
    layers = np.arange(1, 7)
    z_rows = []
    for layer in layers:
        baseline = 0.14 + 0.11 * layer
        wave = 0.18 * np.sin((x + layer) / 2.2)
        ramp = 0.045 * x
        z_rows.append(np.clip(baseline + wave + ramp, 0, 1))
    z = np.asarray(z_rows)
    markers = [(0, 1, z[0, 0]), (3, 2, z[1, 3]), (7, 3, z[2, 7]), (10, 5, z[4, 10]), (14, 6, z[5, 14])]
    return x, layers, z, markers


def demo_sem_palette_showcase() -> plt.Figure:
    """Show the accepted raw-points+SEM style across major soft-edge color families."""

    selections = [
        ("Blue", 0),
        ("Green", 1),
        ("Red", 2),
        ("Purple", 3),
        ("Orange", 4),
        ("Teal", 6),
        ("Pink", 7),
        ("Gray", 5),
    ]
    fig, axes = plt.subplots(2, 4, figsize=(9.7, 4.6), layout="constrained")
    for ax, (label, block_idx) in zip(axes.flat, selections):
        block = SOFT_EDGE_PALETTES[block_idx]
        data = _demo_grouped(seed=90 + block_idx)
        bar_scatter_sem(
            data,
            "group",
            "response",
            ax=ax,
            ylabel="Response" if block_idx in {0, 4} else "",
            fill=block["fill"],
            edge=block["edge"],
            style="compact",
            seed=30 + block_idx,
        )
        ax.set_title(label, fontsize=8.2, pad=5, color=block["edge"][-1], fontweight="bold")
        ax.tick_params(axis="x", labelrotation=28, labelsize=6.7)
        ax.tick_params(axis="y", labelsize=6.8)
        if block_idx not in {0, 4}:
            ax.set_ylabel("")
    fig.suptitle("Raw Points + SEM Palette Families", fontsize=11.2, fontweight="bold")
    return fig


def _demo_rl_panels() -> list[dict[str, object]]:
    return [
        {
            "orientation": "vertical",
            "title": "Gym - Locomotion",
            "subtitle": "Cont. actions, vector obs.",
            "ylabel": "TD3-Normalized",
            "methods": ["TD7", "MR.Q", "TD-MPC2", "DreamerV3", "PPO"],
            "values": [1.56, 1.45, 1.03, 0.76, 0.44],
            "errors": [0.03, 0.04, 0.12, 0.07, 0.03],
            "ylim": (0, 1.7),
        },
        {
            "orientation": "vertical",
            "title": "DMC - Proprioceptive",
            "subtitle": "Cont. actions, vector obs.",
            "ylabel": "Reward (1k)",
            "methods": ["MR.Q", "TD-MPC2", "TD7", "DreamerV3", "PPO"],
            "values": [0.84, 0.79, 0.57, 0.53, 0.25],
            "errors": [0.01, 0.02, 0.02, 0.01, 0.01],
            "ylim": (0, 0.9),
        },
        {
            "orientation": "vertical",
            "title": "DMC - Visual",
            "subtitle": "Cont. actions, pixel obs.",
            "ylabel": "Reward (1k)",
            "methods": ["MR.Q", "DrQ-v2", "TD-MPC2", "DreamerV3", "PPO"],
            "values": [0.60, 0.51, 0.48, 0.46, 0.11],
            "errors": [0.005, 0.01, 0.02, 0.01, 0.015],
            "ylim": (0, 0.65),
        },
        {
            "orientation": "vertical",
            "title": "Atari - 10M",
            "subtitle": "Discrete actions, pixel obs.",
            "ylabel": "Human-Normalized",
            "methods": ["DreamerV3", "MR.Q", "Rainbow", "DQN", "PPO"],
            "values": [3.75, 2.50, 1.10, 0.25, 0.02],
            "errors": [0.48, 0.25, 0.08, 0.03, 0.01],
            "ylim": (0, 4.2),
        },
        {
            "orientation": "horizontal",
            "title": "Parameter Count",
            "subtitle": "Gym (HalfCheetah-v4)",
            "xlabel": "Parameters (1M)",
            "methods": ["MR.Q", "DreamerV3", "TD-MPC2"],
            "values": [4.1, 9.7, 5.5],
            "display_values": ["4.1M", "9.7M", "5.5M"],
            "xlim": (0, 11),
        },
        {
            "orientation": "horizontal",
            "title": "Training FPS",
            "subtitle": "Gym (HalfCheetah-v4)",
            "xlabel": "Frames per second",
            "methods": ["MR.Q", "DreamerV3", "TD-MPC2"],
            "values": [49, 18, 14],
            "display_values": ["49", "18", "14"],
            "xlim": (0, 55),
        },
        {
            "orientation": "horizontal",
            "title": "Evaluation FPS",
            "subtitle": "Gym (HalfCheetah-v4)",
            "xlabel": "Frames per second (1k)",
            "methods": ["MR.Q", "DreamerV3", "TD-MPC2"],
            "values": [1.9, 0.236, 0.027],
            "display_values": ["1.9k", "236", "27"],
            "xlim": (0, 2.2),
        },
        {
            "orientation": "horizontal",
            "title": "Parameter Count",
            "subtitle": "Atari (Any)",
            "xlabel": "Parameters (1M)",
            "methods": ["MR.Q", "DreamerV3", "Rainbow"],
            "values": [4.4, 187.3, 6.5],
            "display_values": ["4.4M", "187.3M", "6.5M"],
            "xlim": (0, 205),
        },
    ]


def demo(kind: str, out_dir: str | Path, formats: Sequence[str], dpi: int, style_name: str = "rl_benchmark") -> list[Path]:
    if kind == "readme-gallery":
        selected = ["bars", "sem-palettes", "violin", "line", "ablation-matrix", "pareto-scatter", "qual-grid", "uncertainty-map"]
        made: list[Path] = []
        for item in selected:
            made.extend(demo(item, out_dir, formats, dpi, style_name=style_name))
        return made

    style = setup_theme(style_name)
    out = Path(out_dir)
    made: list[Path] = []
    grouped = _demo_grouped()

    if kind in {"bar", "all"}:
        compact = setup_theme("compact")
        fig, ax = plt.subplots(figsize=(3.35, 2.55), layout="constrained")
        bar_scatter_sem(grouped, "group", "response", ax=ax, ylabel="Normalized response", style=compact)
        ax.set_title("Mean with raw samples")
        made.extend(save_figure(fig, out / "demo_bar_scatter_sem", formats=formats, dpi=dpi))
        plt.close(fig)
        style = setup_theme(style_name)

    if kind in {"sem-palettes", "all"}:
        setup_theme("compact")
        fig = demo_sem_palette_showcase()
        made.extend(save_figure(fig, out / "demo_bar_scatter_sem_palettes", formats=formats, dpi=dpi))
        plt.close(fig)
        style = setup_theme(style_name)

    if kind in {"violin", "all"}:
        setup_theme("compact")
        fig, ax = plt.subplots(figsize=(4.55, 3.05), layout="constrained")
        violin_box_points(_demo_distribution(), "group", "response", ax=ax, ylabel="Normalized response")
        ax.set_title("Raincloud distribution", fontsize=10.8, fontweight="bold", pad=7)
        made.extend(save_figure(fig, out / "demo_violin_box_points", formats=formats, dpi=dpi))
        plt.close(fig)
        style = setup_theme(style_name)

    if kind in {"line", "all"}:
        setup_theme("compact")
        fig, ax = plt.subplots(figsize=(5.6, 3.25), layout="constrained")
        line_ci(_demo_time(), "day", "signal", group="condition", ax=ax, ylabel="Score", xlabel="Training step (1M)")
        ax.set_title("Training Curves with 95% CI", pad=9)
        made.extend(save_figure(fig, out / "demo_line_ci", formats=formats, dpi=dpi))
        plt.close(fig)
        style = setup_theme(style_name)

    if kind in {"scatter", "all"}:
        setup_theme("compact")
        fig, ax = plt.subplots(figsize=(4.45, 3.05), layout="constrained")
        scatter_regression(_demo_scatter(), "dose", "activity", ax=ax, xlabel="Compute budget", ylabel="Score")
        ax.set_title("Relationship with Trend", pad=9)
        made.extend(save_figure(fig, out / "demo_scatter_regression", formats=formats, dpi=dpi))
        plt.close(fig)
        style = setup_theme(style_name)

    if kind in {"heatmap", "all"}:
        setup_theme("compact")
        fig, ax = plt.subplots(figsize=(3.2, 2.85), layout="constrained")
        heatmap(_demo_heatmap(), ax=ax, cmap="cividis", colorbar_label="Score")
        ax.set_title("Matrix summary")
        made.extend(save_figure(fig, out / "demo_heatmap", formats=formats, dpi=dpi))
        plt.close(fig)
        style = setup_theme(style_name)

    if kind in {"multipanel", "all"}:
        setup_theme("compact")
        fig, axs = plt.subplots(2, 2, figsize=(6.7, 4.65), layout="constrained")
        bar_scatter_sem(grouped, "group", "response", ax=axs[0, 0], ylabel="Response", style="compact")
        violin_box_points(grouped, "group", "response", ax=axs[0, 1], ylabel="Response")
        line_ci(_demo_time(), "day", "signal", group="condition", ax=axs[1, 0], ylabel="Signal", xlabel="Day")
        heatmap(_demo_heatmap(), ax=axs[1, 1], colorbar_label="Score")
        for ax, title in zip(axs.flat, ["Mean", "Distribution", "Trajectory", "Heatmap"]):
            ax.set_title(title)
        add_panel_letters(axs.flat, fontsize=9)
        made.extend(save_figure(fig, out / "demo_multipanel", formats=formats, dpi=dpi))
        plt.close(fig)
        style = setup_theme(style_name)

    if kind in {"bars", "rl-bars", "all"}:
        setup_theme("rl_benchmark")
        fig = rl_benchmark_grid(_demo_rl_panels(), methods_for_legend=RL_METHOD_ORDER, include_legend=True)
        made.extend(save_figure(fig, out / "demo_bar_charts", formats=formats, dpi=max(dpi, 600)))
        if kind == "rl-bars":
            made.extend(save_figure(fig, out / "demo_rl_benchmark_bars", formats=formats, dpi=max(dpi, 600)))
        plt.close(fig)
        style = setup_theme(style_name)

    if kind in {"ai-bars", "all"}:
        metrics, methods, values = _demo_ai_bars()
        colors = [
            AI_SEMANTIC["neutral"],
            "#F1F1A9",
            AI_SEMANTIC["red_1"],
            "#DDB6D7",
            "#C58C55",
            "#DDF3DE",
            AI_SEMANTIC["green_3"],
            AI_SEMANTIC["blue_main"],
        ]
        fig = plt.figure(figsize=(12.5, 3.6), layout=None)
        axes = [
            fig.add_axes([0.07, 0.18, 0.18, 0.58]),
            fig.add_axes([0.33, 0.18, 0.18, 0.58]),
            fig.add_axes([0.59, 0.18, 0.18, 0.58]),
        ]
        legend_ax = fig.add_axes([0.82, 0.18, 0.16, 0.58])
        for i, (metric, ax) in enumerate(zip(metrics, axes)):
            leaderboard_bar(ax, methods, values[:, i], ylabel=metric, colors=colors, annotate=True, sort=False, style=style)
            ax.set_title(metric)
            ax.set_xticks([])
        add_legend_panel(legend_ax, methods, colors)
        made.extend(save_figure(fig, out / "demo_ai_bars", formats=formats, dpi=max(dpi, 600)))
        plt.close(fig)

    if kind in {"radial-ridge", "all"}:
        categories, labels, values = _demo_radial()
        fig, ax = plt.subplots(figsize=(6.0, 5.4), subplot_kw={"projection": "polar"}, layout="constrained")
        radial_ridge_plot(ax, categories, values, labels)
        made.extend(save_figure(fig, out / "demo_radial_ridge", formats=formats, dpi=dpi))
        plt.close(fig)

    if kind in {"sensitivity3d", "all"}:
        x, layers, z, markers = _demo_sensitivity()
        fig = plt.figure(figsize=(7.4, 5.2), layout="constrained")
        ax = fig.add_subplot(111, projection="3d")
        sensitivity3d_plot(ax, x, layers, z, marker_values=markers)
        made.extend(save_figure(fig, out / "demo_sensitivity3d", formats=formats, dpi=dpi))
        plt.close(fig)

    if kind in {"qual-grid", "all"}:
        setup_theme("cvpr_qualitative")
        fig = demo_qual_grid()
        made.extend(save_figure(fig, out / "demo_qual_grid", formats=formats, dpi=dpi))
        plt.close(fig)
        style = setup_theme(style_name)

    if kind in {"metric-suite", "all"}:
        setup_theme("icml_dense")
        fig = demo_metric_suite()
        made.extend(save_figure(fig, out / "demo_metric_suite", formats=formats, dpi=dpi))
        plt.close(fig)
        style = setup_theme(style_name)

    if kind in {"ablation-matrix", "all"}:
        setup_theme("icml_dense")
        fig = demo_ablation_matrix()
        made.extend(save_figure(fig, out / "demo_ablation_matrix", formats=formats, dpi=dpi))
        plt.close(fig)
        style = setup_theme(style_name)

    if kind in {"pareto-scatter", "all"}:
        setup_theme("icml_dense")
        fig = demo_pareto_scatter()
        made.extend(save_figure(fig, out / "demo_pareto_scatter", formats=formats, dpi=dpi))
        plt.close(fig)
        style = setup_theme(style_name)

    if kind in {"uncertainty-map", "all"}:
        setup_theme("aaai_geo")
        fig = demo_uncertainty_map()
        made.extend(save_figure(fig, out / "demo_uncertainty_map", formats=formats, dpi=dpi))
        plt.close(fig)
        style = setup_theme(style_name)

    return made


def _pivot_long(data: pd.DataFrame, x: str, series: str, value: str) -> tuple[list[str], list[str], np.ndarray]:
    pivot = data.pivot_table(index=series, columns=x, values=value, aggfunc="mean")
    return list(pivot.columns.astype(str)), list(pivot.index.astype(str)), pivot.to_numpy(dtype=float)


def _rl_panels_from_table(
    data: pd.DataFrame,
    *,
    panel_col: str,
    method_col: str,
    value_col: str,
    subtitle_col: str | None = None,
    orientation_col: str | None = None,
    error_col: str | None = None,
    display_value_col: str | None = None,
) -> list[dict[str, object]]:
    panels: list[dict[str, object]] = []
    for panel_name, sub in data.groupby(panel_col, sort=False, dropna=False):
        methods = sub[method_col].astype(str).tolist()
        values = pd.to_numeric(sub[value_col], errors="coerce").to_numpy(dtype=float)
        orientation = "vertical"
        if orientation_col and orientation_col in sub:
            first_orientation = str(sub[orientation_col].dropna().iloc[0]) if not sub[orientation_col].dropna().empty else ""
            orientation = first_orientation.lower() if first_orientation else orientation
        panel: dict[str, object] = {
            "title": str(panel_name),
            "subtitle": None,
            "orientation": orientation,
            "methods": methods,
            "values": values,
            "ylabel": str(panel_name) if orientation != "horizontal" else "",
            "xlabel": str(panel_name) if orientation == "horizontal" else "",
        }
        if subtitle_col and subtitle_col in sub and not sub[subtitle_col].dropna().empty:
            panel["subtitle"] = str(sub[subtitle_col].dropna().iloc[0])
        if error_col and error_col in sub:
            panel["errors"] = pd.to_numeric(sub[error_col], errors="coerce").fillna(0).to_numpy(dtype=float)
        if display_value_col and display_value_col in sub:
            panel["display_values"] = sub[display_value_col].astype(str).tolist()
        panels.append(panel)
    return panels


def plot_from_table(
    *,
    data_path: str | Path,
    kind: str,
    out_dir: str | Path,
    formats: Sequence[str],
    dpi: int,
    group: str | None = None,
    value: str | None = None,
    x: str | None = None,
    y: str | None = None,
    series: str | None = None,
    panel: str | None = None,
    subtitle: str | None = None,
    orientation: str | None = None,
    error: str | None = None,
    display_value: str | None = None,
    output_name: str | None = None,
    style_name: str = "rl_benchmark",
    palette_name: str = "rl_pastel",
    annotate_values: bool = False,
    legend_panel: bool = False,
) -> list[Path]:
    """Render common plots directly from a user table."""

    style = setup_theme(style_name)
    data = read_table(data_path)
    out = Path(out_dir)
    stem = output_name or f"{Path(data_path).stem}_{kind.replace('-', '_')}"
    soft_default_kinds = {"violin", "line", "scatter", "radar", "radial-ridge", "pareto-scatter", "metric-suite"}
    effective_palette = "soft_edge" if palette_name == "rl_pastel" and kind in soft_default_kinds else palette_name
    colors = palette(effective_palette, 24, "fill" if effective_palette == "rl_pastel" else "edge")

    if kind == "bar":
        if not group or not value:
            raise ValueError("--kind bar requires --group and --value.")
        if style_name == "rl_benchmark":
            summary = describe_groups(data, group, value)
            methods = summary[group].astype(str).tolist()
            fig, ax = plt.subplots(figsize=(4.0, 2.8), layout="constrained")
            rl_vertical_bar_panel(
                ax,
                methods,
                summary["mean"].to_numpy(dtype=float),
                errors=summary["sem"].fillna(0).to_numpy(dtype=float),
                title=stem.replace("_", " "),
                ylabel=value,
            )
        else:
            setup_theme("compact" if style_name == "compact" else style_name)
            fig, ax = plt.subplots(figsize=(5.2, 3.4), layout="constrained")
            bar_scatter_sem(data, group, value, ax=ax, ylabel=value, edge=colors, style=style)
    elif kind == "violin":
        if not group or not value:
            raise ValueError("--kind violin requires --group and --value.")
        fig, ax = plt.subplots(figsize=(5.2, 3.4), layout="constrained")
        violin_box_points(data, group, value, ax=ax, ylabel=value, colors=colors)
    elif kind == "line":
        if not x or not y:
            raise ValueError("--kind line requires --x and --y; optionally pass --series.")
        fig, ax = plt.subplots(figsize=(5.6, 3.4), layout="constrained")
        line_ci(data, x, y, group=series, ax=ax, ylabel=y, xlabel=x, colors=colors)
    elif kind == "scatter":
        if not x or not y:
            raise ValueError("--kind scatter requires --x and --y.")
        fig, ax = plt.subplots(figsize=(4.8, 3.5), layout="constrained")
        scatter_regression(data, x, y, ax=ax, xlabel=x, ylabel=y, color=colors[0])
    elif kind == "heatmap":
        numeric = data.select_dtypes(include=[np.number])
        if numeric.empty:
            raise ValueError("--kind heatmap requires numeric columns.")
        fig, ax = plt.subplots(figsize=(5.2, 4.2), layout="constrained")
        heatmap(numeric.corr(), ax=ax, cmap="cividis", colorbar_label="Correlation")
    elif kind == "leaderboard":
        if not group or not value:
            raise ValueError("--kind leaderboard requires --group and --value.")
        summary = data.groupby(group, dropna=False)[value].mean().sort_values(ascending=False)
        fig, ax = plt.subplots(figsize=(7.0, 4.3), layout="constrained")
        leaderboard_bar(ax, list(summary.index.astype(str)), summary.to_numpy(), ylabel=value, colors=colors, annotate=True, style=style)
    elif kind == "grouped-bar":
        if not x or not series or not value:
            raise ValueError("--kind grouped-bar requires --x, --series, and --value.")
        categories, labels, arr = _pivot_long(data, x, series, value)
        if legend_panel:
            fig = plt.figure(figsize=(10.5, 4.2), layout="constrained")
            gs = fig.add_gridspec(1, 2, width_ratios=[1, 0.32])
            ax = fig.add_subplot(gs[0, 0])
            legend_ax = fig.add_subplot(gs[0, 1])
        else:
            fig, ax = plt.subplots(figsize=(8.0, 4.2), layout="constrained")
            legend_ax = None
        grouped_bar(ax, categories, arr, labels, ylabel=value, colors=colors, annotate=annotate_values, style=style)
        if legend_ax is not None:
            add_legend_panel(legend_ax, labels, colors)
        else:
            ax.legend(loc="best")
    elif kind == "composition":
        if not x or not series or not value:
            raise ValueError("--kind composition requires --x, --series, and --value.")
        categories, labels, arr = _pivot_long(data, x, series, value)
        fig, ax = plt.subplots(figsize=(7.2, 4.0), layout="constrained")
        composition_bar(ax, categories, arr, labels, ylabel=value, colors=colors, style=style)
        ax.legend(loc="center left", bbox_to_anchor=(1.02, 0.5))
    elif kind == "radar":
        if not x or not series or not value:
            raise ValueError("--kind radar requires --x, --series, and --value.")
        categories, labels, arr = _pivot_long(data, x, series, value)
        fig, ax = plt.subplots(figsize=(5.6, 5.0), subplot_kw={"projection": "polar"}, layout="constrained")
        radar_plot(ax, categories, arr, labels, colors=colors)
    elif kind == "radial-ridge":
        if group and value:
            labels = list(pd.unique(data[group].dropna()))
            categories = [str(i) for i in range(1, len(data.loc[data[group] == labels[0], value]) + 1)]
            rows = [pd.to_numeric(data.loc[data[group] == label, value], errors="coerce").dropna().to_numpy() for label in labels]
            max_len = max(len(row) for row in rows)
            categories = [str(i) for i in range(1, max_len + 1)]
            arr = np.vstack([np.pad(row, (0, max_len - len(row)), mode="edge") for row in rows])
        elif x and series and value:
            categories, labels, arr = _pivot_long(data, x, series, value)
        else:
            raise ValueError("--kind radial-ridge requires either --group/--value or --x/--series/--value.")
        fig, ax = plt.subplots(figsize=(6.0, 5.4), subplot_kw={"projection": "polar"}, layout="constrained")
        radial_ridge_plot(ax, categories, arr, labels, colors=colors)
    elif kind == "sensitivity3d":
        if not x or not series or not value:
            raise ValueError("--kind sensitivity3d requires --x, --series, and --value.")
        pivot = data.pivot_table(index=series, columns=x, values=value, aggfunc="mean").sort_index()
        x_vals = pd.to_numeric(pd.Index(pivot.columns), errors="coerce").to_numpy(dtype=float)
        layers = pd.to_numeric(pd.Index(pivot.index), errors="coerce").to_numpy(dtype=float)
        fig = plt.figure(figsize=(7.4, 5.2), layout="constrained")
        ax = fig.add_subplot(111, projection="3d")
        sensitivity3d_plot(ax, x_vals, layers, pivot.to_numpy(dtype=float))
    elif kind == "rl-benchmark-grid":
        if not panel or not group or not value:
            raise ValueError("--kind rl-benchmark-grid requires --panel, --group, and --value.")
        setup_theme("rl_benchmark")
        panels = _rl_panels_from_table(
            data,
            panel_col=panel,
            method_col=group,
            value_col=value,
            subtitle_col=subtitle,
            orientation_col=orientation,
            error_col=error,
            display_value_col=display_value,
        )
        methods_for_legend = [method for method in RL_METHOD_ORDER if method in set(data[group].astype(str))]
        remaining = [method for method in pd.unique(data[group].astype(str)) if method not in methods_for_legend]
        fig = rl_benchmark_grid(panels, methods_for_legend=methods_for_legend + remaining, include_legend=True)
    elif kind == "qual-grid":
        if not x or not series:
            raise ValueError("--kind qual-grid requires --x image-path column and --series method column; optionally pass --panel row column.")
        row_col = panel or group
        row_labels = list(pd.unique(data[row_col].astype(str))) if row_col else ["Sample"]
        col_labels = list(pd.unique(data[series].astype(str)))
        images: list[list[np.ndarray]] = []
        for row_label in row_labels:
            row_images: list[np.ndarray] = []
            row_data = data[data[row_col].astype(str) == row_label] if row_col else data
            for col_label in col_labels:
                match = row_data[row_data[series].astype(str) == col_label]
                if match.empty:
                    row_images.append(np.ones((96, 128, 3), dtype=float))
                    continue
                image_path = Path(str(match.iloc[0][x])).expanduser()
                if not image_path.is_absolute():
                    image_path = Path(data_path).parent / image_path
                row_images.append(mpimg.imread(image_path))
            images.append(row_images)
        fig = qualitative_result_grid(images, row_labels, col_labels, title=stem.replace("_", " "), style_name=style_name)
    elif kind == "metric-suite":
        if not x or not group or not value:
            raise ValueError("--kind metric-suite requires --x metric column, --group method column, and --value.")
        pivot = data.pivot_table(index=group, columns=x, values=value, aggfunc="mean")
        fig = metric_suite_dashboard(
            list(pivot.columns.astype(str)),
            list(pivot.index.astype(str)),
            pivot.to_numpy(dtype=float),
            title=stem.replace("_", " "),
            style_name=style_name,
        )
    elif kind == "ablation-matrix":
        if not x or not series or not value:
            raise ValueError("--kind ablation-matrix requires --x, --series, and --value.")
        pivot = data.pivot_table(index=series, columns=x, values=value, aggfunc="mean")
        fig, ax = plt.subplots(figsize=(6.2, 3.8), layout="constrained")
        ablation_matrix_plot(
            ax,
            pivot.to_numpy(dtype=float),
            list(pivot.index.astype(str)),
            list(pivot.columns.astype(str)),
            title=stem.replace("_", " "),
            style_name=style_name,
        )
    elif kind == "pareto-scatter":
        if not x or not y:
            raise ValueError("--kind pareto-scatter requires --x and --y.")
        label_col = group or series
        labels = data[label_col].astype(str).tolist() if label_col else [str(i + 1) for i in range(len(data))]
        sizes = pd.to_numeric(data[value], errors="coerce").to_numpy(dtype=float) if value else None
        fig, ax = plt.subplots(figsize=(5.8, 4.1), layout="constrained")
        pareto_scatter_plot(
            ax,
            pd.to_numeric(data[x], errors="coerce").to_numpy(dtype=float),
            pd.to_numeric(data[y], errors="coerce").to_numpy(dtype=float),
            labels,
            size=sizes,
            xlabel=x,
            ylabel=y,
            title=stem.replace("_", " "),
            style_name=style_name,
        )
    elif kind == "uncertainty-map":
        if x and y and value:
            pivot = data.pivot_table(index=y, columns=x, values=value, aggfunc="mean")
            matrix = pivot.to_numpy(dtype=float)
        else:
            numeric = data.select_dtypes(include=[np.number])
            if numeric.empty:
                raise ValueError("--kind uncertainty-map requires numeric columns or --x/--y/--value.")
            matrix = numeric.to_numpy(dtype=float)
        fig, ax = plt.subplots(figsize=(5.2, 4.1), layout="constrained")
        uncertainty_map_plot(ax, matrix, title=stem.replace("_", " "), style_name=style_name)
    else:
        raise ValueError(f"Unsupported table plot kind: {kind}")

    if "ax" in locals() and kind not in {"sensitivity3d", "ablation-matrix", "pareto-scatter", "uncertainty-map"}:
        ax.set_title(stem.replace("_", " "))
    paths = save_figure(fig, out / stem, formats=formats, dpi=dpi)
    plt.close(fig)
    return paths


def parse_formats(value: str) -> list[str]:
    formats = [part.strip().lower().lstrip(".") for part in value.split(",") if part.strip()]
    if not formats:
        raise argparse.ArgumentTypeError("At least one format is required.")
    return formats


def main(argv: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Generate publication-style Python plot demos.")
    parser.add_argument(
        "--demo",
        choices=[
            "all",
            "readme-gallery",
            "bars",
            "bar",
            "sem-palettes",
            "violin",
            "line",
            "scatter",
            "heatmap",
            "multipanel",
            "rl-bars",
            "ai-bars",
            "radial-ridge",
            "sensitivity3d",
            "qual-grid",
            "metric-suite",
            "ablation-matrix",
            "pareto-scatter",
            "uncertainty-map",
        ],
        default="all",
        help="Demo figure type to render.",
    )
    parser.add_argument("--out", default="paper_plot_demo", help="Output folder.")
    parser.add_argument("--formats", type=parse_formats, default=["pdf", "svg", "png"], help="Comma-separated export formats.")
    parser.add_argument("--dpi", type=int, default=450, help="Raster export DPI.")
    parser.add_argument("--style", choices=sorted(STYLE_PRESETS), default="rl_benchmark", help="Figure style preset.")
    parser.add_argument("--palette", choices=sorted(PALETTES), default="rl_pastel", help="Categorical palette.")
    parser.add_argument("--list-styles", action="store_true", help="Print available figure style preset names.")
    parser.add_argument("--list-palettes", action="store_true", help="Print available categorical palette names.")
    parser.add_argument("--data", help="Optional CSV/TSV/Excel file to plot instead of demo data.")
    parser.add_argument(
        "--kind",
        choices=[
            "bar",
            "violin",
            "line",
            "scatter",
            "heatmap",
            "grouped-bar",
            "leaderboard",
            "composition",
            "radar",
            "radial-ridge",
            "sensitivity3d",
            "rl-benchmark-grid",
            "qual-grid",
            "metric-suite",
            "ablation-matrix",
            "pareto-scatter",
            "uncertainty-map",
        ],
        help="Plot kind for --data.",
    )
    parser.add_argument("--group", help="Grouping column for bar/violin/leaderboard/radial-ridge plots.")
    parser.add_argument("--value", help="Value column.")
    parser.add_argument("--x", help="X/category column for line/scatter/grouped/radar/3D plots.")
    parser.add_argument("--y", help="Y column for line/scatter plots.")
    parser.add_argument("--series", help="Series/group column for line/grouped/radar/3D plots.")
    parser.add_argument("--panel", help="Panel/title column for rl-benchmark-grid.")
    parser.add_argument("--subtitle", help="Subtitle column for rl-benchmark-grid.")
    parser.add_argument("--orientation", help="Orientation column with vertical or horizontal values for rl-benchmark-grid.")
    parser.add_argument("--error", help="Error-bar column for rl-benchmark-grid vertical panels.")
    parser.add_argument("--display-value", help="Display-value column for rl-benchmark-grid horizontal labels.")
    parser.add_argument("--output-name", help="Output base filename without extension.")
    parser.add_argument("--annotate-values", action="store_true", help="Add direct value labels to bar charts.")
    parser.add_argument("--legend-panel", action="store_true", help="Use a dedicated legend panel when supported.")
    args = parser.parse_args(argv)

    if args.list_styles:
        for name in sorted(STYLE_PRESETS):
            print(name)
        return 0

    if args.list_palettes:
        for name in sorted(PALETTES):
            print(name)
        return 0

    if args.data:
        if not args.kind:
            parser.error("--data requires --kind.")
        paths = plot_from_table(
            data_path=args.data,
            kind=args.kind,
            out_dir=args.out,
            formats=args.formats,
            dpi=args.dpi,
            group=args.group,
            value=args.value,
            x=args.x,
            y=args.y,
            series=args.series,
            panel=args.panel,
            subtitle=args.subtitle,
            orientation=args.orientation,
            error=args.error,
            display_value=args.display_value,
            output_name=args.output_name,
            style_name=args.style,
            palette_name=args.palette,
            annotate_values=args.annotate_values,
            legend_panel=args.legend_panel,
        )
    else:
        paths = demo(args.demo, args.out, args.formats, args.dpi, style_name=args.style)
    for path in paths:
        print(path)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
