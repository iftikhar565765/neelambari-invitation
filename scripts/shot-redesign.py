#!/usr/bin/env python3
"""Kalyanam redesign — full visual capture: opening, hero, sections, mobile."""
import asyncio, sys
from playwright.async_api import async_playwright

BASE = "http://127.0.0.1:8791/"

async def main():
    async with async_playwright() as pw:
        b = await pw.chromium.launch()

        # ── desktop ──
        pg = await b.new_page(viewport={"width": 1440, "height": 960})
        errors = []
        pg.on("pageerror", lambda e: errors.append("pageerror: " + str(e)))
        pg.on("console", lambda m: errors.append("console: " + m.text) if m.type == "error" else None)
        await pg.goto(BASE, wait_until="networkidle")
        await pg.wait_for_timeout(1600)

        # opening
        await pg.screenshot(path="/tmp/shots/d-open.png")

        # enter via the ticket itself (the real interaction)
        try:
            await pg.click("#envelope", timeout=4000)
            await pg.wait_for_timeout(3600)
        except Exception as e:
            errors.append("enter: %r" % e)
        opening_gone = await pg.evaluate("getComputedStyle(document.getElementById('opening')).display === 'none'")
        errors.append("opening removed: %s" % opening_gone)

        await pg.screenshot(path="/tmp/shots/d-hero-top.png")
        await pg.screenshot(path="/tmp/shots/d-hero-full.png", full_page=True)

        for sel, name in [("#story", "story"), ("#save-the-date", "std"),
                          ("#details", "details"), ("#palette", "palette"),
                          ("#itinerary", "itinerary"), ("#venue", "venue"),
                          ("#countdown", "countdown"), ("#rsvp", "rsvp"),
                          ("#closing", "closing")]:
            el = pg.locator(sel)
            await el.scroll_into_view_if_needed()
            await pg.wait_for_timeout(500)
            await el.screenshot(path=f"/tmp/shots/d-{name}.png")

        await pg.close()

        # ── mobile ──
        m = await b.new_page(viewport={"width": 390, "height": 844})
        m.on("pageerror", lambda e: errors.append("m pageerror: " + str(e)))
        await m.goto(BASE, wait_until="networkidle")
        await m.wait_for_timeout(1400)
        await m.screenshot(path="/tmp/shots/m-open.png")
        try:
            await m.click("#envelope", timeout=4000)
            await m.wait_for_timeout(3600)
        except Exception as e:
            errors.append("m enter: %r" % e)
        await m.screenshot(path="/tmp/shots/m-hero-top.png")
        hero = m.locator("#invitation")
        await hero.scroll_into_view_if_needed()
        await m.wait_for_timeout(400)
        await hero.screenshot(path="/tmp/shots/m-hero-full.png")
        for sel, name in [("#details", "details"), ("#rsvp", "rsvp")]:
            el = m.locator(sel)
            await el.scroll_into_view_if_needed()
            await m.wait_for_timeout(400)
            await el.screenshot(path=f"/tmp/shots/m-{name}.png")
        await m.close()
        await b.close()

        if errors:
            print("ERRORS:")
            for e in errors[:12]:
                print(" -", e)
        else:
            print("no js errors")
        print("done")

asyncio.run(main())
