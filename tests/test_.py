from typing import Literal

from pydantic import BaseModel
from pydantic import StrictStr
from pydantic import StrictInt

from src.schemas.custom_types import Strict
from src.schemas.custom_types import StrictDict
from src.schemas.custom_types import StrictType


# class Foo(BaseModel):
#     c: StrictDict[Strict[int], Strict[int]]
#     d: StrictDict[Strict[str], Strict[str]]


# Foo.validate({
#     "c": {1: "1"},
#     "d": {"1": 1}
# })

class Polygon(StrictType):
    type: Literal['polygon']
    other: StrictInt


class NoPolygon(StrictType):
    type: Literal['nopolygon']
    other: StrictStr


class Golygon(StrictType):
    type: Literal['golygon']
    other1: StrictStr


class Lolygon(StrictType):
    type: Literal['lolygon']
    other1: StrictStr

