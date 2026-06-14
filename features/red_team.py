import urllib3
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
from utils.client import get_client , log_tokens
import requests
import dns.resolver




def get_https_header(url):
    try:
        response = requests.get(url , timeout = 10, verify = False)
        return dict(response.headers)
    except Exception as e:
        return {"Error" : str(e)}


def get_whois_info(domain):
    try:
        response = requests.get(f"https://api.whois.vu/?q={domain}", timeout=10)
        return response.json()
    except Exception as e:
        return {"Error" : str(e)}


def get_dns_records(domain):
    records = {}
    for records_type in ["A" , "MX" , "TXT"]:
        try:
            answer = dns.resolver.resolve(domain, records_type)
            records[records_type] = [str(r) for r in answer]
        except Exception:
            records[records_type] = []
    
    return records


def red_team_agent(user_input, model = "llama-3.3-70b-versatile"):
    url = user_input.split()[-1]
    client , model = get_client(model)
    domain = url.replace("https://" , "").replace("http://" , "").split("/")[0]

    headers = get_https_header(url)
    whois_info = get_whois_info(domain)
    dns_record = get_dns_records(domain)

    osint_summary = f"""
        HTTP Headers: {headers}
        WHOIS Info: {whois_info}
        DNS Records: {dns_record}
        """

    prompt = f"""You are an expert ethical hacker performing a red team assessment.

    You have gathered this real OSINT data about the target: {url}

    {osint_summary}
    Now think step by step like a real attacker:
        Step 1 - Analyze the OSINT data and identify what technology stack is running
        Step 2 - Identify the most likely attack vectors based on what you found
        Step 3 - For each attack vector explain how an attacker would exploit it
        Step 4 - Rate each vulnerability by severity (Critical, High, Medium, Low)
        Step 5 - Give a full attack simulation report in plain English

        Be specific. Use the real data above to support every finding.
"""

    response = client.chat.completions.create(
        model = model,
        messages = [{"role" : "user" , "content" : prompt}]
    )

    log_tokens("red_team", model, response.usage.prompt_tokens, response.usage.completion_tokens)
    return response.choices[0].message.content