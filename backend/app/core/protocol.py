import binascii
import json
from enum import StrEnum
from typing import Any
from pydantic import BaseModel, ValidationError

from encoding import decode, encode

class MessageType(StrEnum):
    REGISTER = "REGISTER"
    HEARTBEAT = "HEARTBEAT"
    TASK = "TASK"
    RESULT = "RESULT"
    ERROR = "ERROR"

class Message(BaseModel):
    type: MessageType
    payload: dict[str, Any]

def pack_json(message: Message, key: str) -> str:
    """ encodes data in json format then encrypts the data
    
    Parameters: 
    message (str): the data to be packed
    key (str): the key that encrypts the data
    """
    raw_json = message.model_dump_json()
    return encode(raw_json, key)

def unpack_json(raw: str, key: str) -> str:
    """ encodes data in json format then encrypts the data
        
    Parameters: 
    message (str): the data to be unpacked
    key (str): the key that decrypts the data
    """
    try:
        decoded_json = decode(raw, key)
        data = json.loads(decoded_json)
        return Message.model_validate(data)
    

    except (json.JSONDecodeError, ValidationError, UnicodeDecodeError,
            binascii.Error,) as exc:
        raise ValueError(f"Invalid Protocol Message: {exc}") from exc