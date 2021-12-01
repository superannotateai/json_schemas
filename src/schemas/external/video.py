from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from src.schemas.base import AnnotationStatusEnum
from src.schemas.base import Attribute as BaseAttribute
from src.schemas.base import BaseInstance
from src.schemas.base import BboxPoints
from src.schemas.base import BaseMetadata
from src.schemas.base import NotEmptyStr
from src.schemas.base import PointLabels
from src.schemas.base import Tag
from pydantic import BaseModel
from pydantic import conlist
from pydantic import Field


class Attribute(BaseAttribute):
    id: Optional[int]
    group_id: Optional[int] = Field(None, alias="groupId")
    name: NotEmptyStr
    group_name: NotEmptyStr = Field(None, alias="groupName")


class VideoType(str, Enum):
    EVENT = "event"
    BBOX = "bbox"


class MetaData(BaseMetadata):
    name: NotEmptyStr
    url: str
    status: Optional[AnnotationStatusEnum]
    duration: Optional[int]
    error: Optional[bool]


class BaseTimeStamp(BaseModel):
    timestamp: int
    attributes: List[Attribute]


class BboxTimeStamp(BaseTimeStamp):
    points: BboxPoints


class EventTimeStamp(BaseTimeStamp):
    pass


class InstanceMetadata(BaseInstance):
    type: VideoType
    class_name: Optional[str] = Field(alias="className")
    point_labels: Optional[PointLabels] = Field(None, alias="pointLabels")
    start: int
    end: int

    class Config:
        fields = {"creation_type": {"exclude": True}}


class BBoxInstanceMetadata(InstanceMetadata):
    type: str = Field(VideoType.BBOX, const=True)


class EventInstanceMetadata(InstanceMetadata):
    type: str = Field(VideoType.EVENT, const=True)


class BaseVideoInstance(BaseModel):
    metadata: InstanceMetadata
    id: Optional[str]
    type: VideoType
    locked: Optional[bool]
    timeline: Dict[float, BaseTimeStamp]


class BaseParameter(BaseModel):
    start: int
    end: int


class BboxParameter(BaseParameter):
    timestamps: conlist(BboxTimeStamp, min_items=1)


class EventParameter(BaseParameter):
    timestamps: conlist(EventTimeStamp, min_items=1)


class BboxInstance(BaseModel):
    meta: BBoxInstanceMetadata
    parameters: conlist(BboxParameter, min_items=1)


class EventInstance(BaseModel):
    meta: EventInstanceMetadata
    parameters: conlist(EventParameter, min_items=1)


ANNOTATION_TYPES = {
    VideoType.BBOX: BboxInstance,
    VideoType.EVENT: EventInstance
}


class VideoAnnotation(BaseModel):
    metadata: MetaData
    instances: Optional[List[Union[EventInstance, BboxInstance]]] = Field(list())
    tags: Optional[List[Tag]] = Field(list())
