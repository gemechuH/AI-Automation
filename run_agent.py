import subprocess
import sys
from pathlib import Path
xsdjhkf

BASE_DIR = Path(__file__).resolve().parent
TMP_DIR = BASE_DIR / ".tmp"
URLS_FILE = TMP_DIR / "urls.txt"


def run_command(command):
    print(f"\nRunning: {' '.join(command)}\n")
    result = subprocess.run(command, capture_output=True, text=True)

    if result.stdout:
        print(result.stdout)

    if result.returncode != 0:
        print("Error:")
        print(result.stderr)
        sys.exit(result.returncode)

    return result.stdout


def get_all_urls():
    if not URLS_FILE.exists():
        print("urls.txt not found. Search step may have failed.")
        sys.exit(1)

    with open(URLS_FILE, "r", encoding="utf-8") as f:
        lines = [line.strip() for line in f.readlines() if line.strip()]

    if not lines:
        print("No URLs found in .tmp/urls.txt")
        sys.exit(1)

    return lines


def score_urls(urls: list[str], topic: str) -> list[str]:
    """
    Scores a list of URLs based on how likely they are to be good sources
    that won't block our simple scraper.
    """
    print("\n--- Scoring URLs ---\n")
    scored_list = []
    
    # Simple list of keywords from the topic
    topic_keywords = [word.lower() for word in topic.split() if len(word) > 3]
    
    # Common sites that block simple python scripts
    hard_sites = ["forbes.com", "medium.com", "bloomberg.com", "wsj.com", "nytimes.com", "reuters.com"]
    
    # Good signs it's an article
    good_words = ["blog", "guide", "tools", "resources", "article", "post", "review"]

    for url in urls:
        score: int = 0
        reasons = []
        url_lower = url.lower()
        
        # 1. Check for topic keywords (+3)
        for keyword in topic_keywords:
            if keyword in url_lower:
                score += 3
                reasons.append(f"+3 (keyword '{keyword}' found)")
                break # Only give +3 once
                
        # 2. Prefer blog/guide paths (+2)
        for word in good_words:
            if word in url_lower:
                score += 2
                reasons.append(f"+2 (good word '{word}' found)")
                break # Only give +2 once
                
        # 3. Penalize hard sites (-3)
        for site in hard_sites:
            if site in url_lower:
                score -= 3
                reasons.append(f"-3 (known hard site '{site}')")
                break
                
        # 4. Check if it's just a homepage (-2)
        # e.g., https://example.com or https://example.com/
        parts = url.split('/')
        if len(parts) <= 4 and (not parts[-1] or parts[-1] == ""):
            score -= 2
            reasons.append("-2 (looks like a homepage)")
        elif len(parts) > 4:
            # 5. Reward specific paths (+1)
            score += 1
            reasons.append("+1 (detailed path)")

        if not reasons:
            reasons.append("0 (no special matches)")

        print(f"URL: {url}")
        print(f"Score: {score} | Reasons: {', '.join(reasons)}\n")
        
        scored_list.append((score, url))

    # Sort from highest score to lowest
    scored_list.sort(key=lambda x: x[0], reverse=True)
    return [url for score, url in scored_list]


def main():
    if len(sys.argv) < 2:
        print('Please provide a research topic! Example: python run_agent.py "AI tools for small business"')
        sys.exit(1)

    topic = sys.argv[1]

    print(f"\n=== Research Agent Started ===")
    print(f"Topic: {topic}")

    # 1. Search the web
    run_command(["python", "execution/search_sources.py", topic])

    # 2. Get and Score URLs
    all_urls = get_all_urls()
    best_urls = score_urls(all_urls, topic)
    
    # 3. Scrape the best one, falling back to next best if needed
    scrape_success = False
    successful_url = "Unknown URL"
    
    for url in best_urls:
        print(f"\nAttempting to scrape URL: {url}")
        
        result = subprocess.run(["python", "execution/scrape_single_site.py", url], capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
            
        if result.returncode == 0:
            scrape_success = True
            successful_url = url
            break # Success, stop trying URLs
        else:
            print("--- URL Scrape Failed. Trying the next best url... ---")
            
    if not scrape_success:
        print("\nCritical Error: All URLs found were blocked or failed to scrape.")
        print("Try running the script again, or try a slightly different search topic.")
        sys.exit(1)

    # 4. Extract data
    result = subprocess.run(
        ["python", "execution/extract_data.py"],
        input=topic + "\n",
        capture_output=True,
        text=True
    )

    if result.stdout:
        print(result.stdout)

    if result.returncode != 0:
        print("Error in extraction:")
        print(result.stderr)
        sys.exit(result.returncode)

    # 5. Export Report
    print(f"\nGenerating final report...")
    result = subprocess.run(
        ["python", "execution/export_results.py", topic, successful_url],
        capture_output=True,
        text=True
    )

    if result.stdout:
        print(result.stdout)

    print("\n=== Research Agent Finished Successfully ===")
    print("Check these files:")
    print("- .tmp/urls.txt")
    print("- .tmp/raw_scrape.txt")
    print("- .tmp/extracted_facts.json")
    print("- outputs/report.md")


if __name__ == "__main__":
    main()
