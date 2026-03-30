# PURPOSE:
# This script takes the final JSON data that the AI extracted and turns it 
# into a clean Markdown report or CSV file so a human can easily read it.

import json
import os

def export_to_markdown():
    # Read the extracted data
    try:
        with open('.tmp/extracted_facts.json', 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: No data found. Did you run extract_data.py first?")
        return

    # Create the outputs folder if it doesn't exist
    os.makedirs('outputs', exist_ok=True)
    
    # Write everything into a beautifully formatted Markdown file
    with open('outputs/final_report.md', 'w', encoding='utf-8') as f:
        f.write("# Final AI Research Report\n\n")
        f.write("Here are the pure facts extracted from the web:\n\n")
        
        if not data:
            f.write("*No facts were found for this topic.*")
        else:
            for item in data:
                f.write(f"- {item['fact']}.\n")
                
    print(f"Success! Report generation complete.")
    print("Open the 'outputs/final_report.md' file to see the results.")

if __name__ == "__main__":
    export_to_markdown()
