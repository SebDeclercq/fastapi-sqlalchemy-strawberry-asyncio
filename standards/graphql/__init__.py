import strawberry
from .queries import Query


__all__: list[str] = ["get_schema"]


def get_schema() -> strawberry.Schema:
    """Retrieves the Strawberry schema."""
    return strawberry.Schema(Query)
