from pydantic import BaseModel


class Message(BaseModel):
    id: str
    message: str
