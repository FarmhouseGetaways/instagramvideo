#!/usr/bin/env python3
"""Build Instagram carousel slides from photos: crop to 4:5, apply the house grade, add a slide-1 hook.

Usage: python3 scripts/make_carousel.py plan.json

{
  "output_dir": "work/out/mr_carousel",
  "ratio": "4:5",                       # 4:5 (1080x1350) | 1:1 (1080x1080)
  "grade": "crisp",
  "hook": {"text": "3 holes of disc golf. 1 arcade.", "position": "top"},
  "slides": [
    {"src": "work/raw/hdr_mr/mountain front by cu.jpg", "focus_x": 0.5, "focus_y": 0.5, "zoom": 1.0},
    {"src": "work/raw/hdr_mr/basket.png", "text": {"text": "Your own private course", "position": "bottom", "size": 64}}
  ]
}
focus_x/focus_y (0–1) pick which part of a wide photo stays in the crop. zoom > 1 crops tighter.
A slide's "text" puts words on that slide in the hook style (position top|center|bottom, size in px).
Set CAROUSEL_FONT to the Montserrat ExtraBold path when it isn't at the Linux default.
"""
import json
import os
import subprocess
import sys

from PIL import Image, ImageDraw, ImageFont

sys.path.insert(0, os.path.dirname(__file__))
from make_reel import GRADES  # noqa: E402  (same house look as the videos)

SIZES = {"4:5": (1080, 1350), "1:1": (1080, 1080)}
FONT = os.environ.get("CAROUSEL_FONT", "/usr/share/fonts/truetype/montserrat/Montserrat-ExtraBold.ttf")


def crop_box(w, h, tw, th, fx, fy, zoom):
    target = tw / th
    if w / h > target:
        ch = h / zoom
        cw = ch * target
    else:
        cw = w / zoom
        ch = cw / target
    x = min(max(fx * w - cw / 2, 0), w - cw)
    y = min(max(fy * h - ch / 2, 0), h - ch)
    return int(x), int(y), int(x + cw), int(y + ch)


def grade(src_png, dst_jpg, grade_name):
    chain = GRADES[grade_name].replace("hqdn3d=1.5:1.5:4:4,", "hqdn3d=1.5:1.5:0:0,")  # spatial only for stills
    vf = chain if chain else "null"
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", src_png, "-vf", vf,
                    "-q:v", "1", "-pix_fmt", "yuvj444p", dst_jpg], check=True)


def draw_hook(img, text, position, size=72):
    d = ImageDraw.Draw(img)
    W, H = img.size
    font = ImageFont.truetype(FONT, size)
    words, lines, line = text.split(), [], ""
    for w in words:
        trial = f"{line} {w}".strip()
        if d.textlength(trial, font=font) <= W - 200 or not line:
            line = trial
        else:
            lines.append(line)
            line = w
    lines.append(line)
    lh = int(size * 1.22)
    block_h = lh * len(lines)
    y0 = {"top": 110, "center": (H - block_h) // 2}.get(position, H - block_h - 150)
    # soft dark gradient behind the text so it reads on any photo
    grad = Image.new("L", (1, block_h + 220))
    for i in range(grad.height):
        a = int(150 * (1 - abs(i - grad.height / 2) / (grad.height / 2)) ** 0.6)
        grad.putpixel((0, i), a)
    shade = Image.new("RGB", (W, grad.height), (0, 0, 0))
    img.paste(shade, (0, max(0, y0 - 110)), grad.resize((W, grad.height)))
    for i, l in enumerate(lines):
        tw = d.textlength(l, font=font)
        d.text(((W - tw) / 2, y0 + i * lh), l, font=font, fill="white",
               stroke_width=3, stroke_fill=(0, 0, 0))
    return img


def main():
    plan = json.load(open(sys.argv[1], encoding="utf-8"))
    tw, th = SIZES[plan.get("ratio", "4:5")]
    out_dir = plan["output_dir"]
    os.makedirs(out_dir, exist_ok=True)
    outputs = []
    for n, s in enumerate(plan["slides"], 1):
        im = Image.open(s["src"]).convert("RGB")
        box = crop_box(*im.size, tw, th, s.get("focus_x", 0.5), s.get("focus_y", 0.5), s.get("zoom", 1.0))
        im = im.crop(box).resize((tw, th), Image.LANCZOS)
        tmp_png = os.path.join(out_dir, f".tmp_{n:02d}.png")
        im.save(tmp_png)
        out = os.path.join(out_dir, f"slide_{n:02d}.jpg")
        grade(tmp_png, out, s.get("grade", plan.get("grade", "crisp")))
        os.remove(tmp_png)
        # per-slide "text" (same style as the hook); the plan-level hook still fills slide 1 when it has none
        t = s.get("text") or (plan.get("hook") if n == 1 else None)
        if t and t.get("text"):
            img = draw_hook(Image.open(out).convert("RGB"), t["text"], t.get("position", "top"), t.get("size", 72))
            img.save(out, quality=95, subsampling=0)
        outputs.append(out)
        print(out)
    return outputs


if __name__ == "__main__":
    main()
