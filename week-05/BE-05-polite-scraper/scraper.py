"""
BE-05 Polite Scraper — Stage 1 Fetch & Cache
"""
import os
import time
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError

BASE_URL = "https://books.toscrape.com/"
USER_AGENT = "FlyRankInternship-BE05/1.0 (+https://github.com/kunalaggarwal)"
REQUEST_TIMEOUT = 10
REQUEST_DELAY = 0.5 # 500ms polite pause

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_cache_path(url: str) -> str:
    # Generate clean filesystem-safe filename from URL
    safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_")
    if not safe_name.endswith(".html"):
        safe_name += ".html"
    return os.path.join(CACHE_DIR, safe_name)

def fetch_html(url: str, use_cache: bool = True) -> tuple[str, bool]:
    """Fetches HTML with disk caching, custom User-Agent, timeout, and status checking.
    Returns (html_content, is_cache_hit)."""
    cache_file = get_cache_path(url)
    if use_cache and os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            print(f"[CACHE HIT] {url} -> {os.path.basename(cache_file)}")
            return f.read(), True

    print(f"[FETCHING]  {url}")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        time.sleep(REQUEST_DELAY) # Polite delay
        with urllib.request.urlopen(req, timeout=REQUEST_TIMEOUT) as response:
            if response.status != 200:
                raise HTTPError(url, response.status, f"Unexpected HTTP status {response.status}", response.headers, None)
            html = response.read().decode("utf-8")
            
        with open(cache_file, "w", encoding="utf-8") as f:
            f.write(html)
        return html, False
    except HTTPError as e:
        print(f"[ERROR] HTTP {e.code} for {url}")
        raise
    except URLError as e:
        print(f"[ERROR] Network error for {url}: {e.reason}")
        raise

if __name__ == "__main__":
    test_url = "https://books.toscrape.com/catalogue/page-1.html"
    print("Run 1:")
    html, hit = fetch_html(test_url)
    assert not hit or os.path.exists(get_cache_path(test_url))
    
    print("\nRun 2:")
    html, hit = fetch_html(test_url)
    assert hit is True
    print("\nStage 1 Checkpoint Passed: Fetch & Cache working reliably.")
