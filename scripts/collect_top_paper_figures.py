#!/usr/bin/env python3
"""Collect a local-only top-paper figure corpus for style study.

The script downloads public paper PDFs, renders selected figure-heavy pages,
auto-crops white margins, and writes metadata/contact sheets under
``research_cache/top_paper_figures``. The cache is intentionally ignored by git:
raw paper figures should be used for local visual analysis, not redistributed.
"""

from __future__ import annotations

import argparse
import csv
from dataclasses import dataclass
import json
from pathlib import Path
import shutil
import subprocess
import sys
import textwrap
import urllib.error
import urllib.request

from PIL import Image, ImageChops


@dataclass(frozen=True)
class PaperSpec:
    slug: str
    title: str
    venue: str
    source_url: str
    pdf_url: str
    pages: tuple[int, int]
    style_family: str
    figure_notes: str


PAPERS = [
    PaperSpec(
        "cvpr2025_vggt",
        "VGGT: Visual Geometry Grounded Transformer",
        "CVPR 2025",
        "https://openaccess.thecvf.com/content/CVPR2025/html/Wang_VGGT_Visual_Geometry_Grounded_Transformer_CVPR_2025_paper.html",
        "https://arxiv.org/pdf/2503.11651",
        (1, 5),
        "cvpr_qualitative",
        "Large qualitative geometry panels, method comparisons, compact captions.",
    ),
    PaperSpec(
        "cvpr2025_megasam",
        "MegaSaM: Accurate, Fast, and Robust Structure and Motion from Casual Dynamic Videos",
        "CVPR 2025",
        "https://openaccess.thecvf.com/content/CVPR2025/html/Li_MegaSaM_Accurate_Fast_and_Robust_Structure_and_Motion_from_Casual_CVPR_2025_paper.html",
        "https://arxiv.org/pdf/2412.04463",
        (1, 6),
        "cvpr_qualitative",
        "Video reconstruction comparison grids with metric callouts.",
    ),
    PaperSpec(
        "cvpr2025_navigation_world_models",
        "Navigation World Models",
        "CVPR 2025",
        "https://openaccess.thecvf.com/content/CVPR2025/html/Bar_Navigation_World_Models_CVPR_2025_paper.html",
        "https://openaccess.thecvf.com/content/CVPR2025/papers/Bar_Navigation_World_Models_CVPR_2025_paper.pdf",
        (1, 4),
        "cvpr_qualitative",
        "Image sequence result rows and clean model/output columns.",
    ),
    PaperSpec(
        "cvpr2025_molmo_pixmo",
        "Molmo and PixMo: Open Weights and Open Data for State-of-the-Art Multimodal Models",
        "CVPR 2025",
        "https://arxiv.org/abs/2409.17146",
        "https://arxiv.org/pdf/2409.17146",
        (1, 8),
        "cvpr_qualitative",
        "Multimodal result tables, qualitative screenshots, and benchmark panels.",
    ),
    PaperSpec(
        "eccv2024_minimalist_vision",
        "Minimalist Vision with Freeform Pixels",
        "ECCV 2024",
        "https://eccv.ecva.net/virtual/2024/poster/914",
        "https://cave.cs.columbia.edu/Statics/publications/pdfs/Klotz_ECCV24.pdf",
        (1, 5),
        "eccv_lowlevel",
        "Low-level vision style with image/metric juxtaposition.",
    ),
    PaperSpec(
        "eccv2024_sea_raft",
        "SEA-RAFT: Simple, Efficient, Accurate RAFT for Optical Flow",
        "ECCV 2024",
        "https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/1065_ECCV_2024_paper.php",
        "https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/01065.pdf",
        (1, 6),
        "eccv_lowlevel",
        "Optical-flow qualitative rows and dense benchmark tables.",
    ),
    PaperSpec(
        "eccv2024_pointllm",
        "PointLLM: Empowering Large Language Models to Understand Point Clouds",
        "ECCV 2024",
        "https://www.ecva.net/papers/eccv_2024/papers_ECCV/html/3601_ECCV_2024_paper.php",
        "https://www.ecva.net/papers/eccv_2024/papers_ECCV/papers/03601.pdf",
        (1, 7),
        "eccv_lowlevel",
        "3D/point-cloud qualitative examples with compact result tables.",
    ),
    PaperSpec(
        "eccv2024_ldp_deep_unfolding",
        "Latent Diffusion Prior Enhanced Deep Unfolding for Snapshot Compressive Imaging",
        "ECCV 2024",
        "https://arxiv.org/abs/2311.14280",
        "https://arxiv.org/pdf/2311.14280",
        (1, 5),
        "eccv_lowlevel",
        "Restoration comparison grids with PSNR/SSIM-style callouts.",
    ),
    PaperSpec(
        "icml2025_train_worst_plan_best",
        "Train for the Worst, Plan for the Best: Understanding Token Ordering in Masked Diffusions",
        "ICML 2025",
        "https://icml.cc/virtual/2025/poster/46605",
        "https://arxiv.org/pdf/2502.06768",
        (1, 6),
        "icml_dense",
        "Dense ablation and benchmark curves with direct comparisons.",
    ),
    PaperSpec(
        "icml2025_collabllm",
        "CollabLLM: From Passive Responders to Active Collaborators",
        "ICML 2025",
        "https://arxiv.org/abs/2502.00640",
        "https://arxiv.org/pdf/2502.00640",
        (1, 5),
        "icml_dense",
        "Model comparison dashboards and compact multi-metric panels.",
    ),
    PaperSpec(
        "icml2025_prediction_worst_off",
        "The Value of Prediction in Identifying the Worst-Off",
        "ICML 2025",
        "https://arxiv.org/abs/2501.19334",
        "https://arxiv.org/pdf/2501.19334",
        (1, 4),
        "icml_dense",
        "Theory/experiment panels with calibration-like summaries.",
    ),
    PaperSpec(
        "icml2025_conformal_bayesian_quadrature",
        "Conformal Prediction as Bayesian Quadrature",
        "ICML 2025",
        "https://arxiv.org/abs/2502.13228",
        "https://arxiv.org/pdf/2502.13228",
        (1, 5),
        "icml_dense",
        "Compact uncertainty curves and calibration visualizations.",
    ),
    PaperSpec(
        "aaai2026_planttraitnet",
        "PlantTraitNet: Uncertainty-Aware Multimodal Learning for Plant Trait Prediction",
        "AAAI 2026",
        "https://ojs.aaai.org/index.php/AAAI/article/view/35144",
        "https://arxiv.org/pdf/2511.06943",
        (1, 6),
        "aaai_geo",
        "Applied multimodal panels with uncertainty and trait maps.",
    ),
    PaperSpec(
        "aaai2026_generalizable_slum_detection",
        "Generalizable Slum Detection from Satellite Imagery with Mixture-of-Experts",
        "AAAI 2026",
        "https://ojs.aaai.org/index.php/AAAI/article/view/35257",
        "https://arxiv.org/pdf/2511.10300",
        (1, 5),
        "aaai_geo",
        "Geospatial heatmaps, satellite/image panels, and uncertainty cues.",
    ),
]


