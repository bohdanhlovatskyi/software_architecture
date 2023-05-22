from repository import IN_MEMORY_BD

async def consume(consumer):
    print("consumer starting")
    await consumer.start()
    print("consumer started")
    try:
        async for msg in consumer:
            print(
                "consumed: ",
                msg.topic,
                msg.value,
                msg.timestamp,
            )
            IN_MEMORY_BD.append(msg.value.decode("utf-8"))

            await consumer.commit()
    finally:
        await consumer.stop()

async def get_logs():
    return IN_MEMORY_BD
