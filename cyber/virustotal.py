from dotenv import load_dotenv
import requests
import os
import time


load_dotenv()
API_KEY = os.getenv("VT")

def scan_url(url):
    headers = {
        "x-apikey" : API_KEY
    }

    submit = requests.post(
        "https://www.virustotal.com/api/v3/urls",
        headers = headers,
        data = {"url" : url} 
    )

    scan_id = submit.json().get("data" , {}).get("id" , "")

    if not scan_id:
        print("VT Response : " , submit.json())
        return "Failed to sumbit URL"

    time.sleep(30)

    result = requests.get(
        f"https://www.virustotal.com/api/v3/analyses/{scan_id}",
        headers = headers
    )
    
    data = result.json().get("data" , {}).get("attributes" , {})
    stats =  data.get("stats" , {})
    print("VT Stats : " , stats)
    result = data.get("results" , {})

    malicious = stats.get("malicious" , 0)
    suspicious = stats.get("suspicious" , 0)
    harmless = stats.get("harmless" , 0)


    flagged_engines = []
    for engine , detail in result.items():
        if detail.get("category") in ["malicious" , "suspicious"]:
            flagged_engines.append(f"{engine} — {detail.get('result', 'unknown')}")


    flagged_list = "\n".join(flagged_engines) if flagged_engines else "None"

    report = f"""
    Malicious Engine  : {malicious}
    Suspicious Engine : {suspicious}
    Harmless Engine   : {harmless}

    Flagged by : 
    {flagged_list}
    """

    return report

