#!/usr/bin/env python3
"""Kalyanam — capture story/palette/rsvp/closing and stitch one sheet."""
import asyncio
from playwright.async_api import async_playwright


async def shoot():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pg = await b.new_page(viewport={"width": 1440, "height": 900})
        await pg.goto("http://127.0.0.1:8791/", wait_until="networkidle")
        await pg.wait_for_timeout(800)
        try:
            await pg.click("#skip-intro", timeout=2500)
            await pg.wait_for_timeout(200)
            await pg.click("#open-invitation", timeout=2500)
            await pg.wait_for_timeout(1400)
        except Exception:
            pass
        for sel, name in [("#story", "story"), ("#palette", "palette"),
                          ("#rsvp", "rsvp"), ("#closing", "closing")]:
            el = pg.locator(sel)
            await el.scroll_into_view_if_needed()
            await pg.wait_for_timeout(600)
            await el.screenshot(path=f"/tmp/kk-{name}.png")
        await b.close()


asyncio.run(shoot())

from PIL import Image

ims = [Image.open(f"/tmp/kk-{n}.png") for n in ["story", "palette", "rsvp", "closing"]]
tw = 700
scaled = [im.resize((tw, int(im.height * tw / im.width))) for im in ims]
H = max(scaled[0].height + scaled[2].height, scaled[1].height + scaled[3].height) + 20
sheet = Image.new("RGB", (tw * 2 + 30, H), (34, 34, 34))
sheet.paste(scaled[0], (0, 0))
sheet.paste(scaled[1], (tw + 30, 0))
y = max(scaled[0].height, scaled[1].height) + 20
sheet.paste(scaled[2], (0, y))
sheet.paste(scaled[3], (tw + 30, y))
sheet.save("/tmp/kk-sheet.jpg", quality=82)
print("sheet saved")
