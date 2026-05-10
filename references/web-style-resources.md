# Web Style Resources

This reference records public resources used to guide the web-inspired aesthetic pass. Use these as style principles, not as code or figure assets to copy.

## Scientific Style Libraries

- [SciencePlots](https://github.com/garrettj403/SciencePlots): Matplotlib styles for scientific papers, theses, presentations, IEEE-like sizing, CJK-aware examples, and color cycles.
- [tueplots](https://tueplots.readthedocs.io/): lightweight Matplotlib extension for publication-sized figures and conference bundles such as ICML/NeurIPS.

Implementation guidance:

- Keep figure size explicit and final-publication oriented.
- Prefer editable PDF/SVG and high-DPI PNG preview exports.
- Keep text large enough after downscaling into a paper column.
- Do not require LaTeX; use font fallbacks that work in ordinary Python environments.

## Palette and Colormap Resources

- [CMasher](https://cmasher.readthedocs.io/index.html): scientific colormaps for accessible and informative Python plots.
- [Colorcet](https://colorcet.holoviz.org/): perceptually accurate continuous and categorical colormaps.
- [Matplotlib colormap guide](https://matplotlib.org/stable/users/explain/colors/colormaps.html): sequential, diverging, cyclic, qualitative, and perceptually uniform colormap guidance.
- [Seaborn color palettes](https://seaborn.pydata.org/generated/seaborn.color_palette.html): common categorical palettes including deep, muted, bright, pastel, dark, and colorblind.
- [ColorBrewer](https://colorbrewer2.org/): sequential, diverging, and qualitative color advice originally designed for maps but broadly useful for scientific figures.
- [PyPalettes](https://pypi.org/project/pypalettes/): a large Python palette collection inspired by the R palette ecosystem.

Implementation guidance:

- Use categorical palettes for methods, models, groups, and treatments.
- Use sequential palettes for magnitude and uncertainty.
- Use diverging palettes only when the data has a meaningful center such as zero, no-change, or baseline.
- Pair light fills with saturated outlines for paper-style categorical plots.
- Keep optional palette adapters optional; do not make the skill depend on extra plotting packages.

## Applied Defaults in This Skill

- `rl_benchmark` remains the default bar-chart implementation but is described publicly as **Bar Charts / 柱状图**.
- `soft_edge` and `soft_edge_vivid` are the preferred categorical palettes for non-heatmap result figures.
- `scientific_sequential`, CMasher, or Colorcet-inspired colormaps are preferred for heatmaps and uncertainty maps.
- Marker shapes are used for line plots; bar-chart legends use square fill/edge patches.
