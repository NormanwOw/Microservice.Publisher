import asyncio

from src.application.send_messages import SendMessages
from src.config import settings
from src.infrastructure.logger.impl import logger
from src.infrastructure.producer import KafkaProducer
from src.infrastructure.uow.impl import get_uow


async def main():
    producer = KafkaProducer(settings, logger)
    await producer.start()
    try:
        while True:
            await SendMessages(get_uow(), producer)()
            await asyncio.sleep(60)
    finally:
        await producer.stop()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
