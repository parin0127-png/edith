# Feature: Live CVE Intelligence Agent

## Purpose
Looks up known vulnerabilities (CVEs) for a specific software and version, so users know if what they're running has known security holes.

## Input
- Software name and version, as text (e.g. "Apache 2.4.49" or "log4j 2.14")

## Output
A list of known CVEs for that software/version, each with:
- CVE ID
- Severity (Critical / High / Medium / Low)
- Short description of the vulnerability
- Recommended fix or version to upgrade to

## Example Input
```
log4j 2.14
```

## Example Output
- CVE-2021-44228 (Critical) — Remote code execution via JNDI lookup (Log4Shell). Upgrade to 2.17.1 or later.
- CVE-2021-45046 (Critical) — Incomplete fix for CVE-2021-44228, still allows DoS/RCE in some configs. Upgrade to 2.17.1 or later.

## What It Checks
- Known CVEs matching the exact software and version given
- Severity level of each CVE
- Whether a fixed version is available
- Whether the vulnerability is actively exploited (if known)