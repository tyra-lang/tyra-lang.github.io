#!/usr/bin/env python3
"""
Generate public/og.png from the Tyra brand design.

Requirements:
    pip install Pillow
    macOS (the script resolves fonts from /System/Library/Fonts and /Library/Fonts)

Usage:
    python3 scripts/generate-og.py

NOTE — macOS-only tool:
    Font resolution is macOS-specific (Georgia, SF Pro / Helvetica / Arial from system
    font directories). On Linux or Windows the script falls back to Pillow's built-in
    bitmap font, which will produce a materially different layout.

    public/og.png is the AUTHORITATIVE committed asset. Regenerate only when the
    brand, tagline, or layout changes, and only on macOS where fonts match the original.
    The committed PNG is what gets deployed; this script is a one-off authoring aid.

The design intent is documented in scripts/og-template.html (HTML + CSS version).
"""

from PIL import Image, ImageDraw, ImageFont
import os

W, H = 1200, 630

# ── Colors ──────────────────────────────────────────────────────────────────
BG        = (13, 17, 23)      # #0d1117  — dark background (matches favicon)
CORAL     = (247, 129, 102)   # #f78166  — Tyra primary (dark-mode)
CORAL_DIM = (191, 61, 32)     # #bf3d20  — Tyra primary (light-mode), accent bar
TEXT_W    = (230, 237, 243)   # #e6edf3  — near-white heading
TEXT_MUT  = (139, 148, 158)   # #8b949e  — muted tagline
TEXT_DIM  = (72, 79, 88)      # #484f58  — very muted domain watermark

img = Image.new("RGB", (W, H), BG)
d   = ImageDraw.Draw(img)


# ── Helpers ──────────────────────────────────────────────────────────────────
def load_font(names: list, size: int):
    """Try several macOS font paths, fall back to default."""
    search_dirs = [
        "/System/Library/Fonts/Supplemental/",
        "/Library/Fonts/",
        "/System/Library/Fonts/",
    ]
    for name in names:
        for base in search_dirs:
            path = base + name
            if os.path.exists(path):
                return ImageFont.truetype(path, size)
    return ImageFont.load_default()


def draw_with_highlight(d, line, x, y, font, base_color, highlight_word, highlight_color):
    """Draw text with a single highlighted word."""
    parts = line.split(highlight_word)
    for i, part in enumerate(parts):
        d.text((x, y), part, font=font, fill=base_color)
        x += d.textlength(part, font=font)
        if i < len(parts) - 1:
            d.text((x, y), highlight_word, font=font, fill=highlight_color)
            x += d.textlength(highlight_word, font=font)


# ── Fonts ────────────────────────────────────────────────────────────────────
serif_bold  = load_font(["Georgia Bold.ttf", "Georgia.ttf"], 68)
serif_brand = load_font(["Georgia Bold.ttf", "Georgia.ttf"], 38)
serif_icon  = load_font(["Georgia Bold.ttf", "Georgia.ttf"], 34)
sans_tag    = load_font(["SF Pro Text.ttf", "Helvetica.ttf", "Arial.ttf"], 26)
sans_dom    = load_font(["SF Pro Text.ttf", "Helvetica.ttf", "Arial.ttf"], 20)


# ── 1. Left accent bar (8px, full height) ────────────────────────────────────
d.rectangle([0, 0, 7, H - 1], fill=CORAL_DIM)


# ── 2. Subtle grid texture ──────────────────────────────────────────────────
GRID = (22, 27, 34)  # slightly lighter than BG
for x in range(0, W, 40):
    d.line([(x, 0), (x, H)], fill=GRID, width=1)
for y in range(0, H, 40):
    d.line([(0, y), (W, y)], fill=GRID, width=1)


# ── 3. "T" icon (rounded rectangle, 56x56) ──────────────────────────────────
ICON_X, ICON_Y = 80, 56
ICON_W, ICON_H = 56, 56

d.rounded_rectangle(
    [ICON_X, ICON_Y, ICON_X + ICON_W, ICON_Y + ICON_H],
    radius=10, outline=CORAL, width=2,
)
t_bbox = d.textbbox((0, 0), "T", font=serif_icon)
tx = ICON_X + (ICON_W - (t_bbox[2] - t_bbox[0])) // 2
ty = ICON_Y + (ICON_H - (t_bbox[3] - t_bbox[1])) // 2
d.text((tx, ty), "T", font=serif_icon, fill=CORAL)


# ── 4. "Tyra" brand name ────────────────────────────────────────────────────
brand_bbox = d.textbbox((0, 0), "Tyra", font=serif_brand)
brand_h    = brand_bbox[3] - brand_bbox[1]
brand_y    = ICON_Y + (ICON_H - brand_h) // 2
d.text((ICON_X + ICON_W + 18, brand_y), "Tyra", font=serif_brand, fill=CORAL)


# ── 5. Heading (two lines, "LLMs" highlighted) ──────────────────────────────
HEAD_Y  = ICON_Y + ICON_H + 36
line_h  = d.textbbox((0, 0), "A", font=serif_bold)[3] + 6

draw_with_highlight(d, "a language LLMs get right", 80, HEAD_Y,
                    serif_bold, TEXT_W, "LLMs", CORAL)
draw_with_highlight(d, "on the first try", 80, HEAD_Y + line_h,
                    serif_bold, TEXT_W, "LLMs", CORAL)


# ── 6. Tagline ───────────────────────────────────────────────────────────────
TAG_Y = HEAD_Y + line_h * 2 + 28
d.text((80, TAG_Y), "Fast · Readable · Spec-injected", font=sans_tag, fill=TEXT_MUT)


# ── 7. Domain watermark (bottom-right) ──────────────────────────────────────
DOM_TXT = "tyra-lang.github.io"
dom_w   = d.textlength(DOM_TXT, font=sans_dom)
dom_h   = d.textbbox((0, 0), DOM_TXT, font=sans_dom)[3]
d.text((W - 80 - dom_w, H - 44 - dom_h), DOM_TXT, font=sans_dom, fill=TEXT_DIM)


# ── Save ─────────────────────────────────────────────────────────────────────
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "public", "og.png")
img.save(OUT, "PNG")
print(f"Saved {W}x{H} PNG -> {os.path.normpath(OUT)}")
