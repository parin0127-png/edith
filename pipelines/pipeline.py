from agents.brain import load_system, get_system_context
from agents.tool_decider import decide_tool
from agents.model_allocator import allocate_model
from agents.executor import execute_tool
from agents.token_reviewer import review_token
from agents.self_improver import add_message, improve_prompt
from utils.safety_box import store_result, get_result
from pipelines.safety_pipeline import run_safety_check

load_system()
def run_pipelines(user_input):
    try : 
        decide_tool(user_input)
        allocate_model()
        result = execute_tool(user_input)

        store_result(result)

        review_token()
        add_message("user" , user_input)
        add_message("assistant" , result)
        improve_prompt()

        return run_safety_check(result)
    
    except Exception as e:
        print(f"AI : {e}")
        result = get_result()
        if result :
            return result
        return "EDITH could not process your request. Please try again."

