import asyncio
import time
import json
from prefect import flow, task, tags, get_client
from prefect.tasks import task_input_hash
from prefect.artifacts import create_markdown_artifact


@task(cache_key_fn=task_input_hash)
def get_meaning_task(id: str) -> int:
    print("TASK: simulating slow compute...")
    time.sleep(5)
    print("TASK: fin")
    if id == "abc":
        result = 1234
    else:
        result = 420

    markdown = f"""# Result

Here we display the result of the compute task, to test viability
of surfacing computation results as artifacts in the Prefect UI

## Value

```
{json.dumps(result)}
```
"""

    create_markdown_artifact(
        key=f"artifact-id-{id}", markdown=markdown, description="You've got mail!"
    )

    return result


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
