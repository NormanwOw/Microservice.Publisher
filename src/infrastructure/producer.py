import json

from aiokafka import AIOKafkaProducer

from src.config import settings
from src.infrastructure.logger.impl import logger
from src.infrastructure.logger.interfaces import ILogger
from src.infrastructure.messaging.interfaces import Producer
from src.infrastructure.messaging.messages import Message


class KafkaProducer(Producer):
    def __init__(self, settings, logger: ILogger):
        self.settings = settings
        self.logger = logger
        self.producer: AIOKafkaProducer | None = None

    async def start(self):
        if not self.producer:
            self.producer = AIOKafkaProducer(
                bootstrap_servers=self.settings.KAFKA_HOSTS,
                enable_idempotence=True,
                linger_ms=10,
                max_batch_size=16384,
            )
            try:
                await self.producer.start()
                self.logger.info('Kafka producer started')
            except Exception:
                self.logger.error('Failed to start producer')
                raise

    async def send_message(self, message: Message):
        if not self.producer:
            await self.start()

        await self.producer.send_and_wait(
            topic=message.topic, value=json.dumps(message.message).encode('utf-8')
        )
        self.logger.info(f'Sent message ID={message.id} to topic {message.topic}')

    async def stop(self):
        if self.producer:
            await self.producer.stop()
            self.logger.info('Kafka producer stopped')


producer = KafkaProducer(settings, logger)