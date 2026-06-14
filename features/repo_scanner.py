from utils.client import get_client
import requests 
from utils.client import log_tokens


RISKY_EXTENSIONS = [".env" , ".yml" , "yaml" , ".json" , "toml", ".ini" , ".config" , "dockerfile" , ".sh"]

def extract_owner_repo(github_url):
    parts = github_url.strip("/").split("/")
    owner = parts[-2]
    repo = parts[-1]
    return owner , repo


def fetch_repo_file(owner , repo):
    url = f"https://api.github.com/repos/{owner}/{repo}/git/trees/main?recursive=1"
    response = requests.get(url)
    if response.status_code != 200:
        url = url.replace("/main?" , "/master?")
        response = requests.get(url)
    data = response.json()
    # print(data)
    all_files = [f["path"] for f in data.get("tree" , []) if f["type"] == "blob"]
    risky_file = [f for f in all_files if any(f.lower().endswith(ext) for ext in RISKY_EXTENSIONS)]
    return risky_file


def fetch_file_content(owner , repo , filepath):
    url = f"https://raw.githubusercontent.com/{owner}/{repo}/main/{filepath}"
    response = requests.get(url)
    if response.status_code != 200:
        url = url.replace("/main" , "/master/")
        response = requests.get(url)
    return response.text if response.status_code == 200 else ""

def scan_repo(github_url , model = "llama-3.3-70b-versatile"):
    client , model = get_client(model)
    owner , repo = extract_owner_repo(github_url)
    risky_files = fetch_repo_file(owner , repo)

    if not risky_files:
        return "No risky extensions found !"
    
    all_content = ""
    for filepath in risky_files[:10]:
        content = fetch_file_content(owner , repo , filepath)
        if content:
            all_content += f"\n\n------{filepath}---\n{content[:2000]}"

    prompt = f"""You are a security expert. Analyze these files from a GitHub repository and find:
                    - Exposed secrets or API keys
                    - Hardcoded passwords
                    - Misconfigurations
                    - Security risks

                Be specific. Mention the file name and the exact issue.

                {all_content}
"""

    response = client.chat.completions.create(
        model = model,
        messages = [{"role" : "user" , "content" : prompt}]
    )
    log_tokens("repo_scanner", model, response.usage.prompt_tokens, response.usage.completion_tokens)
    return response.choices[0].message.content
