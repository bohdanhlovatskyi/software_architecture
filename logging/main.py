import os

import hazelcast
from fastapi import FastAPI
from pydantic import BaseModel

class Message(BaseModel):
    uuid: str
    body: str

print("Logging: connecting to the hazelcast cluster: ", os.environ.get("HAZELCAST_CLUSTER_NAME"))
hz = hazelcast.HazelcastClient(
    cluster_name=os.environ.get("HAZELCAST_CLUSTER_NAME"),
    cluster_members=["logging-db-node-1", "logging-db-node-2"],
)
print("Logging: connected to the hazelcast client")

logging_map = hz.get_map("logging-map").blocking()

app = FastAPI()

@app.get("/")
def get_logs():
    global logging_map
    values = logging_map.values()
    return_str = ";".join(values)
    return return_str

@app.post("/")
def write_log(message: Message):
    global logging_map
    print(f"new message: ", message)
    logging_map.put(message.uuid, message.body)
    return message
