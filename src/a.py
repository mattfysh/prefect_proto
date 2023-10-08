from typing import Optional
from prefect import flow, task
from prefect.tasks import task_input_hash
from .art import make_art


@task(cache_key_fn=task_input_hash)
def do_task_a(id: str) -> int:
    if id == "abc":
        result = 1234
    else:
        result = 420

    make_art(f"{id}-task-a", result)

    return result


@flow(result_storage="s3/cache", log_prints=True)
def do_flow_a(id: str, bust: Optional[str]) -> int:
    tag = f"id={id}/task-a"
    bust_this = bust is not None
    return do_task_a.with_options(tags=[tag], refresh_cache=bust_this)(id)
