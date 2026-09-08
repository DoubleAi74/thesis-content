#!/usr/bin/env python3
"""Crop window chrome from the six automaton frames and emit a contact sheet."""

from __future__ import annotations

from pathlib import Path

from PIL import Image

ROOT = Path(__file__).resolve().parents[3]
SRC = ROOT / "figures"
OUT = Path(__file__).resolve().parents[1]

FRAMES = [
    ("pim1.jpg", "advance"),
    ("pim3.jpg", "squeeze"),
    ("pim6.jpg", "fringe"),
    ("pim8.jpg", "crossing"),
    ("pim9.jpg", "recovery"),
    ("pim11.jpg", "fixation"),
]


def crop_frame(im: Image.Image) -> Image.Image:
    w, h = im.size
    # Title bar ~5.5% of height; window edges a few pixels; status strip at foot.
    left, top = int(0.018 * w), int(0.095 * h)
    right, bot = int(0.982 * w), int(0.955 * h)
    return im.crop((left, top, right, bot))


def main():
    cropped = []
    OUT.mkdir(parents=True, exist_ok=True)
    for i, (name, slug) in enumerate(FRAMES, start=1):
        im = Image.open(SRC / name).convert("RGB")
        c = crop_frame(im)
        dest = OUT / f"panel_{i}_{slug}.jpg"
        c.save(dest, quality=92)
        cropped.append(c)

    # Contact sheet, 3 x 2, matching CH3 sequence layout.
    w, h = cropped[0].size
    gap = 8
    sheet = Image.new("RGB", (3 * w + 2 * gap, 2 * h + gap), (255, 255, 255))
    for i, im in enumerate(cropped):
        r, col = divmod(i, 3)
        sheet.paste(im, (col * (w + gap), r * (h + gap)))
    sheet.save(OUT / "fig06.jpg", quality=92)
    print("wrote", OUT / "fig06.jpg", "and six panels")


if __name__ == "__main__":
    main()
