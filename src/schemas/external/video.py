from enum import Enum
from typing import Dict
from typing import List
from typing import Optional
from typing import Union

from src.schemas.base import AnnotationStatusEnum
from src.schemas.base import BaseAttribute
from src.schemas.base import BaseInstance
from src.schemas.base import BboxPoints
from src.schemas.base import BaseMetadata
from src.schemas.base import NotEmptyStr
from src.schemas.base import PointLabels
from src.schemas.base import Tag

from pydantic import BaseModel
from pydantic import StrictBool
from pydantic import conlist
from pydantic import Field
from pydantic import StrictInt
from pydantic import StrictStr


class Attribute(BaseAttribute):
    name: NotEmptyStr
    group_name: NotEmptyStr = Field(alias="groupName")


class VideoType(str, Enum):
    EVENT = "event"
    BBOX = "bbox"


class MetaData(BaseMetadata):
    width: Optional[StrictInt]
    height: Optional[StrictInt]
    status: Optional[AnnotationStatusEnum]
    duration: Optional[StrictInt]
    error: Optional[StrictBool]


class BaseTimeStamp(BaseModel):
    timestamp: StrictInt
    attributes: Optional[List[Attribute]]


class BboxTimeStamp(BaseTimeStamp):
    points: BboxPoints


class EventTimeStamp(BaseTimeStamp):
    pass


class InstanceMetadata(BaseInstance):
    type: VideoType
    start: StrictInt
    end: StrictInt

    class Config:
        fields = {"creation_type": {"exclude": True}}


class BBoxInstanceMetadata(InstanceMetadata):
    type: StrictStr = Field(VideoType.BBOX, const=True)
    point_labels: Optional[PointLabels] = Field(alias="pointLabels")


class EventInstanceMetadata(InstanceMetadata):
    type: StrictStr = Field(VideoType.EVENT, const=True)


class BaseVideoInstance(BaseModel):
    metadata: InstanceMetadata
    id: Optional[str]
    type: VideoType
    locked: Optional[bool]
    timeline: Dict[float, BaseTimeStamp]


class BaseParameter(BaseModel):
    start: StrictInt
    end: StrictInt


class BboxParameter(BaseParameter):
    timestamps: conlist(BboxTimeStamp, min_items=2)


class EventParameter(BaseParameter):
    timestamps: conlist(EventTimeStamp, min_items=2)


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
