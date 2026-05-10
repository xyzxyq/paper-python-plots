# Paper Python Plots

Publication-ready scientific plotting helpers for Codex skills and Python workflows.

This skill focuses on academic figures for papers, theses, lab reports, posters, and presentations. It includes a reusable Matplotlib helper script for RL/AI benchmark bars, grouped comparisons, bar + raw points + SEM, box/violin + points, line + CI, heatmaps, scatter/regression, radar plots, radial ridge plots, 3D sensitivity plots, and top-paper-inspired qualitative/ablation/uncertainty layouts.

## Highlights

- RL benchmark bar style with light gray panels, pastel fills, saturated edges, error bars, safe method labels, horizontal resource bars, and square color-swatch legends.
- Top-conference style families: `cvpr_qualitative`, `eccv_lowlevel`, `icml_dense`, and `aaai_geo`.
- Layered modules under `scripts/paperplots/` for style registries, palettes, plotters, and demo data.
- Publication-oriented defaults for typography, layout, vector-first export, and nonblank output checks.
- Core plotting path uses Matplotlib, NumPy, and pandas only.
- Optional guidance for scientific palettes, export QA, statistical annotations, and multi-panel figure design.

## Quick Start

Render demo figures:

```bash
python scripts/paper_plot.py --demo rl-bars --out paper_plot_demo
python scripts/paper_plot.py --demo qual-grid --out paper_plot_demo
python scripts/paper_plot.py --demo metric-suite --out paper_plot_demo
python scripts/paper_plot.py --demo ablation-matrix --out paper_plot_demo
python scripts/paper_plot.py --demo pareto-scatter --out paper_plot_demo
python scripts/paper_plot.py --demo uncertainty-map --out paper_plot_demo
python scripts/paper_plot.py --demo all --out paper_plot_demo
```

Render an RL benchmark grid from a table:

```bash
python scripts/paper_plot.py \
  --data results.csv \
  --kind rl-benchmark-grid \
  --panel Panel \
  --group Method \
  --value Score \
  --subtitle Subtitle \
  --orientation Orientation \
  --error Error \
  --display-value Display \
  --out figures
```

Outputs are PDF, SVG, and PNG by default.

Build a local-only reference corpus for style analysis:

```bash
python scripts/collect_top_paper_figures.py --min-figures 20
```

The corpus is written to `research_cache/top_paper_figures/` and ignored by git. Do not publish raw paper PDFs, extracted paper figures, rendered pages, or contact sheets; this repository commits only code, generated demos, source links, and style observations.

## Skill Usage

Install or copy this folder into a Codex skills directory, then ask Codex to use `paper-python-plots` for publication-ready Python figures.

The main skill instructions are in `SKILL.md`; plotting recipes, palette rules, design notes, and export checks are in `references/`.

## License

MIT License.
