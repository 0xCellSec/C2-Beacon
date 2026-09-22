from datetime import UTC, datetime
from enum import StrEnum

from pydantic import BaseModel, Field

class CommandType(StrEnum):
    # structure of commands types avilable 
    SHELL = "shell"
    SLEEP = "sleep"

class BeaconMeta(BaseModel):
    # metadata fields of the target/beacon machine 
    beacon_id: str
    os: str
    hostname: str
    username: str 
    pid: int 
    internal_ip: str 

class BeaconLog(BeaconMeta):
    # tracking fields for the beacon
    agent_id: str
    first_seen: str
    last_seen: str

class TaskRequest(BaseModel):
    beacon_id: str
    command: CommandType
    args: str | None = None
    

class TaskRecord(BaseModel):
    id: str
    beacon_id: str
    command: CommandType
    args: str | None = None
    status: str = "pending"
    created_at: str = Field(default_factory = lambda: datetime.now(UTC).isoformat())
    completed_at: str | None = None


class TaskResult(BaseModel):
    id: str
    task_id: str
    output: str | None = None
    error: str | None = None
    created_at: str = Field(default_factory = lambda: datetime.now(UTC).isoformat())
