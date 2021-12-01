from typing import List
from typing import Optional

from src.schemas.base import Attribute as BaseAttribute
from src.schemas.base import NotEmptyStr
from src.schemas.base import BaseInstance
from src.schemas.base import BaseMetadata
from src.schemas.base import Tag
from pydantic import BaseModel
from pydantic import Field


class Attribute(BaseAttribute):
    id: Optional[int]
    group_id: Optional[int] = Field(None, alias="groupId")
    name: NotEmptyStr
    group_name: NotEmptyStr = Field(None, alias="groupName")


class DocumentInstance(BaseInstance):
    class_id: Optional[int] = Field(None, alias="classId")
    class_name: str = Field(None, alias="classId")
    start: int
    end: int
    attributes: Optional[List[Attribute]] = Field(list())


class DocumentAnnotation(BaseModel):
    metadata: BaseMetadata
    instances: Optional[List[DocumentInstance]] = Field(list())
    tags: Optional[List[Tag]] = Field(list())
    free_text: Optional[str] = Field(None, alias="freeText")
