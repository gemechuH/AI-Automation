import json
import os
import re
import string
import sys

# PURPOSE:
# This script reads the raw text scraped from a website and extracts 
# simple facts that match keywords from the research topic.
# It includes a 'Noise Filter' to skip binary junk and code.

def is_clean_text(text):
    """
    Checks if a string contains mostly printable ASCII characters.
    Skips binary streams, raw PDF code, and long strings of gibberish.
    """
    if not text or len(text.strip()) < 10:
        return False
    
    # Check for common PDF/Binary keywords
    forbidden_patterns = [
        r'obj\s*<', r'endobj', r'stream', r'endstream', r'xref', r'trailer',
        r'%%EOF', r'/MediaBox', r'/Contents', r'\[\s*\d+\s+0\s+R\s*\]'
    ]
    for pattern in forbidden_patterns:
        if re.search(pattern, text):
            return False

    # Count printable vs non-printable characters
    printable = set(string.printable)
    printable_count = sum(1 for char in text if char in printable)
    
    # If more than 20% of the text is non-printable/gibberish, it's probably junk
    if printable_count / len(text) < 0.8:
        return False
        
    return True

def extract_facts(raw_text_path, topic):
    print(f"--- Extracting Facts for Topic: {topic} ---")
    
    if not os.path.exists(raw_text_path):
        print(f"Error: {raw_text_path} not found.")
        return []

    with open(raw_text_path, 'r', encoding='utf-8', errors='ignore') as f:
        content = f.read()

    # Split into sentences (simple logic)
    sentences = re.split(r'(?<=[.!?])\s+', content)
    
    # Break topic into keywords for scoring
    keywords = [word.lower() for word in topic.split() if len(word) > 3]
    
    found_facts = []
    
    for sentence in sentences:
        sentence = sentence.strip().replace('\n', ' ')
        
        # 1. NOISE FILTER: Skip binary junk, code, or very short lines
        if not is_clean_text(sentence):
            continue
            
        # 2. RELEVANCE CHECK: Score based on keyword matches
        score = 0
        sentence_lower = sentence.lower()
        for kw in keywords:
            if kw in sentence_lower:
                score += 1
        
        if score > 0:
            found_facts.append({
                "fact": sentence,
                "score": score
            })

    # Sort by score (most relevant first) and take top 15
    found_facts.sort(key=lambda x: x['score'], reverse=True)
    return found_facts[:15]

def save_facts(facts, output_path):
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, 'w', encoding='utf-8') as f:
        json.dump(facts, f, indent=4)
    print(f"Saved {len(facts)} facts to {output_path}")

if __name__ == "__main__":
    # In a real setup, we'd pass the topic as an argument
    # For now, we ask the user or use a default if piped
    if not sys.stdin.isatty():
        topic = sys.stdin.read().strip()
    else:
        topic = input("Enter research topic: ")

    if not topic:
        topic = "AI Tools"

    facts = extract_facts('.tmp/raw_scrape.txt', topic)
    save_facts(facts, '.tmp/extracted_facts.json')
