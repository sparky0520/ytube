import asyncio
from playwright.async_api import async_playwright

URL = "https://www.youtube.com/@Zdak/shorts"

async def scrape_shorts():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        page = await browser.new_page()

        await page.goto(URL, timeout=0)

        # Scroll to load more shorts
        for _ in range(10):
            await page.mouse.wheel(0, 2000)
            await page.wait_for_timeout(1000)

        # Query all anchor tags inside shorts lockups
        links = await page.eval_on_selector_all(
            "a",
            "els => els.map(e => e.href)"
        )

        shorts = [x for x in links if '/shorts/' in x]

        print("Found:", len(shorts))
        for s in sorted(set(shorts)):
            print(s)

        await browser.close()

asyncio.run(scrape_shorts())
