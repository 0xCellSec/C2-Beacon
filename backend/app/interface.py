from fastapi import WebSocket

from app.core.settings import Config
from app.core.protocol import pack_json, unpack_json, MessageType
from app.handler.registry import BeaconRegistry 
from app.handler.heartbeat import BeaconHeartbeat
from app.handler.tasks import Task
import app.core.models as model
from . import database


async def recieve_data(websocket: WebSocket, database: database) -> None:
    registry = BeaconRegistry()
    heartbeat = BeaconHeartbeat()
    task = Task()
    while True: 
        raw_data = await websocket.receive_text()

        data = unpack_json(raw_data, Config.encryption_key)

        print(f"interface data type: {data.type}")
        # Message type checking 
        if data.type == MessageType.REGISTER: 
            validated_beacon_model = model.BeaconMeta.model_validate(data.payload)
            await registry.register(validated_beacon_model, database, websocket)

        elif data.type == MessageType.HEARTBEAT:
            validated_beacon_model = model.BeaconHeartbeat.model_validate(data.payload)
            await heartbeat.record_heartbeat(validated_beacon_model, database)
            await task.send_task(validated_beacon_model, websocket, database)

        elif data.type == MessageType.RESULT:
            pass