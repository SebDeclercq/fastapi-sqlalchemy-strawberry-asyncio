from typing import Literal
import pydantic


__all__: list[str] = ["Config"]


class Config(pydantic.BaseConfig):
    arbitrary_types_allowed: Literal[True] = True
    underscore_attrs_are_private: Literal[True] = True
