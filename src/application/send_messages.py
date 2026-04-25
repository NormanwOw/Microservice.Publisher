from datetime import datetime, timezone

from sqlalchemy_events import sa_insert_handler

from src.infrastructure.messaging.messages import Message
from src.infrastructure.models import OutboxModel
from src.infrastructure.producer import producer
from src.infrastructure.uow.impl import get_uow
from src.infrastructure.uow.interfaces import IUnitOfWork


@sa_insert_handler(OutboxModel)
async def send_messages():
    uow: IUnitOfWork = get_uow()
    async with uow:
        outbox_messages: list[OutboxModel] = await uow.outbox.find_all(
            OutboxModel.published_at, None, limit=100, with_for_update=True
        )
        if not outbox_messages:
            return

        for outbox_message in outbox_messages:
            message = Message.factory(outbox_message)
            sent_at = datetime.now(timezone.utc)
            outbox_message.published_at = sent_at
            sent_at = sent_at.isoformat(timespec='milliseconds').replace('+00:00', 'Z')
            message.message['sent_at'] = sent_at
            await producer.send_message(message)
            await uow.commit()
