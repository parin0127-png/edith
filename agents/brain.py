import os

system_context = ""

def load_system(filepath = "system.md"):
    global system_context
    if os.path.exists(filepath):
        with open(filepath , "r")as f:
            system_context = f.read()
    else :
        system_context = "system.md not found. EDITH running without master knowledge."

def get_system_context():
    return system_context