import uuid
from fastapi import websockets
import aiosqlite

from app.core.models import TaskResult
from app.core.settings import Config



class ServerResults:
    async def log_task_result(result: TaskResult, database: aiosqlite.Connection):
        await database.execute(
            """
            INSERT INTO task_results (task_id, output, error) VALUE (?, ?, ?)
            """, 
            result.task_id, 
            result.output, 
            result.error, 
            result.created_at,
        )
        await database.commit()
