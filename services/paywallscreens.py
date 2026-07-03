import asyncio
import csv
import re
from playwright.async_api import async_playwright
from bs4 import BeautifulSoup

BASE = "https://www.paywallscreens.com"

# matches things like: $1.2K/month  $1,200/mo  $50k / Month  $1K-$5K/month  $12M/mo
# note: \$\s* (not just \$) because React hydration comments (<!-- -->) split
# "$" from the number into separate text nodes, and get_text(" ", ...) then
# joins them with a space, e.g. "$<!-- -->500K<!-- --> / month" -> "$ 500K / month"
REVENUE_RE = re.compile(
    r'\$\s*[\d,.]+\s*[KkMmBb]?\s*(?:-\s*\$?\s*[\d,.]+\s*[KkMmBb]?)?\s*/\s*(?:mo(?:nth)?)\b',
    re.IGNORECASE
)


def extract_revenue(soup, text):
    """
    Try several strategies since the site doesn't always render revenue
    the same way (missing "/month", different casing, wrapped in a
    labeled stat block instead of loose text, etc).
    """
    # 1. label-based: <label>Revenue</label><span>$X/month</span>
    for label in soup.find_all("label"):
        key = label.get_text(strip=True).lower()
        if "revenue" in key:
            nxt = label.find_next("span")
            if nxt:
                val = nxt.get_text(" ", strip=True)
                if val:
                    return val

    # 2. any element whose class hints at revenue
    el = soup.select_one('[class*="revenue" i]')
    if el:
        val = el.get_text(" ", strip=True)
        if val:
            return val

    # 3. regex over full page text, tolerant of /mo, /Month, ranges, casing
    m = REVENUE_RE.search(text)
    if m:
        return re.sub(r'\$\s+', '$', m.group(0))  # collapse "$ 500K" -> "$500K"

    # 4. last resort: any dollar figure near the word "revenue"
    idx = text.lower().find("revenue")
    if idx != -1:
        window = text[idx: idx + 60]
        m2 = re.search(r'\$\s*[\d,.]+\s*[KkMmBb]?', window)
        if m2:
            return m2.group(0)

    return ""


# ---------------------------
# extract app links fast
# ---------------------------
async def collect_urls(page, limit=None):
    urls = set()
    last = 0
    stall = 0

    while True:
        await page.mouse.wheel(0, 10000)
        await page.wait_for_timeout(1200)

        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        for a in soup.select('a[href^="/apps/"]'):
            urls.add(BASE + a["href"])

        if len(urls) == last:
            stall += 1
        else:
            stall = 0

        last = len(urls)

        print("found:", len(urls))

        # stop early once we have enough (still scroll a little to be safe)
        if limit is not None and len(urls) >= limit:
            break

        if stall >= 4:
            break

    urls = list(urls)

    if limit is not None:
        urls = urls[:limit]

    return urls


# ---------------------------
# scrape single app (fast)
# ---------------------------
async def scrape_app(context, url):
    page = await context.new_page()

    try:
        await page.goto(url, wait_until="domcontentloaded", timeout=30000)

        # give any client-rendered stats (revenue, etc.) a moment to appear
        try:
            await page.wait_for_selector('text=/\\$[\\d.,]+[KMB]?/i', timeout=5000)
        except Exception:
            pass  # some apps genuinely have no revenue figure

        html = await page.content()
        soup = BeautifulSoup(html, "html.parser")

        text = soup.get_text(" ", strip=True)

        app_name = ""
        revenue = ""
        developer = ""
        apple_url = ""

        title = soup.select_one('p[class*="text-xl"]')
        if title:
            app_name = title.get_text(strip=True)

        revenue = extract_revenue(soup, text)

        dev = soup.select_one('a[href*="developer"]')
        if dev:
            developer = dev.get_text(strip=True)

        app = soup.select_one('a[href*="apps.apple.com"]')
        if app:
            apple_url = app["href"]

        values = {"Version": "", "Last updated": "", "Release date": "", "Rating": "", "Downloads": ""}

        for label in soup.find_all("label"):
            key = label.get_text(strip=True)
            if key in values:
                span = label.find_next("span")
                if span:
                    values[key] = span.get_text(" ", strip=True)

        await page.close()

        return [
            app_name,
            revenue,
            developer,
            values["Version"],
            values["Last updated"],
            values["Release date"],
            values["Rating"],
            values["Downloads"],
            apple_url,
            url
        ]

    except Exception:
        await page.close()
        return None


# ---------------------------
# worker pool scraper
# ---------------------------
async def scrape_all(urls, context, concurrency=10):
    results = []
    sem = asyncio.Semaphore(concurrency)

    async def worker(u):
        async with sem:
            return await scrape_app(context, u)

    tasks = [worker(u) for u in urls]

    for f in asyncio.as_completed(tasks):
        r = await f
        if r:
            results.append(r)
            print("done:", len(results))

    return results


# ---------------------------
# main
# ---------------------------
async def main(output="paywallscreens.csv", limit=None, concurrency=12):
    """
    limit: max number of listings to scrape. None = scrape everything found.
    """
    async with async_playwright() as p:
        browser = await p.chromium.launch(headless=True)
        context = await browser.new_context()

        page = await context.new_page()
        await page.goto(BASE, wait_until="networkidle")

        urls = await collect_urls(page, limit=limit)
        await page.close()

        print("TOTAL URLs to scrape:", len(urls))

        data = await scrape_all(urls, context, concurrency=concurrency)

        await browser.close()

    # write ONCE (fast)
    with open(output, "w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow([
            "app_name",
            "monthly_revenue",
            "developer",
            "version",
            "last_updated",
            "release_date",
            "rating",
            "downloads",
            "apple_url",
            "paywall_url"
        ])
        writer.writerows(data)

    print("DONE:", len(data))


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Scrape app listings from paywallscreens.com")
    parser.add_argument("-o", "--output", default="paywallscreens.csv", help="Output CSV file path")
    parser.add_argument("-n", "--limit", type=int, default=None, help="Max number of listings to scrape (default: all)")
    parser.add_argument("-c", "--concurrency", type=int, default=12, help="Number of concurrent scrape workers")

    args = parser.parse_args()

    asyncio.run(main(output=args.output, limit=args.limit, concurrency=args.concurrency))