from typing import List
from domain import Message

from repository import ( 
    LoggingRepository
)

def log_message(message: Message) -> None:
    print(f"new message: ", message)
    LoggingRepository.add_entry(message)

    return message

def get_all_messages() -> List[str]:
    vals = LoggingRepository.get_values()
    return ";".join(vals)
