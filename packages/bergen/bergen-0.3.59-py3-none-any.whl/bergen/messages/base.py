import json
from pydantic import BaseModel
from typing import Optional, Type, TypeVar

from pydantic.types import Json
from pydantic import Field
import uuid

class MessageMetaExtensionsModel(BaseModel):
    """ Extensions to the AMQP Message protocol

    We wrap this in its own message to allow more"""
    progress: Optional[str]

class MessageMetaModel(BaseModel):
    type: str
    reference: str = Field(default_factory=uuid.uuid4)
    extensions: Optional[MessageMetaExtensionsModel] = { }


class MessageDataModel(BaseModel):
    pass

T = TypeVar("T")

class MessageModel(BaseModel):
    data: MessageDataModel
    meta: MessageMetaModel

    def to_message(self) -> bytes:
        return json.dumps(self.dict()).encode()

    def to_channels(self) -> bytes:
        return json.dumps(self.dict())
        
    @classmethod
    def from_message(cls: Type[T], message) -> T:
        return cls(**json.loads(message.body.decode()))

    @classmethod
    def from_channels(cls: Type[T], message: str) -> T:
        return cls(**json.loads(message))

    
