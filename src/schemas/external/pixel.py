from typing import List
from typing import Optional

from src.schemas.base import BaseImageAnnotationInstance
from src.schemas.base import Attribute as BaseAttribute
from src.schemas.base import BaseMetadata
from src.schemas.base import NotEmptyStr
from src.schemas.base import PixelColor
from src.schemas.base import Tag
from pydantic import BaseModel
from pydantic import Field


class Attribute(BaseAttribute):
    id: Optional[int]
    group_id: Optional[int] = Field(None, alias="groupId")
    name: NotEmptyStr
    group_name: NotEmptyStr = Field(None, alias="groupName")


class PixelMetaData(BaseMetadata):
    is_segmented: Optional[bool] = Field(None, alias="isSegmented")


class PixelAnnotationPart(BaseModel):
    color: PixelColor


class PixelAnnotationInstance(BaseImageAnnotationInstance):
    parts: List[PixelAnnotationPart]
    class_id: Optional[int] = Field(None, alias="classId")
    class_name: str = Field(alias="className")
    attributes: Optional[List[Attribute]] = Field(list())


class PixelAnnotation(BaseModel):
    metadata: PixelMetaData
    instances: List[PixelAnnotationInstance]
    tags: Optional[List[Tag]] = Field(list())
