"""
BE-05 Polite Scraper — Stage 4 Clean, Check, & Store
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

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

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
            
    seen = set()
    unique_items = []
    for item in book_items:
        if item["url"] not in seen:
            seen.add(item["url"])
            unique_items.append(item)
            
    return catalogue_pages, unique_items

def parse_book_detail(url: str, source_page: str) -> Dict[str, Any]:
    html, _ = fetch_html(url)
    soup = BeautifulSoup(html, "html.parser")
    
    h1 = soup.find("h1")
    title = h1.text.strip() if h1 else "Unknown Title"
    
    price_elem = soup.find("p", class_="price_color")
    price_text = price_elem.text.strip() if price_elem else ""
    
    # Normalize price: "£51.77" -> 51.77
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

def clean_check_store():
    cat_pages, book_items = discover_catalogue_pages(START_URL, max_pages=3)
    
    valid_records = []
    error_records = []
    
    # Map by canonical product_url to ensure strict idempotency and deduplication
    books_by_url = {}
    
    for item in book_items:
        raw_data = parse_book_detail(item["url"], item["source_page"])
        try:
            validated = BookRecord(**raw_data)
            books_by_url[validated.product_url] = validated.model_dump()
        except ValidationError as e:
            error_records.append({
                "url": item["url"],
                "raw": raw_data,
                "errors": e.errors()
            })
            
    valid_records = list(books_by_url.values())
    
    # Write to output files
    books_file = os.path.join(OUTPUT_DIR, "books.json")
    with open(books_file, "w", encoding="utf-8") as f:
        json.dump(valid_records, f, indent=2)
        
    errors_file = os.path.join(OUTPUT_DIR, "errors.json")
    with open(errors_file, "w", encoding="utf-8") as f:
        json.dump(error_records, f, indent=2)
        
    return valid_records, error_records

if __name__ == "__main__":
    valid, errors = clean_check_store()
    print(f"Validated records: {len(valid)}")
    print(f"Error records: {len(errors)}")
    assert len(valid) == 60
    assert len(errors) == 0
    print("Stage 4 Checkpoint Passed: Exactly 60 records validated and saved to output/books.json.")
