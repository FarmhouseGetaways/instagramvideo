"""Text-on-photo cards for Stories (1080x1920) and feed posts (1080x1350).

Usage: python scripts/make_story_cards.py plan.json
plan.json: {"out_dir": "...", "font_bold": "...ttf", "font_black": "...ttf",
            "cards": [{"name": "story_01", "size": "story"|"feed", "src": "photo.jpg",
                       "focus_x": 0.5, "focus_y": 0.5, "panel": "top"|"bottom"|"middle",
                       "kicker": "small caps line", "title": "big line(s)", "lines": ["...", "..."],
                       "footer": "small line", "leave_link_space": true}]}

Same crisp grade family as make_carousel.py: a little contrast, colour and sharpening.
Text sits inside Instagram's safe zone (top 250px and bottom 340px of a Story are kept clear).
"""
import json, sys, os
from PIL import Image, ImageDraw, ImageEnhance, ImageFilter, ImageFont, ImageOps

SIZES = {"story": (1080, 1920), "feed": (1080, 1350)}


def cover(img, w, h, fx, fy):
    sw, sh = img.size
    scale = max(w / sw, h / sh)
    img = img.resize((round(sw * scale), round(sh * scale)), Image.LANCZOS)
    x = round((img.width - w) * fx)
    y = round((img.height - h) * fy)
    return img.crop((x, y, x + w, y + h))


def grade(img):
    img = ImageEnhance.Contrast(img).enhance(1.08)
    img = ImageEnhance.Color(img).enhance(1.10)
    return img.filter(ImageFilter.UnsharpMask(radius=1.6, percent=70, threshold=2))


def wrap(draw, text, font, max_w):
    out = []
    for para in text.split("\n"):
        words, line = para.split(), ""
        for w in words:
            t = (line + " " + w).strip()
            if draw.textlength(t, font=font) <= max_w:
                line = t
            else:
                out.append(line); line = w
        out.append(line)
    return out


