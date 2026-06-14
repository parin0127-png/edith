import json 
import os 


conversation_history = []
message_count = 0

def add_message(role , content):
    global message_count
    conversation_history.append({"role" : role , "content" : content})
    message_count += 1

    if message_count % 10 == 0:
        compress_history()


def compress_history():
    global conversation_history
    if len(conversation_history) < 10:
        return

    old = conversation_history[-3:]
    recent = conversation_history[-3:]


    summary_line = []
    for msg in old:
        short = msg["content"][:100].replace("\n" , " ")
        summary_line.append(f"{msg['role']} : {short}")

    summary = "|".join(summary_line)
    compressed = {"role" : "system" , "content" : f"Previous context summary : {summary}"}

    compress_history = [compressed] + recent

def improve_prompt():
    if not os.path.exists("agent5_output.json"):
        return None

    with open("agent5_output.json" , "r")as f:
        report = json.load(f)

    suggestions = []
    for warning in report.get("warnings" , []):
        if "large prompt" in warning:
            suggestions.append("Trim prompt — remove examples and extra instructions")
        if "too many tokens" in warning:
            suggestions.append("Limit input to 3000 characters max before sending to LLM")
        if "heavy model" in warning:
            suggestions.append("Switch to lighter model for simple tasks")

    
    with open("agent6_output.json" , "w")as f:
        json.dump({"suggestions" : suggestions} , f, indent = 2)
    
    return suggestions


def get_history():
    return conversation_history