import os
import uuid

import aiohttp
import asyncio

from http import HTTPStatus

from fastapi import FastAPI

app = FastAPI()

@app.post("/")
async def accept_message(msg: str) -> None:
    msg_id = str(uuid.uuid4())

    try:
        logging_url = os.environ.get("LOGGING_SERVICE_URL")
    except Exception as ex:
        print(ex)
        return

    client: aiohttp.ClientSession = aiohttp.ClientSession()

    async with client.post(logging_url, json={"uuid": msg_id, "body": msg}) as resp:
        assert resp.status == 200
        await client.close()
        return resp.text

@app.get("/")
async def get_messages():
    query_result = {}

    try:
        logging_url = os.environ.get("LOGGING_SERVICE_URL")
        message_url = os.environ.get("MESSAGE_SERVICE_URL")
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
