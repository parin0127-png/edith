from dotenv import load_dotenv
import requests
import os 

load_dotenv()

API_KEY = os.getenv("SAFE_BROWSING")

def check_url(url):
    endpoints = f"https://safebrowsing.googleapis.com/v4/threatMatches:find?key={API_KEY}"

    payload = {
        "client" : {
            "clientId" : "EDITH",
            "clientVersion" : "1.0"
        },
        "threatInfo" : {
            "threatTypes": ["MALWARE", "SOCIAL_ENGINEERING", "UNWANTED_SOFTWARE", "POTENTIALLY_HARMFUL_APPLICATION"],
            "platformTypes" : ["ANY_PLATFORM"],
            "threatEntryTypes" : ["URL"],
            "threatEntries" : [{"url" : url}]
        }
    }

    response = requests.post(endpoints , json = payload)
    data = response.json()

    if "matches" in data:
        threats = [match["threatType"] for match in data["matches"]]
        return f"DANGEROUS → found : {','.join(threats)}"
    else : 
        return "SAFE → No threats found"