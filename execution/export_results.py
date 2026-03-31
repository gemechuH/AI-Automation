# PURPOSE:
# This script takes the final JSON data that the AI extracted and turns it 
# into a clean Markdown report that is easy for humans to read.

import json
import os
import sys

def create_report(topic, source_url):
    # 1. Read the extracted data
    try:
        with open('.tmp/extracted_facts.json', 'r', encoding='utf-8') as f:
            data = json.load(f)
    except FileNotFoundError:
        print("Error: No data found. Did you run extract_data.py first?")
        return

    # 2. Setup the outputs folder
    os.makedirs('outputs', exist_ok=True)
    report_path = 'outputs/report.md'
    
    # 3. Create a clean, beginner-friendly Markdown report
    with open(report_path, 'w', encoding='utf-8') as f:
        # Title & Topic
        f.write(f"# AI Research Report\n\n")
        f.write(f"**Research Topic:** {topic}\n")
        f.write(f"**Source Used:** [{source_url}]({source_url})\n\n")
        
        # Summary Section
        f.write("## 1. Short Summary\n")
        f.write("This report contains automatically extracted facts and insights related to your research topic. ")
        f.write("The facts below were pulled directly from the source URL without human intervention.\n\n")
        
        # Findings Section
        f.write("## 2. Key Findings & Topics\n")
        if not data:
            f.write("*No exact facts were found for this topic in the source text.*\n\n")
        else:
            for item in data:
                # We expect the dictionary to have a "fact" key, but lets be safe
                fact_text = item.get('fact', 'Unknown fact')
                f.write(f"- {fact_text}\n")
        
        f.write("\n")
        
        # Limitations Section
        f.write("## 3. Notes & Limitations\n")
        f.write("- **MVP Notice:** This is a Version 1 AI Research Agent. It extracts exact sentences containing your keywords.\n")
        f.write("- **AI Context:** It does not yet perform advanced summarization or cross-referencing.\n")
                
    print(f"\nSuccess! Formatting complete.")
    print(f"Report saved to: {report_path}")

if __name__ == "__main__":
    # If the user ran the runner script, it might pass arguments
    topic = sys.argv[1] if len(sys.argv) > 1 else "Unknown Topic"
    source_url = sys.argv[2] if len(sys.argv) > 2 else "Unknown Source"
    
    create_report(topic, source_url)
