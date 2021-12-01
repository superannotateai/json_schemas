from typing import List
from typing import Optional

from src.schemas.base import BaseMetadata
from src.schemas.base import PixelColor
from src.schemas.base import BaseImageAnnotationInstance
from src.schemas.base import Tag
from pydantic import BaseModel
from pydantic import Field


class PixelMetaData(BaseMetadata):
    is_segmented: Optional[bool] = Field(None, alias="isSegmented")


class PixelAnnotationPart(BaseModel):
    color: PixelColor


class PixelAnnotationInstance(BaseImageAnnotationInstance):
    parts: List[PixelAnnotationPart]


class PixelAnnotation(BaseModel):
    metadata: PixelMetaData
    instances: List[PixelAnnotationInstance]
    tags: Optional[List[Tag]] = Field(list())
