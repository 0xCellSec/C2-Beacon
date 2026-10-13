from datetime import UTC, datetime
from fastapi import WebSocket

import aiosqlite

from app.core.models import TaskRequest, BeaconHeartbeat
from app import interface


class Task():
    
    async def send_task(self, data: BeaconHeartbeat, websocket: WebSocket, database: aiosqlite.Connection) -> str:
        
        rows = await database.execute_fetchall("""
                    SELECT * FROM tasks
                    WHERE task_id  = ? 
                    """, (str(data.beacon_id), )
                    )
        await database.close()

        await websocket.send_text(str(rows))
        
        



