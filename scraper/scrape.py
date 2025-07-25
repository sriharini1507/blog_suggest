from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
import sys

def extract_text_from_url(url):
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # 👈 switch to non-headless
        page = browser.new_page(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 Chrome/118.0.5993.118 Safari/537.36"
        )

        try:
            print(f"Navigating to {url} ...", file=sys.stderr)
            page.goto(url, wait_until="domcontentloaded", timeout=60000)
            content = page.content()
            soup = BeautifulSoup(content, "html.parser")
            for tag in soup(["script", "style", "meta", "noscript"]):
                tag.decompose()
            text = soup.get_text(separator=" ", strip=True)
            return text[:5000]
        except Exception as e:
            return f"Error: {str(e)}"
        finally:
            browser.close()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python scrape.py <url>")
    else:
        url = sys.argv[1]
        print(extract_text_from_url(url))
