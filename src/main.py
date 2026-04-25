import asyncio

from sqlalchemy_events import SQLAlchemyEvents

from src.application.send_messages import send_messages
from src.infrastructure.logger.impl import logger
from src.infrastructure.producer import producer
from src.infrastructure.session import engine


async def main():
    await producer.start()
    await send_messages()
    sa_events = SQLAlchemyEvents(
        engine=engine,
        autodiscover_paths=[
            'src.application'
        ],
        logger=logger,
    )
    await sa_events()
    try:
        while True:
            await asyncio.sleep(9999)
    finally:
        await producer.stop()


try:
    asyncio.run(main())
except KeyboardInterrupt:
    pass
