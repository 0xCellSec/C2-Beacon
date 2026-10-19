import uuid
from fastapi import WebSocket
import aiosqlite
from datetime import datetime, UTC

from app.core.models import TaskResult
from app.core.settings import Config



class ServerResults:
    async def log_task_result(self, result: TaskResult, database: aiosqlite.Connection, websocket: WebSocket):
        print(f"\n\n\n\nRESULTS: {result}")
        now = datetime.now(UTC).isoformat()

        await database.execute(
                    """
                    UPDATE tasks 
                    SET status = ?, completed_at = ? 
                    WHERE task_id = ? 
                    """,
                    (
                        'complete', 
                        now,
                        result.task_id
        
                    )
        )
        
        await database.execute(
            """
            INSERT INTO task_results (task_id, output, error, created_at) VALUES (?, ?, ?, ?)
            """, 
            (result.task_id, 
            result.output, 
            result.error, 
            result.created_at)
        )

        await database.commit()
