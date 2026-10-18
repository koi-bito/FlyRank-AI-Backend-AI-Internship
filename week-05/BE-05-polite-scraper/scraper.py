"""
BE-05 Polite Scraper — Stage 5 Fault-Tolerance & Run Reporting
"""
import os
import re
import json
import time
import datetime
import urllib.request
import urllib.parse
from urllib.error import HTTPError, URLError
from bs4 import BeautifulSoup
from pydantic import BaseModel, Field, ValidationError, field_validator
from typing import Optional, List, Dict, Any

BASE_URL = "https://books.toscrape.com/"
START_URL = "https://books.toscrape.com/catalogue/page-1.html"
USER_AGENT = "FlyRankInternship-BE05/1.0 (+https://github.com/kunalaggarwal)"
REQUEST_TIMEOUT = 10
REQUEST_DELAY = 0.5
MAX_RETRIES = 2

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

# Run metrics counters
metrics = {
    "start_time": "",
    "end_time": "",
    "duration_seconds": 0.0,
    "pages_requested": 0,
    "cache_hits": 0,
    "network_fetches": 0,
    "valid_records": 0,
    "invalid_records": 0,
    "failed_pages": []
}

class BookRecord(BaseModel):
    title: str = Field(..., min_length=1, description="Book title")
    product_url: str = Field(..., description="Canonical absolute product URL")
    price_text: str = Field(..., description="Raw price text with currency symbol")
    price_gbp: float = Field(..., gt=0, description="Normalized numeric price in GBP")
    availability_text: str = Field(..., description="Raw stock availability string")
    rating_text: str = Field(..., description="Text rating (e.g. One, Two, Three, Four, Five)")
    description: Optional[str] = Field(None, description="Product description text or None")
    source_page: str = Field(..., description="Origin catalogue page URL")
    fetched_at: str = Field(..., description="ISO 8601 UTC timestamp of retrieval")

    @field_validator("product_url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        if not v.startswith("https://") and not v.startswith("http://"):
            raise ValueError(f"Invalid URL schema: {v}")
        return v

def get_cache_path(url: str) -> str:
    safe_name = url.replace("https://", "").replace("http://", "").replace("/", "_").replace("?", "_")
    if not safe_name.endswith(".html"):
        safe_name += ".html"
    return os.path.join(CACHE_DIR, safe_name)

def fetch_html_with_resilience(url: str, use_cache: bool = True) -> tuple[str, bool]:
    metrics["pages_requested"] += 1
    cache_file = get_cache_path(url)
    
    if use_cache and os.path.exists(cache_file):
        metrics["cache_hits"] += 1
        with open(cache_file, "r", encoding="utf-8") as f:
            return f.read(), True

    metrics["network_fetches"] += 1
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    
    # Retry policy: Retry on timeouts or 5xx; NEVER retry on 404/403 (wastes quota/doomed to fail)
    attempts = 0
    while attempts <= MAX_RETRIES:
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
            if 400 <= e.code < 500:
                # 4xx client errors (e.g. 404 Not Found) are not transient; abort immediately
                raise
            attempts += 1
            if attempts > MAX_RETRIES:
                raise
            time.sleep(1.0 * attempts)
        except (URLError, TimeoutError) as e:
            attempts += 1
            if attempts > MAX_RETRIES:
                raise
            time.sleep(1.0 * attempts)

def discover_catalogue_pages(start_url: str, max_pages: int = 3) -> tuple[list[str], list[dict]]:
    current_url = start_url
    catalogue_pages = []
    book_items = []
    
    while current_url and len(catalogue_pages) < max_pages:
        html, _ = fetch_html_with_resilience(current_url)
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
            
    seen = set()
    unique_items = []
    for item in book_items:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique_items.append(item)
            
    return catalogue_pages, unique_items

def parse_book_detail(url: str, source_page: str) -> Dict[str, Any]:
    html, _ = fetch_html_with_resilience(url)
    soup = BeautifulSoup(html, "html.parser")
    
    h1 = soup.find("h1")
    title = h1.text.strip() if h1 else "Unknown Title"
    
    price_elem = soup.find("p", class_="price_color")
    price_text = price_elem.text.strip() if price_elem else ""
    
    price_gbp = 0.0
    price_match = re.search(r"[\d\.]+", price_text)
    if price_match:
        try:
            price_gbp = float(price_match.group(0))
        except ValueError:
            price_gbp = 0.0
            
    avail_elem = soup.find("p", class_="instock availability")
    availability_text = avail_elem.text.strip() if avail_elem else ""
    
    rating_text = "Not Rated"
    star_elem = soup.find("p", class_="star-rating")
    if star_elem:
        classes = star_elem.get("class", [])
        for c in classes:
            if c != "star-rating":
                rating_text = c
                break
                
    description = None
    desc_header = soup.find("div", id="product_description")
    if desc_header:
        desc_p = desc_header.find_next_sibling("p")
        if desc_p:
            description = desc_p.text.strip()
            
    fetched_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    
    return {
        "title": title,
        "product_url": url,
        "price_text": price_text,
        "price_gbp": price_gbp,
        "availability_text": availability_text,
        "rating_text": rating_text,
        "description": description,
        "source_page": source_page,
        "fetched_at": fetched_at
    }

def run_resilient_scrape(inject_broken_url: bool = True):
    start_dt = datetime.datetime.now(datetime.timezone.utc)
    metrics["start_time"] = start_dt.isoformat()
    start_clock = time.time()
    
    cat_pages, book_items = discover_catalogue_pages(START_URL, max_pages=3)
    
    # Inject deliberate broken URL to prove resilience (Stage 5 Checkpoint)
    if inject_broken_url:
        book_items.append({
            "url": "https://books.toscrape.com/catalogue/deliberately-broken-fake-book-999.html",
            "source_page": "https://books.toscrape.com/catalogue/page-1.html"
        })
        
    books_by_url = {}
    error_records = []
    
    for item in book_items:
        try:
            raw_data = parse_book_detail(item["url"], item["source_page"])
            validated = BookRecord(**raw_data)
            books_by_url[validated.product_url] = validated.model_dump()
        except HTTPError as e:
            # Handle broken/404 pages gracefully without crashing
            print(f"[RECOVERED] Skipping broken page {item['url']} -> HTTP {e.code}")
            metrics["failed_pages"].append({
                "url": item["url"],
                "error": f"HTTP {e.code}: {e.reason}",
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            })
        except Exception as e:
            print(f"[RECOVERED] Error processing {item['url']} -> {e}")
            metrics["failed_pages"].append({
                "url": item["url"],
                "error": str(e),
                "timestamp": datetime.datetime.now(datetime.timezone.utc).isoformat()
            })
            
    valid_records = list(books_by_url.values())
    metrics["valid_records"] = len(valid_records)
    metrics["invalid_records"] = len(error_records)
    
    end_clock = time.time()
    metrics["end_time"] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    metrics["duration_seconds"] = round(end_clock - start_clock, 2)
    
    # Write output artifacts
    with open(os.path.join(OUTPUT_DIR, "books.json"), "w", encoding="utf-8") as f:
        json.dump(valid_records, f, indent=2)
        
    with open(os.path.join(OUTPUT_DIR, "errors.json"), "w", encoding="utf-8") as f:
        json.dump(error_records, f, indent=2)
        
    with open(os.path.join(OUTPUT_DIR, "run-report.json"), "w", encoding="utf-8") as f:
        json.dump(metrics, f, indent=2)
        
    return valid_records, metrics

if __name__ == "__main__":
    valid_books, report = run_resilient_scrape(inject_broken_url=True)
    print("\n=== RUN REPORT SUMMARY ===")
    print(f"Duration: {report['duration_seconds']}s")
    print(f"Pages Requested: {report['pages_requested']}")
    print(f"Cache Hits: {report['cache_hits']}")
    print(f"Network Fetches: {report['network_fetches']}")
    print(f"Valid Books Saved: {report['valid_records']}")
    print(f"Failed Pages Survived: {len(report['failed_pages'])}")
    
    assert len(valid_books) == 60
    assert len(report["failed_pages"]) == 1
    print("\nStage 5 Checkpoint Passed: Broken page survived, 60 good records preserved, run-report.json generated.")
