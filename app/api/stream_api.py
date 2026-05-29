
import asyncio
import json

from fastapi import APIRouter
from fastapi.responses import (
    StreamingResponse
)

router = APIRouter()


async def event_generator():

    stages = [

        "intent_extraction",

        "schema_generation",

        "appspec_generation",

        "validation",

        "repair"
    ]

    for stage in stages:

        # -----------------------------------
        # STAGE START
        # -----------------------------------

        start_event = {

            "event":
                "stage_start",

            "stage":
                stage
        }

        yield (
            f"data: "
            f"{json.dumps(start_event)}\n\n"
        )

        await asyncio.sleep(1)

        # -----------------------------------
        # STAGE COMPLETE
        # -----------------------------------

        complete_event = {

            "event":
                "stage_complete",

            "stage":
                stage
        }

        yield (
            f"data: "
            f"{json.dumps(complete_event)}\n\n"
        )

        await asyncio.sleep(1)

    # -----------------------------------
    # FINAL EVENT
    # -----------------------------------

    final_event = {

        "event":
            "generation_complete",

        "status":
            "success"
    }

    yield (
        f"data: "
        f"{json.dumps(final_event)}\n\n"
    )


@router.get("/stream-generate")
async def stream_generate():

    return StreamingResponse(

        event_generator(),

        media_type=
            "text/event-stream"
    )

