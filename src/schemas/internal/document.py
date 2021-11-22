from typing import List
from typing import Optional

from src.schemas.utils import Attribute
from src.schemas.utils import BaseInstance
from src.schemas.utils import MetadataBase
from src.schemas.utils import Tag
from pydantic import BaseModel
from pydantic import Field


class DocumentInstance(BaseInstance):
    start: int
    end: int
    attributes: Optional[List[Attribute]] = Field(list())


class DocumentAnnotation(BaseModel):
    metadata: MetadataBase
    instances: Optional[List[DocumentInstance]] = Field(list())
    tags: Optional[List[Tag]] = Field(list())
    free_text: Optional[str] = Field(None, alias="freeText")
