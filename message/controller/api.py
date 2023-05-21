from fastapi import (
    APIRouter, 
)

from service import get_logs as get_logs_
 
router = APIRouter()

@router.get('/')
async def get_logs():
    # transform Messages into json
    messages = await get_logs_()

    return ",".join(messages)