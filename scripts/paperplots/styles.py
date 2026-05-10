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

TOP_PAPER_STYLE_NOTES = {
    "cvpr_qualitative": "Image/result grids with method columns, compact row labels, and thin separators.",
    "eccv_lowlevel": "Low-level vision panels with qualitative strips, metric callouts, and image-friendly spacing.",
    "icml_dense": "Dense benchmark plots with compact axes, small multiples, and direct labels.",
    "aaai_geo": "Geospatial/social-impact style with maps, calibrated colorbars, and uncertainty panels.",
}
