# Lead Nurture Agent Directive

## 1. Goal
Generate a highly personalized, warm, and professional welcome email draft for every new inbound lead captured in the CRM. The email must speak directly to the lead's industry and stated problem to increase conversion rates.

## 2. Inputs
The execution layer will provide a JSON payload containing:
- `lead_name` (String)
- `company_name` (String)
- `industry` (String)
- `problem_description` (String)
- `lead_email` (String)

## 3. Process
1. **Analyze Inputs:** Read the provided lead data. Identify the core pain point (`problem_description`).
2. **Determine Tone:** Professional, empathetic, and solution-oriented.
3. **Draft Context:** Briefly acknowledge their industry and explicitly state that your business has solved similar problems in that specific vertical before.
4. **Call to Action:** End the email by proposing a brief 10-minute discovery call "tomorrow or later this week."

## 4. Expected Output
Return a strictly formatted JSON object:
```json
{
  "subject_line": "String (engaging, customized subject)",
  "email_body": "String (the full email plaintext draft)"
}
```

## 5. Edge Cases & Handling
- **Missing Industry or Problem:** If `industry` or `problem_description` is blank/null, fall back to a generic but warm welcome message focusing on learning more about their needs.
- **Gibberish Names (e.g., "asdf"):** Do not use the name in the greeting if it is obviously fake or purely lowercase consonants. Use "Hi there," instead.
- **Profanity in Problem Description:** Automatically flag the lead as spam and return an empty string for the email body.
