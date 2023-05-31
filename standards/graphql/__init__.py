import strawberry
from .queries import Query


__all__: list[str] = ["get_schema"]


def get_schema() -> strawberry.Schema:
    return strawberry.Schema(Query)
