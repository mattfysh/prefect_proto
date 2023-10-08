import json
from prefect.artifacts import create_markdown_artifact


def make_art(key, value):
    markdown = f"""# Result

Here we display the result of the compute task, to test viability
of surfacing computation results as artifacts in the Prefect UI

## Value

```
{json.dumps(value)}
```
"""
    create_markdown_artifact(key=key, markdown=markdown)
