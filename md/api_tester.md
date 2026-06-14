# Feature: API Security Tester

## Purpose
Checks an API spec or list of endpoints for security weaknesses, so developers can fix them before attackers find them.

## Input
- API spec (OpenAPI/Swagger JSON), or
- A list of endpoints with HTTP methods, as text

## Output
A list of issues found, each with:
- The endpoint and method affected
- What the issue is
- Why it matters
- How to fix it

## Example Input
```
GET /api/users - returns all users, no auth required
POST /api/login - no rate limiting
GET /api/users/{id}/ssn - returns SSN, requires basic auth only
```

## Example Output
- GET /api/users — no authentication required, anyone can list all users. Add authentication.
- POST /api/login — no rate limiting, vulnerable to brute force. Add rate limiting and lockout.
- GET /api/users/{id}/ssn — sensitive data (SSN) protected only by basic auth. Use stronger auth and consider removing this endpoint entirely.

## What It Checks
- Missing or weak authentication
- Missing rate limiting
- Sensitive data exposure (PII, tokens, secrets in responses)
- Bad input validation (injection risks)
- Overly permissive CORS settings
- Missing HTTPS enforcement