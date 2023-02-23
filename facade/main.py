import os
import uuid
import json
import requests

from http import HTTPStatus

from fastapi import (
    FastAPI,
    status
)

app = FastAPI()

@app.post("/")
def accept_message(msg: str) -> None:
    msg_id = str(uuid.uuid4())

    logging_url = os.environ.get("LOGGING_SERVICE_URL")
    resp = requests.post(logging_url, json={"uuid": msg_id, "body": msg})
    return resp.status_code

@app.get("/")
def get_messages():
    # TODO: use some nice enum
    query_result = {}

    try:
        logging_url = os.environ.get("LOGGING_SERVICE_URL")
        logging_service_resp = requests.get(logging_url)
        if logging_service_resp.status_code == HTTPStatus(200):
            query_result["logged_messages"] = logging_service_resp.text
    except Exception as ex:
        print(ex)
    
    try:
        message_url = os.environ.get("MESSAGE_SERVICE_URL")
        message_service_resp = requests.get(message_url)
        if logging_service_resp.status_code == HTTPStatus(200):
            query_result["message_service"] = message_service_resp.text
    except Exception as ex:
        print(ex)
        
    if len(query_result.keys()) != 0:
        return query_result
    
    # TODO: what to do ?
    return {"STATUS": "NOT OK"}
