"""Top-paper inspired style registries.

These dictionaries are intentionally lightweight so the compatibility CLI can
use them without depending on a larger style framework.
"""

TOP_PAPER_PALETTES = {
    "cvpr_qualitative": [
        "#2B6CB0",
        "#DD6B20",
        "#38A169",
        "#805AD5",
        "#D53F8C",
        "#319795",
        "#718096",
    ],
    "eccv_lowlevel": [
        "#1B4965",
        "#5FA8D3",
        "#CAE9FF",
        "#F6AE2D",
        "#F26419",
        "#6A994E",
        "#9D4EDD",
    ],
    "icml_dense": [
        "#3A5A40",
        "#588157",
        "#A3B18A",
        "#DDA15E",
        "#BC6C25",
        "#457B9D",
        "#6D597A",
    ],
    "aaai_geo": [
        "#005F73",
        "#0A9396",
        "#94D2BD",
        "#E9D8A6",
        "#EE9B00",
        "#CA6702",
        "#BB3E03",
    ],
}

WEB_INSPIRED_PALETTES = {
    "soft_edge_vivid": [
        "#6182CC",
        "#41AB5D",
        "#EF3B2C",
        "#807DBA",
        "#F16913",
        "#4EB3D3",
        "#DD3497",
        "#BF812D",
    ],
    "ml_conference": [
        "#1F77B4",
        "#FF7F0E",
        "#2CA02C",
        "#D62728",
        "#9467BD",
        "#8C564B",
        "#17BECF",
        "#7F7F7F",
    ],
    "nature_muted": [
        "#4E79A7",
        "#59A14F",
        "#F28E2B",
        "#E15759",
        "#76B7B2",
        "#B07AA1",
        "#9C755F",
        "#BAB0AC",
    ],
    "colorblind_bright": [
        "#0072B2",
        "#E69F00",
        "#009E73",
        "#D55E00",
        "#CC79A7",
        "#56B4E9",
        "#F0E442",
        "#000000",
    ],
    "scientific_sequential": [
        "#F7FCF0",
        "#E0F3DB",
        "#CCEBC5",
        "#A8DDB5",
        "#7BCCC4",
        "#4EB3D3",
        "#2B8CBE",
        "#08589E",
    ],
}

SOFT_EDGE_PALETTES = [
    {"fill": ["#eef3f8", "#e0eff2", "#c0daf0", "#9dabd0"], "edge": ["#b9d8f7", "#90b8f1", "#6182cc", "#424d95"]},
    {"fill": ["#e5f5e0", "#c7e9c0", "#a1d99b", "#74c476"], "edge": ["#a1d99b", "#74c476", "#41ab5d", "#238b45"]},
    {"fill": ["#fee0d2", "#fcbba1", "#fc9272", "#fb6a4a"], "edge": ["#fc9272", "#fb6a4a", "#ef3b2c", "#cb181d"]},
    {"fill": ["#f2f0f7", "#dadaeb", "#bcbddc", "#9e9ac8"], "edge": ["#bcbddc", "#9e9ac8", "#807dba", "#6a51a3"]},
    {"fill": ["#feedde", "#fdd0a2", "#fdae6b", "#fd8d3c"], "edge": ["#fdae6b", "#fd8d3c", "#f16913", "#d94801"]},
    {"fill": ["#f0f0f0", "#d9d9d9", "#bdbdbd", "#969696"], "edge": ["#bdbdbd", "#969696", "#737373", "#525252"]},
    {"fill": ["#e0f3db", "#ccebc5", "#a8ddb5", "#7bccc4"], "edge": ["#a8ddb5", "#7bccc4", "#4eb3d3", "#2b8cbe"]},
    {"fill": ["#fde0dd", "#fcc5c0", "#fa9fb5", "#f768a1"], "edge": ["#fa9fb5", "#f768a1", "#dd3497", "#ae017e"]},
    {"fill": ["#f6e8c3", "#dfc27d", "#bf812d", "#8c510a"], "edge": ["#dfc27d", "#bf812d", "#8c510a", "#543005"]},
    {"fill": ["#e0f3f8", "#abd9e9", "#74add1", "#4575b4"], "edge": ["#abd9e9", "#74add1", "#4575b4", "#313695"]},
    {"fill": ["#f1eef6", "#d7b5d8", "#df65b0", "#ce1256"], "edge": ["#d7b5d8", "#df65b0", "#ce1256", "#91003f"]},
    {"fill": ["#f7fcb9", "#addd8e", "#31a354", "#006837"], "edge": ["#addd8e", "#31a354", "#006837", "#004529"]},
    {"fill": ["#bfd3e6", "#9ebcda", "#8c96c6", "#8856a7"], "edge": ["#9ebcda", "#8c96c6", "#8856a7", "#810f7c"]},
    {"fill": ["#fef0d9", "#fdcc8a", "#fc8d59", "#e34a33"], "edge": ["#fdcc8a", "#fc8d59", "#e34a33", "#b30000"]},
    {"fill": ["#edf8b1", "#7fcdbb", "#41b6c4", "#225ea8"], "edge": ["#7fcdbb", "#41b6c4", "#225ea8", "#081d58"]},
    {"fill": ["#fde0dd", "#fa9fb5", "#e7298a", "#c51b7d"], "edge": ["#fa9fb5", "#e7298a", "#c51b7d", "#8e0152"]},
    {"fill": ["#ffff7b", "#fec44f", "#d95f0e", "#993404"], "edge": ["#fec44f", "#d95f0e", "#993404", "#662506"]},
    {"fill": ["#e5f5f9", "#99d8c9", "#2ca25f", "#006d2c"], "edge": ["#99d8c9", "#2ca25f", "#006d2c", "#00441b"]},
]

SOFT_EDGE_FILLS = [color for block in SOFT_EDGE_PALETTES for color in block["fill"]]
SOFT_EDGE_EDGES = [color for block in SOFT_EDGE_PALETTES for color in block["edge"]]

TOP_PAPER_STYLE_NOTES = {
    "cvpr_qualitative": "Image/result grids with method columns, compact row labels, and thin separators.",
    "eccv_lowlevel": "Low-level vision panels with qualitative strips, metric callouts, and image-friendly spacing.",
    "icml_dense": "Dense benchmark plots with compact axes, small multiples, and direct labels.",
    "aaai_geo": "Geospatial/social-impact style with maps, calibrated colorbars, and uncertainty panels.",
}

WEB_STYLE_NOTES = {
    "SciencePlots": "Paper-style Matplotlib rcParams and journal-like sizing; useful inspiration for compact typography and vector-first exports.",
    "tueplots": "Publication bundle presets for venues such as ICML/NeurIPS; useful inspiration for explicit figure dimensions.",
    "CMasher/Colorcet": "Perceptually informed scientific colormaps for heatmaps, uncertainty maps, and continuous fields.",
    "Seaborn/ColorBrewer/PyPalettes": "Accessible categorical, sequential, and diverging palette families; useful as optional palette adapters.",
}
