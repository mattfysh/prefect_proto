import asyncio
import time
from prefect import flow, task, tags, get_client
from prefect.tasks import task_input_hash


@task(cache_key_fn=task_input_hash)
def get_meaning_task(id: str) -> int:
    print("TASK: simulating slow compute...")
    time.sleep(20)
    print("TASK: ")
    if id == "abc":
        return 123
    return 42


@flow(result_storage="s3/cache", log_prints=True)
def get_meaning(id: str) -> int:
    return get_meaning_task(id)


async def run(id):
    tag = f"id={id}"
    async with get_client() as client:
        await client.create_concurrency_limit(tag=tag, concurrency_limit=1)
    with tags(tag):
        return get_meaning(id)


def handler(event, context):
    id = event["id"]
    result = asyncio.get_event_loop().run_until_complete(run(id))
    return f"done: {result}"
