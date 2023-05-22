from typing import List

import os
import consul
import hazelcast

from domain import Message

c = consul.Consul(
    host=os.environ["CONSUL_IP"], 
    port=os.environ["CONSUL_PORT"]
)

class LoggingHZRepository:

    def __init__(self) -> None:
        self.hz_client = hazelcast.HazelcastClient()

        hz_map = c.kv.get("HAZELCAST_MAP_NAME")[1]["Value"].decode("utf-8")
        self.logging_map = self.hz_client.get_map(hz_map).blocking()

    def add_entry(self, message: Message) -> None:
        self.logging_map.put(message.uuid, message.body)

    def get_values(self) -> List[str]:
        return self.logging_map.values()

LoggingRepository = LoggingHZRepository()