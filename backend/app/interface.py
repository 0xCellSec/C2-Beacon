from fastapi import WebSocket

from app.core.settings import Config
from app.core.protocol import pack_json, unpack_json, MessageType
from app.handler.registry import BeaconRegistry 
from app.handler.heartbeat import BeaconHeartbeat
from app.core.models import BeaconMeta, BeaconLog
from . import database


async def recieve_data(websocket: WebSocket, database: database) -> None:
    registry = BeaconRegistry()
    heartbeat = BeaconHeartbeat()
    while True: 
        raw_data = await websocket.receive_text()

        data = unpack_json(raw_data, Config.encryption_key)

        # Message type checking 
        if data.type == MessageType.REGISTER: 
            validated_beacon_model = BeaconMeta.model_validate(data.payload)
            await registry.register(validated_beacon_model, database, websocket)
        



def send_data(json_data: str, key: str) -> int:
    data = json_data