import os
import random
import aiohttp
import asyncio

from typing import List
from kafka import KafkaProducer, errors

from domain import Message

producer = KafkaProducer(
    bootstrap_servers=[
        os.environ["KAFKA_INSTANCE"]
    ]
)

async def log_message(message: Message) -> str:
    try:
        logging_urls = os.environ.get("LOGGING_SERVICE_URLS").split(",")
        rand_instance_id = random.randint(0, len(logging_urls) - 1)
        logging_url = logging_urls[rand_instance_id]
    except Exception as ex:
        print(ex)
        return

    client: aiohttp.ClientSession = aiohttp.ClientSession()

    print("sending msg ", message.uuid, " to ", rand_instance_id, " instance")
    
    # # TODO: I assume serialization logic should be within Messaage class
    async with client.post(logging_url, json={"uuid": message.uuid, "body": message.body}) as resp:
        await client.close()
        return resp.text
    
def save_message(message: Message) -> str:
    future = producer.send(
        os.environ["KAFKA_TOPIC"],
        str.encode(message.body)
    )

    try:
        record_metadata = future.get(timeout=10)
        print(record_metadata)
    except errors.KafkaError as err:
        # Decide what to do if produce request failed...
        print(err)
        pass

    return "OK"

async def get_all_messages() -> str:
    query_result = {}

    try:
        # TODO: better way would be to query all of those, and 
        # wait for the first to finish (it should pass all the info from db)
        logging_urls = os.environ.get("LOGGING_SERVICE_URLS").split(",")
        rand_instance_id = random.randint(0, len(logging_urls) - 1)
        logging_url = logging_urls[rand_instance_id]

        message_url = os.environ.get("MESSAGE_SERVICE_URL")

        print(f"logging url: |{logging_url}| message url: |{message_url}|")
    except Exception as ex:
        print(ex)
        return

    client: aiohttp.ClientSession = aiohttp.ClientSession()
    await asyncio.gather(
        log_msg(client, logging_url, "logging_service", query_result),
        log_msg(client, message_url, "message_service", query_result)
    )
    await client.close()

    return query_result

async def get_message(client: aiohttp.ClientSession, url: str) -> str:
    async with client.get(url) as response:
        assert response.status == 200
        return await response.text()

async def log_msg(
    client: aiohttp.ClientSession, url: str, key: str, storage: dict
) -> None:
    try:
        storage[key] = await get_message(client, url)
    except Exception as ex:
        print(ex)

