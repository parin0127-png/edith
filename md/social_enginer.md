# Feature: Social Engineering Analyzer

## Purpose
Analyzes an email or message to check if it looks like phishing or a social engineering attempt, so non-technical users can stay safe.

## Input
- Full text of a suspicious email or message, including sender and subject if available

## Output
A verdict (Phishing / Suspicious / Safe) with:
- The reasons behind the verdict
- Specific red flags found (or why it looks safe)
- What the user should do

## Example Input
```
From: security@paypa1-support.com
Subject: Urgent - Your account will be suspended

Dear user, we noticed unusual activity. Click here to verify your account
within 24 hours or it will be permanently suspended: http://paypa1-verify.com
```

## Example Output
- Verdict: Phishing
- Sender domain "paypa1-support.com" uses a "1" instead of "l" — common spoofing trick
- Urgent language ("24 hours", "permanently suspended") is a pressure tactic
- Link domain "paypa1-verify.com" does not match the real PayPal domain
- Action: Do not click the link. Delete the email or report it to your IT/security team.

## What It Checks
- Sender domain spoofing (lookalike domains)
- Urgency / pressure language
- Suspicious links (mismatched or lookalike URLs)
- Requests for sensitive info (passwords, OTPs, card numbers)
- Generic greetings and poor grammar (common phishing signs)
- Attachments with risky file types