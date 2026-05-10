# Export Checklist

Run this before delivering final scientific figures.

## Layout

- No clipped axis labels, tick labels, titles, legends, colorbars, annotations, or panel letters.
- Panel order matches the caption and the scientific story.
- Shared axes and legends are consistent across panels.
- Text is readable at final print size; avoid shrinking after export.
- Long labels are wrapped, abbreviated, or moved into the caption.

## Visual Integrity

- Raw data are visible when sample-level variation matters.
- Error bars are identified as SEM, SD, or CI.
- Axis limits do not hide meaningful variation or exaggerate effects without explanation.
- Color meanings are consistent across panels.
- Proposed/key methods use the same semantic color across related figures.
- Dense benchmark bars have enough edge contrast and, when needed, hatch separation for grayscale print.
- Direct value labels are legible and do not collide with bar tops or panel titles.
- RL benchmark panels have clear title/subtitle spacing, readable vertical method labels, and short-bar labels that do not collide with error caps.
- RL benchmark bar legends use square fill/edge swatches; marker symbols are reserved for line/curve plots.
- Horizontal resource bars show both method names and gray value suffixes without clipping.
- Heatmap colorbar has label and meaningful limits.
- Qualitative grids have readable row/column labels and do not distort images by accidental aspect changes.
- Pareto and dense benchmark direct labels do not collide; label only highlighted methods when the panel is crowded.
- Map/uncertainty panels include calibrated colorbar labels and use colormaps that match the encoded quantity.
- Polar or 3D views are justified by the data structure; otherwise use a clearer 2D alternative.

## Statistics

- Tests match the design: paired/unpaired, one-way/two-way, parametric/nonparametric.
- Multiple-comparison correction is stated when pairwise tests are shown.
- Stars or p-values correspond to the tests actually run.
- Statistical annotations do not overlap data, legends, or panel labels.

## Files

- Save PDF and SVG for editable vector line art.
- Save PNG previews at 300-600 dpi.
- Avoid JPG for final figures.
- Keep script, data transformation, and exported figure reproducible.
- Re-open at least one exported output and check it is nonblank.
