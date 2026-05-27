# figures4papers Integration

Use this reference when the user asks for ChenLiu-1996/figures4papers style or when a project-specific `figure_*` script should be converted into a reusable paper-python-plots workflow.

Source repository: <https://github.com/ChenLiu-1996/figures4papers>

Inspected source revision during integration: `ebebf0e Update README.md`.

## What To Reuse

- Minimalist Matplotlib cleanup: top/right spines off, frameless legends, explicit font and spine widths, editable vector text.
- Semantic palette: dark blue for the key method, greens for improvements, reds/pinks for contrasts, neutral gray for references, gold for one callout.
- Strong bar encoding: black bar edges, direct value labels, optional hatches, and tightened y-ranges when all scores occupy a narrow band.
- Layout patterns: ultra-wide multi-metric bars, legend-only axes for long method lists, and consistent per-panel typography.
- Export policy: PDF/SVG first, PNG preview at 300 dpi, and 600 dpi for dense bar panels.
- Pattern coverage: grouped bars, trend lines, heatmaps, radar/polar comparisons, conceptual sphere/geometry panels, and multi-panel comparison layouts.

## What Not To Reuse

- Do not copy figures, assets, paper-specific data, or exact claims from the source repo into user outputs.
- Do not force LaTeX rendering unless the environment has LaTeX and math-rich labels require it.
- Do not use wide/tight y-ranges if the scientific claim needs a zero baseline or absolute scale.
- Do not treat project scripts as a universal package API; this skill provides the reusable API in `scripts/paperplots/figures4papers.py`.

## Recommended API

Use the helper module when the requested figure should visibly match the figures4papers house style:

```python
from paperplots.figures4papers import (
    Figures4PapersStyle,
    apply_figures4papers_style,
    create_subplots,
    finalize_figure,
    make_grouped_bar,
)

apply_figures4papers_style(Figures4PapersStyle(font_size=16, axes_linewidth=2.5))
fig, axes = create_subplots(1, 1, figsize=(8, 4))
make_grouped_bar(
    axes[0],
    ["AUROC", "AUPRC", "PPVn"],
    [[0.54, 0.22, 0.21], [0.79, 0.70, 0.45]],
    ["Baseline", "Ours"],
    ylabel="Score",
    annotate=True,
)
finalize_figure(fig, "figures/method_comparison", formats=["pdf", "svg", "png"], dpi=300)
```

Use the CLI demo for visual checking:

```bash
python scripts/paper_plot.py --demo figures4papers --out figures4papers_demo --formats png,pdf
python scripts/paper_plot.py --style figures4papers --palette figures4papers --list-styles
```

## Routing

- Use `figures4papers` for direct requests to match that repository, top-venue manuscript bar/trend/heatmap panels, or when long method lists need legend-only axes and strong edge encodings.
- Use the existing default `bars`/`rl_benchmark` style for lightweight benchmark grids and RL/control examples.
- Use `nn_report` for neural-network, OCR, classification, error-reduction, and training-report figures.
- Use `cvpr_qualitative`, `eccv_lowlevel`, `icml_dense`, or `aaai_geo` when the figure is closer to image grids, dense ablations, Pareto dashboards, or geospatial/uncertainty panels.
