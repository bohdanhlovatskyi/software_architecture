from typing import List
from domain import Message

class DummyRepository:

    def __init__(self) -> None:
        self.logging_map = {}

    def add_entry(self, message: Message) -> None:
        self.logging_map[message.uuid] = message.body

    def get_values(self) -> List[str]:
        return list(self.logging_map.values())

LoggingRepository = DummyRepository()