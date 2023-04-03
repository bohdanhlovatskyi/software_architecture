from fastapi import (
    APIRouter, 
    HTTPException
)

from domain import Message
from service import log_message, get_all_messages

router = APIRouter()

@router.get('/')
def get_messages():
    return get_all_messages()

@router.post('/', status_code=200)
def post_message(message: Message):
    if len(message.body) == 0:
        raise HTTPException(status_code=400, detail="Empty message was passed")

    return log_message(message)
