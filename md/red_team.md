# Feature: AI Red Team Agent

## Purpose
Thinks like an attacker. Given a description of a system, it lists possible ways that system could be attacked, so defenders can fix weak points first.

## Input
- A description of a system, app, or network setup, as text (e.g. "Web app with login page, MySQL database, hosted on AWS EC2, no firewall rules configured")

## Output
A list of possible attack paths, each with:
- The attack path / scenario
- What part of the system it targets
- How serious it could be
- How to defend against it

## Example Input
```
Web app with a login page and admin panel at /admin.
Backend is Node.js with a MySQL database.
No rate limiting on login. Admin panel has no extra authentication.
```

## Example Output
- Brute force attack on login page — no rate limiting means attackers can try many passwords. Add rate limiting and account lockout.
- Direct access to /admin panel — same login as regular users, no extra protection. Add separate authentication (like 2FA) for admin access.
- Possible SQL injection if inputs aren't sanitized — review all database queries for parameterized statements.

## What It Checks
- Authentication and access control weaknesses
- Missing rate limiting / brute force protection
- Exposed admin or sensitive endpoints
- Common attack chains based on the described architecture
- Network/infrastructure level risks if mentioned (firewalls, open ports, etc.)