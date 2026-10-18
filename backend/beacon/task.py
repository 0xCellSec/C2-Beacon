from fastapi import WebSocket
import subprocess
import ast

from app.core.protocol import Message, MessageType, pack_json
from app.core.settings import Config


class Tasking():
    
    async def respond_result(command: list, websocket: WebSocket) -> None:
        commands = ast.literal_eval(commands)
        for command in commands:
            print(f"COMMAND:{command, type(commands)}\n")
            raw_command = command[3]
            executed = subprocess.run(raw_command, capture_output=True)

            response = Message(type=MessageType.RESULT, payload={'output': executed.stdout, 'error': executed.stderr})

            data = pack_json(response, Config.encryption_key)
            print(type(data), data)
            print(f"COMMAND EXECUTION RESPONSE: {response}")
            await websocket.send(data)

        await websocket.close()
    