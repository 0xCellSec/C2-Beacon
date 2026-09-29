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

class FakeWebSocket():
    async def accept(self):
        pass

    def get_priv_ip(self) -> str:
        host = socket.gethostname()
        private_ip = socket.gethostbyname(host)

        return str(private_ip)

    async def receive_text(self) -> encoding.encode:

        # get host data
        operating = os.uname()
        host_pid = int(os.getpid())
        host_username = str(os.getlogin())
        private_ip = self.get_priv_ip()

        # craft beacon message
        fake_beacon_message = json.dumps({'type': 'REGISTER', 
                                        'payload':{'os':str(operating.sysname), 'hostname':str(operating.nodename), 'username': host_username, 
                                        'pid': host_pid, 
                                        'internal_ip': private_ip}})
        
        return encoding.encode(fake_beacon_message, Config.encryption_key)

async def test_registry():
    fake_ws = FakeWebSocket()
    
    async with aiosqlite.connect(Config.database_file_path) as db:
        await db.executescript(database.SCHEMA)
        await db.commit()

        await interface.recieve_data(fake_ws, db)

if __name__ == '__main__':
    asyncio.run(test_registry())