def _request(url: str) -> urllib.request.Request:
    return urllib.request.Request(
        url,
        headers={
            "User-Agent": "paper-python-plots local research collector/1.0",
            "Accept": "application/pdf,*/*",
        },
    )


def download(url: str, path: Path, force: bool = False) -> bool:
    if path.exists() and path.stat().st_size > 10_000 and not force:
        return True
    try:
        with urllib.request.urlopen(_request(url), timeout=60) as response:
            data = response.read()
    except (urllib.error.URLError, TimeoutError) as exc:
        print(f"[warn] download failed: {url} ({exc})", file=sys.stderr)
        return False
    if len(data) < 10_000:
        print(f"[warn] suspiciously small PDF response: {url}", file=sys.stderr)
        return False
    path.write_bytes(data)
    return True


def find_pdftoppm(explicit: str | None = None) -> str:
    candidates = [explicit] if explicit else []
    candidates.extend(
        [
            shutil.which("pdftoppm"),
            r"C:\texlive\2025\bin\windows\pdftoppm.exe",
            r"C:\Program Files\poppler\Library\bin\pdftoppm.exe",
        ]
    )
    for candidate in candidates:
        if candidate and Path(candidate).exists():
            return str(candidate)
    raise RuntimeError("pdftoppm was not found. Install Poppler or pass --pdftoppm.")


def crop_whitespace(image_path: Path, output_path: Path, padding: int = 12) -> None:
    image = Image.open(image_path).convert("RGB")
    bg = Image.new("RGB", image.size, "white")
    diff = ImageChops.difference(image, bg)
    bbox = diff.getbbox()
    if bbox:
        left, top, right, bottom = bbox
        left = max(0, left - padding)
        top = max(0, top - padding)
        right = min(image.width, right + padding)
        bottom = min(image.height, bottom + padding)
        image = image.crop((left, top, right, bottom))
    image.save(output_path)


