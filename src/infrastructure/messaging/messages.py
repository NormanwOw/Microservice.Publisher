from typing import Self

from pydantic import BaseModel

from src.infrastructure.models import OutboxModel


class Message(BaseModel):
    id: str
    message: dict
    topic: str

    @classmethod
    def factory(cls, outbox: OutboxModel) -> Self:
        message = {
            'message_id': str(outbox.id),
            'action': outbox.action,
            'external_reference': outbox.external_reference,
            'payload': outbox.payload,
            'producer': outbox.producer,
        }
        return cls(
            id=str(outbox.id),
            message=message,
            topic=outbox.topic,
        )
