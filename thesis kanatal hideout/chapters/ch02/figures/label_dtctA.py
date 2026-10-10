"""Add page-readable axis labels while preserving every original plot pixel.

Run with Python 3 and Pillow. The horizontal label is Latin Modern italic from
the thesis TeX setup. The other labels are the thesis symbols A with a roman
subscript c, and A, set upright beside the curve each one names: the
subscripted symbol by the green curve, A by the red one.

At 0.48 of the thesis text width the labels are approximately 11 pt.
"""

from pathlib import Path
import subprocess
import tempfile

from PIL import Image, ImageDraw, ImageFont


HERE = Path(__file__).resolve().parent
LEFT, BOTTOM = 46, 42
# Cap height of the existing italic p, so the titles match.
CAP_PX = 19
# Gap between a vertical label and the plot image.
MARGIN_GAP = 5


def font(name, size):
    path = subprocess.check_output(["kpsewhich", name], text=True).strip()
    if not path:
        raise FileNotFoundError(f"TeX font not found: {name}")
    return ImageFont.truetype(path, size)


def label(text, typeface):
    box = typeface.getbbox(text)
    tile = Image.new("RGB", (box[2] - box[0] + 4, box[3] - box[1] + 4), "white")
    ImageDraw.Draw(tile).text((2 - box[0], 2 - box[1]), text, font=typeface, fill="black")
    return tile


def ink_bbox(image):
    mask = image.convert("L").point(lambda value: 255 if value < 250 else 0)
    box = mask.getbbox()
    if box is None:
        raise RuntimeError("rendered label is blank")
    return box


def column_bottoms(image):
    pixels = image.load()
    bottoms = []
    for x in range(image.width):
        bottom = -1
        for y in range(image.height - 1, -1, -1):
            if pixels[x, y] != (255, 255, 255):
                bottom = y
                break
        bottoms.append(bottom)
    return bottoms


def capital_metrics(image):
    """Cap height, and the width of the capital before a descending subscript."""
    bottoms = column_bottoms(image)
    ink = [bottom for bottom in bottoms if bottom >= 0]
    if not ink:
        raise RuntimeError("rendered label is blank")
    capital_bottom = min(ink)
    capital_end = 0
    for x, bottom in enumerate(bottoms):
        if bottom >= 0 and bottom <= capital_bottom + 2:
            capital_end = x
    return capital_bottom + 1, capital_end + 1


def render_math(body):
    """Rasterize one math expression and scale its capitals to CAP_PX."""
    tex = (
        "\\documentclass[11pt,border=1pt]{standalone}\n"
        "\\usepackage{lmodern}\n"
        "\\begin{document}\n"
        f"${body}$\n"
        "\\end{document}\n"
    )
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp)
        (work / "label.tex").write_text(tex)
        subprocess.run(
            ["pdflatex", "-interaction=nonstopmode", "-halt-on-error", "label.tex"],
            cwd=work,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        subprocess.run(
            ["pdftoppm", "-png", "-r", "600", "label.pdf", "label"],
            cwd=work,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
        rendered = Image.open(work / "label-1.png").convert("RGB")

    cropped = rendered.crop(ink_bbox(rendered))
    cap, capital_width = capital_metrics(cropped)
    if cap < 8:
        raise RuntimeError(f"could not measure the capital height ({cap}px)")
    scale = CAP_PX / cap
    scaled = cropped.resize(
        (max(1, round(cropped.width * scale)), max(1, round(cropped.height * scale))),
        Image.Resampling.LANCZOS,
    )
    return scaled, max(1, round(capital_width * scale))


def intercept_y(image, colour):
    """Median height where a curve meets the vertical axis."""
    pixels = image.load()
    spine = 33
    found = []
    for x in range(spine + 3, spine + 22):
        for y in range(image.height):
            red, green, blue = pixels[x, y]
            if colour == "green" and green > 90 and green > red + 25 and green > blue + 15:
                found.append(y)
            elif colour == "red" and red > 140 and red > green + 40 and red > blue + 40:
                found.append(y)
    if not found:
        raise RuntimeError(f"no {colour} curve beside the axis")
    found.sort()
    return found[len(found) // 2]


def capital_centre(tile):
    """Row of the capital's optical centre, ignoring a subscript on the right."""
    pixels = tile.load()
    span = max(1, int(tile.width * 0.6))
    top, baseline = tile.height, 0
    for x in range(span):
        for y in range(tile.height):
            if pixels[x, y] != (255, 255, 255):
                top = min(top, y)
                baseline = max(baseline, y)
    if top >= tile.height:
        raise RuntimeError("label capital is blank")
    return (top + baseline) / 2


def place(canvas, tile, anchor_y):
    """Right-align an upright label so its capital sits on anchor_y."""
    if tile.width + MARGIN_GAP > LEFT or tile.height > canvas.height:
        raise RuntimeError(f"label {tile.size} does not fit the {LEFT}px margin")
    x = LEFT - MARGIN_GAP - tile.width
    y = int(round(anchor_y - capital_centre(tile)))
    y = max(0, min(y, canvas.height - tile.height))
    canvas.paste(tile, (x, y))


def main():
    original = Image.open(HERE / "src" / "dtctA.unlabelled.png").convert("RGB")
    width, height = original.size
    result = Image.new("RGB", (width + LEFT, height + BOTTOM), "white")
    result.paste(original, (LEFT, 0))

    horizontal = label("p", font("lmroman10-italic.otf", 30))
    result.paste(horizontal, (LEFT + (width - horizontal.width) // 2, height + 9))

    continuous, _ = render_math(r"A_{\mathrm{c}}")
    discrete, _ = render_math("A")
    place(result, continuous, intercept_y(original, "green"))
    place(result, discrete, intercept_y(original, "red"))

    # No regeneration, resampling or changes to the plot, ticks or axis limits.
    assert result.crop((LEFT, 0, LEFT + width, height)).tobytes() == original.tobytes()
    result.save(HERE / "dtctA.png")


if __name__ == "__main__":
    main()
