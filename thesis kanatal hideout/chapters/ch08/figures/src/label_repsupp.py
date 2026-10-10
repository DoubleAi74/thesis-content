"""Add print-size axis labels while retaining the original PDF plot artwork.

Requires pymupdf and reportlab. Run from any directory. The immutable input
PDFs in repsupp-originals make reruns safe. Lower panels are translated only;
upper plot paths are stretched vertically without changing their values.
"""
from io import BytesIO
from pathlib import Path

import pymupdf as pdf
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

HERE = Path(__file__).resolve().parent
FONT = Path('/System/Library/Fonts/Supplemental/Times New Roman.ttf')
pdfmetrics.registerFont(TTFont('LabelSerif', str(FONT)))
pdfmetrics.registerFont(TTFont('LabelItalic', str(FONT.with_name('Times New Roman Italic.ttf'))))
TEXT_WIDTH = 595.27559 - 144  # A4 with one-inch margins, in PDF points.
SHIFT = 70
TOP = 14.44000244140625
BASE = 58.988494873046875
STRETCH = 2.15
NEW_BASE = TOP + STRETCH * (BASE - TOP)


def build(n):
    source = pdf.open(HERE / 'repsupp-originals' / f'repsupp_N{n}.pdf')
    old = source[0]
    w, h = old.rect.width, old.rect.height
    result = pdf.open()
    page = result.new_page(width=w, height=h + SHIFT)
    # Preserve all lower artwork, including the colour scale and every label.
    page.show_pdf_page(pdf.Rect(0, 66 + SHIFT, w, h + SHIFT), source, 0,
                       clip=pdf.Rect(0, 66, w, h))
    # Preserve the three suppression-rate titles without stretching their text.
    page.show_pdf_page(pdf.Rect(0, 0, w, 11), source, 0,
                       clip=pdf.Rect(0, 0, w, 11))
    stream = BytesIO()
    c = canvas.Canvas(stream, pagesize=(w, h + SHIFT))
    scale = TEXT_WIDTH * (1 if n == 20 else .92) / w
    fs = 9 / scale  # Both figures have nine-point axis labels in the thesis.
    tick_fs = 8 / scale

    def text(x, y, value, size=fs, centred=True):
        c.setFont('LabelSerif', size)
        if centred:
            c.drawCentredString(x, h + SHIFT - y, value)
        else:
            c.drawRightString(x, h + SHIFT - y, value)

    for col in range(3):
        left = 34.252498626708984 + col * 165.2667
        right = left + 129.1146125793457
        # Exclude the original tick numerals so they retain normal proportions.
        clip = pdf.Rect(left - 4, TOP - .5, right + .5, BASE + .5)
        dest = pdf.Rect(clip.x0, TOP + STRETCH * (clip.y0 - TOP),
                        clip.x1, TOP + STRETCH * (clip.y1 - TOP))
        page.show_pdf_page(dest, source, 0, clip=clip, keep_proportion=False)
        for label, old_y in [('0', BASE), ('1', 16.561355590820312)]:
            text(left - 7, TOP + STRETCH * (old_y - TOP) + tick_fs * .33,
                 label, tick_fs, centred=False)
        # The short second line specifies the full-store initial condition.
        c.saveState()
        c.translate(left - 25, h + SHIFT - (TOP + NEW_BASE) / 2)
        c.rotate(90)
        c.setFont('LabelSerif', fs)
        c.drawCentredString(0, 0, 'Survival probability')
        c.drawCentredString(0, -fs * 1.05, '(full store)')
        c.restoreState()
        bars = [d for d in old.get_drawings()
                if d['fill'] is not None and d['fill'][2] > .4
                and d['rect'].y1 < 60
                and left < d['rect'].x0 < right]
        assert len(bars) == n + 1, (n, col, len(bars))
        for i in (range(0, 21, 5) if n == 20 else range(0, 11, 2)):
            x = (bars[i]['rect'].x0 + bars[i]['rect'].x1) / 2
            c.setLineWidth(.6)
            c.line(x, h + SHIFT - NEW_BASE, x, h + SHIFT - NEW_BASE - 3)
            text(x, NEW_BASE + 13, str(i), tick_fs)
        label = 'Initial replicator count, '
        total = pdfmetrics.stringWidth(label, 'LabelSerif', fs) + pdfmetrics.stringWidth('i', 'LabelItalic', fs)
        x = (left + right - total) / 2
        c.setFont('LabelSerif', fs)
        c.drawString(x, h + SHIFT - NEW_BASE - 28, label)
        c.setFont('LabelItalic', fs)
        c.drawString(x + pdfmetrics.stringWidth(label, 'LabelSerif', fs), h + SHIFT - NEW_BASE - 28, 'i')
    c.save()
    overlay = pdf.open(stream=stream.getvalue(), filetype='pdf')
    page.show_pdf_page(page.rect, overlay, 0)
    result.set_metadata({'title': f'Survival maps, N={n}',
                         'subject': 'Original plot artwork with labelled full-store marginals'})
    result.save(HERE.parent / f'repsupp_N{n}.pdf', garbage=4, deflate=True)


if __name__ == '__main__':
    for store in (20, 10):
        build(store)
