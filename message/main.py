import os
import consul
import asyncio
import argparse
import uvicorn
from fastapi import FastAPI, status
from aiokafka import AIOKafkaConsumer

from dotenv import load_dotenv, find_dotenv
load_dotenv(find_dotenv())

import controller
import service

argParser = argparse.ArgumentParser()
argParser.add_argument("-p", "--port", help="port to run", required=True)
args = argParser.parse_args()

c = consul.Consul(
    host=os.environ["CONSUL_IP"], 
    port=os.environ["CONSUL_PORT"]
)

c.agent.service.register(
    name=os.environ["SERVICE_NAME"],
    port=int(args.port),
    address=os.environ["SERVICE_HOST"],
    service_id=f"{os.environ['SERVICE_NAME']}:{args.port}",
)

app = FastAPI()
app.include_router(
    controller.router, 
    tags=['message'], 
    prefix='/message'
)

loop = asyncio.get_event_loop()

print(
    "Creating messaage service: ",
    c.kv.get("KAFKA_TOPIC")[1]["Value"].decode("utf-8"),
    c.kv.get("KAFKA_INSTANCE")[1]["Value"].decode("utf-8") 
    )

consumer = AIOKafkaConsumer(
    c.kv.get("KAFKA_TOPIC")[1]["Value"].decode("utf-8"),
    bootstrap_servers=c.kv.get("KAFKA_INSTANCE")[1]["Value"].decode("utf-8"),
    loop=loop, 
    group_id=c.kv.get("KAFKA_CONSUMER_GROUP")[1]["Value"].decode("utf-8"), 
    session_timeout_ms=60000,
)

@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "OK"}

def startup_event(loop, consumer):
    print("startup event scheduled")
    loop.create_task(service.consume(consumer))
    loop.run_forever()

if __name__ == "__main__":
    from threading import Thread

    t = Thread(target=startup_event, args=(loop, consumer))
    t.start()

    uvicorn.run(app, host="0.0.0.0", port=int(args.port))
