from utils.client import get_client , log_tokens

def generate_threat_report(user_input , model = "openai/gpt-oss-120b"):
    findings = user_input
    client , model = get_client(model)
    prompt = f"""You are a professional penetration tester. Based on these security findings, generate a clean professional report with these sections:

                    1. Executive Summary — short summary of overall security posture
                    2. Critical Findings — most dangerous issues found
                    3. Medium Findings — moderate risk issues
                    4. Low Findings — minor issues
                    5. Recommendations — clear steps to fix everything

                    Keep language simple and professional. No technical jargon.

                FINDINGS:
                {findings[:6000]}
"""

    response = client.chat.completions.create(
        model = model,
        messages = [{"role" : "user" , "content" : prompt}]
    )

    log_tokens("threat_report_generator", model, response.usage.prompt_tokens, response.usage.completion_tokens)
    return response.choices[0].message.content