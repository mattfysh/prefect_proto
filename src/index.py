from prefect import flow


@flow
def get_meaning():
    return 42


def handler(event, context):
    get_meaning()
    return "done"
