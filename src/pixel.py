from typing import List
from typing import Optional

from src.utils import BaseImageInstance
from src.utils import MetadataBase
from src.utils import PixelColor
from src.utils import Tag
from pydantic import BaseModel
from pydantic import Field


class PixelMetaData(MetadataBase):
    is_segmented: Optional[bool] = Field(None, alias="isSegmented")


class PixelAnnotationPart(BaseModel):
    color: PixelColor


class PixelAnnotationInstance(BaseImageInstance):
    parts: List[PixelAnnotationPart]


class PixelAnnotation(BaseModel):
    metadata: PixelMetaData
    instances: List[PixelAnnotationInstance]
    tags: Optional[List[Tag]] = Field(list())
