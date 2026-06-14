from openai import OpenAI
from dotenv import load_dotenv
from datetime import datetime
import os
import json


load_dotenv()

GROQ_MODELS = [
    "llama-3.1-8b-instant",
    "llama-3.3-70b-versatile",
    "openai/gpt-oss-120b",
    "openai/gpt-oss-20b"
]

MISTRAL_MODELS = [
    "mistral-large-latest",
    "mistral-small-latest",
    "ministral-3b-latest",
    "ministral-8b-latest",
    "pixtral-large-latest",
    "pixtral-12b-latest"
]

def get_client(model):
    if model in GROQ_MODELS:
        return OpenAI(
            api_key = os.getenv("GROQ"),
            base_url="https://api.groq.com/openai/v1"
        ), model 
    elif model in MISTRAL_MODELS:
        return  OpenAI(
            api_key = os.getenv("MISTRAL"),
            base_url = "https://api.mistral.ai/v1" 
        ), model
    else :
        return OpenAI(
            api_key=os.getenv("GROQ"),
            base_url="https://api.groq.com/openai/v1"
        ), "llama-3.3-70b-versatile"



def log_tokens(tool , model , prompt_tokens , completion_tokens):
    log_entry = {
        "time" : datetime.now().strftime("%H:%M:%S"), 
        "tool" : tool,
        "model" : model,
        "prompt_tokens" : prompt_tokens,
        "completion_tokens" : completion_tokens,
        "total_tokens" : prompt_tokens + completion_tokens
    }

    logs = []

    if os.path.exists("token_log.json"):
        with open("token_log.json" , "r")as f:
            logs = json.load(f)


    logs.append(log_entry)

    with open("token_log.json" , "w")as f:
        json.dump(logs , f , indent = 2)
        