from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import sys
import time

def extract_text_from_url(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=False)  # Use True for deployment
            context = browser.new_context(
                ignore_https_errors=True,
                user_agent=(
                    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
                    "AppleWebKit/537.36 (KHTML, like Gecko) "
                    "Chrome/114.0.0.0 Safari/537.36"
                )
            )

            page = context.new_page()
            print(f"🔍 Navigating to {url} ...", file=sys.stderr)
            page.goto(url, wait_until="load", timeout=70000)
            time.sleep(3)  # Let JS content load

            content = page.content()
            browser.close()

            soup = BeautifulSoup(content, "html.parser")
            for tag in soup(["script", "style", "meta", "noscript"]):
                tag.decompose()

            text = soup.get_text(separator=" ", strip=True)
            clean_text = text[:5000].strip()
            return clean_text if clean_text else "Error: No readable content found."

    except Exception as e:
        print(f"Scraper error: {str(e)}", file=sys.stderr)
        return "Error: Scraping failed"

# CLI for testing
if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scrape.py <url>")
    else:
        url = sys.argv[1]
        print(extract_text_from_url(url))
