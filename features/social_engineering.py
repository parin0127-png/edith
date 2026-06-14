from utils.client import get_client , log_tokens


def analyze_social_engineering(message , model = "ministral-3b-latest"):
    client , model = get_client(model)
    prompt = f"""You are a cybersecurity expert specialized in social engineering attacks. Analyze this message and detect:
    - Phishing attempts
    - Manipulation tactics
    - Impersonation
    - Urgency tricks
    - Suspicious links or requests
    - Emotional manipulation

    Be specific. Explain what is suspicious and why.

    MESSAGE:
    {message[:4000]}
    """

    response = client.chat.completions.create(
        model = model,
        messages = [{"role" : "user" , "content" : prompt}] 
    )

    log_tokens("social_engineering", model, response.usage.prompt_tokens, response.usage.completion_tokens)
    return response.choices[0].message.content
    