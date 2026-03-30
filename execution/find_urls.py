import urllib.request
import urllib.parse
import re

def search():
    query = urllib.parse.quote("best AI tools for small business 2026")
    url = f"https://html.duckduckgo.com/html/?q={query}"
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64)'}
    req = urllib.request.Request(url, headers=headers)
    try:
        html = urllib.request.urlopen(req).read().decode('utf-8')
        links = re.findall(r'<a class="result__url" href="([^"]+)">([^<]+)</a>', html)
        for link, text in links[:5]:
            # Duckduckgo wraps urls in /l/?uddg=...
            if 'uddg=' in link:
                actual_url = urllib.parse.unquote(link.split('uddg=')[1].split('&')[0])
                print(actual_url)
            else:
                print(link)
    except Exception as e:
        print(f"Failed: {e}")

search()
