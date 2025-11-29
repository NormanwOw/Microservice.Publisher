import asyncio

from src.infrastructure.producer import producer


async def main():
    await producer.start()
    try:
        while True:
            await asyncio.sleep(1)
    finally:
        await producer.stop()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
