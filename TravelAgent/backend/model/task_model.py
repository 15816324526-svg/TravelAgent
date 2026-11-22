#建立内部完整任务记录

from enum import StrEnum

from pydantic import BaseModel

from api.api_model import PlanRequest

class TaskStatus(StrEnum):
    ACCEPTED = "accepted"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"

class PlanTaskRecord(BaseModel):
    task_id: str
    status: TaskStatus
    request: PlanRequest
