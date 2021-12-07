from typing import List
from typing import Optional

from src.schemas.base import BaseImageAnnotationInstance
from src.schemas.base import BaseAttribute
from src.schemas.base import BaseImageMetadata
from src.schemas.base import NotEmptyStr
from src.schemas.base import StrictStr
from src.schemas.base import PixelColor
from src.schemas.base import Tag
from src.schemas.base import Comment

from pydantic import BaseModel
from pydantic import Field


class Attribute(BaseAttribute):
    name: NotEmptyStr
    group_name: NotEmptyStr = Field(alias="groupName")


class MetaData(BaseImageMetadata):
    is_segmented: Optional[bool] = Field(alias="isSegmented")
    is_predicted: Optional[bool] = Field(alias="isPredicted")


class AnnotationPart(BaseModel):
    color: PixelColor


class AnnotationInstance(BaseImageAnnotationInstance):
    parts: List[AnnotationPart]
    class_name: StrictStr = Field(alias="className")
    attributes: Optional[List[Attribute]] = Field(list())


class PixelAnnotation(BaseModel):
    metadata: MetaData
    instances: List[AnnotationInstance]
    tags: Optional[List[Tag]] = Field(list())
    comments: Optional[List[Comment]] = Field(list())
