#!/usr/bin/env python3
"""Optimize website images: auto-orient, resize, compress."""
import shutil
from pathlib import Path
from PIL import Image, ImageOps

ROOT = Path(__file__).resolve().parents[1]
SRC = ROOT.parent / "for_website"
MAX_DIM = 1800
QUALITY = 82

MAPPING = {
    "me": SRC / "me",
    "photography": SRC / "photography",
    "moto": SRC / "moto",
    "monkey": SRC / "monkey business",
}

EXTS = {".jpg", ".jpeg", ".png", ".webp", ".gif"}


def slugify(name: str) -> str:
    base = Path(name).stem.lower()
    out = []
    for ch in base:
        if ch.isalnum():
            out.append(ch)
        elif ch in " -_":
            out.append("-")
    slug = "".join(out)
    while "--" in slug:
        slug = slug.replace("--", "-")
    return slug.strip("-") or "image"


def optimize(src_path: Path, dst_dir: Path, index: int) -> str:
    dst_dir.mkdir(parents=True, exist_ok=True)
    slug = slugify(src_path.name)
    dst_name = f"{index:02d}-{slug}.jpg"
    dst_path = dst_dir / dst_name

    with Image.open(src_path) as img:
        img = ImageOps.exif_transpose(img)
        if img.mode in ("RGBA", "P"):
            bg = Image.new("RGB", img.size, (255, 248, 240))
            if img.mode == "P":
                img = img.convert("RGBA")
            bg.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
            img = bg
        elif img.mode != "RGB":
            img = img.convert("RGB")

        w, h = img.size
        if max(w, h) > MAX_DIM:
            scale = MAX_DIM / max(w, h)
            img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)

        img.save(dst_path, "JPEG", quality=QUALITY, optimize=True)

    return dst_name


def main():
    for folder, src_dir in MAPPING.items():
        dst_dir = ROOT / "assets" / "img" / folder
        if dst_dir.exists():
            for f in dst_dir.glob("*"):
                if f.is_file():
                    f.unlink()
        files = sorted(
            p for p in src_dir.iterdir()
            if p.is_file() and p.suffix.lower() in EXTS
        )
        print(f"{folder}: {len(files)} images")
        for i, src in enumerate(files, 1):
            name = optimize(src, dst_dir, i)
            print(f"  -> {name}")

    cv_src = ROOT.parent / "resume.pdf"
    cv_dst = ROOT / "assets" / "cv" / "Shivam_Singh_CV.pdf"
    shutil.copy2(cv_src, cv_dst)
    print(f"CV copied -> {cv_dst.relative_to(ROOT)}")

    # Pipeline teaser for spatial video work
    pipeline_src = ROOT.parent.parent / "figures" / "beautiful_pipeline.png"
    if pipeline_src.exists():
        dst = ROOT / "assets" / "img" / "research" / "spatial-video-pipeline.jpg"
        with Image.open(pipeline_src) as img:
            img = img.convert("RGB")
            w, h = img.size
            if max(w, h) > MAX_DIM:
                scale = MAX_DIM / max(w, h)
                img = img.resize((int(w * scale), int(h * scale)), Image.Resampling.LANCZOS)
            img.save(dst, "JPEG", quality=QUALITY, optimize=True)
        print(f"Pipeline teaser -> {dst.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
