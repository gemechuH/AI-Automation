# PURPOSE:
# This script takes a single URL, downloads the webpage, and strips away the coding (HTML) 
# so the AI only has to read plain text. It includes a resilient retry mechanism to 
# handle websites that try to block automated scraping (like 403 Forbidden errors).

import urllib.request
import urllib.error
import sys
import os
import time
from html.parser import HTMLParser

# A simple tool to rip text out of HTML code
class SimpleTextExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.result = []
        # Ignore text inside these tags (scripts, CSS styling)
        self.ignore = False 

    def handle_starttag(self, tag, attrs):
        if tag in ['script', 'style', 'nav', 'header', 'footer']:
            self.ignore = True

    def handle_endtag(self, tag):
        if tag in ['script', 'style', 'nav', 'header', 'footer']:
            self.ignore = False

    def handle_data(self, data):
        if not self.ignore:
            clean = data.strip()
            if clean:
                self.result.append(clean)

def scrape(url, max_retries=3):
    print(f"Scraping: {url}...")
    
    # Send headers that mimic a real web browser to avoid getting blocked
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
        'Accept-Language': 'en-US,en;q=0.5',
        'Connection': 'keep-alive'
    }
    
    req = urllib.request.Request(url, headers=headers)
    
    for attempt in range(1, max_retries + 1):
        try:
            # Download the webpage
            html = urllib.request.urlopen(req, timeout=10).read().decode('utf-8', errors='ignore')
            
            # Extract the text
            extractor = SimpleTextExtractor()
            extractor.feed(html)
            text = " ".join(extractor.result)
            
            return text
            
        except urllib.error.HTTPError as e:
            print(f"Attempt {attempt}/{max_retries} failed with HTTP Error {e.code}: {e.reason}")
        except Exception as e:
            print(f"Attempt {attempt}/{max_retries} failed. Reason: {e}")
            
        if attempt < max_retries:
            print("Retrying in 2 seconds...")
            time.sleep(2)
            
    print(f"Failed to scrape {url} completely after {max_retries} attempts.")
    return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a URL! Example: python scrape_single_site.py https://example.com")
        sys.exit(1)
        
    url = sys.argv[1]
    text_data = scrape(url)
    
    if text_data:
        os.makedirs('.tmp', exist_ok=True)
        # Save the raw text for the AI to read next
        with open('.tmp/raw_scrape.txt', 'w', encoding='utf-8') as f:
            f.write(text_data)
        print(f"Successfully scraped {len(text_data)} characters!")
        print("Data saved to .tmp/raw_scrape.txt")
        sys.exit(0) # Success
    else:
        # Exit with error so the main runner knows it failed
        sys.exit(1)
