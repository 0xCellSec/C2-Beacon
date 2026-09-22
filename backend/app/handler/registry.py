from datetime import UTC, datetime
from fastapi import WebSocket

import aiosqlite

from app.core.models import BeaconMeta, BeaconLog


class BeaconRegistry:
    def __init__(self) -> None:
        self._connections: dict[str, WebSocket] = {}

    async def register(
        self,
        meta: BeaconMeta,
        database: aiosqlite.Connection,
        websocket: WebSocket,
    ) -> None:
        """ logs a beacon into the database serverside

        Parameter: 
        meta (BeaconMeta): this is the metadata struct of the beacon that will be logged
        database (aiosqlite.Connection): the database that the beacon will be logged to
        websocket (websocket): the websocket the beacon sends the data through 
        """
        await websocket.accept()
        print("Beacon Found!")

        # keep a memory websocket log
        self._connections[id] = websocket
        now = datetime.now(UTC).isoformat()

        # keep a stored beacon log
        await database.execute(
            """
            INSERT INTO beacons (id, hostname, os, username, pid, internal_ip, first_seen, last_seen)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            ON CONFLICT(id) DO UPDATE SET
                hostname = excluded.hostname,
                os = excluded.os,
                username = excluded.username,
                pid = excluded.pid,
                internal_ip = excluded.internal_ip,
                last_seen = excluded.last_seen
            """,
            (
                id,
                meta.hostname,
                meta.os,
                meta.username,
                meta.pid,
                meta.internal_ip,
                now,
                now,
            ),
        )

        await database.commit()

    async def unregister(self, id: str, database: aiosqlite.Connection) -> None:
        # remove log from memory
        self._connections.pop(id, None)
        now = datetime.now(UTC).isoformat()

        await database.execute(
            """
            UPDATE beacon SET last_seen = ? WHERE id = ? 
            """,
            (now, id),
        )

        await database.commit()

