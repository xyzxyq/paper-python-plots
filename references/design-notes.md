# Design Notes

## Bar Chart Default

Use `--demo bars` or the `rl_benchmark` implementation for default bar charts, benchmark grids, method comparisons, and sample-efficiency figures. Call the output a bar chart unless the user's domain is explicitly RL/control/robotics. This style favors:

- light gray plot panels on a white page,
- pastel bar fills with saturated same-hue outlines,
- compact serif-like typography,
- in-bar vertical method labels,
- thin error bars,
- horizontal bars for parameters, FPS, latency, cost, or memory,
- one bottom shared legend with square color swatches for bar grids.

Use `--demo bars` to inspect the default bar aesthetic; `--demo rl-bars` remains as a compatibility alias.
Keep title and subtitle as two distinct lines; if a vertical bar is too short, move its method label outside the bar rather than letting it collide with the error cap.

## Screenshot Soft-Edge Palette

Use `soft_edge` for most non-heatmap categorical figures when the user wants the screenshot-inspired look: light fills, saturated outlines, white raw points, and readable direct labels. Sample across hue families for multi-group plots instead of using several neighboring shades of one color.

## AI-Conference Alternative

Use `--style ai_conference` for ML, AI, benchmark, and systems-paper figures. This style favors:

- Helvetica/Arial-like sans-serif typography.
- Larger labels than journal micro-panels.
- Strong left/bottom axes and black bar edges.
- Frameless legends.
- Wide layouts for multi-metric comparison.
- Direct value labels on bars when small differences matter.

## Wide Panels

Use a wide canvas when comparing many methods across metrics. A 3-4x width-to-height ratio is acceptable for benchmark strips. Put each metric in its own panel when y-ranges differ.

## Legend Panels

Use a dedicated legend panel when:

- method names are long,
- there are more than 5 series,
- legends would cover data,
- x tick labels would become unreadable.

## Direct Labels

Direct bar labels work best for leaderboard and metric panels. Keep the format consistent, usually two decimals for normalized scores. Do not label every point in dense scatter or distribution plots.

## Polar And 3D Restraint

Radar, radial ridge, and 3D sensitivity plots are attention-grabbing, but they should earn their place:

- Use radar for profile shape, not exact ranking.
- Use radial ridge for cyclic/named category distributions.
- Use 3D only when the layer dimension is part of the scientific story.
- If precision is the priority, fall back to heatmaps, faceted line plots, or grouped bars.
