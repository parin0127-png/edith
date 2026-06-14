from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from pipelines.pipeline import run_pipelines
from cyber.safe_browsing import check_url
from cyber.virustotal import scan_url
from cyber.ipinfo import check_ip
from cyber.dns_lookup import dns_look


app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins = ["*"],
    allow_methods = ["*"],
    allow_headers = ["*"],
)

class UserInput(BaseModel):
    text : str


@app.post("/analyze")
def analyze(input : UserInput):
    result = run_pipelines(input.text)
    return {"result" : result}


@app.get("/tools/safe-browsing")
def safe_browsing_tool(url : str):
    result = check_url(url)
    return {"result" : result}

@app.get("/tools/virustotal")
def virustotal_tool(url : str):
    result = scan_url(url)
    return {"result" : result}

@app.get("/tools/ipinfo")
def ipinfo_tool(ip : str):
    result = check_ip(ip)
    return {"result" : result}

@app.get("/tools/dns-lookup")
def dns_lookup_tool(domain : str):
    result = dns_look(domain)
    return {"result" : result}