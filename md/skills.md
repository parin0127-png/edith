# EDITH — Skills Reference

This file gives detailed input/output specs for each tool, and decision rules for picking the right one.

---

## 1. repo_scanner
- Input: GitHub repo link or raw source code (string)
- Output: List of issues — hardcoded secrets, bad patterns, outdated dependencies, with file/line if available
- Use when: Input contains code, file paths, repo links, or words like "scan my repo", "check my code"

## 2. api_tester
- Input: API spec (OpenAPI/Swagger JSON) or list of endpoints with HTTP methods
- Output: Security issues — missing auth, weak rate limits, bad input validation, per endpoint
- Use when: Input contains endpoint paths (e.g. /api/users), HTTP methods (GET/POST), or words like "API", "endpoint"

## 3. threat_report
- Input: Raw findings or scan results (text or list)
- Output: Plain English report — what was found, severity, what to do
- Use when: Input is already a list of vulnerabilities/findings and user wants it explained or summarized

## 4. social_engineering
- Input: Full email/message text, including sender and subject if available
- Output: Verdict (phishing / suspicious / safe) with reasons
- Use when: Input looks like an email, message, or user says "is this phishing", "check this email"

## 5. cloud_auditor
- Input: Cloud config file (AWS IAM JSON, S3 policy, Azure/GCP config)
- Output: List of misconfigurations — open access, bad permissions, exposed resources
- Use when: Input contains cloud config keywords (bucket, IAM, policy, role, permissions)

## 6. package_detector
- Input: requirements.txt, package.json, or list of package names with versions
- Output: List of suspicious/typosquatted/vulnerable packages with reasons
- Use when: Input looks like a dependency list (package names, version numbers)

## 7. dockerfile_auditor
- Input: Dockerfile content or CI/CD pipeline YAML
- Output: List of issues — root user, exposed secrets, risky commands, open ports
- Use when: Input contains Dockerfile commands (FROM, RUN, USER, EXPOSE) or CI YAML

## 8. red_team_agent
- Input: Description of a system, app, or network setup (text)
- Output: List of possible attack paths against that system
- Use when: User asks "how could this be attacked", "find attack paths", or gives a system description without code/config

## 9. cve_agent
- Input: Software name and version (e.g. "Apache 2.4.49")
- Output: List of known CVEs for that software/version with severity
- Use when: User mentions a specific software name + version and asks about vulnerabilities

---

## Decision Rules (Priority Order)

1. If input is clearly a list of findings/vulnerabilities already → threat_report
2. If input mentions a specific software name + version, and asks about CVEs → cve_agent
3. If input is an email or message text → social_engineering
4. If input is a Dockerfile or CI YAML → dockerfile_auditor
5. If input is a cloud config (IAM, bucket policy) → cloud_auditor
6. If input is a dependency/package list → package_detector
7. If input is an API spec or endpoint list → api_tester
8. If input is source code or a repo link → repo_scanner
9. If input is a general system description asking about attack possibilities → red_team_agent

## Edge Cases
- If input is too short or unclear (less than 10 characters), still pick the closest matching tool — do not leave tool blank
- If input matches more than one tool, follow the priority order above (top wins)
- If input is plain conversation with no security content, default to threat_report and let it explain that no issues were found