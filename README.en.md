# Paper Python Plots

[简体中文](README.md) · A Python / Codex skill for turning experimental data into publication-ready scientific figures.

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?style=flat-square&logo=python&logoColor=white)
![Matplotlib](https://img.shields.io/badge/Matplotlib-first-11557C?style=flat-square)
![Codex Skill](https://img.shields.io/badge/Codex-skill-111111?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

**Paper Python Plots** is a Codex skill and Python helper for papers, theses, experiment reports, posters, and lab presentations. It helps Codex inspect your data, choose a figure type, generate reusable Python plotting code, and export editable publication assets.

The baseline path stays lightweight: **Matplotlib + NumPy + pandas**. If Seaborn, CMasher, Colorcet, or SciencePlots are already installed, the skill can use them as optional palette/style enhancements.

## Gallery

All images below are generated demos from this repository, not copied paper figures.

| Bar Charts | SEM Palettes | Distribution | Training Curves |
|---|---|---|---|
| ![Bar charts](assets/gallery/demo_bar_charts.png) | ![SEM palettes](assets/gallery/demo_bar_scatter_sem_palettes.png) | ![Distribution](assets/gallery/demo_violin_box_points.png) | ![Training curves](assets/gallery/demo_line_ci.png) |

| Ablation Matrix | Pareto Trade-off | Qualitative Grid | Uncertainty Map |
|---|---|---|---|
| ![Ablation matrix](assets/gallery/demo_ablation_matrix.png) | ![Pareto scatter](assets/gallery/demo_pareto_scatter.png) | ![Qualitative grid](assets/gallery/demo_qual_grid.png) | ![Uncertainty map](assets/gallery/demo_uncertainty_map.png) |

## When To Use It

- You have CSV, Excel, pandas, or NumPy data and need a paper-style result figure.
- You are unsure whether to use bars, rainclouds, training curves, heatmaps, Pareto plots, or multi-panel layouts.
- You want raw points, SEM/CI, statistical annotations, direct labels, consistent palettes, and vector exports.
- You want Codex to write reusable Python plotting code based on a target paper style.
- You want top-conference-inspired layout principles without copying copyrighted paper figures.

## Install As A Codex Skill

Clone this repository into your Codex skills directory:

```powershell
cd C:\Users\<your-user-name>\.codex\skills
git clone https://github.com/xyzxyq/paper-python-plots.git
```

Or copy the whole folder to:

```text
C:\Users\<your-user-name>\.codex\skills\paper-python-plots
```

Then start a new Codex conversation and ask:

```text
Use $paper-python-plots to turn my dataset into a publication-ready Python figure.
```

You can also use the CLI directly:

```bash
python scripts/paper_plot.py --demo readme-gallery --out assets/gallery --formats png --dpi 220
python scripts/paper_plot.py --list-styles
python scripts/paper_plot.py --list-palettes
```

## Prompting Guide

A good prompt includes: **data location + scientific claim + figure style + export requirements**.

```text
Use $paper-python-plots.
My data is in results.xlsx. Use Method, Dataset, Score, and SEM.
The main claim is that Ours outperforms the baselines across datasets.
Use the default bar-chart style, export PDF/SVG/PNG, and give me reusable Python code.
```

If you do not know which plot to use:

```text
Use $paper-python-plots.
First inspect this CSV and decide the best publication figure type.
Prefer raw-data-visible plots and add SEM/CI only when justified.
Do not hide the sample distribution just to make the figure cleaner.
```

## Style-Specific Prompts

| Goal | Prompt |
|---|---|
| Default benchmark bars | `Use the default bar-chart style: light gray panels, pastel fills, saturated edges, error bars, shared legend, and paper benchmark layout.` |
| Raw Points + SEM | `Draw Bar + Raw Points + SEM with light fills, strong edges, all raw samples, mean bars, and SEM error bars.` |
| Distribution | `Draw a high-quality distribution figure, preferably raincloud or violin + box + raw points, with sample size and mean/median markers.` |
| Training curves | `Draw top-conference-style training curves with mean lines, CI ribbons, markers, endpoint labels, and a shared legend.` |
| Ablation | `Draw an ICML-style ablation matrix with cell values, relative gains, and outlined best values.` |
| Pareto trade-off | `Draw a Pareto trade-off plot with cost/latency on x, performance on y, Pareto frontier, highlighted key methods, and parameter-size bubbles.` |
| Qualitative grid | `Draw a CVPR-style qualitative grid with examples as rows, methods as columns, metric badges, and zoom/callout boxes.` |
| Uncertainty map | `Draw an AAAI/geospatial-style uncertainty map with prediction, uncertainty, residual panels, and compact colorbars.` |

## Figure And Style Cheatsheet

| Name | Best For |
|---|---|
| `--demo bars` | Default bar charts for benchmark, method comparison, and resource results. |
| `--demo sem-palettes` | Raw Points + SEM palette families. |
| `--demo violin` | Raincloud-style distribution plots. |
| `--demo line` | Training curves and trends. |
| `--demo pareto-scatter` | Performance-cost trade-offs. |
| `--demo ablation-matrix` | Ablation matrices and table-like heatmaps. |
| `--demo qual-grid` | Qualitative image/result comparisons. |
| `--demo uncertainty-map` | Prediction, uncertainty, residual, and map-like panels. |

| Style | Best For |
|---|---|
| `rl_benchmark` | Default bar-chart style. The name is kept for compatibility; user-facing docs call it Bar Charts. |
| `paper_showcase` | General top-paper visual polish. |
| `cvpr_qualitative` | Qualitative grids, method columns, metric badges, and zoom callouts. |
| `icml_dense` | Training curves, ablation matrices, metric suites, and Pareto trade-offs. |
| `aaai_geo` | Map-like heatmaps, uncertainty panels, remote-sensing/social-impact results. |
| `nature_minimal` | Restrained journal-style line art. |
| `bio_stats` | Raw-data-visible statistical experiment figures. |

## CLI Examples

Render the full showcase:

```bash
python scripts/paper_plot.py --demo all --out paper_plot_demo
```

Render a bar chart from a table:

```bash
python scripts/paper_plot.py \
  --data results.csv \
  --kind bar \
  --group Method \
  --value Score \
  --out figures
```

Render a benchmark grid:

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

Render an ablation matrix:

```bash
python scripts/paper_plot.py \
  --data ablation.csv \
  --kind ablation-matrix \
  --x Model \
  --series Component \
  --value Score \
  --out figures
```

The default export set is `PDF + SVG + PNG`. To export PNG only:

```bash
python scripts/paper_plot.py --demo bars --out paper_plot_demo --formats png
```

## Suggested Data Columns

- Group comparison: `Group` / `Method` / `Condition` + `Value`.
- Error-bar bars: `Method`, `Score`, `SEM` or `Error`.
- Training curves: `Step`, `Score`, `Method`, with repeated rows per step when available.
- Ablation matrix: `Component`, `Model`, `Score`.
- Pareto plot: `Method`, `Latency` / `Cost`, `Score`, optional `Params`.
- Multi-panel figures: add `Panel`, `Subtitle`, `Orientation`, or similar columns.

## Design Principles

- The chart type should serve the scientific claim, not decoration.
- Show raw data whenever possible.
- Use light fills plus strong edges for screen and print clarity.
- Check for clipped labels, crowded legends, overlapping annotations, and colorbar issues.
- Export PDF/SVG first; use PNG as a preview or bitmap workflow output.
- Do not copy paper figures; imitate layout, hierarchy, color logic, and information density.

## Local Reference Corpus

To build a local-only reference corpus:

```bash
python scripts/collect_top_paper_figures.py --min-figures 20
```

The cache is written to `research_cache/top_paper_figures/`, which is ignored by git. Do not publish raw paper PDFs, extracted figures, rendered pages, or contact sheets.

## License

MIT License.
