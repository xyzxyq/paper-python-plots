# Palettes

## Rules

- Prefer colorblind-aware categorical palettes for groups.
- Use perceptually ordered sequential colormaps for continuous magnitude.
- Use diverging colormaps only when there is a meaningful center such as zero, baseline, or no-change.
- Avoid rainbow/jet-style maps unless there is a domain-specific reason.
- Make fills lighter than edges for bar/point overlays; this keeps the figure refined and preserves contrast.
- Pair color with marker shape, line style, direct labels, or ordering when the figure must survive grayscale printing.

## Built-In Palette Names

The helper script exposes:
- `rl_pastel`: RL/AI benchmark palette with pastel fills, saturated outlines, and optional marker shapes for line plots.
- `ai_semantic`: figures4papers-inspired AI-paper palette with explicit semantic roles.
- `screenshot`: soft fill/dark edge pairs inspired by the user's screenshots.
- `okabe_ito`: colorblind-aware categorical palette.
- `journal_muted`: restrained paper-style colors for multi-series plots.
- `nature_soft`: subdued fill colors with darker outlines.

## RL Benchmark Palette

Use `rl_pastel` for reinforcement-learning and AI method comparison figures like task grids, parameter bars, FPS bars, and shared method legends.

```python
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
```

Rules:
- Fill bars with the pastel color and outline with the saturated edge.
- Use square fill/edge swatches for bar-chart legends.
- Use the same marker in line plots and marker-based shared legends.
- Keep the plot panel background light gray and the page background white.
- Put method names vertically inside bars when x-axis labels would clutter the panel; move labels outside very short bars to avoid error-bar overlap.

## AI-Conference Semantic Palette

Use this palette when reproducing the strong, polished benchmark style common in top AI/ML papers.

```python
AI_SEMANTIC = {
    "blue_main": "#0F4D92",       # proposed method / key result
    "blue_secondary": "#3775BA",  # secondary proposed variant
    "green_1": "#DDF3DE",        # light improvement band
    "green_2": "#AADCA9",
    "green_3": "#8BCF8B",        # strong improvement
    "red_1": "#F6CFCB",          # soft baseline/contrast
    "red_2": "#E9A6A1",
    "red_strong": "#B64342",
    "neutral": "#CFCECE",
    "neutral_dark": "#4D4D4D",
    "highlight": "#FFD700",      # one callout only
    "teal": "#42949E",
    "violet": "#9A4D8E",
}
```

Role mapping:
- Blue: proposed method, ours, reference winner, or main trajectory.
- Green: positive variants, improvements, ablations that add capability.
- Red/pink: baselines, negative contrasts, failed/removed variants.
- Neutral gray: older methods, background categories, controls.
- Gold: one important highlight; do not use it as a normal category color.

Print-safe rules:
- Use black bar edges for dense benchmark charts.
- Use hatch patterns when nearby colors may collapse in grayscale.
- Put exact values above bars when the reader needs numerical comparison.
- Prefer a dedicated legend panel when method names are long.

## Screenshot-Inspired Fill/Edge Sets

These are transcribed from the screenshot idea: light fills, stronger borders.

```python
SCREENSHOT_PALETTES = [
    {"fill": ["#eef3f8", "#e0eff2", "#c0daf0", "#9dabd0"], "edge": ["#b9d8f7", "#90b8f1", "#6182cc", "#424d95"]},
    {"fill": ["#e5f5e0", "#c7e9c0", "#a1d99b", "#74c476"], "edge": ["#a1d99b", "#74c476", "#41ab5d", "#238b45"]},
    {"fill": ["#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a"], "edge": ["#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d"]},
    {"fill": ["#f2f0f7", "#dadaeb", "#bcbddc", "#9e9ac8"], "edge": ["#bcbddc", "#9e9ac8", "#807dba", "#6a51a3"]},
    {"fill": ["#feedde", "#fdd0a2", "#fdae6b", "#fd8d3c"], "edge": ["#fdae6b", "#fd8d3c", "#f16913", "#d94801"]},
    {"fill": ["#f0f0f0", "#d9d9d9", "#bdbdbd", "#969696"], "edge": ["#bdbdbd", "#969696", "#737373", "#525252"]},
]
```

## Top-Paper Style Families

These palettes are intentionally compact role palettes, not copies from any specific paper.

- `cvpr_qualitative`: saturated blue/orange/green/purple/pink/teal/gray for method columns and qualitative result labels.
- `eccv_lowlevel`: deep blue to light cyan plus orange/green/violet accents for restoration, flow, spectral, and image comparison panels.
- `icml_dense`: muted green/olive/orange/blue/violet for dense benchmark curves, ablation matrices, and metric suites.
- `aaai_geo`: teal/seafoam/sand/orange/red for geospatial maps, uncertainty panels, and social-impact result figures.

Rules:
- For qualitative grids, reserve strong colors for method labels, dividers, callout boxes, or metric badges; do not tint the images themselves unless the data encoding requires it.
- For ablation matrices and uncertainty maps, use sequential colormaps for magnitude and add explicit colorbar labels.
- For pareto plots, use direct labels and one highlighted method instead of a crowded legend.

## Continuous Colormaps

- Matplotlib defaults worth using: `viridis`, `cividis`, `magma`, `inferno`, `plasma`.
- CMasher and Colorcet add many scientific colormaps when installed; use them for specialized sequential/diverging/cyclic needs.
- For heatmaps, choose the colormap based on semantics before aesthetics.
