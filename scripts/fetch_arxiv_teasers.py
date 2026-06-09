#!/usr/bin/env python3
"""Download arXiv PDFs and extract first-page teaser figures."""
import subprocess
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "assets" / "img" / "research"
TMP = ROOT / "scripts" / ".arxiv_tmp"
OUT.mkdir(parents=True, exist_ok=True)
TMP.mkdir(parents=True, exist_ok=True)

PAPERS = {
    "pause-and-think": "2606.00616",
    "anticipate-adapt-act": "2602.19518",
    "adaptbot": "2502.02067",
    "anticipate-and-act": "2502.02066",
}

ABSTRACTS = {
    "pause-and-think": (
        "Recent Vision-Language Models struggle with grounded reasoning, temporal consistency, "
        "and context-aware planning in videos. We introduce Pause-and-Think-T, a reasoning-centric "
        "training dataset that encourages models to pause, reason over visual evidence, and produce "
        "concise, actionable responses. A compact 4B-parameter model fine-tuned on our dataset "
        "achieves 58.0% accuracy at 59× fewer parameters than Qwen3-VL-235B, matching GPT-5.2 on "
        "scene understanding while remaining suitable for real-time edge deployment."
    ),
    "anticipate-adapt-act": (
        "Anticipating and adapting to failures is a key capability robots need to collaborate "
        "effectively with humans in complex domains. We present a hybrid framework that integrates "
        "the generic prediction capabilities of an LLM with the probabilistic sequential "
        "decision-making capability of Relational Dynamic Influence Diagram Language. For any given "
        "task, the robot reasons about the task and the capabilities of the human attempting to "
        "complete it, predicts potential failures, and executes actions to prevent or recover from them."
    ),
    "adaptbot": (
        "We present AdaptBot, a framework combining Large Language Models, Knowledge Graphs, and "
        "Human-in-the-Loop approaches to enable embodied agents to handle unseen tasks and adapt to "
        "new scenarios. The system decomposes generic tasks into specific executable actions while "
        "refining domain knowledge through human feedback, bridging the gap between high-level "
        "reasoning and grounded task execution in household environments."
    ),
    "anticipate-and-act": (
        "We present an intelligent household agent that learns task execution patterns by extracting "
        "user behavior and preferences using Large Language Models and designing task and action "
        "representations in Planning Domain Definition Language (PDDL). By integrating LLM-based task "
        "anticipation with classical planning, the system enables efficient task execution in "
        "household environments."
    ),
}


def download(paper_id: str, slug: str) -> Path:
    pdf_path = TMP / f"{slug}.pdf"
    url = f"https://arxiv.org/pdf/{paper_id}.pdf"
    print(f"Downloading {url}")
    urllib.request.urlretrieve(url, pdf_path)
    return pdf_path


def extract_teaser(pdf_path: Path, slug: str) -> bool:
    prefix = TMP / slug
    # Render first page at 150 DPI
    subprocess.run(
        ["pdftoppm", "-png", "-r", "150", "-f", "1", "-l", "1", str(pdf_path), str(prefix)],
        check=True,
        capture_output=True,
    )
    page_png = TMP / f"{slug}-1.png"
    if not page_png.exists():
        page_png = TMP / f"{slug}-01.png"
    if not page_png.exists():
        candidates = list(TMP.glob(f"{slug}*.png"))
        if not candidates:
            return False
        page_png = candidates[0]

    from PIL import Image
    with Image.open(page_png) as img:
        w, h = img.size
        # Crop top ~55% which usually contains figure + title on arXiv papers
        crop_h = int(h * 0.55)
        teaser = img.crop((0, 0, w, crop_h))
        if teaser.mode != "RGB":
            teaser = teaser.convert("RGB")
        out = OUT / f"{slug}-teaser.jpg"
        teaser.save(out, "JPEG", quality=85, optimize=True)
        print(f"  teaser -> {out.name} ({teaser.size[0]}x{teaser.size[1]})")
    return True


def write_abstracts():
    abs_dir = ROOT / "assets" / "data"
    abs_dir.mkdir(parents=True, exist_ok=True)
    for slug, text in ABSTRACTS.items():
        (abs_dir / f"{slug}.txt").write_text(text, encoding="utf-8")
    print(f"Abstracts written to {abs_dir.relative_to(ROOT)}")


def main():
    for slug, paper_id in PAPERS.items():
        try:
            pdf = download(paper_id, slug)
            extract_teaser(pdf, slug)
        except Exception as e:
            print(f"  WARN {slug}: {e}")
    write_abstracts()


if __name__ == "__main__":
    main()
