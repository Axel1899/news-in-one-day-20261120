#!/usr/bin/env python3
"""
compose.py — assemble the "news in one day" front page for 20 November 2026.

Builds a 1024x1024 newspaper-style front page from five pre-generated,
text-free editorial illustration panels (../panels/p1.jpg .. p5.jpg).
Every word on the page is typeset here with PIL so the text is always
crisp and correctly spelled — the AI-generated panels contain no text
at all by design.

Output: entry.png next to this script. The file holds JPEG bytes
(quality 88) under the entry.png name, which the competition rules
explicitly allow (format is detected from the first bytes).

Run:  python3 compose.py
"""

from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

HERE = Path(__file__).resolve().parent
PANELS = HERE.parent / "panels"
OUT = HERE / "entry.png"

SANS_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSans-Bold.ttf"
SERIF_BOLD = "/usr/share/fonts/truetype/liberation/LiberationSerif-Bold.ttf"

CANVAS = 1024
MARGIN = 28
CONTENT_W = CANVAS - 2 * MARGIN  # 968

BLACK = (13, 13, 13)
WHITE = (255, 255, 255)
KICKER_ON_BLACK = (205, 205, 205)
FOOTER_GRAY = (110, 110, 110)


def font(path: str, size: int) -> ImageFont.FreeTypeFont:
    return ImageFont.truetype(path, size)


def text_w(draw: ImageDraw.ImageDraw, text: str, f: ImageFont.FreeTypeFont) -> int:
    return int(draw.textlength(text, font=f))


def fit_font(draw, text, path, max_width, start, minimum=12):
    """Largest font size <= start whose text fits max_width."""
    size = start
    while size > minimum:
        f = font(path, size)
        if text_w(draw, text, f) <= max_width:
            return f
        size -= 1
    return font(path, minimum)


def tracked_width(draw, text, f, tracking):
    return sum(text_w(draw, ch, f) for ch in text) + tracking * (len(text) - 1)


def draw_tracked_center(draw, cx, y, text, f, tracking, fill):
    x = cx - tracked_width(draw, text, f, tracking) // 2
    for ch in text:
        draw.text((x, y), ch, font=f, fill=fill)
        x += text_w(draw, ch, f) + tracking


