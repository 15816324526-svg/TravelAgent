from api.api_model import (
    PlanTaskCompletedEvent,
    PlanTaskFailedEvent,
    PlanTaskProgressEvent,
    PlanTaskSummary,
)

from api.sse import PlanTaskEvent, encode_sse_event

import asyncio
from collections.abc import AsyncIterator

progress_event = PlanTaskProgressEvent(
    task_id="task-001",
    progress=42,
    current_stage="select_places_and_stay",
    eta_seconds=32,
)

completed_event = PlanTaskCompletedEvent(
    task_id="task-001",
    result_id="result-001",
    summary=PlanTaskSummary(
        days=2,
        nights=1,
        place_count=7,
        budget_per_night=500,
        highlights=["顺路安排，减少往返"],
    ),
)

failed_event = PlanTaskFailedEvent(
    task_id="task-001",
    message="生成行程时发生错误，请重新规划",
)

async def demo_event_stream(
        source_events: list[PlanTaskEvent],
) -> AsyncIterator[str]:
    for event in source_events:
        yield encode_sse_event(event)

async def consume_stream(
        source_events: list[PlanTaskEvent],
) -> None:
    async for encoded in demo_event_stream(source_events):
        assert encoded.startswith("event:")
        assert "\ndata: " in encoded
        assert encoded.endswith("\n\n")

        print(repr(encoded))

async def main() -> None:
    #第一条路径完全消费完成后，才运行第二条路径。

    print("completed path")

    await consume_stream([
        progress_event,
        completed_event,
    ])

    print("failed path")

    await consume_stream([
        progress_event,
        failed_event,
    ])

if __name__=="__main__":
    asyncio.run(main())