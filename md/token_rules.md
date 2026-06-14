# EDITH — Token Optimization Rules

EDITH runs on free tier API keys (Groq, Mistral). To avoid hitting rate limits and to keep costs at zero, EDITH tracks and controls token usage automatically.

---

## Why This Matters

- Free tier APIs have limits on tokens per minute and requests per minute
- A single long prompt can use up the whole limit in one call
- Heavy models (120b, large) cost more tokens and are slower — they should only be used for hard tasks
- Without limits, one bad input could break the whole pipeline for everyone

---

## Model Sizes

- **light**: llama-3.1-8b-instant, ministral-3b-latest, ministral-8b-latest, openai/gpt-oss-20b
  - Use for: simple, short tasks
- **medium**: llama-3.3-70b-versatile, mistral-small-latest, pixtral-12b-latest
  - Use for: normal tasks, most scans
- **heavy**: openai/gpt-oss-120b, mistral-large-latest, pixtral-large-latest
  - Use for: complex, large inputs only

---

## Limits (Agent 5 checks these every 3 messages)

| Check | Limit | Why |
|-------|-------|-----|
| Prompt size | 2000 tokens | A prompt this big means the input is too large and may slow down or fail the free tier |
| Total tokens per call | 3000 tokens | Above this, one call eats too much of the per-minute limit |
| Heavy model on simple task | Heavy model + total tokens under 500 | Heavy models are for hard tasks — using them for small tasks wastes capacity |

If any of these are crossed, Agent 5 writes a warning to `agent5_output.json`.

---

## Agent 6 Response to Warnings

| Warning | Suggestion |
|---------|-----------|
| Large prompt | Trim prompt — remove examples and extra instructions |
| Too many tokens | Limit input to 3000 characters max before sending to LLM |
| Heavy model for simple task | Switch to a lighter model |

---

## History Compression

- Every 10 messages, conversation history is compressed
- Keeps the last 3 messages in full
- Everything older becomes one short summary line
- This keeps prompts small even in long conversations

---

## Rate Limiting

- 10 second cooldown between tool calls
- Prevents hitting Groq free tier rate limits when multiple requests come quickly