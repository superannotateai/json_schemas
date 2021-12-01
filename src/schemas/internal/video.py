from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from src.schemas.base import Attribute
from src.schemas.base import BaseInstance
from src.schemas.base import BboxPoints
from src.schemas.base import BaseMetadata
from src.schemas.base import PointLabels
from src.schemas.base import Tag
from pydantic import BaseModel
from pydantic import constr
from pydantic import Field
from pydantic import StrictStr


class VideoType(str, Enum):
    EVENT = "event"
    BBOX = "bbox"


class MetaData(BaseMetadata):
    name: Optional[StrictStr]
    width: Optional[int]
    height: Optional[int]
    duration: Optional[int]


class BaseTimeStamp(BaseModel):
    active: Optional[bool]
    attributes: Optional[Dict[constr(regex=r"^[-|+]$"), List[Attribute]]]  # noqa: F722


class BboxTimeStamp(BaseTimeStamp):
    points: Optional[BboxPoints]


class BaseVideoInstance(BaseInstance):
    id: Optional[str]
    type: VideoType
    locked: Optional[bool]
    timeline: Dict[float, BaseTimeStamp]


class BboxInstance(BaseVideoInstance):
    point_labels: Optional[PointLabels] = Field(None, alias="pointLabels")
    timeline: Dict[float, BboxTimeStamp]


class EventInstance(BaseVideoInstance):
    pass


class VideoAnnotation(BaseModel):
    metadata: MetaData
    instances: Optional[List[Union[EventInstance, BboxInstance]]] = Field(list())
    tags: Optional[List[Tag]] = Field(list())
