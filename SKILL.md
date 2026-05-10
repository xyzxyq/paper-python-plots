---
name: paper-python-plots
description: Create publication-ready scientific data figures with Python. Use when Codex needs to plot academic paper, thesis, lab report, manuscript, poster, or presentation results from CSV, Excel, pandas, NumPy, or tabular experimental data using Matplotlib/Seaborn-style workflows; choose chart types, build polished bar charts and benchmark grids, top-conference-style comparisons, multi-panel figures, radar/radial ridge/3D sensitivity plots, statistical annotations, semantic palettes, polished typography/layout, and vector-first PDF/SVG plus high-resolution PNG/TIFF-ready outputs.
---

# Paper Python Plots

## Core Workflow

Use this skill when numeric truth matters and the final output should look like a high-level scientific paper figure. Default bar and benchmark figures to the polished bar-chart style: light gray panels, pastel fills, saturated outlines, in-bar method labels when useful, error bars, compact paper typography, and shared legends.

1. Inspect the data and the claim before plotting.
   Identify variables, units, grouping columns, sample size, missing values, repeated-measures structure, and the exact comparison or trend the figure must communicate.
2. Choose the plot by scientific message.
   Prefer raw-data-visible plots for group comparisons; use line+CI for trajectories; scatter/regression for relationships; heatmaps for matrices; multi-panel layouts for related claims.
3. Use the bundled helper when it saves boilerplate.
   Read or import `scripts/paper_plot.py` for theme setup, palettes, statistics helpers, reusable plot functions, demos, and export QA.
4. Export as editable vector first.
   Save PDF and SVG for line art/text, plus PNG at 300-600 dpi for previews or bitmap workflows. Avoid JPG for final scientific figures.
5. Verify the rendered artifact.
   Open or inspect exported files for clipping, tiny text, missing legends, blank panels, overlapping labels, and misleading axes.

## Plot Choices

- **Bar charts / benchmark bars**: use the current `rl_benchmark` implementation by default, but describe the output as bar charts unless the user explicitly asks for RL/control benchmarks. Prefer multi-panel task grids, vertical labels inside method bars, safe outside labels for very short bars, horizontal bars for parameters/FPS/cost, and bottom shared legends with square color swatches.
- **CVPR qualitative results**: use `cvpr_qualitative` with `qual-grid` for image/result grids, method columns, compact row labels, and thin separators. Do not copy paper figures; use the style grammar on the user's own data/images.
- **ECCV low-level vision**: use `eccv_lowlevel` for restoration, flow, spectral, or dense visual-comparison panels where metric callouts sit near qualitative rows.
- **ICML dense results**: use `icml_dense` for ablation matrices, metric suites, compact benchmark curves, pareto tradeoffs, and multi-metric dashboards.
- **AAAI geospatial/social-impact results**: use `aaai_geo` for map-like heatmaps, uncertainty maps, calibrated colorbars, regional comparisons, and satellite/remote-sensing result panels.
- **AI benchmark comparisons**: use `ai_conference` only when the user wants a stronger modern bar-chart look rather than the lighter RL-paper style.
- **Mean comparisons**: keep the accepted bar+raw points+SEM look: screenshot-style light fills, saturated edges, raw points, and SEM bars. Use it only when the mean is the claim.
- **Distributions**: use the upgraded violin/box/raw-point style with `soft_edge` fill/edge colors, mean diamonds, and restrained grid panels.
- **Time/course or dose response**: use line plots with confidence intervals or SEM ribbons, visible markers, direct end labels, and the screenshot-inspired `soft_edge` palette.
- **Relationships**: use scatter plots with white/soft fills, saturated outlines, direct labels or highlights, and a subdued model line only if justified.
- **Matrices/images**: use perceptually ordered colormaps, readable cell values when the matrix is small, labeled colorbars, and fixed aspect only when the matrix semantics need it.
- **Radar / radial ridge**: use for compact multi-category profiles or cyclic category distributions when a Cartesian chart would hide the pattern.
- **3D sensitivity**: use sparingly for layered sensitivity surfaces where the third axis is meaningful; otherwise prefer a heatmap or faceted 2D lines.
- **Multi-panel figures**: design panels around one argument; keep shared axes, panel letters, legend placement, and color meaning consistent.

