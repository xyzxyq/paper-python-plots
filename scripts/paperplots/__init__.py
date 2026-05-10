"""Layered plotting helpers for the paper-python-plots skill."""

from .styles import TOP_PAPER_PALETTES, TOP_PAPER_STYLE_NOTES
from .top_paper_plots import (
    ablation_matrix_plot,
    demo_ablation_matrix,
    demo_metric_suite,
    demo_pareto_scatter,
    demo_qual_grid,
    demo_uncertainty_map,
    metric_suite_dashboard,
    pareto_scatter_plot,
    qualitative_result_grid,
    uncertainty_map_plot,
)

__all__ = [
    "TOP_PAPER_PALETTES",
    "TOP_PAPER_STYLE_NOTES",
    "ablation_matrix_plot",
    "demo_ablation_matrix",
    "demo_metric_suite",
    "demo_pareto_scatter",
    "demo_qual_grid",
    "demo_uncertainty_map",
    "metric_suite_dashboard",
    "pareto_scatter_plot",
    "qualitative_result_grid",
    "uncertainty_map_plot",
]
