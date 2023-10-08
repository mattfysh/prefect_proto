import asyncio
from prefect import tags, get_client
from .c import do_flow_c
from .b import do_flow_b
from .a import do_flow_a

entry = {
    "c": do_flow_c,
    "b": do_flow_b,
    "a": do_flow_a,
}


def noentry(id, bust):
    raise Exception("Unknown entry point")


async def run(step, id, bust):
    tag = f"id={id}"

    async with get_client() as client:
        await asyncio.gather(
            client.create_concurrency_limit(tag=f"{tag}/task-a", concurrency_limit=1),
            client.create_concurrency_limit(tag=f"{tag}/task-b", concurrency_limit=1),
            client.create_concurrency_limit(tag=f"{tag}/task-c", concurrency_limit=1),
        )

    with tags(tag):
        fn = entry.get(step, noentry)
        return fn(id, bust)


def handler(event, context):
    step = event.get("step", "c")
    id = event["id"]
    bust = event.get("bust")
    result = asyncio.get_event_loop().run_until_complete(run(step, id, bust))
    return f"done: {result}"
