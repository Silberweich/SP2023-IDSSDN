from fastapi import FastAPI
from dotenv import load_dotenv

import pathlib
import os

from api.format import ResponseFormat, ErrorFormat
from api.reqfilehandle import RequestFileHandler

app = FastAPI()

## Main Application

# Default route for testing
@app.get("/", response_description="Send hello motherfucker", tags = ["Default"])
async def send_dummy_data():
    return ResponseFormat("Hello", "MF hello'ed")

@app.get("/fetch-rules", response_description= "pull data from MISP API to local", tags = ["MISP"])
async def fetch_rules():
    data = []

    fileHandle = RequestFileHandler(**env_to_dict())

    if fileHandle.get_rules():
        return ResponseFormat(data, "Rules Successfully pulled to local")
    else:
        return ErrorFormat("504", "placeholder")

@app.post("/fetch-rules", response_description= "pull data from MISP API to local, with filtering", tags = ["MISP"])
async def fetch_rules_filtered():
    return ErrorFormat("400", "Not Implemented yet")

## Utilities
def env_to_dict() -> dict:
    load_dotenv()
    return {k:os.getenv(k) for k in ["MISP_API", "MISP_API_TOKEN", "RULES_PATH", "RULES_TEMP_PATH"]}