## Statistical Handling

- Do not add significance stars automatically. First identify the experimental design, independent/dependent variables, paired vs unpaired samples, and planned comparisons.
- For one-way independent groups, a common workflow is descriptive stats, Shapiro-Wilk per group when sample sizes permit, Levene for variance, then ANOVA+Tukey if assumptions are acceptable or Kruskal-Wallis+Dunn when nonparametric analysis is appropriate.
- Treat p-value annotations as reporting, not decoration. Prefer exact p-values when space allows; use stars only when the target journal or user explicitly wants them.
- If the statistics are uncertain or high-stakes, state the assumption and keep the plotting code separable from the inference code.

## Bundled Resources

- `scripts/paper_plot.py`
  Compatibility CLI and import surface. Run `python scripts/paper_plot.py --demo bars --out <folder>` for the default bar-chart style or `--demo qual-grid|metric-suite|ablation-matrix|pareto-scatter|uncertainty-map` for top-paper-inspired styles. Use `--demo readme-gallery` to regenerate the open-source README gallery. `--demo rl-bars` remains available as a compatibility alias. It can also plot common CSV/TSV/Excel tables directly, for example `python scripts/paper_plot.py --data results.xlsx --kind rl-benchmark-grid --panel Panel --group Method --value Score --subtitle Subtitle --orientation Orientation --error Error --display-value Display --out figures`.
- `scripts/paperplots/`
  Layered implementation modules for style registries, palettes, top-paper plotters, and demo data. Prefer adding new families here rather than expanding the CLI file.
- `scripts/collect_top_paper_figures.py`
  Local-only research collector for downloading public PDFs and rendering/cropping candidate result figures into `research_cache/top_paper_figures/`. The cache is ignored by git and must not be published.
- `references/plot-recipes.md`
  Load when choosing or implementing a figure type.
- `references/palettes.md`
  Load when selecting colors, translating screenshot-inspired palettes, or checking accessibility.
- `references/design-notes.md`
  Load when polishing style, sizing, legend placement, or deciding whether 3D/polar views are justified.
- `references/top-paper-style-corpus.md`
  Load when deciding which top-paper-inspired style family to imitate and what local reference cache was used.
- `references/web-style-resources.md`
  Load when selecting web-inspired scientific plotting resources, optional palette adapters, or README/open-source positioning.
- `references/export-checklist.md`
  Load before final delivery or when journal/publisher constraints matter.

## Implementation Defaults

- Use Matplotlib as the base renderer. Use Seaborn, SciencePlots, statannotations, PtitPrince, CMasher, Colorcet, SciPy, statsmodels, or scikit-posthocs only when installed or when the user approves adding dependencies.
- Expose optional Seaborn, CMasher, and Colorcet palettes when they are already installed; never make them mandatory for the baseline CLI.
- Use the `rl_benchmark` implementation for bar figures by default, while calling it the default bar-chart style in user-facing text.
- Use `soft_edge` for most non-heatmap categorical figures when the user wants the screenshot-like fill/edge aesthetic.
- Use `cvpr_qualitative`, `eccv_lowlevel`, `icml_dense`, or `aaai_geo` when the user references top-conference result figures, image comparison grids, dense ablations, pareto tradeoffs, or uncertainty/map-like outputs.
- For RL/AI benchmark grids, pair `--style rl_benchmark` with `--palette rl_pastel`.
- For RL/AI bar grids, use square fill/edge legend swatches. Reserve marker shapes for line/curve plots that actually draw markers.
- Use semantic colors: blue for proposed/key method, green for gains/improvements, red/pink for baselines or contrasts, neutral gray for references/background, gold for a single highlight.
- Use `layout="constrained"` for new figures where possible. Avoid calling `tight_layout()` after constrained layout unless adapting external code.
- Use Helvetica/Arial-like sans-serif fonts by default and include CJK-capable fallbacks when Chinese labels may appear.
- Keep figures at final publication size from the start; avoid resizing text-heavy plots after export.
- Use color plus hatch/edge/shape/line style differences when series must remain distinguishable in grayscale or color-vision-deficiency contexts.
- Prefer code that saves deterministic outputs: set random seeds for jitter/demo data and keep palette/order explicit.
