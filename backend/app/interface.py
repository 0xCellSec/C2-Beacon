from app.core.settings import Config

from fastapi import WebSocket, APIRouter
import uuid


from app.core.protocol import pack_json, unpack_json, MessageType
from app.handler.registry import BeaconRegistry 
from app.core.models import BeaconMeta
from . import database


async def recieve_data(websocket: WebSocket, database: database) -> None:
    Beacon = BeaconRegistry()
    beacon_id = str(uuid.uuid4())
    while True: 
        raw_data = await websocket.receive_text()

        data = unpack_json(raw_data, Config.encryption_key)

        validated_beacon_meta = BeaconMeta.model_validate(data.payload)
        # Message type checking 
        if data.type == MessageType.REGISTER:
            await Beacon.register(beacon_id, validated_beacon_meta, database, websocket)

        



def send_data(json_data: str, key: str) -> int:
    data = json_data