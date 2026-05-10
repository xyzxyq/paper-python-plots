# Top-Paper Style Corpus

This skill uses a local-only research cache to study result-figure style from recent top-conference papers. The cache lives at `research_cache/top_paper_figures/` and is ignored by git. Do not commit raw PDFs, rendered paper pages, cropped figures, or contact sheets.

## Source Basis

- CVPR 2025 award/proceedings pages: <https://cvpr.thecvf.com/Conferences/2025/BestPapersDemos>
- ECCV 2024 awards/proceedings pages: <https://eccv.ecva.net/Conferences/2024/Awards>
- ICML 2025 awards/poster pages: <https://icml.cc/virtual/2025/awards_detail>
- AAAI 2026 outstanding paper note: <https://aihub.org/2026/01/22/congratulations-to-the-aaai2026-outstanding-paper-award-winners/>

## Local Collection Workflow

Run:

```bash
python scripts/collect_top_paper_figures.py --min-figures 20
```

The collector downloads public PDFs where available, renders selected figure-heavy pages with `pdftoppm`, auto-crops white margins with Pillow, writes `metadata.json`/`metadata.csv`, and creates a local contact sheet. The extracted files are for local visual analysis only.

## Papers And Style Notes

| Venue | Paper | Style Family | Observations |
| --- | --- | --- | --- |
| CVPR 2025 | VGGT: Visual Geometry Grounded Transformer | `cvpr_qualitative` | Large qualitative panels, repeated method columns, compact captions, restrained separators. |
| CVPR 2025 | MegaSaM | `cvpr_qualitative` | Video/geometry rows, reconstruction comparisons, metric callouts near visual evidence. |
| CVPR 2025 | Navigation World Models | `cvpr_qualitative` | Sequential image results, clean model-output columns, spatial examples. |
| CVPR 2025 | Molmo and PixMo | `cvpr_qualitative` | Multimodal qualitative examples, benchmark summaries, high information density. |
| ECCV 2024 | Minimalist Vision with Freeform Pixels | `eccv_lowlevel` | Low-level vision comparisons with image crops and quantitative callouts. |
| ECCV 2024 | SEA-RAFT | `eccv_lowlevel` | Optical-flow examples, color-coded fields, dense tables/curves. |
| ECCV 2024 | PointLLM | `eccv_lowlevel` | 3D examples mixed with compact method comparisons. |
| ECCV 2024 | Latent Diffusion Prior Enhanced Deep Unfolding | `eccv_lowlevel` | Restoration panels, PSNR/SSIM-like labels, qualitative grids. |
| ICML 2025 | Train for the Worst, Plan for the Best | `icml_dense` | Dense ablations, small-multiple benchmark curves, direct labels. |
| ICML 2025 | CollabLLM | `icml_dense` | Benchmark dashboards, model comparisons, compact legends. |
| ICML 2025 | The Value of Prediction in Identifying the Worst-Off | `icml_dense` | Theory plus experiment panels, uncertainty/calibration framing. |
| ICML 2025 | Conformal Prediction as Bayesian Quadrature | `icml_dense` | Calibration and uncertainty plots with compact axes. |
| AAAI 2026 | PlantTraitNet | `aaai_geo` | Applied multimodal and uncertainty-aware result panels. |
| AAAI 2026 | Generalizable Slum Detection from Satellite Imagery with Mixture-of-Experts | `aaai_geo` | Geospatial heatmaps, map-like panels, calibrated uncertainty cues. |

## Style Families

- `cvpr_qualitative`: image/result grids, method columns, row labels, thin dividers, minimal axes.
- `eccv_lowlevel`: image restoration/flow/spectral panels, metric callouts, side-by-side qualitative evidence.
- `icml_dense`: compact benchmark curves, ablation matrices, pareto scatter plots, multi-metric dashboards.
- `aaai_geo`: map/heatmap panels, uncertainty overlays, calibrated colorbars, region-aware labeling.

## Copyright Boundary

Use this corpus to extract style principles, not to copy exact paper figures. Public repository contents should include source links and observations only; raw figures and PDFs remain local.
