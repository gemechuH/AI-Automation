# PURPOSE: 
# This script searches the web for a topic and saves the top URLs to a file.
# It acts as the "eyes" of the execution layer.

import urllib.request
import urllib.parse
import re
import sys
import os

def search_duckduckgo(query):
    # Encode the search query so the web URL can read it safely
    safe_query = urllib.parse.quote(query)
    url = f"https://html.duckduckgo.com/html/?q={safe_query}"
    
    # Pretend to be a normal web browser so we don't get blocked
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(url, headers=headers)
    
    try:
        print(f"Searching for: {query}...")
        html = urllib.request.urlopen(req).read().decode('utf-8')
        
        # Simple regex to find the links in the DuckDuckGo HTML
        links = re.findall(r'<a class="result__url" href="([^"]+)">([^<]+)</a>', html)
        
        results = []
        for link, text in links[:3]: # Get top 3 links
            # Clean up the DuckDuckGo redirect link
            if 'uddg=' in link:
                actual_url = urllib.parse.unquote(link.split('uddg=')[1].split('&')[0])
                results.append(actual_url)
            else:
                results.append(link)
                
        return results
    except Exception as e:
        print(f"Search failed: {e}")
        return []

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Please provide a search topic! Example: python search_sources.py \"AI CRMs\"")
        sys.exit(1)
        
    topic = sys.argv[1]
    urls = search_duckduckgo(topic)
    
    # Save the URLs to a temporary text file for the next step
    os.makedirs('.tmp', exist_ok=True)
    with open('.tmp/urls.txt', 'w') as f:
        for u in urls:
            f.write(u + '\n')
            print(f"Found URL: {u}")
            
    print("Saved URLs to .tmp/urls.txt")
