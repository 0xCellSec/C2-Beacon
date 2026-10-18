from fastapi import WebSocket
import subprocess
import ast

from app.core.protocol import Message, MessageType, pack_json
from app.core.settings import Config



class Tasking():
    
    async def respond_result(command: list, websocket: WebSocket) -> None:
        for i in len(command):
            raw_command = command[i][1]
            executed = subprocess.run(raw_command, capture_output=True)

            response = Message(type=MessageType.RESULT, payload={executed.stdout})

            data = pack_json(response)
            await websocket.send_text(data)

    