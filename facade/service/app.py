import os
import random
import aiohttp
import asyncio

import consul

from typing import List
from kafka import KafkaProducer, KafkaAdminClient, errors
from kafka.admin import NewPartitions

from domain import Message

c = consul.Consul(host=os.environ["CONSUL_IP"], port=os.environ["CONSUL_PORT"])

producer = KafkaProducer(
    bootstrap_servers=c.kv.get("KAFKA_INSTANCE")[1]["Value"].decode("utf-8"), 
    # KAFKA_CONSUMER_GROUP=c.kv.get("KAFKA_CONSUMER_GROUP")[1]["Value"].decode("utf-8")
)

if len(producer.partitions_for(c.kv.get("KAFKA_TOPIC")[1]["Value"].decode("utf-8"))) == 1:
    print("Increassing number of partitions to allow parallelisation for consumer")
    admin_client = KafkaAdminClient(
        bootstrap_servers=c.kv.get("KAFKA_INSTANCE")[1]["Value"].decode("utf-8")
    )

    topic_partitions = {}
    topic_partitions[
        c.kv.get("KAFKA_TOPIC")[1]["Value"].decode("utf-8")
    ] = NewPartitions(total_count=3)
    admin_client.create_partitions(topic_partitions)

async def log_message(message: Message) -> str:
    logging_urls = list(list(filter(
        lambda service: service["Service"] == "logging",
        c.agent.services().values()
    )))

    logging_urls = [f'http://{item["Address"]}:{item["Port"]}/logging' for item in logging_urls]
        
    rand_instance_id = random.randint(0, len(logging_urls) - 1)
    logging_url = logging_urls[rand_instance_id]

    client: aiohttp.ClientSession = aiohttp.ClientSession()

    print("sending msg ", message.uuid, " to ", rand_instance_id, " instance")
    
    async with client.post(logging_url, json={"uuid": message.uuid, "body": message.body}) as resp:
        await client.close()
        return resp.text
    
def save_message(message: Message) -> str:
    future = producer.send(
        c.kv.get("KAFKA_TOPIC")[1]["Value"].decode("utf-8"),
        str.encode(message.body),
    )

    try:
        record_metadata = future.get(timeout=10)
    except errors.KafkaError as err:
        # Decide what to do if produce request failed...
        print(err)
        pass

    return "OK: message saved"

async def get_all_messages() -> str:
    query_result = {}

    logging_urls = list(filter(
        lambda service: service["Service"] == "logging",
        c.agent.services().values()
        ))

    logging_urls = [f'http://{item["Address"]}:{item["Port"]}/logging' for item in logging_urls]

    rand_instance_id = random.randint(0, len(logging_urls) - 1)
    logging_url = logging_urls[rand_instance_id]

    message_urls = list(filter(
        lambda service: service["Service"] == "message",
        c.agent.services().values()
    ))

    message_urls = [f'http://{item["Address"]}:{item["Port"]}/message' for item in message_urls]

    rand_instance_id = random.randint(0, len(message_urls) - 1)
    message_url = message_urls[rand_instance_id]

    print(f"logging url: |{logging_url}| message url: |{message_url}|")

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

