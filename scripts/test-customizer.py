#!/usr/bin/env python3
"""Kalyanam customizer end-to-end: preview, live edit, theme switch."""
import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()
        pc = await b.new_page(viewport={"width": 1600, "height": 1000})
        errors = []
        pc.on("pageerror", lambda e: errors.append(str(e)))
        await pc.goto("http://127.0.0.1:8791/customize.html", wait_until="networkidle")
        await pc.wait_for_timeout(2200)

        # the preview overlay must be open — the iframe has no size otherwise
        try:
            await pc.click("#preview-toggle", timeout=2000)
            await pc.wait_for_timeout(1500)
        except Exception:
            pass

        frame = pc.frames[-1]  # the preview iframe
        await frame.wait_for_selector("#invitation-title", timeout=10000)
        names = await frame.eval_on_selector(".kcard-names", 'el => el.textContent.trim().replace(/\\s+/g," ")')
        print("preview names:", names)

        # live edit propagates into the iframe
        await pc.fill("#f-couple-partnerOne", "Karthik")
        await pc.wait_for_timeout(1400)
        names2 = await frame.eval_on_selector(".kcard-names", 'el => el.textContent.trim().replace(/\\s+/g," ")')
        print("after live edit:", names2)
        await pc.fill("#f-couple-partnerOne", "Arjun")   # restore sample
        await pc.wait_for_timeout(600)

        # walk to the design step with the preview closed (overlay blocks clicks)
        try:
            await pc.click("#preview-close", timeout=1500)
            await pc.wait_for_timeout(400)
        except Exception:
            pass
        for _ in range(8):
            lbl = await pc.eval_on_selector("#flow-step-name", "el=>el.textContent")
            if "Colour" in lbl:
                break
            await pc.click("#flow-next", timeout=2000)
            await pc.wait_for_timeout(300)
            try:
                await pc.click("#preview-close", timeout=800)
            except Exception:
                pass
        await pc.wait_for_timeout(400)
        lbl = await pc.eval_on_selector("#flow-step-name", "el=>el.textContent")
        print("now at step:", lbl)

        cards = pc.locator(".theme-card")
        n = await cards.count()
        print("theme cards:", n)
        if n:
            await cards.nth(1).click()   # rani
            await pc.wait_for_timeout(1400)
            ink = await frame.evaluate("getComputedStyle(document.querySelector('.kcard-names')).color")
            bg = await frame.evaluate("getComputedStyle(document.body).backgroundColor")
            print("rani theme -> hero color:", ink, "| body bg:", bg)
            await cards.nth(0).click()   # back to marigold
            await pc.wait_for_timeout(900)
            bg2 = await frame.evaluate("getComputedStyle(document.body).backgroundColor")
            print("marigold restored -> body bg:", bg2)

        print("page errors:", errors[:5] if errors else "none")
        await b.close()

asyncio.run(main())
