import uuid
from pydantic import BaseModel, Field

def get_str_uuid():
    return str(uuid.uuid4())

class Message(BaseModel):
    uuid: str = Field(default_factory=get_str_uuid)
    body: str
