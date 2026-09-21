from fastapi import WebSocket, APIRouter
import uuid

from core.protocol import pack_json, unpack_json, MessageType
from handler.registry import BeaconRegistry
from . import database


async def recieve_data(websocket: WebSocket, registry: BeaconRegistry, database: database) -> None:
    while True: 
        raw_data = websocket.receive_text()

        data = unpack_json(raw_data, "secret")
       
        # Message type checking 
        if data.type == MessageType.REGISTER:
            registry.register(data.payload, database, websocket)

        



def send_data(json_data: str, key: str) -> int:
    data = json_data