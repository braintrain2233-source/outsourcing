import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import sys

BASE_URL = "https://braintrain2233-source.github.io/outsourcing/"

def check_link(url):
    try:
        r = requests.head(url, allow_redirects=True, timeout=5)
        if r.status_code >= 400:
            return False, r.status_code
        return True, r.status_code
    except requests.RequestException:
        return False, None

def crawl_page(url, visited):
    if url in visited:
        return
    visited.add(url)

    try:
        res = requests.get(url, timeout=10)
        res.raise_for_status()
    except requests.RequestException:
        print(f"[ERROR] ページ取得失敗: {url}")
        return

    soup = BeautifulSoup(res.text, "html.parser")
    for link in soup.find_all("a", href=True):
        full_url = urljoin(url, link["href"])
        alive, status = check_link(full_url)
        status_text = f"{'OK' if alive else 'NG'} ({status})"
        print(f"{full_url} → {status_text}")
        if BASE_URL in full_url:
            crawl_page(full_url, visited)

if __name__ == "__main__":
    print(f"=== {BASE_URL} のリンクチェック開始 ===")
    crawl_page(BASE_URL, set())
    print("=== チェック完了 ===")
