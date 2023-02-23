from fastapi import FastAPI
from pydantic import BaseModel


app = FastAPI()
LOGGING_MAP = {}

class Message(BaseModel):
    uuid: str
    body: str

@app.get("/")
def get_logs():
    return LOGGING_MAP

@app.post("/")
def write_log(message: Message):
    # TODO: add some logging
    print("new msg: ", message)
    LOGGING_MAP[message.uuid] = message.body

    return message
