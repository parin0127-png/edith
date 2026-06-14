from utils.client import get_client, log_tokens

def audit_pipeline(user_input, model = "openai/gpt-oss-20b"):
    file_type = "dockerfile"
    file_content = user_input
    client , model = get_client(model)
    if file_type == "dockerfile":
        context = "Dockerfile"
    else : 
        context = "Github Actions CI/CD pipelines"


    prompt = f"""You are a security expert. Analyze this {context} and find:
            - Privilege escalation risks (running as root, sudo misuse)
            - Exposed secrets or API keys hardcoded inside
            - Dangerous commands or risky base images
            - Missing security best practices

            Be specific. Mention the exact line or section and the exact issue.

            {file_content}
        """

    response = client.chat.completions.create(
        model = model,
        messages = [{"role" : "user" , "content" : prompt}]
    )

    log_tokens("dockerfile_auditor", model, response.usage.prompt_tokens, response.usage.completion_tokens)
    return response.choices[0].message.content
