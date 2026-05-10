"""Neural-network report plotters for classification/OCR experiments.

These helpers are tuned for course projects, thesis chapters, and paper result
sections where method names are long, metrics are close to saturation, and
error counts matter as much as accuracy.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

import matplotlib.pyplot as plt
from matplotlib import colors as mcolors
from matplotlib.lines import Line2D
from matplotlib.patches import Patch, Rectangle
import numpy as np
import pandas as pd

from .styles import SOFT_EDGE_EDGES, SOFT_EDGE_FILLS


@dataclass(frozen=True)
class FamilyStyle:
    fill: str
    edge: str


NN_FAMILY_STYLES: dict[str, FamilyStyle] = {
    "CNN": FamilyStyle("#DDEBFA", "#2B6CB0"),
    "Sequence": FamilyStyle("#E8F4DD", "#4C9A2A"),
    "OCR": FamilyStyle("#FFF0D6", "#C26A00"),
    "Hybrid": FamilyStyle("#F7DCE7", "#C33C76"),
    "Holdout": FamilyStyle("#E8E8E8", "#6B7280"),
    "Baseline": FamilyStyle("#ECECEC", "#7A7A7A"),
    "Ours": FamilyStyle("#DFF2EF", "#178C7B"),
}


def _fallback_family_style(index: int) -> FamilyStyle:
    return FamilyStyle(SOFT_EDGE_FILLS[(index * 5) % len(SOFT_EDGE_FILLS)], SOFT_EDGE_EDGES[(index * 5 + 2) % len(SOFT_EDGE_EDGES)])


def _family_style(family: str, index: int = 0) -> FamilyStyle:
    return NN_FAMILY_STYLES.get(str(family), _fallback_family_style(index))


def _panel_axis(ax: plt.Axes, *, xgrid: bool = True) -> None:
    ax.set_facecolor("#F6F7F5")
    for spine in ("top", "right"):
        ax.spines[spine].set_visible(False)
    ax.spines["left"].set_color("#BCBCBC")
    ax.spines["bottom"].set_color("#BCBCBC")
    ax.spines["left"].set_linewidth(0.9)
    ax.spines["bottom"].set_linewidth(0.9)
    ax.tick_params(axis="both", width=0.8, length=3.0, pad=2.2, colors="#202020")
    if xgrid:
        ax.grid(axis="x", color="#DEDEDE", linewidth=0.72, zorder=0)


def _score_limits(values: Sequence[float]) -> tuple[float, float]:
    arr = np.asarray(values, dtype=float)
    arr = arr[np.isfinite(arr)]
    if arr.size == 0:
        return 0.0, 1.0
    lo = float(np.nanmin(arr))
    hi = float(np.nanmax(arr))
    if lo >= 0.55 and hi <= 1.01:
        lower = max(0.0, np.floor((lo - 0.045) * 20) / 20)
        return lower, 1.005
    pad = max((hi - lo) * 0.12, 0.02)
    return max(0.0, lo - pad), hi + pad


def _metric_label(value: float) -> str:
    if 0 <= value <= 1.2:
        return f"{value * 100:.1f}"
    return f"{value:.2f}"


def _add_family_legend(fig: plt.Figure, families: Sequence[str], *, y: float = 0.045) -> None:
    seen: list[str] = []
    for family in families:
        if family not in seen:
            seen.append(str(family))
    handles = [
        Patch(facecolor=_family_style(fam, i).fill, edgecolor=_family_style(fam, i).edge, linewidth=1.15, label=fam)
        for i, fam in enumerate(seen)
    ]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, y), ncol=min(len(handles), 6), frameon=False, fontsize=8.1)


def classification_report_figure(
    data: pd.DataFrame,
    *,
    method_col: str = "method",
    accuracy_col: str = "accuracy",
    f1_col: str | None = "macro_f1",
    wrong_col: str | None = "wrong",
    family_col: str | None = "family",
    title: str = "Classification Method Comparison",
) -> plt.Figure:
    """Draw a compact method-comparison report for classification results."""

    frame = data.copy()
    frame[accuracy_col] = pd.to_numeric(frame[accuracy_col], errors="coerce")
    if f1_col and f1_col in frame:
        frame[f1_col] = pd.to_numeric(frame[f1_col], errors="coerce")
    if wrong_col and wrong_col in frame:
        frame[wrong_col] = pd.to_numeric(frame[wrong_col], errors="coerce")
    if family_col is None or family_col not in frame:
        family_col = "_family"
        frame[family_col] = "Method"
    frame = frame.sort_values(accuracy_col, ascending=True).reset_index(drop=True)
    methods = frame[method_col].astype(str).tolist()
    families = frame[family_col].astype(str).tolist()
    metric_cols = [accuracy_col]
    metric_titles = ["Exact-match accuracy"]
    if f1_col and f1_col in frame:
        metric_cols.append(f1_col)
        metric_titles.append("Macro-F1 / balanced score")

    fig = plt.figure(figsize=(5.1 * len(metric_cols), 3.75), layout=None)
    gs = fig.add_gridspec(1, len(metric_cols), left=0.145, right=0.985, top=0.78, bottom=0.22, wspace=0.22)
    colors = [_family_style(fam, i) for i, fam in enumerate(families)]
    y = np.arange(len(methods))

    all_values = frame[metric_cols].to_numpy(dtype=float).ravel()
    xmin, xmax = _score_limits(all_values)
    for idx, (col, panel_title) in enumerate(zip(metric_cols, metric_titles)):
        ax = fig.add_subplot(gs[0, idx])
        vals = frame[col].to_numpy(dtype=float)
        bars = ax.barh(
            y,
            vals - xmin,
            left=xmin,
            height=0.58,
            color=[mcolors.to_rgba(style.fill, 0.88) for style in colors],
            edgecolor=[style.edge for style in colors],
            linewidth=1.05,
            zorder=3,
        )
        best_idx = int(np.nanargmax(vals))
        bars[best_idx].set_edgecolor("#111111")
        bars[best_idx].set_linewidth(1.65)
        _panel_axis(ax)
        ax.set_xlim(xmin, xmax)
        ax.set_ylim(-0.65, len(methods) - 0.35)
        ax.set_yticks(y, methods if idx == 0 else [""] * len(methods), fontsize=8.0)
        ax.set_xlabel("Score (%)" if np.nanmax(vals) <= 1.2 else "Score", labelpad=4)
        ax.set_title(panel_title, fontsize=10.2, fontweight="bold", pad=8)
        ax.xaxis.set_major_formatter(lambda v, _pos: f"{v * 100:.0f}" if xmax <= 1.2 else f"{v:.1f}")
        for row, (yi, val) in enumerate(zip(y, vals)):
            label_x = min(val + (xmax - xmin) * 0.012, xmax - (xmax - xmin) * 0.02)
            ax.text(
                label_x,
                yi,
                _metric_label(float(val)),
                ha="left" if label_x > val else "right",
                va="center",
                fontsize=7.6,
                fontweight="bold" if row == best_idx else "normal",
                color="#1F2937",
                zorder=5,
                clip_on=False,
            )
            if idx == 0 and wrong_col and wrong_col in frame and np.isfinite(frame.loc[row, wrong_col]):
                wrong = int(frame.loc[row, wrong_col])
                ax.text(
                    xmax + (xmax - xmin) * 0.035,
                    yi,
                    f"{wrong} err",
                    ha="left",
                    va="center",
                    fontsize=7.0,
                    color="#6B7280",
                    bbox={"boxstyle": "round,pad=0.18", "facecolor": "white", "edgecolor": "#D1D5DB", "linewidth": 0.55},
                    clip_on=False,
                )
        if idx == 0 and wrong_col and wrong_col in frame:
            ax.text(1.035, 1.035, "errors", transform=ax.transAxes, ha="left", va="bottom", fontsize=7.0, color="#6B7280")

    best_method = str(frame.loc[int(np.nanargmax(frame[accuracy_col].to_numpy(dtype=float))), method_col])
    fig.suptitle(title, fontsize=12.4, fontweight="bold", y=0.965)
    fig.text(
        0.145,
        0.842,
        f"Sorted by accuracy; best method: {best_method}. Error counts are shown as side badges.",
        fontsize=8.0,
        color="#6B7280",
    )
    _add_family_legend(fig, families)
    return fig


def training_curves_figure(
    data: pd.DataFrame,
    *,
    step_col: str = "epoch",
    value_col: str = "value",
    method_col: str = "method",
    metric_col: str | None = None,
    title: str = "Training Dynamics",
) -> plt.Figure:
    """Draw compact training curves with marker thinning and endpoint labels."""

    frame = data.copy()
    frame[step_col] = pd.to_numeric(frame[step_col], errors="coerce")
    frame[value_col] = pd.to_numeric(frame[value_col], errors="coerce")
    if metric_col and metric_col in frame:
        metrics = frame[metric_col].astype(str).drop_duplicates().tolist()
    else:
        metric_col = "_metric"
        frame[metric_col] = "Validation accuracy"
        metrics = ["Validation accuracy"]
    methods = frame[method_col].astype(str).drop_duplicates().tolist()
    edge_cycle = ["#2B6CB0", "#4C9A2A", "#C26A00", "#C33C76", "#6B7280", "#6A51A3"]
    fill_cycle = ["#DDEBFA", "#E8F4DD", "#FFF0D6", "#F7DCE7", "#E8E8E8", "#ECE6FA"]
    markers = ["o", "s", "^", "D", "P", "v"]

    fig = plt.figure(figsize=(5.0 * len(metrics), 3.55), layout=None)
    gs = fig.add_gridspec(1, len(metrics), left=0.075, right=0.985, top=0.70, bottom=0.25, wspace=0.22)
    for panel_idx, metric in enumerate(metrics):
        ax = fig.add_subplot(gs[0, panel_idx])
        sub_metric = frame[frame[metric_col].astype(str) == metric]
        endpoints: list[tuple[float, float, str, str]] = []
        for method_idx, method in enumerate(methods):
            sub = sub_metric[sub_metric[method_col].astype(str) == method]
            if sub.empty:
                continue
            summary = (
                sub.groupby(step_col, dropna=False)[value_col]
                .agg(mean="mean", sem=lambda x: float(np.std(x, ddof=1) / np.sqrt(len(x))) if len(x) > 1 else 0.0, n="count")
                .reset_index()
                .sort_values(step_col)
            )
            xs = summary[step_col].to_numpy(dtype=float)
            mean = summary["mean"].to_numpy(dtype=float)
            sem = summary["sem"].to_numpy(dtype=float)
            edge = edge_cycle[method_idx % len(edge_cycle)]
            fill = fill_cycle[method_idx % len(fill_cycle)]
            show_ribbon = bool(np.nanmax(sem) > 0)
            if show_ribbon:
                ax.fill_between(xs, mean - 1.96 * sem, mean + 1.96 * sem, color=mcolors.to_rgba(fill, 0.55), linewidth=0, zorder=1)
            markevery = max(1, int(np.ceil(len(xs) / 6)))
            ax.plot(
                xs,
                mean,
                color=edge,
                linewidth=1.9,
                marker=markers[method_idx % len(markers)],
                markersize=4.6,
                markerfacecolor=fill,
                markeredgecolor=edge,
                markeredgewidth=0.85,
                markevery=markevery,
                zorder=3,
                label=method,
            )
            if len(xs):
                endpoints.append((float(xs[-1]), float(mean[-1]), method, edge))
                is_loss = "loss" in metric.lower()
                best_idx = int(np.nanargmin(mean) if is_loss else np.nanargmax(mean))
                ax.scatter([xs[best_idx]], [mean[best_idx]], s=42, facecolors="white", edgecolors=edge, linewidths=1.25, zorder=4)
        _panel_axis(ax)
        ax.set_title(str(metric), fontsize=10.2, fontweight="bold", pad=8)
        ax.set_xlabel("Epoch")
        ax.set_ylabel("Loss" if "loss" in str(metric).lower() else "Score")
        xmin, xmax = ax.get_xlim()
        ax.set_xlim(xmin, xmax + (xmax - xmin) * 0.18)
        endpoints = sorted(endpoints, key=lambda item: item[1])
        ymin, ymax = ax.get_ylim()
        gap = max((ymax - ymin) * 0.075, 1e-5)
        last = -np.inf
        for ex, ey, label, color in endpoints:
            adjusted = max(ey, last + gap)
            ax.annotate(label, (ex, adjusted), xytext=(6, 0), textcoords="offset points", ha="left", va="center", fontsize=7.4, color=color, fontweight="bold", clip_on=False)
            last = adjusted
        if last > ymax:
            ax.set_ylim(ymin, last + gap)
    handles = [
        Line2D([0], [0], color=edge_cycle[i % len(edge_cycle)], marker=markers[i % len(markers)], markerfacecolor=fill_cycle[i % len(fill_cycle)], markeredgecolor=edge_cycle[i % len(edge_cycle)], linewidth=1.8, label=method)
        for i, method in enumerate(methods)
    ]
    fig.legend(handles=handles, loc="lower center", bbox_to_anchor=(0.5, 0.035), ncol=min(len(handles), 4), frameon=False, fontsize=8.0)
    fig.suptitle(title, fontsize=12.4, fontweight="bold", y=0.965)
    fig.text(0.075, 0.812, "Markers are thinned; endpoint labels and best-epoch rings emphasize convergence.", fontsize=8.0, color="#6B7280")
    return fig


def ablation_table_figure(
    data: pd.DataFrame,
    *,
    row_col: str,
    col_col: str,
    value_col: str,
    error_col: str | None = None,
    title: str = "Ablation Matrix",
) -> plt.Figure:
    """Draw a table-like heatmap for narrow metric ranges."""

    pivot = data.pivot_table(index=row_col, columns=col_col, values=value_col, aggfunc="mean", sort=False)
    rows = list(pivot.index.astype(str))
    cols = list(pivot.columns.astype(str))
    arr = pivot.to_numpy(dtype=float)
    err_arr = None
    if error_col and error_col in data:
        err_pivot = data.pivot_table(index=row_col, columns=col_col, values=error_col, aggfunc="mean", sort=False).reindex(index=pivot.index, columns=pivot.columns)
        err_arr = err_pivot.to_numpy(dtype=float)
    fig, ax = plt.subplots(figsize=(1.18 * len(cols) + 2.5, 0.55 * len(rows) + 2.2), layout="constrained")
    spread = float(np.nanmax(arr) - np.nanmin(arr))
    cmap = "YlGnBu" if spread > 0.08 else "Blues"
    if spread <= 0.08:
        center = float(np.nanmedian(arr))
        vmin = center - max(spread * 0.85, 0.015)
        vmax = center + max(spread * 0.85, 0.015)
    else:
        vmin = float(np.nanmin(arr))
        vmax = float(np.nanmax(arr))
    im = ax.imshow(arr, cmap=cmap, aspect="auto", vmin=vmin, vmax=vmax)
    ax.set_title(title, fontsize=11.0, fontweight="bold", pad=10)
    ax.set_xticks(np.arange(len(cols)), cols, rotation=26, ha="right")
    ax.set_yticks(np.arange(len(rows)), rows)
    baseline = arr[0]
    best = np.nanargmax(arr, axis=0)
    norm = mcolors.Normalize(vmin=vmin, vmax=vmax)
    cmap_obj = plt.get_cmap(cmap)
    for r in range(arr.shape[0]):
        for c in range(arr.shape[1]):
            val = arr[r, c]
            delta = val - baseline[c]
            rgb = np.asarray(cmap_obj(norm(val))[:3])
            luminance = float(np.dot(rgb, [0.2126, 0.7152, 0.0722]))
            color = "white" if luminance < 0.5 else "#1F2937"
            if err_arr is not None and np.isfinite(err_arr[r, c]):
                label = f"{val * 100:.1f}\n{int(round(err_arr[r, c]))} err"
            else:
                label = f"{val * 100:.1f}\n{delta * 100:+.1f}" if r > 0 else f"{val * 100:.1f}"
            ax.text(c, r, label, ha="center", va="center", fontsize=7.0, color=color, linespacing=0.92)
            if best[c] == r:
                ax.add_patch(Rectangle((c - 0.48, r - 0.48), 0.96, 0.96, fill=False, edgecolor="#111111", linewidth=1.35))
    ax.set_xticks(np.arange(arr.shape[1] + 1) - 0.5, minor=True)
    ax.set_yticks(np.arange(arr.shape[0] + 1) - 0.5, minor=True)
    ax.grid(which="minor", color="white", linewidth=1.2)
    ax.tick_params(which="minor", bottom=False, left=False)
    ax.tick_params(length=0)
    for spine in ax.spines.values():
        spine.set_visible(False)
    cbar = fig.colorbar(im, ax=ax, fraction=0.035, pad=0.025)
    cbar.set_label("Score", labelpad=4)
    cbar.outline.set_linewidth(0.6)
    return fig


def error_reduction_figure(
    data: pd.DataFrame,
    *,
    method_col: str = "method",
    wrong_col: str = "wrong",
    family_col: str | None = "family",
    title: str = "Error Reduction Path",
) -> plt.Figure:
    """Draw wrong-sample reduction as a clean improvement chain."""

    frame = data.copy()
    frame[wrong_col] = pd.to_numeric(frame[wrong_col], errors="coerce")
    frame = frame.dropna(subset=[wrong_col]).reset_index(drop=True)
    if family_col is None or family_col not in frame:
        family_col = "_family"
        frame[family_col] = "Method"
    # Preserve user order when it already looks like a development path; otherwise
    # fall back to high-to-low wrong count.
    if not frame[wrong_col].is_monotonic_decreasing:
        frame = frame.sort_values(wrong_col, ascending=False).reset_index(drop=True)
    methods = frame[method_col].astype(str).tolist()
    families = frame[family_col].astype(str).tolist()
    wrong = frame[wrong_col].to_numpy(dtype=float)
    baseline = float(wrong[0]) if len(wrong) else 1.0
    reduction = (baseline - wrong) / max(baseline, 1e-9)
    x = np.arange(len(methods))
    styles = [_family_style(fam, i) for i, fam in enumerate(families)]
    fig, ax = plt.subplots(figsize=(max(6.0, 0.82 * len(methods) + 2.2), 3.8), layout=None)
    fig.subplots_adjust(left=0.08, right=0.985, top=0.84, bottom=0.31)
    bars = ax.bar(
        x,
        wrong,
        width=0.58,
        color=[mcolors.to_rgba(style.fill, 0.9) for style in styles],
        edgecolor=[style.edge for style in styles],
        linewidth=1.15,
        zorder=3,
    )
    best = int(np.nanargmin(wrong))
    bars[best].set_edgecolor("#111111")
    bars[best].set_linewidth(1.65)
    ax.plot(x, wrong, color="#2F3437", linestyle="--", linewidth=1.2, marker="o", markersize=3.8, zorder=4)
    for i, (xi, count, red) in enumerate(zip(x, wrong, reduction)):
        ax.text(xi, count + max(wrong) * 0.035, f"{int(count)}", ha="center", va="bottom", fontsize=8.0, fontweight="bold")
        if i > 0:
            ax.annotate(
                f"-{red * 100:.0f}%",
                xy=(xi - 0.5, max(wrong[i - 1], count) * 0.78),
                xytext=(xi - 0.5, max(wrong[i - 1], count) * 0.78),
                ha="center",
                va="center",
                fontsize=7.0,
                color="#2F855A",
                bbox={"boxstyle": "round,pad=0.18", "facecolor": "#EAF7EA", "edgecolor": "#A7D7A7", "linewidth": 0.55},
            )
    ax.set_xticks(x, methods, rotation=20, ha="right")
    ax.set_ylabel("Wrong samples")
    ax.set_title(title, fontsize=11.0, fontweight="bold", pad=10)
    ax.set_ylim(0, max(wrong) * 1.22)
    _panel_axis(ax, xgrid=False)
    ax.grid(axis="y", color="#DEDEDE", linewidth=0.72, zorder=0)
    _add_family_legend(fig, families, y=0.035)
    return fig


def demo_nn_report_figures() -> dict[str, plt.Figure]:
    """Generate a realistic classification/OCR result showcase."""

    summary = pd.DataFrame(
        {
            "method": ["ResNet18", "EfficientNet-B0", "ConvNeXt-Tiny", "CNN-BiLSTM", "OCR-only", "OCR+ConvNeXt", "OCR+BiLSTM", "Strict OCR"],
            "accuracy": [0.700, 0.815, 0.925, 0.955, 0.965, 0.985, 0.990, 0.960],
            "macro_f1": [0.585, 0.722, 0.892, 0.922, 0.954, 0.980, 0.983, 0.948],
            "wrong": [60, 37, 15, 9, 7, 3, 2, 8],
            "family": ["CNN", "CNN", "CNN", "Sequence", "OCR", "Hybrid", "Hybrid", "Holdout"],
        }
    )
    rng = np.random.default_rng(2026)
    epochs = np.arange(1, 31)
    curve_rows: list[dict[str, object]] = []
    curve_specs = {
        "ResNet18": (0.54, 0.71, 9.0, 0.92, 0.52),
        "ConvNeXt-Tiny": (0.60, 0.925, 7.0, 0.82, 0.24),
        "OCR+ConvNeXt": (0.72, 0.985, 5.4, 0.55, 0.08),
        "OCR+BiLSTM": (0.74, 0.990, 5.0, 0.50, 0.06),
    }
    for method, (start, final, tau, loss_start, loss_end) in curve_specs.items():
        for seed in range(3):
            acc = final - (final - start) * np.exp(-epochs / tau) + rng.normal(0, 0.006, size=len(epochs))
            loss = loss_end + (loss_start - loss_end) * np.exp(-epochs / (tau * 0.8)) + rng.normal(0, 0.01, size=len(epochs))
            for epoch, a, l in zip(epochs, acc, loss):
                curve_rows.append({"epoch": epoch, "method": method, "metric": "Validation accuracy", "value": np.clip(a, 0, 1)})
                curve_rows.append({"epoch": epoch, "method": method, "metric": "Validation loss", "value": max(l, 0.02)})
    curves = pd.DataFrame(curve_rows)
    ablation = pd.DataFrame(
        [
            ("CNN only", "No TTA", 0.925, 15),
            ("CNN only", "3 views", 0.940, 12),
            ("CNN only", "5 views", 0.945, 11),
            ("+ BiLSTM", "No TTA", 0.955, 9),
            ("+ BiLSTM", "3 views", 0.965, 7),
            ("+ BiLSTM", "5 views", 0.970, 6),
            ("+ OCR fallback", "No TTA", 0.975, 5),
            ("+ OCR fallback", "3 views", 0.985, 3),
            ("+ OCR fallback", "5 views", 0.990, 2),
        ],
        columns=["component", "tta", "accuracy", "wrong"],
    )
    ablation["tta"] = pd.Categorical(ablation["tta"], categories=["No TTA", "3 views", "5 views"], ordered=True)
    return {
        "demo_nn_classification_report": classification_report_figure(summary, title="OCR Classification Results"),
        "demo_nn_training_curves": training_curves_figure(curves, step_col="epoch", value_col="value", method_col="method", metric_col="metric", title="Training Dynamics"),
        "demo_nn_ablation_table": ablation_table_figure(ablation, row_col="component", col_col="tta", value_col="accuracy", error_col="wrong", title="Hybrid OCR Ablation"),
        "demo_nn_error_reduction": error_reduction_figure(summary, title="Wrong Sample Reduction"),
    }
