from typing import Optional
from prefect import flow, task
from prefect.tasks import task_input_hash
from .art import make_art
from .a import do_flow_a


@task(cache_key_fn=task_input_hash)
def do_task_b(id: int, a_result: int) -> int:
    result = a_result / 3
    make_art(f"{id}-task-b", result)
    return result


@flow(result_storage="s3/cache", log_prints=True)
def do_flow_b(id: str, bust: Optional[str]) -> int:
    bust_deep = "all" if bust == "all" else None
    a_result = do_flow_a(id, bust_deep)

    tag = f"id={id}/task-b"
    bust_this = bust is not None
    return do_task_b.with_options(tags=[tag], refresh_cache=bust_this)(id, a_result)
