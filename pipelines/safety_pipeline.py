import re 

BLOCKED_PATTERNS = [
    r"sk-[a-zA-Z0-9]{20,}",
    r"AIza[0-9A-Za-z\-_]{35}",
    r"ghp_[a-zA-Z0-9]{36}",
    r"password\s*=\s*['\"][^'\"]+['\"]",
    r"ignore previous instructions",
    r"ignore all instructions",
    r"you are now",
    r"act as",
]

SENSITIVE_PATTERNS = [
    r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+",
    r"\b\d{10}\b",
]

def check_output(result):
    result_lower = result.lower()

    for pattern in BLOCKED_PATTERNS:
        if re.search(pattern , result_lower):
            return False, "Output blocked by safety pipeline."

    for pattern in SENSITIVE_PATTERNS:
        if re.search(pattern , result):
            result = re.sub(pattern , "[REDACTED]" , result)

    return True , result


def run_safety_check(result):
    passed , output = check_output(result)
    if not passed :
        return "EDITH detected unsafe content in the output. Request blocked."
    return output