# Paper Python Plots

[简体中文](README.md) · Publication-ready Python figures for papers, theses, posters, and experiment reports.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-first-11557C?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)
![Codex Skill](https://img.shields.io/badge/Codex-skill-111111?style=flat-square)

**Paper Python Plots** is a Codex skill and Python helper for turning experimental data into polished scientific figures. It keeps the core path lean with Matplotlib, NumPy, and pandas, while optionally adapting installed libraries such as Seaborn, CMasher, Colorcet, and SciencePlots.

It is designed for the figures researchers actually need: benchmark bar charts, raw-sample statistics, training curves, distributions, ablations, Pareto trade-offs, qualitative result grids, uncertainty maps, radial plots, and 3D sensitivity panels.

## Gallery

All images below are generated demos from this repository, not copied paper figures.

| Bar Charts | SEM Palettes | Distribution | Training Curves |
|---|---|---|---|
| ![Bar charts](assets/gallery/demo_bar_charts.png) | ![SEM palettes](assets/gallery/demo_bar_scatter_sem_palettes.png) | ![Distribution](assets/gallery/demo_violin_box_points.png) | ![Training curves](assets/gallery/demo_line_ci.png) |

| Ablation Matrix | Pareto Trade-off | Qualitative Grid | Uncertainty Map |
|---|---|---|---|
| ![Ablation matrix](assets/gallery/demo_ablation_matrix.png) | ![Pareto scatter](assets/gallery/demo_pareto_scatter.png) | ![Qualitative grid](assets/gallery/demo_qual_grid.png) | ![Uncertainty map](assets/gallery/demo_uncertainty_map.png) |

## Why It Looks Different

- **Bar charts by default look like paper benchmark figures**: light gray panels, pastel fills, saturated outlines, error bars, safe in-bar labels, horizontal resource bars, and square color legends.
- **Soft fill + strong edge palettes** preserve the screenshot-inspired aesthetic for distributions, line plots, scatter plots, and multi-panel figures.
- **Top-paper style families** provide reusable visual grammar for CVPR qualitative grids, ICML dense dashboards, AAAI/geospatial uncertainty panels, and low-level vision comparison sheets.
- **Vector-first export** writes PDF/SVG plus high-DPI PNG by default and checks that PNG outputs are nonblank.
- **Optional palette adapters** expose installed Seaborn, CMasher, and Colorcet palettes without making them required dependencies.

## Quick Start

Render the full showcase:

```bash
python scripts/paper_plot.py --demo all --out paper_plot_demo
```

Render the README gallery:

```bash
python scripts/paper_plot.py --demo readme-gallery --out assets/gallery --formats png --dpi 220
```

Render one figure type:

```bash
python scripts/paper_plot.py --demo bars --out paper_plot_demo
python scripts/paper_plot.py --demo sem-palettes --out paper_plot_demo
python scripts/paper_plot.py --demo line --out paper_plot_demo
python scripts/paper_plot.py --demo ablation-matrix --out paper_plot_demo
python scripts/paper_plot.py --demo pareto-scatter --out paper_plot_demo
python scripts/paper_plot.py --demo uncertainty-map --out paper_plot_demo
```

List available styles and palettes:

```bash
python scripts/paper_plot.py --list-styles
python scripts/paper_plot.py --list-palettes
```

## Plot Your Data

Bar chart with raw points and SEM:

```bash
python scripts/paper_plot.py \
  --data results.csv \
  --kind bar \
  --group Method \
  --value Score \
  --out figures
```

Benchmark grid with vertical reward panels and horizontal resource panels:

```bash
python scripts/paper_plot.py \
  --data benchmark.csv \
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

Dense ablation matrix:

```bash
python scripts/paper_plot.py \
  --data ablation.csv \
  --kind ablation-matrix \
  --x Model \
  --series Component \
  --value Score \
  --out figures
```

Outputs are PDF, SVG, and PNG unless `--formats` is specified.

## Style Families

| Style | Best For |
|---|---|
| `rl_benchmark` | Default bar charts and benchmark/resource comparisons. User-facing docs call this simply **Bar Charts**. |
| `paper_showcase` | General top-paper visual polish for mixed plots. |
| `cvpr_qualitative` | Image/result grids, method columns, metric badges, zoom callouts. |
| `icml_dense` | Ablations, training curves, metric dashboards, Pareto trade-offs. |
| `aaai_geo` | Map-like heatmaps, uncertainty panels, geospatial/social-impact results. |
| `nature_minimal` | Restrained journal-like line art. |
| `bio_stats` | Raw-data-visible statistical comparisons. |

## Research-Inspired, Not Copied

The visual system is inspired by public resources such as SciencePlots, tueplots, CMasher, Colorcet, Matplotlib colormaps, Seaborn palettes, ColorBrewer, PyPalettes, and recent top-conference result figures. Raw reference paper figures are local-only and ignored by git.

To build a local reference cache for analysis:

```bash
python scripts/collect_top_paper_figures.py --min-figures 20
```

The cache is written to `research_cache/top_paper_figures/`. Do not publish raw paper PDFs, extracted figures, rendered pages, or contact sheets.

## Use as a Codex Skill

Copy this folder into a Codex skills directory, then ask Codex:

```text
Use $paper-python-plots to turn my dataset into a publication-ready Python figure.
```

The main instructions live in `SKILL.md`; plotting recipes, palette rules, design notes, source links, and export checks live in `references/`.

## License

MIT License.
