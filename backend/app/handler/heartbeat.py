from datetime import UTC, datetime


import aiosqlite

from app.core.models import BeaconHeartbeat


class BeaconHeartbeat:

    async def record_heartbeat(
        self,
        log: BeaconHeartbeat, 
        database: aiosqlite.Connection,
    ) -> None:
        
        beacon_id = log.beacon_id
        current_time = datetime.now(UTC).isoformat()


        await database.execute(
            """
            UPDATE beacons 
            SET last_seen  = ?
            WHERE beacon_id = ? 
            """,
            (
                current_time,
                beacon_id
            ))
        await database.commit()