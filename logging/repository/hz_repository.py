from typing import List

import os
import hazelcast

from domain import Message

class LoggingHZRepository:

    def __init__(self) -> None:
        self.hz_client = hazelcast.HazelcastClient(
            cluster_name=os.environ.get("HAZELCAST_CLUSTER_NAME"),
            cluster_members=["logging-db-node-1", "logging-db-node-2"],
        )

        self.logging_map = self.hz_client.get_map("logging-map").blocking()

    def add_entry(self, message: Message) -> None:
        self.logging_map.put(message.uuid, message.body)

    def get_values(self) -> List[str]:
        return self.logging_map.values()

LoggingRepository = LoggingHZRepository()