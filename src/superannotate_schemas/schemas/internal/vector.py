from typing import List
from typing import Optional
from typing import Union

from superannotate_schemas.schemas.base import BaseVectorInstance
from superannotate_schemas.schemas.base import BboxPoints
from superannotate_schemas.schemas.base import BaseAttribute
from superannotate_schemas.schemas.base import Comment
from superannotate_schemas.schemas.base import BaseImageMetadata as Metadata
from superannotate_schemas.schemas.base import Tag
from superannotate_schemas.schemas.base import AxisPoint
from superannotate_schemas.schemas.base import VectorAnnotationTypeEnum
from superannotate_schemas.schemas.base import StrictNumber

from pydantic import BaseModel
from pydantic import StrictInt
from pydantic import StrictFloat
from pydantic import conlist
from pydantic import Field
from pydantic import validate_model
from pydantic import ValidationError
from pydantic import validator


class Attribute(BaseAttribute):
    id: StrictInt
    group_id: StrictInt = Field(alias="groupId")


class VectorInstance(BaseVectorInstance):
    attributes: Optional[List[Attribute]] = Field(list())


class Point(VectorInstance, AxisPoint):
    pass


class PolyLine(VectorInstance):
    points: List[Union[StrictFloat, StrictInt]]


class Polygon(VectorInstance):
    points: conlist(Union[StrictFloat, StrictInt], min_items=3)


class Bbox(VectorInstance):
    points: BboxPoints


class RotatedBoxPoints(VectorInstance):
    x1: StrictNumber
    y1: StrictNumber
    x2: StrictNumber
    y2: StrictNumber
    x3: StrictNumber
    y3: StrictNumber
    x4: StrictNumber
    y4: StrictNumber


class RotatedBox(VectorInstance):
    points: RotatedBoxPoints


class Ellipse(VectorInstance):
    cx: StrictNumber
    cy: StrictNumber
    rx: StrictNumber
    ry: StrictNumber
    angle: StrictNumber


class TemplatePoint(BaseModel):
    id: StrictInt
    x: StrictNumber
    y: StrictNumber


class TemplateConnection(BaseModel):
    id: StrictInt
    from_connection: StrictInt = Field(alias="from")
    to_connection: StrictInt = Field(alias="to")


class Template(VectorInstance):
    points: conlist(TemplatePoint, min_items=1)
    connections: List[TemplateConnection]
    template_id: StrictInt = Field(alias="templateId")


class CuboidPoint(BaseModel):
    f1: AxisPoint
    f2: AxisPoint
    r1: AxisPoint
    r2: AxisPoint


class Cuboid(VectorInstance):
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
