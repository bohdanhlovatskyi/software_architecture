from fastapi import (
    APIRouter, 
    HTTPException
)

from domain import Message
from service import log_message, get_all_messages, save_message

router = APIRouter()

@router.get('/')
async def get_messages():
    return await get_all_messages()

@router.post('/', status_code=200)
async def post_messages(message: str):
    if len(message) == 0:
        raise HTTPException(status_code=400, detail="Empty message was passed")

    msg = Message(body=message)
    try:
        log_msg_res = await log_message(msg)
    except Exception as ex:
        print(ex)

    try:
        save_msg_res = save_message(msg)
    except Exception as ex:
        print(ex)

    return "OK"
