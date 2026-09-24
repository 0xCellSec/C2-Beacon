# importing project py modules 
from app import interface, database
from app.core import models
import asyncio
import aiosqlite
from app.core import encoding
from app.core.settings import Config

# importing pythin lib
import uuid
import json


class FakeWebSocket():
    async def accept(self):
        pass

    async def receive_text(self):
        
        fake_beacon_message = json.dumps({'type': 'REGISTER', 
                                        'payload':{'beacon_id' :str(uuid.uuid4()), 'os':'Linux', 'hostname':'OS_HOSTNAME', 'username':'OS_USERNAM', 
                                        'pid':34829, 
                                        'internal_ip':'127.0.0.1'}})

        return encoding.encode(fake_beacon_message, Config.encryption_key)

async def test_registry():
    fake_ws = FakeWebSocket()
    
    async with aiosqlite.connect(Config.database_file_path) as db:
        await db.executescript(database.SCHEMA)
        await db.commit()

        await interface.recieve_data(fake_ws, db)

if __name__ == '__main__':
    asyncio.run(test_registry())