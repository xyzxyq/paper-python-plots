"""Small deterministic demo tables for top-paper inspired plots."""

from __future__ import annotations

import numpy as np
import pandas as pd


def metric_suite_table() -> pd.DataFrame:
    methods = ["Base", "Aug", "Ours-S", "Ours-L"]
    metrics = ["Acc.", "Robust", "Speed"]
    values = np.array([[0.72, 0.61, 0.83], [0.76, 0.66, 0.74], [0.82, 0.71, 0.69], [0.86, 0.78, 0.62]])
    return pd.DataFrame(
        [{"method": method, "metric": metric, "value": float(values[i, j])} for i, method in enumerate(methods) for j, metric in enumerate(metrics)]
    )