def framed(c, cfg, W, H):
    """Landscape photo as a rounded card on a blurred, darkened copy of itself.
    Keeps a 1500px-wide source sharp instead of cropping a sliver of it to fill 9:16."""
    src = grade(ImageOps.exif_transpose(Image.open(c["src"])).convert("RGB"))
    bg = cover(src, W, H, 0.5, 0.5).filter(ImageFilter.GaussianBlur(38))
    bg = ImageEnhance.Brightness(bg).enhance(0.42)
    pad = 84
    f_kick = ImageFont.truetype(cfg["font_bold"], 34)
    f_title = ImageFont.truetype(cfg["font_black"], c.get("title_size", 86))
    f_line = ImageFont.truetype(cfg["font_bold"], c.get("line_size", 46))
    f_foot = ImageFont.truetype(cfg["font_bold"], 32)
    d = ImageDraw.Draw(bg)
    top = [(c["kicker"].upper(), f_kick, 22, (255, 214, 140))] if c.get("kicker") else []
    top += [(t, f_title, 8, (255, 255, 255)) for t in wrap(d, c["title"], f_title, W - pad * 2)]
    below = []
    for ln in c.get("lines", []):
        below += [(t, f_line, 14, (255, 255, 255)) for t in wrap(d, ln, f_line, W - pad * 2)]
    if c.get("footer"):
        below += [(t, f_foot, 8, (235, 235, 235)) for t in wrap(d, c["footer"], f_foot, W - pad * 2)]
    hgt = lambda blk: sum(d.textbbox((0, 0), t, font=f)[3] + g for t, f, g, _ in blk)
    story = c.get("size", "story") == "story"
    safe_top, safe_bot = (250, 340) if story else (90, 110)
    safe_bot += 190 if c.get("leave_link_space") else 0
    gap = 56
    room = H - safe_top - safe_bot - hgt(top) - hgt(below) - gap * (2 if below else 1)
    cw = W - 120
    ch = round(cw * src.height / src.width)
    if ch > room:
        ch = room; cw = round(ch * src.width / src.height)
    card_img = cover(src, cw, ch, c.get("focus_x", 0.5), c.get("focus_y", 0.5))
    total = hgt(top) + gap + ch + (gap + hgt(below) if below else 0)
    y = safe_top + max(0, (H - safe_top - safe_bot - total) // 2)
    def put(blk, y):
        for t, f, g, col in blk:
            x = (W - d.textlength(t, font=f)) / 2
            d.text((x + 2, y + 3), t, font=f, fill=(0, 0, 0)); d.text((x, y), t, font=f, fill=col)
            y += d.textbbox((0, 0), t, font=f)[3] + g
        return y
    y = put(top, y) + gap
    cx = (W - cw) // 2
    shadow = Image.new("L", (W, H), 0)
    ImageDraw.Draw(shadow).rounded_rectangle((cx - 6, y + 14, cx + cw + 6, y + ch + 24), radius=34, fill=170)
    bg = Image.composite(Image.new("RGB", (W, H), (0, 0, 0)), bg, shadow.filter(ImageFilter.GaussianBlur(24)))
    mask = Image.new("L", (cw, ch), 0)
    ImageDraw.Draw(mask).rounded_rectangle((0, 0, cw, ch), radius=30, fill=255)
    bg.paste(card_img, (cx, y), mask)
    d = ImageDraw.Draw(bg)
    put(below, y + ch + gap)
    return bg


def card(c, cfg):
    W, H = SIZES[c.get("size", "story")]
    if c.get("frame"):
        out = os.path.join(cfg["out_dir"], c["name"] + ".jpg")
        framed(c, cfg, W, H).save(out, quality=92, subsampling=0)
        return out
    img = ImageOps.exif_transpose(Image.open(c["src"])).convert("RGB")
    img = grade(cover(img, W, H, c.get("focus_x", 0.5), c.get("focus_y", 0.5)))

    pad = 84
    max_w = W - pad * 2
    f_kick = ImageFont.truetype(cfg["font_bold"], 34)
    f_title = ImageFont.truetype(cfg["font_black"], c.get("title_size", 86))
    f_line = ImageFont.truetype(cfg["font_bold"], c.get("line_size", 46))
    f_foot = ImageFont.truetype(cfg["font_bold"], 32)

    probe = ImageDraw.Draw(img)
    blocks = []  # (text, font, gap_after, colour)
    if c.get("kicker"):
        blocks.append((c["kicker"].upper(), f_kick, 22, (255, 214, 140)))
    for t in wrap(probe, c["title"], f_title, max_w):
        blocks.append((t, f_title, 8, (255, 255, 255)))
    if c.get("lines"):
        blocks[-1] = (blocks[-1][0], blocks[-1][1], 34, blocks[-1][3])
        for ln in c["lines"]:
            for t in wrap(probe, ln, f_line, max_w):
                blocks.append((t, f_line, 14, (255, 255, 255)))
    if c.get("footer"):
        blocks[-1] = (blocks[-1][0], blocks[-1][1], 30, blocks[-1][3])
        for t in wrap(probe, c["footer"], f_foot, max_w):
            blocks.append((t, f_foot, 8, (235, 235, 235)))

    heights = [probe.textbbox((0, 0), t, font=f)[3] for t, f, _, _ in blocks]
    total = sum(heights) + sum(g for _, _, g, _ in blocks)

    safe_top = 250 if c.get("size", "story") == "story" else 90
    safe_bot = 340 if c.get("size", "story") == "story" else 110
    if c.get("leave_link_space"):
        safe_bot += 190
    panel = c.get("panel", "top")
    if panel == "top":
        y0 = safe_top
    elif panel == "bottom":
        y0 = H - safe_bot - total
    else:
        y0 = (H - total) // 2

    # Soft dark scrim behind the text block so it reads on any photo.
    scrim = Image.new("L", (W, H), 0)
    sd = ImageDraw.Draw(scrim)
    sd.rounded_rectangle((pad - 46, y0 - 46, W - pad + 46, y0 + total + 46), radius=40, fill=150)
    scrim = scrim.filter(ImageFilter.GaussianBlur(30))
    dark = Image.new("RGB", (W, H), (12, 14, 12))
    img = Image.composite(dark, img, scrim)

    d = ImageDraw.Draw(img)
    y = y0
    for (t, f, gap, col), h in zip(blocks, heights):
        x = (W - d.textlength(t, font=f)) / 2
        d.text((x + 2, y + 3), t, font=f, fill=(0, 0, 0))
        d.text((x, y), t, font=f, fill=col)
        y += h + gap

    out = os.path.join(cfg["out_dir"], c["name"] + ".jpg")
    img.save(out, quality=92, subsampling=0)
    return out


def main():
    cfg = json.load(open(sys.argv[1], encoding="utf-8"))
    os.makedirs(cfg["out_dir"], exist_ok=True)
    for c in cfg["cards"]:
        print(card(c, cfg))


if __name__ == "__main__":
    main()
