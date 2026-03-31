# PURPOSE:
# This script extracts relevant facts from the raw scraped text based on the 
# user's topic. It uses basic keyword scoring to find the most relevant sentences.

import json
import os
import sys
import re
from collections import Counter

def get_keywords(topic):
    """Extracts meaningful keywords from the topic (ignores common stop words)."""
    # Simple list of words to ignore to improve search quality
    stop_words = {"that", "need", "with", "have", "this", "best", "some", "what", "where", "when", "why", "how"}
    
    # Split by non-alphanumeric characters
    words = re.findall(r'\b\w+\b', topic.lower())
    
    # Keep words that are > 2 chars and not in standard stop words
    keywords = [w for w in words if len(w) > 2 and w not in stop_words]
    
    # If the user typed a very short topic, just use the whole thing
    if not keywords:
        keywords = words
        
    return keywords

def extract_facts(raw_text, topic, max_facts=15):
    print(f"AI Brain is analyzing the text for topic: '{topic}'")
    
    keywords = get_keywords(topic)
    print(f"Searching for keywords: {keywords}")
    
    # Split text into rough sentences (by period, avoiding acronyms if possible, though basic for MVP)
    sentences = [s.strip() for s in raw_text.split('.') if len(s.strip()) > 15]
    
    scored_sentences = []
    
    for sentence in sentences:
        score = 0
        s_lower = sentence.lower()
        
        # Give 1 point for every keyword found in the sentence
        for kw in keywords:
            if kw in s_lower:
                score += 1
                
        # Bonus points if multiple keywords appear close together (simple full string match check)
        if len(keywords) > 1 and " ".join(keywords[:2]) in s_lower:
            score += 2
            
        if score > 0:
            scored_sentences.append((score, sentence))
            
    # Sort by highest score first
    scored_sentences.sort(key=lambda x: x[0], reverse=True)
    
    # Deduplicate similar sentences (basic fuzzy match via first 20 chars)
    unique_facts = []
    seen = set()
    
    for score, sent in scored_sentences:
        sig = sent[:20].lower()
        if sig not in seen:
            seen.add(sig)
            # Clean up the sentence slightly
            clean_fact = sent.replace('\n', ' ').replace('\r', '')
            unique_facts.append({"fact": clean_fact + ".", "score": score})
            
        if len(unique_facts) >= max_facts:
            break
            
    return unique_facts

if __name__ == "__main__":
    try:
        with open('.tmp/raw_scrape.txt', 'r', encoding='utf-8') as f:
            raw_text = f.read()
    except FileNotFoundError:
        print("Error: Could not find raw text. Did you run scrape_single_site.py first?")
        sys.exit(1)
        
    # Read topic from stdin (passed by run_agent.py subprocess)
    print("What was your research topic? (Waiting for input...)", file=sys.stderr)
    topic = sys.stdin.read().strip()
    
    if not topic:
        topic = "Unknown Topic"
    
    extracted_data = extract_facts(raw_text, topic)
    
    os.makedirs('.tmp', exist_ok=True)
    with open('.tmp/extracted_facts.json', 'w', encoding='utf-8') as f:
        json.dump(extracted_data, f, indent=4)
        
    print(f"Extraction complete! Found {len(extracted_data)} highly relevant facts.")
    print("Saved clean data to .tmp/extracted_facts.json")
