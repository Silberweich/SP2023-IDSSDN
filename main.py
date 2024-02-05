import uvicorn

# runs app.py with uvicorn server
if __name__ == "__main__":
    uvicorn.run("api.app:app", host="0.0.0.0", port=80, reload=True)