from typing import List
from typing import Optional

from src.schemas.base import BaseImageMetadata as Metadata
from src.schemas.base import PixelColor
from src.schemas.base import BaseAttribute
from src.schemas.base import BaseImageAnnotationInstance
from src.schemas.base import Tag
from src.schemas.base import Comment

from pydantic import BaseModel
from pydantic import StrictInt
from pydantic import Field


class Attribute(BaseAttribute):
    id: StrictInt
    group_id: StrictInt = Field(alias="groupId")


class AnnotationPart(BaseModel):
    color: PixelColor


class AnnotationInstance(BaseImageAnnotationInstance):
    parts: List[AnnotationPart]
    class_id: StrictInt = Field(alias="classId")
    attributes: Optional[List[Attribute]] = Field(list())


class PixelAnnotation(BaseModel):
    metadata: Metadata
    instances: List[AnnotationInstance]
    tags: Optional[List[Tag]] = Field(list())
    comments: Optional[List[Comment]] = Field(list())
