from fastapi import FastAPI, status ,Request
from fastapi.responses import JSONResponse, StreamingResponse

from uuid import uuid4

from api.api_model import PlanRequest, PlanTaskAccepted ,ApiError

from backend.model.task_model import PlanTaskRecord, TaskStatus

import asyncio

import json

from api.sse import stream_task_events, PlanTaskEvent

from backend.model.plan_model import PlanResult

#FastAPI() → 创建一个 Web 应用对象
app = FastAPI()
#uv run uvicorn main:app --reload

#Python程序内部的异常信号
class TaskNotFoundError(Exception):
    pass
#注册异常处理器
@app.exception_handler(TaskNotFoundError)
async def task_not_found_handler(
    _request: Request,
    _exception: TaskNotFoundError,
) -> JSONResponse:
    error = ApiError(
        code="TASK_NOT_FOUND",
        message="未找到对应的规划任务"
    )

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=error.model_dump(),
    )

class ResultNotFoundError(Exception):
    pass
#注册结果不存在处理器
@app.exception_handler(ResultNotFoundError)
async def result_not_found_handler(
    _request:Request,
    _exception: ResultNotFoundError
) -> JSONResponse:
    error = ApiError(
        code="RESULT_NOT_FOUND",
        message="未找到对应的规划结果"
    )

    return JSONResponse(
        status_code=status.HTTP_404_NOT_FOUND,
        content=error.model_dump(),
    )


#添加任务表
plan_tasks: dict[str, PlanTaskRecord] = {}

task_event_queues: dict[
    str,
    asyncio.Queue[PlanTaskEvent],
] = {}

plan_results: dict[str, PlanResult] = {}

#查找任务 允许查找不到
def find_plan_task(task_id: str) -> PlanTaskRecord | None:
    return plan_tasks.get(task_id)

#必须找到任务
def require_plan_task(task_id: str) -> PlanTaskRecord:
    task = find_plan_task(task_id)

    if task is None:
        raise TaskNotFoundError()

    return task

#查找结果 允许查找不到
def find_plan_result(result_id: str,) -> PlanResult | None:
    return plan_results.get(result_id)

#必须找到结果
def require_plan_result(result_id: str) -> PlanResult:
    result = find_plan_result(result_id)

    if result is None:
        raise ResultNotFoundError()

    return result

#如果收到访问 /health 的 GET 请求，就调用紧随其后的函数-----------------------------
#"/health"：浏览器访问的 URL 路径
#最小 Web服务活着
@app.get("/health")
def health_check():
    return {"status": "ok"}

#添加路由
#创建任务并把任务放入队列
@app.post(
    "/api/plan-tasks",
    status_code = status.HTTP_202_ACCEPTED,
    response_model = PlanTaskAccepted,
)
async def create_plan_task(plan_request: PlanRequest) -> PlanTaskAccepted:
    task_id = f"task-{uuid4()}"
    task = PlanTaskRecord(
        task_id = task_id,
        status = TaskStatus.ACCEPTED,
        request = plan_request,
    )
    plan_tasks[task_id] = task
    task_event_queues[task_id] = asyncio.Queue()
    return PlanTaskAccepted(task_id=task_id)


#SSE获取任务进度
@app.get(
    "/api/plan-tasks/{task_id}/events",
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ApiError,
            "description": "任务不存在",
        },
    },
)
async def receive_task_progress(
    task_id: str
) -> StreamingResponse:
    task = require_plan_task(task_id)
    event_queue = task_event_queues[task.task_id]

    return StreamingResponse(
        stream_task_events(event_queue),
        media_type="text/event-stream",
    )

#添加结果查询路由
@app.get(
    "/api/plan-results/{result_id}",
    response_model=PlanResult,
    responses={
        status.HTTP_404_NOT_FOUND: {
            "model": ApiError,
            "description": "规划结果不存在",
        },
    },
)
async def get_plan_result(
    result_id: str,
) -> PlanResult:
    result = require_plan_result(result_id)

    return result
