import subprocess
import sys
from pathlib import Path


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


def main():
    if len(sys.argv) < 2:
        print('Please provide a research topic! Example: python run_agent.py "AI tools for small business"')
        sys.exit(1)

    topic = sys.argv[1]

    print(f"\n=== Research Agent Started ===")
    print(f"Topic: {topic}")

    run_command(["python", "execution/search_sources.py", topic])

    urls = get_all_urls()
    scrape_success = False
    
    for url in urls:
        print(f"\nAttempting to scrape URL: {url}")
        
        # We handle this command manually instead of via run_command to not exit immediately on failure
        result = subprocess.run(["python", "execution/scrape_single_site.py", url], capture_output=True, text=True)
        
        if result.stdout:
            print(result.stdout)
            
        if result.returncode == 0:
            scrape_success = True
            break # Success, stop trying URLs
        else:
            print("--- URL Scrape Failed. Trying the next one in the list... ---")
            
    if not scrape_success:
        print("\nCritical Error: All URLs found were blocked or failed to scrape.")
        print("Try running the script again, or try a slightly different search topic.")
        sys.exit(1)

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

    print("\n=== Research Agent Finished Successfully ===")
    print("Check these files:")
    print("- .tmp/urls.txt")
    print("- .tmp/raw_scrape.txt")
    print("- .tmp/extracted_facts.json")


if __name__ == "__main__":
    main()
