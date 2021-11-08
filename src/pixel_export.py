from typing import List
from typing import Optional

from src.utils import BaseImageInstance
from src.utils import Attribute as BaseAttribute
from src.utils import MetadataBase
from src.utils import NotEmptyStr
from src.utils import PixelColor
from src.utils import Tag
from pydantic import BaseModel
from pydantic import Field


class Attribute(BaseAttribute):
    id: Optional[int]
    group_id: Optional[int] = Field(None, alias="groupId")
    name: NotEmptyStr
    group_name: NotEmptyStr = Field(None, alias="groupName")


class PixelMetaData(MetadataBase):
    is_segmented: Optional[bool] = Field(None, alias="isSegmented")


class PixelAnnotationPart(BaseModel):
    color: PixelColor


class PixelAnnotationInstance(BaseImageInstance):
    parts: List[PixelAnnotationPart]
    class_id: Optional[int] = Field(None, alias="classId")
    class_name: str = Field(alias="className")
    attributes: Optional[List[Attribute]] = Field(list())


class PixelExportAnnotation(BaseModel):
    metadata: PixelMetaData
    instances: List[PixelAnnotationInstance]
    tags: Optional[List[Tag]] = Field(list())
