import uuid


def _get_random_id() -> str:
    return uuid.uuid4().hex
