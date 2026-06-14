import json
import os


message_count = 0

def review_token():
    global message_count
    message_count += 1

    if message_count % 3 != 0:
        return None

    if not os.path.exists("token_log.json"):
        return None

    with open("token_log.json" , "r")as f:
        logs = json.load(f)

    
    if not logs:
        return None

    total_tokens = sum(log["total_tokens"] for log in logs)

    tool_usage = {}
    for log in logs:
        tool = log["tool"]
        tool_usage[tool] = tool_usage.get(tool , 0) + log["total_tokens"]
        
    
    biggest_spender = max(tool_usage, key = tool_usage.get)

    warnings = []
    for log in logs :
        if log["prompt_tokens"] > 2000:
            warnings.append(f"{log['tool']} has very large prompt : {log['prompt_tokens']} tokens.")
        if log["total_tokens"] > 3000:
            warnings.append(f"{log['tool']} used too much tokens in one call : {log['total_tokens']} tokens.")
        if log["model"] in ["openai/gpt-oss-120b", "mistral-large-latest"] and log["total_tokens"] < 500:
            warnings.append(f"{log['tool']} has used heavy models for simple task.")

        
    report = {
        "biggest_spender" : biggest_spender,
        "total_tokens_used" : total_tokens,
        "tool_breakdown" : tool_usage,
        "warnings" : warnings
    }

    with open("agent5_output.json" , "w")as f:
        json.dump(report, f, indent = 2)
    

    return report