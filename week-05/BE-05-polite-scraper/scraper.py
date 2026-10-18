"""
BE-05 Polite Scraper — Stage 3 Raw Record Extraction
"""
import os
import time
import datetime
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from typing import Optional, Dict, Any

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

def discover_catalogue_pages(start_url: str, max_pages: int = 3) -> tuple[list[str], list[dict]]:
    """Discovers book URLs and retains their source catalogue page."""
    current_url = start_url
    catalogue_pages = []
    book_items = []
    
    while current_url and len(catalogue_pages) < max_pages:
        html, _ = fetch_html(current_url)
        catalogue_pages.append(current_url)
        soup = BeautifulSoup(html, "html.parser")
        
        articles = soup.find_all("article", class_="product_pod")
        for article in articles:
            h3 = article.find("h3")
            if h3 and h3.find("a"):
                rel_link = h3.find("a")["href"]
                abs_link = urllib.parse.urljoin(current_url, rel_link)
                book_items.append({"url": abs_link, "source_page": current_url})
                
        next_li = soup.find("li", class_="next")
        if next_li and next_li.find("a"):
            next_rel = next_li.find("a")["href"]
            current_url = urllib.parse.urljoin(current_url, next_rel)
        else:
            current_url = None
            
    # Deduplicate by URL
    seen = set()
    unique_items = []
    for item in book_items:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique_items.append(item)
            
    return catalogue_pages, unique_items

def parse_book_detail(url: str, source_page: str) -> Dict[str, Any]:
    """Parses a single book detail page into the 8 required raw fields."""
    html, _ = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    
    # 1. Title
    h1 = soup.find("h1")
    title = h1.text.strip() if h1 else "Unknown Title"
    
    # 2. Product URL (Canonical absolute URL)
    product_url = url
    
    # 3. Price text
    price_elem = soup.find("p", class_="price_color")
    price_text = price_elem.text.strip() if price_elem else ""
    
    # 4. Availability text
    avail_elem = soup.find("p", class_="instock availability")
    availability_text = avail_elem.text.strip() if avail_elem else ""
    
    # 5. Rating text
    rating_text = "Not Rated"
    star_elem = soup.find("p", class_="star-rating")
    if star_elem:
        classes = star_elem.get("class", [])
        for c in classes:
            if c != "star-rating":
                rating_text = c
                break
                
    # 6. Description (Optional; null if missing)
    description = None
    desc_header = soup.find("div", id="product_description")
    if desc_header:
        desc_p = desc_header.find_next_sibling("p")
        if desc_p:
            description = desc_p.text.strip()
            
    # 7. Source page
    # 8. Fetched at (ISO timestamp)
    fetched_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    return {
        "title": title,
        "product_url": product_url,
        "price_text": price_text,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": fetched_at
    }

if __name__ == "__main__":
    cat_pages, book_items = discover_catalogue_pages(START_URL, max_pages=3)
    print(f"Discovered {len(book_items)} books across {len(cat_pages)} catalogue pages.")
    
    # Extract details for the books
    raw_records = []
    for idx, item in enumerate(book_items, 1):
        record = parse_book_detail(item["url"], item["source_page"])
        raw_records.append(record)
        if idx % 15 == 0 or idx == len(book_items):
            print(f"Extracted {idx}/{len(book_items)} book detail pages...")
            
    print("\n--- Sample Complete Raw Record (All 8 Keys) ---")
    import pprint
    pprint.pprint(raw_records[0])
    
    assert len(raw_records) == 60
    assert all(k in raw_records[0] for k in [
        "title", "product_url", "price_text", "availability_text",
        "rating_text", "description", "source_page", "fetched_at"
    ])
    print(f"\nStage 3 Checkpoint Passed: Extracted {len(raw_records)} complete raw records.")
