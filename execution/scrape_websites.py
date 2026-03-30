import sys
import json
import urllib.request
import urllib.error
import re
from html.parser import HTMLParser
import os

class TextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.text = []
        self.skip_tags = {'script', 'style', 'head', 'meta', 'link', 'noscript', 'nav', 'footer', 'header'}
        self.current_tag = []

    def handle_starttag(self, tag, attrs):
        self.current_tag.append(tag)

    def handle_endtag(self, tag):
        if self.current_tag and self.current_tag[-1] == tag:
            self.current_tag.pop()

    def handle_data(self, data):
        if not self.current_tag or self.current_tag[-1] not in self.skip_tags:
            clean_text = data.strip()
            if clean_text:
                self.text.append(clean_text)

    def get_text(self):
        return ' '.join(self.text)

def scrape_url(url):
    print(f"Scraping: {url}")
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'}
    req = urllib.request.Request(url, headers=headers)
    try:
        with urllib.request.urlopen(req, timeout=10) as response:
            html = response.read().decode('utf-8', errors='ignore')
            extractor = TextExtractor()
            extractor.feed(html)
            text = extractor.get_text()
            # Clean up excessive whitespace
            text = re.sub(r'\s+', ' ', text)
            print(f"Successfully scraped {len(text)} characters.")
            return text
    except Exception as e:
        print(f"Failed to scrape {url}: {e}")
        return None

def main():
    if len(sys.argv) < 2:
        print("Usage: python scrape_websites.py <url1> <url2> ...")
        sys.exit(1)

    urls = sys.argv[1:]
    results = {}
    
    for url in urls:
        content = scrape_url(url)
        if content:
            results[url] = content

    os.makedirs('.tmp', exist_ok=True)
    out_path = os.path.join('.tmp', 'scraped_data.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(results, f, indent=2, ensure_ascii=False)
    
    print(f"Scraping complete. Saved to {out_path}")

if __name__ == "__main__":
    main()
