# Directive: Basic Topic Research

## 1. Goal
Research a specific topic (e.g., "Best AI CRM tools") and return structured facts without filler content.

## 2. Inputs Needed
- `topic`: The subject to research.
- `raw_text`: The scraped website text provided by the `scrape_single_site.py` script.

## 3. Process instructions
1. Read the `raw_text` from the latest scrape.
2. Extract only factual claims related to the `topic`.
3. Ignore promotional jargon, ads, and navigation menus.
4. Format the extracted facts into key-value pairs (e.g., Tool Name, Price, Feature).

## 4. Expected Output
A clean JSON list or bulleted markdown list of findings to be handed off to `export_results.py`.

## 5. Edge Cases
- **No relevant data:** If the scraped page has no information about the topic, return `{"status": "failed", "reason": "no relevant data found"}`.
- **Paywalls:** If the text asks you to "subscribe to read more," flag the source as unusable.