def draw_center(draw, cx, y, text, f, fill):
    draw.text((cx - text_w(draw, text, f) // 2, y), text, font=f, fill=fill)


def wrap(draw, text, f, max_width, max_lines=2):
    words = text.split()
    lines, cur = [], ""
    for w in words:
        trial = f"{cur} {w}".strip()
        if text_w(draw, trial, f) <= max_width or not cur:
            cur = trial
        else:
            lines.append(cur)
            cur = w
    if cur:
        lines.append(cur)
    return lines[:max_lines]


def cover_crop(img: Image.Image, w: int, h: int, focus_y: float = 0.5) -> Image.Image:
    """Scale img to cover (w, h) and crop; focus_y = vertical centre of the
    crop window as a fraction of the scaled image height (0=top, 1=bottom)."""
    scale = max(w / img.width, h / img.height)
    nw, nh = round(img.width * scale), round(img.height * scale)
    img = img.resize((nw, nh), Image.LANCZOS)
    x0 = (nw - w) // 2
    y0 = int((nh - h) * focus_y)
    y0 = max(0, min(nh - h, y0))
    return img.crop((x0, y0, x0 + w, y0 + h))


def headline_bar(draw, x, y, w, headline, kicker, head_start, head_min,
                 kicker_size, pad_top=12, pad_bottom=12, line_gap=4):
    """Black bar with a fitted/wrapped white headline + grey kicker.
    Returns the bar height used."""
    inner_w = w - 2 * 16
    hf = fit_font(draw, headline, SANS_BOLD, inner_w, head_start, head_min)
    lines = wrap(draw, headline, hf, inner_w, max_lines=2)
    line_h = int(hf.size * 1.16)
    kf = font(SANS_BOLD, kicker_size)
    if text_w(draw, kicker, kf) > inner_w:
        kf = fit_font(draw, kicker, SANS_BOLD, inner_w, kicker_size, 11)
    bar_h = pad_top + line_h * len(lines) + line_gap + int(kf.size * 1.25) + pad_bottom
    draw.rectangle([x, y, x + w, y + bar_h], fill=BLACK)
    ty = y + pad_top
    for ln in lines:
        draw.text((x + 16, ty), ln, font=hf, fill=WHITE)
        ty += line_h
    draw.text((x + 16, ty + line_gap), kicker, font=kf, fill=KICKER_ON_BLACK)
    return bar_h


def main() -> None:
    page = Image.new("RGB", (CANVAS, CANVAS), WHITE)
    draw = ImageDraw.Draw(page)
    cx = CANVAS // 2
    y = 18

    # --- masthead ------------------------------------------------------
    mf = font(SANS_BOLD, 21)
    draw_tracked_center(draw, cx, y, "THE WORLD IN ONE DAY", mf, 7, BLACK)
    y += 30

    # --- date ----------------------------------------------------------
    df = fit_font(draw, "FRIDAY, 20 NOVEMBER 2026", SERIF_BOLD, CONTENT_W, 74, 40)
    draw_center(draw, cx, y, "FRIDAY, 20 NOVEMBER 2026", df, BLACK)
    y += int(df.size * 1.18) + 6

    # --- double rule ---------------------------------------------------
    draw.rectangle([MARGIN, y, MARGIN + CONTENT_W, y + 6], fill=BLACK)
    draw.rectangle([MARGIN, y + 9, MARGIN + CONTENT_W, y + 11], fill=BLACK)
    y += 20

    # --- lead story ----------------------------------------------------
    lead = Image.open(PANELS / "p1.jpg").convert("RGB")
    page.paste(cover_crop(lead, CONTENT_W, 272, focus_y=0.46), (MARGIN, y))
    y += 272
    y += headline_bar(
        draw, MARGIN, y, CONTENT_W,
        "RUSSIAN MISSILES LAND IN POLAND",
        "NATO TERRITORY STRUCK - JETS SCRAMBLED, WARSAW DEMANDS REINFORCEMENTS",
        head_start=46, head_min=30, kicker_size=21,
    )
    y += 12

    # --- 2x2 grid --------------------------------------------------------
    stories = [
        ("p2.jpg", 0.40, "TRUMP, XI, PUTIN MEET IN SHENZHEN",
         "TRILATERAL PEACE DECLARATION AT APEC"),
        ("p3.jpg", 0.42, "AI CRASH WIPES OUT 2026 GAINS",
         "NASDAQ -5.4% \u2022 NVIDIA -14% \u2022 $4 TRILLION GONE"),
        ("p4.jpg", 0.40, "COP31 ERASES FOSSIL-FUEL PLEDGE",
         "ANTALYA TALKS SPILL INTO OVERTIME"),
        ("p5.jpg", 0.80, "GTA VI EARNS $3.79 BILLION IN A DAY",
         "BIGGEST ENTERTAINMENT LAUNCH EVER"),
    ]
    col_w = (CONTENT_W - 20) // 2  # 474
    img_h, bar_h = 124, 88
    for row in range(2):
        row_y = y + row * (img_h + bar_h + 12)
        for col in range(2):
            img_file, focus, head, kick = stories[row * 2 + col]
            x = MARGIN + col * (col_w + 20)
            img = Image.open(PANELS / img_file).convert("RGB")
            page.paste(cover_crop(img, col_w, img_h, focus_y=focus), (x, row_y))
            headline_bar(draw, x, row_y + img_h, col_w, head, kick,
                         head_start=26, head_min=18, kicker_size=15,
                         pad_top=9, pad_bottom=9, line_gap=3)
    y += 2 * (img_h + bar_h) + 12

    # --- footer (only if it fits) ---------------------------------------
    if y + 24 <= CANVAS - 10:
        ff = font(SANS_BOLD, 14)
        draw_center(draw, cx, y + 4,
                    "SOURCES: AP / ISW \u2022 REUTERS \u2022 INVESTOPEDIA \u2022 UN NEWS \u2022 CNN",
                    ff, FOOTER_GRAY)

    page.save(OUT, "JPEG", quality=88)
    print(f"wrote {OUT}  bytes={OUT.stat().st_size}  size={page.size}  content_bottom={y}")


if __name__ == "__main__":
    main()
