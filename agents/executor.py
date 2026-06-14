import importlib 
import json

TOOL_MAP = {
    "repo_scanner": ("repo_scanner", "scan_repo"),
    "api_tester": ("api_tester", "test_api_security"),
    "threat_report": ("threat_report_generator", "generate_threat_report"),
    "social_engineering": ("social_engineering", "analyze_social_engineering"),
    "cloud_auditor": ("cloud_auditor", "audit_cloud_config"),
    "package_detector": ("package_detector", "scan_packages"),
    "dockerfile_auditor": ("dockerfile_auditor", "audit_pipeline"),
    "red_team_agent": ("red_team", "red_team_agent"),
    "cve_agent": ("cve_agent", "cve_agent")
}

def execute_tool(user_input):
    with open("agent3_output.json" , "r")as f:
        agent3_data = json.load(f)

    tool = agent3_data["tool"]
    model = agent3_data["model"]

    try :
        file_name , func_name = TOOL_MAP[tool]
        model = importlib.import_module(f"features.{file_name}")
        feature_func = getattr(model , func_name)
        result = feature_func(user_input , model = model)

        if not result or len(result.strip()) < 10:
            return fallback(tool , user_input)

        return result
    except Exception as e:
        print(f"Error : {e}")
        return fallback(tool , user_input)
    

def fallback(tool , user_input):
    return f"Tool {tool} failed. Please check your input and try again."