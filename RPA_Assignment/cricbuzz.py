import asyncio
from playwright.async_api import async_playwright

QUERY = "cricbuzz india vs south africa women final scorecard 2025"

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=False)
        page = await browser.new_page()

        await page.goto("https://www.bing.com")

        # wait until input is really ready
        await page.wait_for_selector('xpath=//*[@id="sb_form_q"]', state="visible")

        search_input = page.locator('xpath=//*[@id="sb_form_q"]')
        await search_input.click()
        await search_input.fill("")          # reset (bing sometimes keeps text cache)
        await asyncio.sleep(0.30)            # IMPORTANT – hydration settle
        await search_input.fill(QUERY)

        await search_input.press("Enter")

        await page.wait_for_selector("li.b_algo h2 a", timeout=15000)
        first_link = page.locator("li.b_algo h2 a").first
        await first_link.click()

        await page.wait_for_load_state("load")
        print("final URL:", page.url)

        await asyncio.sleep(5)
        await browser.close()

asyncio.run(main())
