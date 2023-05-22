import os
import asyncio
from fastapi import FastAPI, status
from aiokafka import AIOKafkaConsumer

import controller
import service

app = FastAPI()
app.include_router(
    controller.router, 
    tags=['message'], 
    prefix='/message'
)

loop = asyncio.get_event_loop()
consumer = AIOKafkaConsumer(
    os.environ["KAFKA_TOPIC"],
    bootstrap_servers=os.environ["KAFKA_INSTANCE"],
    loop=loop, 
    group_id=os.environ["KAFKA_GROUP_ID"], 
    session_timeout_ms=60000,
)

@app.get("/", status_code=status.HTTP_200_OK)
def health_check():
    return {"status": "OK"}

@app.on_event("startup")
async def startup_event():
    loop.create_task(service.consume(consumer))

@app.on_event("shutdown")
async def shutdown_event():
    await consumer.stop()
