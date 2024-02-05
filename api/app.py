from fastapi import FastAPI
from dotenv import load_dotenv
import pathlib
import os


from api.format import ResponseFormat, ErrorFormat
from api.reqfilehandle import *

app = FastAPI()

## Main Application

# Default route for testing
@app.get("/", response_description="Send hello motherfucker", tags = ["Default"])
async def send_dummy_data():
    return ResponseFormat("Hello", "MF hello'ed")

@app.get("/get-rules", response_description= "When this URL is called, pull data from MISP API to local", tags = ["Default"])
async def get_rules():
    data = []

    env = env_to_dict()

    if data:
        return ResponseFormat(data, "Rules Successfully pulled to local")
    else:
        return ErrorFormat("504", "placeholder")
    
## Utilities
async def env_to_dict() -> dict:
    load_dotenv()
    return {k:os.getenv(k) for k in ["MISP_API", "MISP_API_TOKEN", "RULES_PATH", "RULES_TEMP_PATH"]}