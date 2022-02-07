from enum import Enum
from typing import Optional
from typing import List
from typing import Any
from typing import Union

from superannotate_schemas.schemas.base import BaseModel
from superannotate_schemas.schemas.base import TimedBaseModel
from superannotate_schemas.schemas.base import StrictInt
from superannotate_schemas.schemas.base import StrictStr
from superannotate_schemas.schemas.base import HexColor
from superannotate_schemas.schemas.enums import ClassTypeEnum


class Attribute(TimedBaseModel):
    id: Optional[StrictInt]
    group_id: Optional[StrictInt]
    project_id: Optional[StrictInt]
    name: StrictStr
    count: Optional[StrictInt]

    def __hash__(self):
        return hash(f"{self.id}{self.group_id}{self.name}")


class AttributeGroup(TimedBaseModel):
    id: Optional[StrictInt]
    class_id: Optional[StrictInt]
    name: StrictStr
    is_multiselect: Optional[bool]
    attributes: List[Attribute]

    def __hash__(self):
        return hash(f"{self.id}{self.class_id}{self.name}")


class AnnotationClass(TimedBaseModel):
    id: Optional[StrictInt]
    project_id: Optional[StrictInt]
    type: ClassTypeEnum = ClassTypeEnum.OBJECT
    name: StrictStr
    color: HexColor
    count: Optional[StrictInt]
    attribute_groups: List[AttributeGroup] = []

    def __hash__(self):
        return hash(f"{self.id}{self.type}{self.name}")

    class Config:
        validate_assignment = True
        use_enum_values = False
        json_encoders = {
            ClassTypeEnum: lambda value: value.api_repr()
        }

    def _get_value(
        cls,
        v: Any,
        to_dict: bool,
        by_alias: bool,
        include: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']],
        exclude: Optional[Union['AbstractSetIntStr', 'MappingIntStrAny']],
        exclude_unset: bool,
        exclude_defaults: bool,
        exclude_none: bool,
    ) -> Any:
        if isinstance(v, Enum):
            return v.value

        return super()._get_value(v, to_dict, by_alias, include, exclude, exclude_unset, exclude_defaults, exclude_none)


class AnnotationClasses(BaseModel):
    __root__: List[AnnotationClass]
