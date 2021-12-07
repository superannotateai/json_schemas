from typing import List
from typing import Optional

from src.schemas.base import BaseAttribute
from src.schemas.base import BaseInstance
from src.schemas.base import BaseMetadata as Metadata
from src.schemas.base import Tag

from pydantic import BaseModel
from pydantic import Field
from pydantic import StrictStr
from pydantic import StrictInt


class Attribute(BaseAttribute):
    id: StrictInt
    group_id: StrictInt = Field(None, alias="groupId")


class DocumentInstance(BaseInstance):
    start: int
    end: int
    attributes: Optional[List[Attribute]] = Field(list())


class DocumentAnnotation(BaseModel):
    metadata: Metadata
    instances: Optional[List[DocumentInstance]] = Field(list())
    tags: Optional[List[Tag]] = Field(list())
    free_text: Optional[StrictStr] = Field(None, alias="freeText")
