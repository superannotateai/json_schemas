from pydantic import StrictInt
from pydantic import StrictStr
from typing import Any
from pydantic import BaseModel
from pydantic.errors import WrongConstantError
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper
from pydantic.errors import MissingError
from pydantic.typing import Literal


class CustomFieldMeta(type):
    def __getitem__(self, key_value_type: Any):
        return type('CustomFieldValue', (self,), {'key_value_type': key_value_type})




class StrictDict(metaclass=CustomFieldMeta):
    key_value_type: Any = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):

        if not isinstance(v, dict):
            raise TypeError("type dict expected")

        key_type, value_type = cls.key_value_type
        errors = []

        for key in v:
            try:
                key_type(key)
            except ValidationError as e:
                errors.append("")

            try:
                value_type(v[key])
            except ValidationError as e:
                errors.append("")

        return v


class Foo(BaseModel):
    c: StrictDict[StrictInt, StrictInt]
    d: StrictDict[StrictStr, StrictInt]


Foo.validate({
    "c": {1: "1"},
    "d": {"1": 1}
})


class StrictType(BaseModel):
    class Config:
        key_field = "type"


class Polygon(StrictType):
    type: Literal['polygon']
    other: StrictInt


class NoPolygon(StrictType):
    type: Literal['nopolygon']
    other: StrictStr


class Golygon(StrictType):
    type: Literal['golygon']
    other1: StrictStr


class Lolygon(StrictType):
    type: Literal['lolygon']
    other1: StrictStr



class PolyMorphList(metaclass=CustomFieldMeta):
    key_value_type: Any = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, values):
        errors = []
        for loc, instance in enumerate(values):
            for model in cls.key_value_type:

                # check if the model is subclass of StrictType
                if not issubclass(model, StrictType):
                    raise ValidationError(model=model,errors=[
                        ErrorWrapper(exc=MissingError(), loc=(loc,model.__name__))
                    ])

                # check if identifier field exist
                if not model.__fields__.get(model.Config.key_field):
                    raise ValidationError(model=model,errors=[
                        ErrorWrapper(exc=MissingError(), loc=(loc,model.__name__,model.Config.key_field))
                    ])

                # check if identifier field is literal
                if "Literal" not in str(model.__fields__.get(model.Config.key_field).type_):
                    raise ValidationError(model=model, errors=[
                        ErrorWrapper(exc=TypeError("Literal expected."), loc=(loc, model.__name__, model.Config.key_field))
                    ])

                # Validate literal field only
                try:
                    model.__fields__.get(model.Config.key_field).validators[0](None, instance[model.Config.key_field], None, None, None)
                except WrongConstantError:
                    continue

                # Validate instance
                try:
                    model.validate(instance)
                    break
                except ValidationError as e:
                    errors.append(ErrorWrapper(exc=e.raw_errors[0].exc,loc= tuple([loc] + list(e.errors()[0]['loc']))))

        if errors:
            raise ValidationError(
                model=cls,
                errors=errors
            )
        return values

# class Jungle(BaseModel):
#     tree: PolyMorphList[Polygon, NoPolygon, Golygon, Lolygon]
#
#
# Jungle.validate({"tree" : [
#     {"type": "polygon", "other": 1},
#     {"type": "nopolygon", "other": []},
#     {"type": "golygon", "other1": "1"},
#     {"type": "lolygon" , "other1": 12}
# ]})








