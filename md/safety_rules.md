# EDITH — Safety Rules

EDITH uses a Safety Pipeline to check every result before it goes back to the user. This is pure Python, no AI — fast and predictable.

---

## Why This Matters

- AI output can sometimes leak sensitive data (API keys, passwords, emails) found while scanning
- Prompt injection attempts in user input could try to make the AI ignore its rules
- A pure code check catches these problems every time, with no extra tokens used

---

## Blocked Patterns (Hard Block)

If any of these are found in the output, EDITH blocks the result completely and shows: "EDITH detected unsafe content in the output. Request blocked."

| Pattern | Catches |
|---------|---------|
| sk-xxxxxxxxxxxxxxxxxxxx | OpenAI-style API keys |
| AIzaxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx | Google API keys |
| ghp_xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx | GitHub tokens |
| password = "..." | Hardcoded passwords |
| "ignore previous instructions" | Prompt injection |
| "ignore all instructions" | Prompt injection |
| "you are now" | Prompt injection / role override |
| "act as" | Prompt injection / role override |

---

## Sensitive Patterns (Auto Redact)

These are not blocked — they are automatically replaced with `[REDACTED]` so EDITH does not expose personal data.

| Pattern | Catches |
|---------|---------|
| Email addresses | name@example.com style text |
| 10 digit numbers | Phone numbers |

---

## How It Works

1. Agent 4 produces a result
2. Result is checked against Blocked Patterns first
   - If matched → result is fully blocked, replaced with a safe message
3. If not blocked, result is checked against Sensitive Patterns
   - Matches are redacted, rest of result stays as is
4. Final safe result is returned to user

This check runs on every single response, with no exceptions.

---

## What Safety Pipeline Does NOT Do

- Does not check user input before sending to AI (input sanitization is a separate task, still to be built)
- Does not use any AI model — pure regex pattern matching only
- Does not store or log blocked content anywhere