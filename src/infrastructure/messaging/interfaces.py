from abc import ABC, abstractmethod

from src.infrastructure.messaging.messages import Message


class Producer(ABC):
    @abstractmethod
    async def start(self):
        raise NotImplementedError

    @abstractmethod
    async def send_message(self, message: Message):
        raise NotImplementedError

    @abstractmethod
    async def stop(self):
        raise NotImplementedError
