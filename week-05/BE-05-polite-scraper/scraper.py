"""
BE-05 Polite Scraper — Stage 0 Target Classification
Target Sandbox: https://books.toscrape.com
Scope: First 3 catalogue pages only (60 books).
"""
import os

BASE_URL = "https://books.toscrape.com/"
USER_AGENT = "FlyRankInternship-BE05/1.0 (+https://github.com/kunalaggarwal)"
REQUEST_TIMEOUT = 10
REQUEST_DELAY = 0.5 # 500ms minimum delay between network calls

CACHE_DIR = os.path.join(os.path.dirname(__file__), "cache")
OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "output")

os.makedirs(CACHE_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

print("Stage 0: Target classified as sandbox at books.toscrape.com.")
