# AI Research Agent System (Version 1)

Welcome to your V1 AI Research Agent! This system uses a **3-Layer Architecture** so that your AI (the "Brain") doesn't get confused trying to do everything at once. 

By separating instructions, decision-making, and heavy lifting, you get reliable results every time.

## The 3 Layers

### 1. Directive Layer (The "What")
- **Where it lives:** `directives/` folder
- **What it is:** Markdown files acting as Standard Operating Procedures (SOPs).
- **Purpose:** Tells the AI exactly *what* the goal is, the expected output format, and how to handle edge cases.

### 2. Orchestration Layer (The "Brain")
- **Where it lives:** Your AI chat window (or an AI API script).
- **What it is:** The reasoning engine.
- **Purpose:** The AI reads the Directive, looks at the extracted data, makes decisions, and formats the final answer.

### 3. Execution Layer (The "Muscle")
- **Where it lives:** `execution/` folder
- **What it is:** Simple Python scripts.
- **Purpose:** Does the boring, repetitive work that AIs are bad at (like downloading webpage HTML, saving files, and searching Google).

---

## How to use this Version 1 System:
1. Read the `directives/research_topic.md` to understand your goal.
2. Run `python execution/search_sources.py "your topic"` to find links.
3. Run `python execution/scrape_single_site.py <url>` to download the text.
4. Run `python execution/extract_data.py` to organize the text.
5. Run `python execution/export_results.py` to save to a CSV/JSON file!