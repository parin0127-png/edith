from openai import OpenAI
from dotenv import load_dotenv
from agents.brain import get_system_context
import os
import json
from utils.client import log_tokens

load_dotenv()

client = OpenAI(api_key = os.getenv("GROQ"),
                base_url="https://api.groq.com/openai/v1")


MD_FILES = {
    "repo_scanner": "repo.md",
    "api_tester": "api_tester.md",
    "threat_report": "threat_report.md",
    "social_engineering": "social_enginer.md",
    "cloud_auditor": "cloud.md",
    "package_detector": "package.md",
    "dockerfile_auditor": "docker.md",
    "red_team_agent": "red_team.md",
    "cve_agent": "cve.md"
}

def load_tool_md(tool_name):
    filepath = MD_FILES.get(tool_name)
    if filepath and os.path.exists(filepath):
        with open(filepath , "r")as f:
            return f.read()
    return ""
def decide_tool(user_input):
    system_context = get_system_context()
    input_size = len(user_input)

    if input_size < 500:
        complexity = "light"
    elif input_size < 2000:
        complexity = "medium"
    else :
        complexity = "heavy"

    prompt = f"""You are a tool decider for EDITH security platform.

                Here is what EDITH can do:
                {system_context}

                User input: {user_input}

                Reply with JSON only:
                {{
                "tool": "tool_name",
                "complexity": "{complexity}",
                "input_size": {input_size}
                }}

            Tool names: repo_scanner, api_tester, threat_report, social_engineering, cloud_auditor, package_detector, dockerfile_auditor, red_team_agent, cve_agent
"""

    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages = [{"role" : "user" , "content" : prompt}]
    )

    log_tokens("tool_decider", "llama-3.1-8b-instant", response.usage.prompt_tokens, response.usage.completion_tokens)
    result = response.choices[0].message.content

    if not result:
        raise ValueError("Empty response from model")

    print("RAW RESULT:", repr(result))
    parsed = json.loads(result)
    tool_name = parsed["tool"]
    

    tool_context = load_tool_md(tool_name)
    parsed["tool_context"] = tool_context

    with open("agent2_output.json" , "w")as f:
        f.write(result)


    return parsed
    
