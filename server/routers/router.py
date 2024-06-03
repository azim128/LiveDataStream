import asyncio

from fastapi import APIRouter, BackgroundTasks
from fastapi.responses import StreamingResponse
from pydantic import BaseModel
from services.sse_service import clients, notify_clients
from utils.db_utils import add_value_to_db

router = APIRouter()


class ValueModel(BaseModel):
    value: str


@router.post("/add-value/")
async def add_value(data: ValueModel, background_tasks: BackgroundTasks):
    add_value_to_db(data.value)
    background_tasks.add_task(notify_clients, f"{data.value}")
    return {"message": "Value added successfully"}


@router.get("/events/")
async def events():

    async def event_generator():
        queue = asyncio.Queue()
        clients.append(queue)
        try:
            while True:
                message = await queue.get()
                yield f"data: {message}\n\n"
        except asyncio.CancelledError:
            clients.remove(queue)

    return StreamingResponse(event_generator(), media_type="text/event-stream")
