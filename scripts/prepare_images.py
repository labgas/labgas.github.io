"""Prepare website images from the lab's shared Drive folder.

Source images are full-resolution originals (some over 25 MB) in mixed formats,
including HEIC. This script derives web-sized, consistently cropped versions into
assets/images/ so the repository never carries the originals.

Re-run it after adding or replacing a source photo:

    python scripts/prepare_images.py

Pass --source to point at a different folder. Missing sources are reported and
skipped rather than treated as errors, so the script is safe to run on a machine
that does not have the Drive folder mounted.

Requires: pillow, pillow-heif
"""

from __future__ import annotations

import argparse
import os
import sys

from PIL import Image, ImageOps

try:
    import pillow_heif

    pillow_heif.register_heif_opener()
except ImportError:  # HEIC sources will simply be reported as unreadable
    pass

DEFAULT_SOURCE = r"G:\My Drive\LaBGAS\LaBGAS_GENERAL\LaBGAS_website"
ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
IMAGES = os.path.join(ROOT, "assets", "images")
TEAM = os.path.join(IMAGES, "team")

# Source filename -> output slug. Only unambiguously named files are mapped:
# guessing which person an "IMG_3742.jpg" shows would risk putting the wrong
# face against a name, which is worse than the initials-avatar fallback.
PORTRAITS = {
    "Profile photos/VanOudenhove_MG_5928s.jpg": "lukas-van-oudenhove",
    # Sources below identified by the lab — their filenames give nothing away.
    "Profile photos/Profile pic.jpg": "nathalie-weltens",
    "Profile photos/IMG_1674.jpg": "maaike-van-den-houte",
    "Profile photos/IMG-7152 (2).jpg": "livia-guadagnoli",
    "Profile photos/portrait_2023_BoushraDALILE.jpg": "boushra-dalile",
    "Profile photos/Iris.JPG": "iris-coppieters",
    "Profile photos/Liene.jpg": "liene-bervoets",
    "Profile photos/Annalena.png": "annalena-fuchs",
    "Profile photos/Nele.png": "nele-mattelaer",
    "Profile photos/Tabea.png": "tabea-eimer",
    "Profile photos/Ynse.HEIC": "ynse-dooms",
    "Profile photos/Dina.png": "dina-satriawan",
    "Profile photos/LixinQ.jpg": "lixin-qiu",
    "Profile photos/FrancoR.jpg": "franco-ruiz",
    "Profile photos/Elin_color.JPG": "elin-marie-johansson",
    "Profile photos/Sybren.jpg": "sybren-rinckhout",
    "Profile photos/Jim.jpg": "jim-draux",
    "Profile photos/Tuur.jpg": "tuur-abts",
    "Profile photos/Alexine foto.png": "alexine-mennes",
}

PORTRAIT_PX = 480
# Faces sit above the middle of a portrait, so a centred square crop tends to cut
# foreheads and include too much torso. Bias the crop window upward.
VERTICAL_BIAS = 0.38

# Per-person crop windows for sources the automatic rule handles badly — full
# length shots, mainly, where a square crop of the whole frame leaves the face
# too small to recognise. Values are (centre_x, centre_y, side) as fractions of
# the image width/height. Add an entry here rather than editing the source photo.
CROP_OVERRIDES = {
    "ynse-dooms": (0.59, 0.42, 0.44),
}


def square_crop(im: Image.Image, size: int, override=None, greyscale: bool = False) -> Image.Image:
    im = ImageOps.exif_transpose(im)
    if im.mode not in ("RGB", "L"):
        im = im.convert("RGB")
    w, h = im.size
    if override:
        cx, cy, frac = override
        side = int(w * frac)
        left = int(w * cx - side / 2)
        top = int(h * cy - side / 2)
    else:
        side = min(w, h)
        left = (w - side) // 2
        top = int((h - side) * VERTICAL_BIAS) if h > w else (h - side) // 2
    side = max(1, min(side, w, h))
    left = max(0, min(left, w - side))
    top = max(0, min(top, h - side))
    im = im.crop((left, top, left + side, top + side)).resize((size, size), Image.LANCZOS)
    if greyscale:
        im = ImageOps.grayscale(im).convert("RGB")
    return im


def save_jpeg(im: Image.Image, path: str, quality: int = 86) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    im.convert("RGB").save(path, "JPEG", quality=quality, optimize=True, progressive=True)


def rel(path: str) -> str:
    return os.path.relpath(path, ROOT).replace("\\", "/")


def do_portraits(source: str, greyscale: bool = False) -> "tuple[int, list]":
    done, missing = 0, []
    for src_rel, slug in PORTRAITS.items():
        src = os.path.join(source, src_rel.replace("/", os.sep))
        if not os.path.isfile(src):
            missing.append(f"{src_rel} (not found)")
            continue
        try:
            with Image.open(src) as im:
                if min(im.size) < 100:
                    missing.append(f"{src_rel} (too small: {im.size[0]}x{im.size[1]})")
                    continue
                out = os.path.join(TEAM, f"{slug}.jpg")
                cropped = square_crop(im, PORTRAIT_PX, CROP_OVERRIDES.get(slug), greyscale)
                save_jpeg(cropped, out)
                done += 1
                print(f"  portrait  {slug}.jpg  <- {src_rel}")
        except Exception as exc:
            missing.append(f"{src_rel} ({type(exc).__name__}: {exc})")
    return done, missing


