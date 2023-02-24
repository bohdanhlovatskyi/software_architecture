from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()
LOGGING_MAP = {}

class Message(BaseModel):
    uuid: str
    body: str

@app.get("/")
def get_logs():
    return ";".join(LOGGING_MAP.values())

@app.post("/")
def write_log(message: Message):
    print(f"new message: ", message)
    LOGGING_MAP[message.uuid] = message.body

    return message
