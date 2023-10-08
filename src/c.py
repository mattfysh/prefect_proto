from typing import Optional
from prefect import flow, task
from prefect.tasks import task_input_hash
from .art import make_art
from .b import do_flow_b


@task(cache_key_fn=task_input_hash)
def do_task_c(id: int, b_result: int) -> int:
    result = b_result * 10
    make_art(f"{id}-task-c", result)
    return result


@flow(result_storage="s3/cache", log_prints=True)
def do_flow_c(id: str, bust: Optional[str]) -> int:
    bust_deep = "all" if bust == "all" else None
    b_result = do_flow_b(id, bust_deep)

    tag = f"id={id}/task-c"
    bust_this = bust is not None
    return do_task_c.with_options(tags=[tag], refresh_cache=bust_this)(id, b_result)
