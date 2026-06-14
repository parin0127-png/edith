import requests

def check_ip(ip):
    response = requests.get(f"https://ipinfo.io/{ip}/json")
    data = response.json()

    if "error" in data:
        return "Invalid IP address."

    org = data.get("org" , "Unknown")
    city = data.get("city" , "Unknown")
    region = data.get("region" , "Unknown")
    country = data.get("country" , "Unknown")
    hostname = data.get("hostname" , "UnKnown")
    timezone = data.get("timezone" , "Unknown")

    report = f""" 
    IP          :   {ip}
    Hostname    :   {hostname}
    ORG/ISP     :   {org}
    City        :   {city}
    Region      :   {region}
    Country     :   {country}
    Timezone    :   {timezone}
    """

    return report