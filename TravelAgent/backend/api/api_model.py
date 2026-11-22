from datetime import date
from pydantic import BaseModel, Field

from typing import Literal

from enum import StrEnum

class PlanRequest(BaseModel):
    destination: str = Field(
        min_length=1,
        description="城市",
    )
    start_date: date = Field(
        description="起始日期",
    )
    end_date: date = Field(
        description="结束日期",
    )
    traveler_account: int = Field(
        ge=1,
        description="旅行人数",
    )
    transport_modes: list[str] = Field(
        min_length=1,
        description="可选择的出行方式",
    )
    accommodation_types: list[str] = Field(
        min_length=1,
        description="可选择的居住方式",
    )
    budget_per_night: float = Field(
        ge=0,
        description="每晚居住预算",
    )
    special_requirements: str | None = Field(
        max_length= 2000,
        description="额外要求",
    )

class PlanTaskAccepted(BaseModel):
    task_id: str = Field(
        min_length=1,
        description="后端创建的规划任务编号",
    )

class ApiError(BaseModel):
    code: str = Field(
        description="稳定的机器可读错误代码"
    )
    message: str = Field(
        description= "给用户阅读的错误说明"
    )

class PlanStageId(StrEnum):
    UNDERSTAND_PREFERENCES = "understand_preferences"
    SELECT_PLACES_AND_STAY = "select_places_and_stay"
    OPTIMIZE_ROUTE = "optimize_route"
    BUILD_ITINERARY = "build_itinerary"

class PlanTaskProgressEvent(BaseModel):
    #限制字段只能是某个固定值
    type: Literal["progress"] = "progress"
    task_id: str = Field(
        min_length=1,
        description="规划任务编号",
    )
    progress: int = Field(
        ge=0,
        le=99,
        description="当前进度百分比，范围为0到99",
    )
    current_stage: str = Field(
        description="当前的执行阶段",
    )
    eta_seconds: int | None = Field(
        ge=0,
        description="预计剩余秒数",
    )

class PlanTaskSummary(BaseModel):
    days: int = Field(
        ge=1,
        description="行程天数",
    )
    nights: int = Field(
        ge=0,
        description="住宿晚数",
    )
    place_count: int = Field(
        ge=0,
        description="地点数量",
    )
    budget_per_night: float = Field(
        ge=0,
        description="每晚住宿预算",
    )
    highlights: list[str] = Field(
        description="规划亮点",
    )

class PlanTaskCompletedEvent(BaseModel):
    type: Literal["completed"] = "completed"
    task_id: str = Field(
        min_length=1,
        description="规划任务编号",
    )
    #完成事件的进度只能百分百
    progress: Literal[100]=100
    result_id: str = Field(
      min_length=1,
      description="已经保存的规划结果编号",
    )
    summary: PlanTaskSummary

class PlanTaskFailedEvent(BaseModel):
    type: Literal["failed"] = "failed"
    task_id: str = Field(
        min_length=1,
        description="规划任务编号",
    )
    message: str = Field(
        min_length=1,
        description="任务失败说明",
    )

class TaskNotFoundError(Exception):
    pass