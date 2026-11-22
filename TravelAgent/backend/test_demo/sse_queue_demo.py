import asyncio

from api.api_model import (
    PlanTaskCompletedEvent,
    PlanTaskProgressEvent,
    PlanTaskSummary,
)

from api.sse import PlanTaskEvent, stream_task_events

async def produce_events(
        event_queue: asyncio.Queue[PlanTaskEvent],
) -> None:
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

    await event_queue.put(progress_event)
    await event_queue.put(completed_event)

async def consume_events(
        event_queue: asyncio.Queue[PlanTaskEvent],
) -> None:
    async for encoded in stream_task_events(event_queue):
        print(repr(encoded))

async def main() -> None:
    event_queue: asyncio.Queue[PlanTaskEvent] = asyncio.Queue()

    await asyncio.gather(
        produce_events(event_queue),
        consume_events(event_queue),
    )

if __name__ == "__main__":
    asyncio.run(main())