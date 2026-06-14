# Feature: Repo Scanner

## Purpose
Scans a GitHub repo or source code for security issues. Helps developers find problems before they ship code.

## Input
- A GitHub repo link, or
- Pasted source code (one or more files as text)

## Output
A list of issues found, each with:
- File name / line number (if available)
- What the issue is
- Why it matters
- How to fix it

## Example Input
```
def connect_db():
    password = "admin123"
    return mysql.connect(host="localhost", user="root", password=password)
```

## Example Output
- Hardcoded password found on line 2 — move to environment variable
- Database user is "root" — use a limited-privilege user instead

## What It Checks
- Hardcoded secrets (passwords, API keys, tokens)
- Outdated or vulnerable dependencies
- Bad coding patterns (SQL injection risk, unsafe eval, etc.)
- Missing input validation
- Insecure default configurations