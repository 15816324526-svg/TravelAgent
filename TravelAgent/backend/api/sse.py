from api_model import (
    PlanTaskCompletedEvent,
    PlanTaskFailedEvent,
    PlanTaskProgressEvent,
)

PlanTaskEvent = (
    PlanTaskProgressEvent
    | PlanTaskCompletedEvent
    | PlanTaskFailedEvent
)

import asyncio
from collections.abc import AsyncIterator

def encode_sse_event(event: PlanTaskEvent) -> str:
    #将传入的event转换为json
#     #PlanTaskProgressEvent(
#     task_id="task-001",
#     progress=42,
#     current_stage="select_places_and_stay",
#     eta_seconds=32,
#     )
#转换为：
#{"type":"progress","task_id":"task-001","progress":42,"current_stage":"select_places_and_stay","eta_seconds":32}
    data = event.model_dump_json()

#event:progress/completed/failed
#data:转换好的json
#第一个\n结束data 第二个\n结束整个SSE事件
    return f"event: {event.type}\ndata: {data}\n\n"

async def stream_task_events(
        event_queue: asyncio.Queue[PlanTaskEvent],
) -> AsyncIterator[str]:
    while True:
        event = await event_queue.get()

        yield encode_sse_event(event)

        if event.type in {"completed","failed"}:
            return 