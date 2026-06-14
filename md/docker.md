# Feature: Dockerfile / CI Pipeline Auditor

## Purpose
Audits Dockerfiles and CI/CD pipeline files for security issues that could lead to compromised containers or build environments.

## Input
- Dockerfile content, or
- CI/CD pipeline YAML (GitHub Actions, GitLab CI, etc.), pasted as text

## Output
A list of issues found, each with:
- The exact line or command with the problem
- What the issue is
- Why it matters
- How to fix it

## Example Input
```dockerfile
FROM ubuntu:latest
USER root
RUN curl http://example.com/install.sh | bash
RUN chmod 777 /app
EXPOSE 22
ENV API_KEY=sk-12345abcdef
```

## Example Output
- "FROM ubuntu:latest" — using "latest" tag is unpredictable, pin a specific version
- "USER root" — container runs as root, should use a non-root user
- "curl | bash" — downloading and running scripts directly is risky, verify scripts first
- "chmod 777 /app" — gives everyone full access, use more restrictive permissions
- "EXPOSE 22" — exposing SSH port is risky in containers, remove if not needed
- "ENV API_KEY=sk-..." — hardcoded API key, move to secrets manager or build args

## What It Checks
- Running as root user
- Hardcoded secrets/API keys in env vars or commands
- curl/wget piped directly into bash
- Overly permissive file permissions (chmod 777)
- Exposed risky ports (like 22 for SSH)
- Use of "latest" tags instead of pinned versions