def do_normalise_existing(greyscale: bool = False) -> "tuple[int, list]":
    """Square-crop and resize any portrait already sitting in assets/images/team/.

    The Drive folder is not the only way a photo arrives — someone drops a file
    straight into the repo named after the person's slug. Those are full-size
    originals (several MB, arbitrary aspect ratio) where every other portrait is
    a 480px square, so normalise them in place.

    Files already at the target size are left alone, which makes this safe to
    re-run: re-cropping an already-cropped image would zoom in a little further
    each time.
    """
    done, problems = 0, []
    if not os.path.isdir(TEAM):
        return 0, problems
    for name in sorted(os.listdir(TEAM)):
        path = os.path.join(TEAM, name)
        if not os.path.isfile(path) or not name.lower().endswith((".jpg", ".jpeg", ".png")):
            continue
        try:
            with Image.open(path) as im:
                if im.size == (PORTRAIT_PX, PORTRAIT_PX):
                    continue
                if min(im.size) < 100:
                    problems.append(f"{name} (too small: {im.size[0]}x{im.size[1]})")
                    continue
                slug = os.path.splitext(name)[0]
                before = im.size
                cropped = square_crop(im, PORTRAIT_PX, CROP_OVERRIDES.get(slug), greyscale)
            out = os.path.join(TEAM, slug + ".jpg")
            save_jpeg(cropped, out)
            if out != path:
                os.remove(path)
            done += 1
            print(f"  normalise {slug}.jpg  {before[0]}x{before[1]} -> {PORTRAIT_PX}x{PORTRAIT_PX}")
        except Exception as exc:
            problems.append(f"{name} ({type(exc).__name__}: {exc})")
    return done, problems


def do_logo(source: str) -> "list[str]":
    problems = []
    src = os.path.join(source, "LabGAS-logo.png")
    if not os.path.isfile(src):
        return ["LabGAS-logo.png (not found)"]
    try:
        with Image.open(src) as im:
            im = im.convert("RGBA")
            # Trim the transparent margin so the mark sits tight in the masthead.
            bbox = im.getbbox()
            if bbox:
                im = im.crop(bbox)
            os.makedirs(IMAGES, exist_ok=True)
            for name, width in (("labgas-logo.png", 900), ("labgas-logo-small.png", 240)):
                w, h = im.size
                out = im.resize((width, max(1, round(h * width / w))), Image.LANCZOS)
                out.save(os.path.join(IMAGES, name), "PNG", optimize=True)
                print(f"  logo      {name}  {out.size[0]}x{out.size[1]}")

            # Favicons need a square canvas; the logo is landscape, so pad it
            # rather than distorting or cropping the mark.
            w, h = im.size
            side = max(w, h)
            for name, px in (("favicon-32.png", 32), ("favicon-180.png", 180)):
                canvas = Image.new("RGBA", (side, side), (0, 0, 0, 0))
                canvas.paste(im, ((side - w) // 2, (side - h) // 2), im)
                canvas.resize((px, px), Image.LANCZOS).save(
                    os.path.join(IMAGES, name), "PNG", optimize=True
                )
                print(f"  favicon   {name}  {px}x{px}")
    except Exception as exc:
        problems.append(f"LabGAS-logo.png ({type(exc).__name__}: {exc})")
    return problems


def do_group(source: str) -> "list[str]":
    problems = []
    src = os.path.join(source, "Lab group photos", "groupphoto_all.jpg")
    if not os.path.isfile(src):
        return ["Lab group photos/groupphoto_all.jpg (not found)"]
    try:
        with Image.open(src) as im:
            im = ImageOps.exif_transpose(im)
            # Wide banner for the home page.
            w, h = im.size
            banner = im.resize((1600, round(h * 1600 / w)), Image.LANCZOS)
            save_jpeg(banner, os.path.join(IMAGES, "lab-group.jpg"))
            print(f"  group     lab-group.jpg  {banner.size[0]}x{banner.size[1]}")

            # Open Graph card: 1200x630, cropped from the centre of the group shot.
            target_ratio = 1200 / 630
            if w / h > target_ratio:
                new_w = int(h * target_ratio)
                box = ((w - new_w) // 2, 0, (w - new_w) // 2 + new_w, h)
            else:
                new_h = int(w / target_ratio)
                box = (0, 0, w, new_h)
            og = im.crop(box).resize((1200, 630), Image.LANCZOS)
            save_jpeg(og, os.path.join(IMAGES, "og-image.jpg"))
            print("  group     og-image.jpg  1200x630")
    except Exception as exc:
        problems.append(f"groupphoto_all.jpg ({type(exc).__name__}: {exc})")
    return problems


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--source", default=DEFAULT_SOURCE, help="folder holding the original images")
    ap.add_argument(
        "--greyscale",
        action="store_true",
        help="render all portraits in greyscale. The source photos are a mix of colour and "
        "black-and-white, which reads as inconsistent on the team page; this makes them uniform.",
    )
    args = ap.parse_args()

    # Photos dropped straight into assets/images/team/ are normalised whether or
    # not the Drive folder is reachable, so this works on any machine.
    n_local, problems_local = do_normalise_existing(args.greyscale)

    if not os.path.isdir(args.source):
        if n_local:
            print(f"\nNormalised {n_local} portrait(s) already in {rel(TEAM)}/")
        else:
            print(f"Source folder not available: {args.source}")
            print("Nothing to do — existing images in assets/images/ are left untouched.")
        for p in problems_local:
            print(f"  · {p}")
        return 0

    print(f"Source: {args.source}\n")
    n, missing = do_portraits(args.source, args.greyscale)
    missing += do_logo(args.source)
    missing += do_group(args.source)

    missing += problems_local
    print(f"\n{n}/{len(PORTRAITS)} portraits written to {rel(TEAM)}/"
          + (f", {n_local} normalised in place" if n_local else ""))
    if missing:
        print(f"\n{len(missing)} skipped:")
        for m in missing:
            print(f"  · {m}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
