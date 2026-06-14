from dotenv import load_dotenv
from openai import OpenAI
import os
import json
from utils.client import log_tokens

load_dotenv()
client = OpenAI(api_key = os.getenv("GROQ") , 
                base_url="https://api.groq.com/openai/v1")


MODELS = {
    "light": ["llama-3.1-8b-instant", "ministral-3b-latest", "ministral-8b-latest", "openai/gpt-oss-20b"],
    "medium": ["llama-3.3-70b-versatile", "mistral-small-latest", "pixtral-12b-latest"],
    "heavy": ["openai/gpt-oss-120b", "mistral-large-latest", "pixtral-large-latest"]
}

def allocate_model():
    with open("agent2_output.json" , "r")as f:
        agent2_data = json.load(f)

    tool = agent2_data["tool"]
    complexity = agent2_data["complexity"]
    input_size = agent2_data["input_size"]

    model_choices = MODELS.get(complexity , MODELS["medium"])

    prompt = f"""You are a model allocator for EDITH security platform.

                    Tool to run: {tool}
                    Complexity: {complexity}
                    Input size: {input_size} characters

                    Available models for this complexity: {model_choices}

                    Pick the single best model for this tool and task.
                    Reply with JSON only:
                    {{
                    "tool": "{tool}",
                    "model": "chosen_model_name",
                    "complexity": "{complexity}"
                    }}
                """

    response = client.chat.completions.create(
        model = "llama-3.1-8b-instant",
        messages = [{"role" : "user" , "content" : prompt}]
    )

    log_tokens("model_allocator", "llama-3.1-8b-instant", response.usage.prompt_tokens, response.usage.completion_tokens)
    result = response.choices[0].message.content

    with open("agent3_output.json" , "w")as f:
        f.write(result)

    return json.loads(result)