from utils.client import get_client, log_tokens
import json


def parser_package(file_content , file_type):
    packages = []

    if file_type == "requirements":
        for line in file_content.split():
            if line and not line.startswith("#"):
                packages.append(line)

    elif file_type == "packages.json":
        data = json.loads(file_content)
        deps = data.get("dependencies" , {})
        devs = data.get("devDependencies" , {})
        all_deps = {**deps , **devs}
        for name , version in all_deps:
            packages.append(f"{name} == {version}")
    

    return packages


def scan_packages(user_input, model = "llama-3.1-8b-instant"):
    file_content = user_input
    file_type = "requirements"
    client , model = get_client(model)
    packages = parser_package(file_content, file_type)

    if not packages:
        return "No packages found in files !"

    packages_text = "\n".join(packages)

    prompt = f"""You are a security expert. Analyze these packages and find:
                - Typosquatting (fake packages with names similar to popular ones)
                - Hijacked or compromised packages
                - Packages with suspicious names or unusual behavior
                - Packages known for malicious activity

            Be specific. Mention the package name and the exact issue.

            {packages_text}
        """

    response = client.chat.completions.create(
        model = model,
        messages = [{"role" : "user" , "content" : prompt}]
    )

    log_tokens("package_detector", model, response.usage.prompt_tokens, response.usage.completion_tokens)
    return response.choices[0].message.content