# EDITH — AI-Powered Security Intelligence Platform

<div align="center">

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-Backend-009688.svg)](https://fastapi.tiangolo.com/)
[![Groq](https://img.shields.io/badge/LLM-Groq-orange.svg)](https://groq.com/)
[![Mistral](https://img.shields.io/badge/LLM-Mistral-yellow.svg)](https://mistral.ai/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](#license)
[![Status](https://img.shields.io/badge/Status-Active-brightgreen.svg)](#)
[![Track](https://img.shields.io/badge/Microsoft%20Agents%20League-🎨%20Creative%20Apps-0078D4.svg)](https://aka.ms/agentsleague/register)

**A multi-agent AI security platform that thinks like an attacker — and explains it in plain English.**

[Demo Video](#demo-video) · [Features](#features) · [Architecture](#how-edith-works) · [Getting Started](#getting-started) · [Author](#author)

</div>

---

## 🏆 Microsoft Agents League 2026 — Creative Apps Track

EDITH is submitted under the **Creative Apps** track of the [Microsoft Agents League Hackathon 2026](https://aka.ms/agentsleague/register). It is an innovative AI-powered security application built using AI-assisted development, demonstrating how agentic AI can be applied creatively to real-world cybersecurity problems.

---

## Demo Video

> 🎥 **[Watch the Demo on YouTube](#)** ← *(add your link here)*

---

## Overview

**EDITH** (**E**ven **D**ead **I**'m **T**he **H**ero) is an AI-powered security intelligence platform inspired by Tony Stark's AI system.

Give EDITH a GitHub repo, an API spec, a cloud config, a Dockerfile, a package list, a suspicious message, or just a URL — and it automatically routes your input through the right AI security tool, analyzes it like an attacker would, and explains everything in plain English.

Built for developers, security teams, and non-technical users alike.

---

## Table of Contents

- [How EDITH Works](#how-edith-works)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Getting Your API Keys](#getting-your-api-keys)
- [Running the Project](#running-the-project)
- [Using EDITH](#using-edith)
- [Safety & Security](#safety--security)
- [Author](#author)
- [License](#license)

---

## How EDITH Works

EDITH runs every request through a structured **multi-agent pipeline**. Each agent does one job and passes its output to the next stage via a small JSON file.

```
User Input
     │
     ▼
┌──────────────────────────────┐
│  Agent 1 — System Brain      │  Loads system context and capabilities
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────────┐
│  Agent 2 — Tool Decider      │  Reads input, picks the right security tool
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────────┐
│  Agent 3 — Model Allocator   │  Picks the best AI model for the task
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────────┐
│  Agent 4 — Executor          │  Runs the tool with fallback protection
└─────────────┬────────────────┘
              │
              ▼
┌──────────────────────────────┐
│  Safety Pipeline (No AI)     │  Blocks secrets, injections & redacts PII
└─────────────┬────────────────┘
              │
              ▼
         Final Result → User
```

**Resilience by design:** If a tool fails or returns a poor result, the Executor falls back to a safe default — no retry loops, no wasted API calls.

**Safety by code:** The Safety Pipeline is pure regex — no AI — and runs on every output before it reaches the user.

---

## Features

### AI Security Tools

| # | Feature | What it Does |
|---|---------|--------------|
| 1 | **Repo Scanner** | Scans a public GitHub repo for exposed secrets, hardcoded credentials, and risky config files |
| 2 | **API Security Tester** | Analyzes an OpenAPI spec for broken auth, missing rate limits, and exposed endpoints |
| 3 | **Threat Report Generator** | Converts raw security findings into a clean professional pentest-style report |
| 4 | **Social Engineering Analyzer** | Detects phishing, impersonation, urgency tricks, and manipulation tactics in messages |
| 5 | **Cloud Misconfiguration Auditor** | Finds exposed storage buckets, weak IAM policies, and bad security groups in cloud configs |
| 6 | **Malicious Package Detector** | Flags typosquatted, hijacked, or suspicious packages from `requirements.txt` |
| 7 | **Dockerfile / CI Pipeline Auditor** | Detects privilege escalation risks, hardcoded secrets, and unsafe base images |
| 8 | **AI Red Team Agent** | Gathers real OSINT (HTTP headers, WHOIS, DNS records) and simulates an attacker walkthrough |
| 9 | **Live CVE Intelligence Agent** | Queries the NVD database for real CVEs on a given technology/version and explains risk + fix |

### Built-in Cyber Tools

| Tool | Purpose |
|------|---------|
| **Google Safe Browsing** | Checks if a URL is flagged as malware, phishing, or unwanted software |
| **VirusTotal** | Scans a URL against 70+ antivirus engines |
| **IP Info** | Returns ISP, geolocation, and hostname data for any IP address |
| **DNS Lookup** | Resolves IPv4/IPv6, hostname, and reachability for a domain |

---

## Tech Stack

| Layer | Technology |
|-------|-----------|
| Backend | FastAPI (Python) |
| Frontend | HTML + Tailwind CSS + Vanilla JS |
| Primary LLM | Groq (`llama-3.3-70b-versatile`, `gpt-oss` models) |
| Secondary LLM | Mistral (`mistral-large-latest`, `mistral-small-latest`, `ministral`) |
| Security APIs | Google Safe Browsing · VirusTotal · ipinfo.io · NVD CVE Database |
| Output Storage | Fernet-encrypted local file — no database required |
| AI-Assisted Dev | GitHub Copilot (used throughout development) |

---

## Project Structure

```
EDITH/
├── agents/
│   ├── brain.py                 # Agent 1 — System Brain
│   ├── tool_decider.py          # Agent 2 — Tool Decider
│   ├── model_allocator.py       # Agent 3 — Model Allocator
│   ├── executor.py              # Agent 4 — Executor
│   ├── token_reviewer.py        # Token usage auditor
│   └── self_improver.py         # Prompt optimization agent
├── cyber/
│   ├── safe_browsing.py
│   ├── virustotal.py
│   ├── ipinfo.py
│   └── dns_lookup.py
├── features/
│   ├── repo_scanner.py
│   ├── api_tester.py
│   ├── threat_report_generator.py
│   ├── social_engineering.py
│   ├── cloud_auditor.py
│   ├── package_detector.py
│   ├── dockerfile_auditor.py
│   ├── red_team.py
│   └── cve_agent.py
├── pipelines/
│   ├── pipeline.py              # Main orchestration pipeline
│   └── safety_pipeline.py       # Output filtering (no AI)
├── utils/
│   ├── client.py                # LLM client + token logger
│   └── safety_box.py            # Encrypted result storage
├── UI/
│   ├── index.html               # Login / Register
│   ├── setup.html               # API key setup
│   ├── dashboard.html           # Main interface
│   ├── style.css
│   └── script.js
├── main.py                      # FastAPI entry point
├── .env                         # API keys (not committed)
└── requirements.txt
```

---

## Getting Started

### Prerequisites

- Python 3.10 or higher
- A modern web browser
- (Optional) VS Code or any code editor

### Clone the Repository

```bash
git clone https://github.com/<your-username>/edith.git
cd edith
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

---

## Getting Your API Keys

EDITH needs a few free API keys. All have free tiers and take only a few minutes to set up.

### 1. Groq API Key *(required)*

1. Go to [console.groq.com/keys](https://console.groq.com/keys)
2. Sign up or log in → Click **Create API Key**
3. Copy the key — it starts with `gsk_`

### 2. Mistral API Key *(required)*

1. Go to [console.mistral.ai/api-keys](https://console.mistral.ai/api-keys/)
2. Sign up or log in → Click **Create new key**
3. Copy the key

### 3. Google Safe Browsing API Key *(optional)*

1. Go to [Google Cloud Console → Safe Browsing API](https://console.cloud.google.com/apis/library/safebrowsing.googleapis.com)
2. Enable the API → **Credentials → Create Credentials → API Key**
3. Copy the key — it starts with `AIza`

### 4. VirusTotal API Key *(optional)*

1. Create a free account at [virustotal.com](https://www.virustotal.com/)
2. Go to your profile → **API Key** → Copy it

### Configure `.env`

Create a `.env` file in the project root:

```env
GROQ=your_groq_api_key_here
MISTRAL=your_mistral_api_key_here
SAFE_BROWSING=your_google_safe_browsing_key_here
VT=your_virustotal_api_key_here
```

> Only `GROQ` and `MISTRAL` are required for core AI features.

---

## Running the Project

### 1. Start the Backend

```bash
uvicorn main:app --reload --port 8000
```

API server: `http://127.0.0.1:8000`

### 2. Serve the Frontend

```bash
cd UI
python -m http.server 5500
```

Frontend: `http://127.0.0.1:5500`

### 3. Open EDITH in your browser

```
http://127.0.0.1:5500/index.html
```

---

## Using EDITH

| Step | Action |
|------|--------|
| **1. Register / Login** | Create an operator account on the login page |
| **2. Setup** *(one-time)* | Enter your API keys, or skip and add them later from Settings |
| **3. Dashboard** | Paste any input — logs, configs, repo URLs, messages — and click **Analyze Context**. EDITH picks the right tool automatically. |
| **4. Tools** | Use the Tools tab for quick lookups: Safe Browsing, VirusTotal, IP Info, DNS Lookup |
| **5. Settings** | Update your API keys anytime via the gear icon |

---

## Safety & Security

- All AI output passes through a **code-only safety pipeline** before being shown to the user
- API keys and secrets found in scanned content are **automatically blocked or redacted**
- **Prompt-injection attempts** are detected and blocked
- Results are **Fernet-encrypted** locally before caching
- All tools used are **legal, public, and purely defensive** — no offensive or intrusive scanning

---

## Author

**Parin Prajapati**
📧 [parin0127@gmail.com](mailto:parin0127@gmail.com)

*Submitted to the Microsoft Agents League Hackathon 2026 — 🎨 Creative Apps Track*

---

## License

This project is licensed under the [MIT License](LICENSE).

---

<div align="center">
  <sub>Built with by Parin Prajapati · Microsoft Agents League 2026 · Creative Apps Track</sub>
</div>