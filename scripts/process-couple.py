#!/usr/bin/env python3
"""Kalyanam — couple art post-processing.
white-bg illustration -> rembg -> white-matte despill -> trim -> resize -> optimized RGBA png
"""
import io
from pathlib import Path
from PIL import Image
from rembg import remove, new_session

SRC = Path("/home/z/my-project/kalyanam-invitation/_raw-art/couple.png")
OUT = Path("/home/z/my-project/kalyanam-invitation/assets/art/couple.png")

session = new_session("isnet-general-use")

img = Image.open(SRC).convert("RGBA")
out = remove(img, session=session, post_process_mask=True).convert("RGBA")

# white-matte despill: rebuild true colour for semi-transparent pixels
px = out.load()
w, h = out.size
for y in range(h):
    for x in range(w):
        r, g, b, a = px[x, y]
        if 0 < a < 255:
            af = a / 255.0
            r = max(0, min(255, round((r - (1 - af) * 255) / af)))
            g = max(0, min(255, round((g - (1 - af) * 255) / af)))
            b = max(0, min(255, round((b - (1 - af) * 255) / af)))
            px[x, y] = (r, g, b, a)

# trim to visible bbox
alpha = out.getchannel("A")
bbox = alpha.point(lambda v: 255 if v > 8 else 0).getbbox()
out = out.crop(bbox)

# resize to max long edge 1200
w, h = out.size
if max(w, h) > 1200:
    s = 1200 / max(w, h)
    out = out.resize((round(w * s), round(h * s)), Image.LANCZOS)

buf = io.BytesIO()
out.quantize(colors=256, method=Image.FASTOCTREE, dither=Image.FLOYDSTEINBERG).save(buf, "PNG", optimize=True)
OUT.parent.mkdir(parents=True, exist_ok=True)
OUT.write_bytes(buf.getvalue())
print(f"couple.png -> {out.size[0]}x{out.size[1]}, {len(buf.getvalue())//1024} KB")
