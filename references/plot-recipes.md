# Plot Recipes

Use these compact recipes to pick a figure form before writing code.

## Group Comparisons

**RL benchmark bar grid**
- Use first for RL/AI task comparison figures.
- Put reward/task performance panels on the top row and resource/cost/FPS panels on the bottom row.
- Use light gray axes background, pastel fills, saturated outlines, thin error bars, and vertical in-bar method labels.
- Use horizontal bars for parameter count, FPS, memory, latency, and cost.
- Add one shared bottom legend using square method color swatches; avoid repeating legends inside panels.

**AI benchmark grouped bars**
- Use for methods x metrics tables such as AUROC/AUPRC/accuracy/F1.
- Use a wide canvas; each metric can be its own panel.
- Use blue for the proposed method, greens for strong related methods, red/pink for baseline contrasts, and gray for background references.
- Use black edges, optional hatches, and direct value labels when exact comparison matters.
- Move long method names into a legend panel instead of crowding the x-axis.

**Leaderboard bars**
- Use for a single metric with many methods.
- Sort descending unless the domain has a fixed order.
- Highlight the proposed method in blue and keep alternatives in muted red/pink/neutral colors.
- Add numeric labels above bars when values are close.

**Composition breakdown bars**
- Use for proportions or category composition across groups.
- Normalize to 100% when comparing composition rather than absolute counts.
- Keep the same component color across every panel.

**Bar + raw points + SEM**
- Use when the mean itself is the scientific object.
- Show every sample as a jittered point.
- Encode bars with light fills and darker edges; keep error bars black or dark gray.
- Label whether error bars are SEM, SD, or CI.

**Box/violin + raw points**
- Use when distributions, skew, outliers, or sample size matter.
- Overlay points with partial transparency.
- Use violin only when sample size is large enough for a meaningful density estimate.

**Raincloud**
- Use for polished distribution summaries in manuscripts and talks.
- Combine half-violin/density, box summary, and raw points.
- If PtitPrince is unavailable, approximate with violin + box + jittered points.

## Trends

**Line + SEM/CI ribbon**
- Use for time courses, dose response, training curves, ablations, and repeated x-values.
- Show observed x positions with markers.
- Use consistent colors per group and light ribbons.
- Avoid smoothing unless the model is part of the claim.

**Scatter + model line**
- Use for relationships between two continuous variables.
- Plot raw points first; fit a line only when linearity is reasonable.
- Include sample size and statistic in caption or annotation, not as oversized title text.

## Matrices

**Heatmap**
- Use for correlation, confusion, enrichment, distance, expression, or score matrices.
- Use sequential colormaps for magnitude, diverging colormaps for signed values centered at a meaningful zero.
- Always include a colorbar label with units or score definition.
- Rotate tick labels only as much as needed; abbreviate long names.

**Ablation matrix**
- Use for dense component/configuration results, especially ICML-style ablations.
- Put configurations on rows and metrics/tasks on columns.
- Annotate cell values when the matrix is small enough; otherwise reserve text for row/column labels and highlight extrema.

**Uncertainty map**
- Use for map-like, geospatial, calibration, or uncertainty panels.
- Always include a calibrated colorbar label and avoid rainbow maps unless the domain convention requires them.
- Pair maps with direct region labels only when they do not obscure the encoded values.

## Top-Paper Result Panels

**Qualitative result grid**
- Use for CVPR/ECCV-style image/result panels.
- Arrange rows as examples/tasks and columns as input, baselines, and proposed method.
- Use compact method labels, thin separators, stable aspect ratios, and minimal axes.
- Keep paper reference images local-only; apply the layout to the user's own images.

**Metric suite dashboard**
- Use for multi-metric benchmark summaries such as accuracy, robustness, speed, cost, or latency.
- Give each metric a compact panel with shared method order and direct values.
- Use this for summarized results, not raw distributions.

**Pareto scatter**
- Use for accuracy/cost/latency/model-size tradeoffs.
- Label points directly when there are fewer than roughly 12 methods; otherwise label the highlighted method and frontier.

## Profile And Advanced Views

**Radar comparison**
- Use for 3-8 metrics where each series is a profile rather than a precise ranking.
- Keep series count low; more than 4 profiles usually becomes hard to read.
- Use fills lightly and lines strongly.

**Radial ridge plot**
- Use for comparing several distributions over cyclic or named categories.
- Keep category labels short around the perimeter.
- Do not use if exact area comparison is more important than profile shape.

**3D filled sensitivity plot**
- Use when x, layer, and value are all meaningful and the audience needs a layered sensitivity surface.
- Use Matplotlib `PolyCollection` for filled ridges; keep viewpoint stable and annotate only a few important points.
- Avoid 3D when a heatmap or small-multiple line plot would communicate the pattern more accurately.

## Multi-Panel Figures

- Assign one message per panel.
- Use panel letters `a`, `b`, `c` or `A`, `B`, `C` consistently.
- Align axes and color semantics across panels.
- Use one shared legend when multiple panels show the same groups.
- Prefer constrained layout or subplot mosaic; avoid manual pixel nudging until the final polish pass.
