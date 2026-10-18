"""
BE-05 Polite Scraper — Stage 2 Catalogue Discovery
"""
import os
import time
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup

BASE_URL = "https://books.toscrape.com/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"
USER_AGENT = "FlyRankInternship-BE05/1.0 (+https://github.com/kunalaggarwal)"
REQUEST_TIMEOUT = 10
REQUEST_DELAY = 0.5 # 500ms polite pause

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def get_cache_path(url: str) -> str:
    safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_")
    if not safe_name.endswith(".html"):
        safe_name += ".html"
    return os.path.join(CACHE_DIR, safe_name)

def fetch_html(url: str, use_cache: bool = True) -> tuple[str, bool]:
    cache_file = get_cache_path(url)
    if use_cache and os.path.exists(cache_file):
        with open(cache_file, "r", encoding="utf-8") as f:
            return f.read(), True

    print(f"[FETCHING]  {url}")
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        time.sleep(REQUEST_DELAY)
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

def discover_catalogue_pages(start_url: str, max_pages: int = 3) -> tuple[list[str], list[str]]:
    """Crawls up to max_pages catalogue pages and returns (catalogue_urls, book_urls)."""
    current_url = start_url
    catalogue_pages = []
    book_urls = []
    
    while current_url and len(catalogue_pages) < max_pages:
        html, _ = fetch_html(current_url)
        catalogue_pages.append(current_url)
        soup = BeautifulSoup(html, "html.parser")
        
        # Each book card is an <article class="product_pod">
        articles = soup.find_all("article", class_="product_pod")
        for article in articles:
            h3 = article.find("h3")
            if h3 and h3.find("a"):
                rel_link = h3.find("a")["href"]
                # Convert relative URL to canonical absolute URL
                abs_link = urllib.parse.urljoin(current_url, rel_link)
                book_urls.append(abs_link)
                
        # Find pagination "next" link
        next_li = soup.find("li", class_="next")
        if next_li and next_li.find("a"):
            next_rel = next_li.find("a")["href"]
            current_url = urllib.parse.urljoin(current_url, next_rel)
        else:
            current_url = None
            
    # Deduplicate while preserving order
    unique_books = list(dict.fromkeys(book_urls))
    return catalogue_pages, unique_books

if __name__ == "__main__":
    cat_pages, books = discover_catalogue_pages(START_URL, max_pages=3)
    print(f"\ncatalogue_pages={len(cat_pages)}, discovered={len(books)}, unique_urls={len(set(books))}")
    assert len(cat_pages) == 3
    assert len(books) == 60
    assert len(set(books)) == 60
    print("Stage 2 Checkpoint Passed: Discovered exactly 60 unique book URLs across 3 catalogue pages.")
