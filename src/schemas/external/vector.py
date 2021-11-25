from typing import List
from typing import Optional
from typing import Union

from src.schemas.base import BaseVectorInstance as BaseInstance
from src.schemas.base import Attribute as BaseAttribute
from src.schemas.base import BboxPoints
from src.schemas.base import Comment
from src.schemas.base import Metadata
from src.schemas.base import Tag
from src.schemas.base import NotEmptyStr
from src.schemas.base import VectorAnnotationTypeEnum
from src.schemas.base import AxisPoint
from pydantic import BaseModel
from pydantic import conlist
from pydantic import Field
from pydantic import validate_model
from pydantic import ValidationError
from pydantic import validator


class Attribute(BaseAttribute):
    id: Optional[int]
    group_id: Optional[int] = Field(None, alias="groupId")
    name: NotEmptyStr
    group_name: NotEmptyStr = Field(None, alias="groupName")


class BaseVectorInstance(BaseInstance):
    class_id: Optional[int] = Field(None, alias="classId")
    class_name: str = Field(alias="className")
    attributes: Optional[List[Attribute]] = Field(list())


class Point(BaseVectorInstance, AxisPoint):
    pass


class PolyLine(BaseVectorInstance):
    points: List[float]


class Polygon(BaseVectorInstance):
    points: List[float]


class Bbox(BaseVectorInstance):
    points: BboxPoints


class RotatedBoxPoints(BaseVectorInstance):
    x1: float
    y1: float
    x2: float
    y2: float
    x3: float
    y3: float
    x4: float
    y4: float


class RotatedBox(BaseVectorInstance):
    points: RotatedBoxPoints


class Ellipse(BaseVectorInstance):
    cx: float
    cy: float
    rx: float
    ry: float
    angle: float


class TemplatePoint(BaseModel):
    id: int
    x: float
    y: float


class TemplateConnection(BaseModel):
    id: int
    from_connection: int = Field(alias="from")
    to_connection: int = Field(alias="to")


class Template(BaseVectorInstance):
    points: conlist(TemplatePoint, min_items=1)
    connections: List[TemplateConnection]
    template_id: Optional[int] = Field(None, alias="templateId")
    template_name: str = Field(alias="templateName")


class CuboidPoint(BaseModel):
    f1: AxisPoint
    f2: AxisPoint
    r1: AxisPoint
    r2: AxisPoint


class Cuboid(BaseVectorInstance):
    points: CuboidPoint


ANNOTATION_TYPES = {
    VectorAnnotationTypeEnum.BBOX: Bbox,
    VectorAnnotationTypeEnum.TEMPLATE: Template,
    VectorAnnotationTypeEnum.CUBOID: Cuboid,
    VectorAnnotationTypeEnum.POLYGON: Polygon,
    VectorAnnotationTypeEnum.POINT: Point,
    VectorAnnotationTypeEnum.POLYLINE: PolyLine,
    VectorAnnotationTypeEnum.ELLIPSE: Ellipse,
    VectorAnnotationTypeEnum.RBBOX: RotatedBox,
}


class VectorAnnotation(BaseModel):
    metadata: Metadata
    comments: Optional[List[Comment]] = Field(list())
    tags: Optional[List[Tag]] = Field(list())
    instances: Optional[
        List[
            Union[Template, Cuboid, Point, PolyLine, Polygon, Bbox, Ellipse, RotatedBox]
        ]
    ] = Field(list())

    @validator("instances", pre=True, each_item=True)
    def check_instances(cls, instance):
        # todo add type checking
        annotation_type = instance.get("type")
        result = validate_model(ANNOTATION_TYPES[annotation_type], instance)
        if result[2]:
            raise ValidationError(
                result[2].raw_errors, model=ANNOTATION_TYPES[annotation_type]
            )
        return instance