def render_page(pdftoppm: str, pdf_path: Path, page: int, raw_output: Path, dpi: int) -> bool:
    prefix = raw_output.with_suffix("")
    cmd = [pdftoppm, "-png", "-r", str(dpi), "-f", str(page), "-l", str(page), "-singlefile", str(pdf_path), str(prefix)]
    result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=False)
    if result.returncode != 0:
        print(f"[warn] render failed {pdf_path.name} page {page}: {result.stderr.strip()}", file=sys.stderr)
        return False
    return raw_output.exists()


def make_contact_sheet(images: list[Path], output: Path, thumb_width: int = 360) -> None:
    if not images:
        return
    thumbs: list[Image.Image] = []
    for image_path in images:
        image = Image.open(image_path).convert("RGB")
        ratio = thumb_width / image.width
        thumb = image.resize((thumb_width, max(1, int(image.height * ratio))))
        thumbs.append(thumb)
    columns = 4
    rows = (len(thumbs) + columns - 1) // columns
    cell_height = max(thumb.height for thumb in thumbs) + 34
    sheet = Image.new("RGB", (columns * thumb_width, rows * cell_height), "white")
    for i, thumb in enumerate(thumbs):
        x = (i % columns) * thumb_width
        y = (i // columns) * cell_height
        sheet.paste(thumb, (x, y))
    sheet.save(output)


def collect(args: argparse.Namespace) -> int:
    out = Path(args.out)
    pdf_dir = out / "pdfs"
    raw_dir = out / "rendered_pages"
    figure_dir = out / "figures"
    for folder in [pdf_dir, raw_dir, figure_dir]:
        folder.mkdir(parents=True, exist_ok=True)

    pdftoppm = find_pdftoppm(args.pdftoppm)
    records: list[dict[str, object]] = []
    figure_paths: list[Path] = []

    for paper in PAPERS:
        pdf_path = pdf_dir / f"{paper.slug}.pdf"
        if not args.skip_download:
            ok = download(paper.pdf_url, pdf_path, force=args.force)
            if not ok:
                continue
        elif not pdf_path.exists():
            print(f"[warn] missing cached PDF: {pdf_path}", file=sys.stderr)
            continue

        for idx, page in enumerate(paper.pages, start=1):
            raw_page = raw_dir / f"{paper.slug}_p{page}.png"
            figure_path = figure_dir / f"{paper.slug}_fig{idx:02d}_p{page}.png"
            if render_page(pdftoppm, pdf_path, page, raw_page, args.dpi):
                crop_whitespace(raw_page, figure_path)
                figure_paths.append(figure_path)
                records.append(
                    {
                        "slug": paper.slug,
                        "title": paper.title,
                        "venue": paper.venue,
                        "style_family": paper.style_family,
                        "source_url": paper.source_url,
                        "pdf_url": paper.pdf_url,
                        "page": page,
                        "local_figure": str(figure_path),
                        "notes": paper.figure_notes,
                    }
                )

    metadata_json = out / "metadata.json"
    metadata_json.write_text(json.dumps(records, indent=2, ensure_ascii=False), encoding="utf-8")

    metadata_csv = out / "metadata.csv"
    if records:
        with metadata_csv.open("w", newline="", encoding="utf-8") as handle:
            writer = csv.DictWriter(handle, fieldnames=list(records[0]))
            writer.writeheader()
            writer.writerows(records)

    make_contact_sheet(figure_paths, out / "contact_sheet.png")
    summary = textwrap.dedent(
        f"""\
        # Local Top-Paper Figure Corpus

        Figures collected: {len(figure_paths)}
        Papers attempted: {len(PAPERS)}

        This directory is a local research cache. Do not commit raw PDFs,
        rendered paper pages, extracted/cropped figures, or contact sheets.
        """
    )
    (out / "README.md").write_text(summary, encoding="utf-8")

    if len(figure_paths) < args.min_figures:
        print(f"[error] only collected {len(figure_paths)} figures, below --min-figures={args.min_figures}", file=sys.stderr)
        return 2
    print(f"Collected {len(figure_paths)} local figure candidates in {figure_dir}")
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Build a local-only corpus of top-paper figure candidates.")
    parser.add_argument("--out", default="research_cache/top_paper_figures", help="Local cache directory.")
    parser.add_argument("--min-figures", type=int, default=20, help="Fail if fewer figure files are collected.")
    parser.add_argument("--dpi", type=int, default=150, help="PDF render DPI.")
    parser.add_argument("--pdftoppm", help="Optional path to pdftoppm executable.")
    parser.add_argument("--skip-download", action="store_true", help="Use cached PDFs only.")
    parser.add_argument("--force", action="store_true", help="Re-download PDFs even if cached.")
    args = parser.parse_args(argv)
    return collect(args)


if __name__ == "__main__":
    raise SystemExit(main())
