from datetime import datetime, timezone

from src.infrastructure.messaging.interfaces import Producer
from src.infrastructure.messaging.messages import Message
from src.infrastructure.models import OutboxModel
from src.infrastructure.uow.interfaces import IUnitOfWork


class SendMessages:
    def __init__(self, uow: IUnitOfWork, producer: Producer):
        self.uow = uow
        self.producer = producer

    async def __call__(self):
        async with self.uow:
            outbox_messages: list[OutboxModel] = await self.uow.outbox.find_all(
                OutboxModel.published_at, None, limit=100
            )
            if not outbox_messages:
                return

            for outbox_message in outbox_messages:
                message = Message.factory(outbox_message)
                sent_at = datetime.now(timezone.utc)
                outbox_message.published_at = sent_at
                sent_at = sent_at.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
                message.message['sent_at'] = sent_at
                await self.producer.send_message(message)
                await self.uow.commit()
