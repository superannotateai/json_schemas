from typing import List
from typing import Optional

from src.utils import Attribute
from src.utils import BaseInstance
from src.utils import MetadataBase
from src.utils import Tag
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
