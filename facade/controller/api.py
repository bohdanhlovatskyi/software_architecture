from fastapi import (
    APIRouter, 
    HTTPException
)

from domain import Message
from service import log_message, get_all_messages

router = APIRouter()

@router.get('/')
async def get_messages():
    return await get_all_messages()

@router.post('/', status_code=200)
async def post_messages(message: str):
    if len(message) == 0:
        raise HTTPException(status_code=400, detail="Empty message was passed")

    return await log_message(Message(body=message))
