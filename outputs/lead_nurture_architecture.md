# System Architecture: AI Lead Nurturing System

This document outlines the 3-layer architecture for the Automated Lead Nurturing System, converting the business action plan into a structured software design.

---

## 2. Orchestration Logic (Decision Making)
The Orchestration Layer acts as the "Brain," determining how to handle the data passing between the CRM and the AI model.

### Step-by-Step Decision Flow:
1. **Receive Payload:** The orchestrator is triggered by the execution layer with a new lead JSON payload.
2. **Data Validation:**
   - *Check:* Are all required fields present?
   - *Decision:* If yes, proceed. If `industry` or `problem` is missing, select the "Fallback Prompt Template."
   - *Check:* Is the name gibberish or spam?
   - *Decision:* Clean the name or abort the process if flagged as spam.
3. **Prompt Construction:** Map the sanitized inputs into the prompt format defined in the `directives/lead_nurture_agent.md`.
4. **Tool Use (LLM Call):** Call the ChatGPT API (or equivalent LLM) with the constructed prompt.
5. **Output Validation:** Ensure the LLM returns the exact required JSON structure (`subject_line` and `email_body`). Force a retry if formatting is broken.
6. **Handoff:** Pass the validated JSON back to the execution layer for delivery.

---

## 3. Execution Layer (Doing the Work)
The Execution layer contains deterministic Python scripts that handle APIs, webhooks, and formatting. It performs no creative thinking.

### Required Scripts & Tools:

#### 1. `execution/hubspot_listener.py`
- **Purpose:** Acts as a webhook endpoint or polling script that detects when a new contact is added to HubSpot.
- **Action:** Extracts `Name`, `Email`, `Company`, `Industry`, and `Problem` using the HubSpot API and normalizes it into a standard JSON dictionary.
- **Handoff:** Passes the dictionary to the Orchestration component.

#### 2. `execution/llm_client.py`
- **Purpose:** A deterministic wrapper for the OpenAI API.
- **Action:** Takes the final prompt string from the Orchestrator, sends the HTTP request to OpenAI, handles rate-limits/retries, and returns the raw string response.

#### 3. `execution/create_email_draft.py`
- **Purpose:** Takes the final customized email content and pushes it to the user's outbox.
- **Action:** Connects to the Gmail API (or HubSpot Email API), assigns the `lead_email` as the recipient, inserts the `subject_line`, and saves the `email_body` as a Draft ready for human review.
