from utils.client import get_client , log_tokens
import requests



def fetch_spec_url(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.text
    return None


def test_api_security(input_data , model = "mistral-small-latest"):
    client , model = get_client(model)
    if input_data.startswith("http"):
        spec = fetch_spec_url(input_data)
        if not spec:
            return "Could not fetch spec from url"
    else:
        spec = input_data

    
    prompt = f"""You are an API security expert. Analyze this OpenAPI spec and find:
                    - Broken authentication
                    - Exposed sensitive data
                    - Missing rate limits
                    - Missing authorization checks
                    - Insecure endpoints
                    - Bad permissions

                Be specific. Mention the endpoint and the exact issue.

                {spec[:6000]}
            """

    response = client.chat.completions.create(
        model = model,
        messages = [{"role" : "user" , "content" : prompt}]
    )
    
    log_tokens("api_tester", model, response.usage.prompt_tokens, response.usage.completion_tokens)
    return response.choices[0].message.content
