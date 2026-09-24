import aiosqlite
from collections.abc import AsyncIterator
from app.core.settings import Config


DATABASE_PATH = Config.database_file_path

SCHEMA = """
CREATE TABLE IF NOT EXISTS beacons (
    beacon_id   TEXT PRIMARY KEY,
    hostname    TEXT NOT NULL,
    os          TEXT NOT NULL,
    username    TEXT NOT NULL,
    pid         INTEGER NOT NULL,
    internal_ip TEXT NOT NULL,
    first_seen  TEXT NOT NULL,
    last_seen   TEXT NOT NULL
);

CREATE TABLE IF NOT EXISTS tasks (
    beacon_id           TEXT PRIMARY KEY,
    beacon_id    TEXT NOT NULL,
    command      TEXT NOT NULL,
    args         TEXT,
    status       TEXT NOT NULL DEFAULT 'pending',
    created_at   TEXT NOT NULL,
    completed_at TEXT,
    FOREIGN KEY (beacon_id) REFERENCES beacons(id)
);

CREATE TABLE IF NOT EXISTS task_results (
    beacon_id         TEXT PRIMARY KEY,
    task_id    TEXT NOT NULL UNIQUE,
    output     TEXT,
    error      TEXT,
    created_at TEXT NOT NULL,
    FOREIGN KEY (task_id) REFERENCES tasks(id)
);
"""


async def init_db() -> None:
    async with aiosqlite.connect(DATABASE_PATH) as db:
        await db.executescript(SCHEMA)
        await db.execute("PRAGMA journal_mode=WAL")
        await db.execute("PRAGMA foreign_keys=ON")
        await db.commit()

async def get_db() -> AsyncIterator[aiosqlite.Connection]:
    db = await aiosqlite.connect(DATABASE_PATH)
    db.row_factory = aiosqlite.Row
    await db.execute("PRAGMA foreign_keys=ON")
    try:
        yield db
    finally:
        await db.close()