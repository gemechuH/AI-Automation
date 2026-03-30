# PURPOSE:
# This script represents the "AI processing" step in your execution layer. 
# Since this is a beginner version, we simulate the AI extraction. In a real system, 
# this script would send the raw text to OpenAI/Anthropic and ask 'extract facts'.

import json
import os

def extract_facts(raw_text, topic):
    # This is a basic mock. It just finds sentences with your topic in it!
    # In V2, you would replace this with an actual call to an AI API.
    print("AI Brain is reading the text...")
    
    sentences = raw_text.split('.')
    found_facts = []
    
    for sentence in sentences:
        # If the topic keyword is in the sentence, save it as a "fact"
        if topic.lower() in sentence.lower():
            clean_fact = sentence.strip()
            if len(clean_fact) > 10: # ignore super short broken sentences
                found_facts.append({"fact": clean_fact})
                
    return found_facts

if __name__ == "__main__":
    
    # 1. Read the raw text we scraped in the previous step
    try:
        with open('.tmp/raw_scrape.txt', 'r', encoding='utf-8') as f:
            raw_text = f.read()
    except FileNotFoundError:
        print("Error: Could not find raw text. Did you run scrape_single_site.py first?")
        exit(1)
        
    topic = input("What was your research topic? (e.g., AI CRM): ")
    
    # 2. Extract the data
    extracted_data = extract_facts(raw_text, topic)
    
    # 3. Save the structured data
    os.makedirs('.tmp', exist_ok=True)
    with open('.tmp/extracted_facts.json', 'w') as f:
        json.dump(extracted_data, f, indent=4)
        
    print(f"Extraction complete! Found {len(extracted_data)} facts.")
    print("Saved clean data to .tmp/extracted_facts.json")
