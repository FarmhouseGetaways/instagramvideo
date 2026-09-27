#!/usr/bin/env python3
"""Make iMessage-style chat bubbles as transparent PNGs for the "Where are you?" format.

Usage: python3 scripts/text_bubbles.py out_dir "them:Where are you??" "me:Red Barn Ranch."
Writes bubble1.png, bubble2.png, … sized for a 1080-wide canvas.
"""
import os
import sys

from PIL import Image, ImageDraw, ImageFilter, ImageFont

FONT = "/usr/share/fonts/truetype/open-sans/OpenSans-Semibold.ttf"
SIZE = 54
MAX_W = 720
PAD_X, PAD_Y, RADIUS = 40, 26, 46
COLORS = {"them": ((233, 233, 235), (0, 0, 0)), "me": ((11, 132, 254), (255, 255, 255))}


def wrap(draw, text, font):
    lines, line = [], ""
    for word in text.split():
        trial = f"{line} {word}".strip()
        if draw.textlength(trial, font=font) <= MAX_W - 2 * PAD_X or not line:
            line = trial
        else:
            lines.append(line)
            line = word
    lines.append(line)
    return lines


def bubble(text, who, path):
    font = ImageFont.truetype(FONT, SIZE)
    probe = ImageDraw.Draw(Image.new("RGBA", (1, 1)))
    lines = wrap(probe, text, font)
    line_h = int(SIZE * 1.3)
    w = int(max(probe.textlength(l, font=font) for l in lines)) + 2 * PAD_X
    h = line_h * len(lines) + 2 * PAD_Y
    margin = 24
    img = Image.new("RGBA", (w + 2 * margin, h + 2 * margin), (0, 0, 0, 0))
    shadow = Image.new("RGBA", img.size, (0, 0, 0, 0))
    ImageDraw.Draw(shadow).rounded_rectangle(
        (margin, margin + 6, margin + w, margin + h + 6), RADIUS, fill=(0, 0, 0, 90))
    img = Image.alpha_composite(img, shadow.filter(ImageFilter.GaussianBlur(10)))
    bg, fg = COLORS[who]
    d = ImageDraw.Draw(img)
    d.rounded_rectangle((margin, margin, margin + w, margin + h), RADIUS, fill=bg + (255,))
    for i, l in enumerate(lines):
        d.text((margin + PAD_X, margin + PAD_Y + i * line_h), l, font=font, fill=fg)
    img.save(path)
    return img.size


def main():
    out_dir = sys.argv[1]
    os.makedirs(out_dir, exist_ok=True)
    for i, arg in enumerate(sys.argv[2:], 1):
        who, text = arg.split(":", 1)
        path = os.path.join(out_dir, f"bubble{i}.png")
        w, h = bubble(text.strip(), who.strip(), path)
        print(path, w, h, who)


if __name__ == "__main__":
    main()
