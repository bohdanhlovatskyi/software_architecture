import os
import uuid
import random

import aiohttp
import asyncio

from http import HTTPStatus

from fastapi import FastAPI

app = FastAPI()

@app.post("/")
async def accept_message(msg: str) -> None:
    msg_id = str(uuid.uuid4())

    try:
        logging_urls = os.environ.get("LOGGING_SERVICE_URLS").split(",")
        rand_instance_id = random.randint(0, len(logging_urls) - 1)
        logging_url = logging_urls[rand_instance_id]
    except Exception as ex:
        print(ex)
        return

    client: aiohttp.ClientSession = aiohttp.ClientSession()

    print("sending msg ", msg_id, " to ", rand_instance_id, " instance")
    async with client.post(logging_url, json={"uuid": msg_id, "body": msg}) as resp:
        assert resp.status == 200
        await client.close()
        return resp.text

@app.get("/")
async def get_messages():
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
    storage[key] = await get_message(client, url)
