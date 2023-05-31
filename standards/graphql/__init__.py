import strawberry
from .queries import Query


__all__: list[str] = ["schema"]


schema: strawberry.Schema = strawberry.Schema(Query)
