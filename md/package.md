# Feature: Malicious Package Detector

## Purpose
Checks a list of software packages (dependencies) for malicious, typosquatted, or known vulnerable packages before they get installed.

## Input
- requirements.txt content, or
- package.json content, or
- A plain list of package names with versions, as text

## Output
A list of flagged packages, each with:
- Package name and version
- What is wrong with it (typosquat, known vulnerability, suspicious)
- What the safe alternative or fixed version is

## Example Input
```
requests==2.31.0
reqeusts==1.0.0
python-jwt==1.0.0
flask==3.0.0
```

## Example Output
- "reqeusts==1.0.0" — typosquat of "requests", likely malicious. Remove this package.
- "python-jwt==1.0.0" — known vulnerable package with security issues. Use "PyJWT" instead.
- "requests==2.31.0" and "flask==3.0.0" — no issues found

## What It Checks
- Typosquatted package names (misspellings of popular packages)
- Known vulnerable packages (matches against known bad package lists)
- Suspicious or abandoned packages
- Outdated versions with known fixes available