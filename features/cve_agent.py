from utils.client import get_client , log_tokens
import requests


def fetch_cves(technology , version):
    search_query = f"{technology} {version}"
    url = f"https://services.nvd.nist.gov/rest/json/cves/2.0?keywordSearch={search_query}&resultsPerPage=5"

    response = requests.get(url)
    data = response.json()

    cves = []
    for item in data.get("vulnerabilities" , []):
        cve = item["cve"]
        cve_id = cve["id"]
        description = cve["descriptions"][0]["value"]
        cves.append(f"{cve_id}  {description}")
    
    return cves


def analyzes_cves(technology , version, cves , model = "openai/gpt-oss-120b"):
    client , model = get_client(model)
    if not cves:
        return f"No known cves found for {technology} {version}."

    cve_text = "\n".join(cves)

    prompt = f"""You are a security expert. A user is running {technology} {version}.
                These are the real known CVEs for this version:

                {cve_text}

                For each CVE:
                - Explain what the vulnerability is in simple English
                - Explain what a hacker can actually do with it
                - Give one clear fix or recommendation

                Be specific. Be short. No fluff.
            """
        
    response = client.chat.completions.create(
        model = model,
        messages = [{"role" : "user" , "content" : prompt}]
    )

    log_tokens("cve_agent", model, response.usage.prompt_tokens, response.usage.completion_tokens)
    return response.choices[0].message.content


def cve_agent(user_input, model = "none"):
    parts = user_input.split()
    technology = parts[0]
    version = parts[1] if len(parts) > 1 else ""
    cves = fetch_cves(technology, version)
    return analyzes_cves(technology, version, cves)
