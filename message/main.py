from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def get_logs():
    return "Not implemented yet"

