from utils.client import get_client, log_tokens

def audit_cloud_config(config_text , model = "mistral-large-latest"):
    client , model = get_client(model)

    prompt = f"""You are a cloud security expert. Analyze this cloud configuration and find:
- Exposed or public storage buckets
- Weak IAM policies
- Overly permissive roles
- Missing encryption
- Public access where it should be private
- Bad permission settings
- Security group misconfigurations

Be specific. Mention the exact setting and why it is a security risk.

CONFIG:
{config_text[:6000]}
"""

    response = client.chat.completions.create(
        model = model,
        messages=[{"role": "user", "content": prompt}]
    )

    log_tokens("cloud_auditor", model, response.usage.prompt_tokens, response.usage.completion_tokens)
    return response.choices[0].message.content
