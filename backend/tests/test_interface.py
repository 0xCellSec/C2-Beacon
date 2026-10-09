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

class FakeWebSocket():
    def __init__(self, messages: list[str]):
        self.messages = messages
        self.sent_messages = []
    
    async def accept(self):
        pass

    async def receive_text(self):
        return(self.messages.pop(0))

    def send_text(self, text: str):
        self.sent_messages.append(text)
         
    def send_json(data: dict):
        pass
         

def get_priv_ip() -> str:
        host = socket.gethostname()
        private_ip = socket.gethostbyname(host)

        return str(private_ip)


async def test_registry():
    
    # get host data
    operating = os.uname()
    host_pid = int(os.getpid())
    host_username = str(os.getlogin())
    private_ip = get_priv_ip()

    try: 

        async with aiosqlite.connect(Config.database_file_path) as db:
            await db.executescript(database.SCHEMA)
            await db.commit()

            # craft beacon message
            print("test registry")
            register_message = encoding.encode(json.dumps({'type': 'REGISTER', 
                                                        'payload':{'os':str(operating.sysname), 
                                                                    'hostname':str(operating.nodename), 
                                                                    'username': host_username, 
                                                                    'pid': host_pid, 
                                                                    'internal_ip': private_ip}
                                                                    }), Config.encryption_key)
                    
            messages = [register_message]
            
            fake_ws = FakeWebSocket(messages)

            await interface.recieve_data(fake_ws, db)

            id  = fake_ws.sent_messages[0]
            
            print(f"test_interface: {str(id)}\n {len(id)}")

            await db.execute("""
                                    INSERT INTO tasks(task_id, command, args, created_at) 
                                    VALUES (?, "SHELL", "whoami", ?)
                                    """, (id, datetime.now(UTC).isoformat()))
            

            time.sleep(5)
            heartbeat_message = encoding.encode(json.dumps({'type': 'HEARTBEAT', 
                                                                'payload': {'agent_id' : str(id), 
                                                                            'first_seen': '',
                                                                            'last_seen': ''}}), Config.encryption_key)

            messages.append(heartbeat_message)

            await interface.recieve_data(fake_ws, db)
            task = fake_ws.sent_messages[0]
            print(task)

    except (IndexError) as err:
        print(f"ERROR: {err}")

if __name__ == '__main__':
    asyncio.run(test_registry())