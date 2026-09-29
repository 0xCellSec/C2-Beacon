import binascii
import json
from enum import StrEnum
from typing import Any
from pydantic import BaseModel, ValidationError

from . import encoding

class MessageType(StrEnum):
    REGISTER = "REGISTER" # beacon -> server : sends metadata
    HEARTBEAT = "HEARTBEAT" # beacon -> server : shows its still connected 
    TASK = "TASK" # server -> beacon : gives task to execute
    RESULT = "RESULT" # beacon -> server : result of the completed task
    ERROR = "ERROR" # server <-> beacon : displays issue between the server and beacon

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
    return encoding.encode(raw_json, key)

def unpack_json(raw: str, key: str) -> Message:
    """ Decrypts the data into json then decods the json into a string
        
    Parameters: 
    message (str): the data to be unpacked
    key (str): the key that decrypts the data
    """
    try:
        decoded_json = encoding.decode(raw, key)
        data = json.loads(decoded_json)
        return Message.model_validate(data)
    

    except (json.JSONDecodeError, ValidationError, UnicodeDecodeError,
            binascii.Error,) as exc:
        raise ValueError(f"Invalid Protocol Message: {exc}") from exc