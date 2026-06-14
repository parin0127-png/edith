# Feature: Threat Report Generator

## Purpose
Takes raw security findings from other scans and turns them into a clear, plain English report — so both developers and non-technical users understand what's wrong and what to do.

## Input
- Raw findings or scan results, as text or a list (e.g. output from other EDITH tools, or pasted scan results from elsewhere)

## Output
A clear report with:
- Summary of what was scanned
- List of issues, each with severity (Critical / High / Medium / Low)
- Plain English explanation of each issue
- Recommended next steps, ordered by priority

## Example Input
```
- Hardcoded password found in db.py line 12
- S3 bucket "company-data" allows public read access
- Outdated package "flask==0.12" with known CVE
```

## Example Output
- Summary: 3 issues found — 1 Critical, 1 High, 1 Medium
- Critical: Hardcoded password in db.py — anyone with access to the code can see your database password. Fix first.
- High: Public S3 bucket "company-data" — anyone on the internet can read this data. Restrict access immediately.
- Medium: Outdated Flask version with known vulnerability — upgrade to the latest version when possible.
- Next steps: 
    1) Remove hardcoded password and use environment variables, 
    2) Make S3 bucket private, 
    3) Upgrade Flask

## What It Checks
- Groups and ranks findings by severity
- Removes technical jargon, explains impact in plain language
- Avoids repeating raw scan output — focuses on what it means and what to do
- Orders recommendations by priority (most urgent first)