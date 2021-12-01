from pydantic import StrictInt
from pydantic import StrictStr
from typing import Any
from pydantic import BaseModel
from pydantic.errors import WrongConstantError
from pydantic import ValidationError
from pydantic.error_wrappers import ErrorWrapper
from pydantic.errors import MissingError
from pydantic.typing import Literal

class MyFieldMeta(type):
    def __getitem__(self, key_value_type: Any):
        return type('MyFieldValue', (self,), {'key_value_type': key_value_type})


class StrictDict(metaclass=MyFieldMeta):
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
            if not isinstance(key, key_type):
                errors.append(TypeError(f"[{key}] key expected {key_type.__name__}"))
                continue
            if not isinstance(v[key], value_type):
                errors.append(TypeError(f"[{key}].value expected {value_type.__name__}"))
        if errors:
            print(errors)
        return v


# class Foo(BaseModel):
#     c: StrictDict[StrictInt, StrictStr]
#     d: StrictDict[StrictStr, StrictInt]
#
#
# Foo.validate({
#     "c": {1: "sdfasd"},
#     "d": {"1": 1}
# })


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
    other1: StrictStr



class PolyMyFieldMeta(type):

    def __getitem__(self, key_value_type: Any):
        return type('PolyMyFieldMeta', (self,), {'key_value_type': key_value_type})

class PolyMorphList(metaclass=PolyMyFieldMeta):

    key_value_type: Any = None

    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, values):
        errors = []
        for loc, instance in enumerate(values):
            for model in cls.key_value_type:

                # check if the model has identifier field
                if not model.__fields__.get(model.Config.key_field):
                    raise ValidationError(model=model,errors=[
                        ErrorWrapper(exc=MissingError(), loc=(model.Config.key_field,))
                    ])

                # TODO: check if identifier field is literal
                # if not issubclass(model.__fields__.get(model.Config.key_field).type_.__class__,Literal.__class__):
                #     raise TypeError(f"{model.__name__}[{model.Config.key_field}] Literal expected.")

                # check if identifier field is literal
                if "Literal" not in str(model.__fields__.get(model.Config.key_field).type_):
                    raise TypeError(f"{model.__name__}[{model.Config.key_field}] Literal expected.")


                # Validate literal field only
                try:
                    model.__fields__.get(model.Config.key_field).validators[0](0, instance[model.Config.key_field], 0, 0, 0)
                except WrongConstantError:
                    continue

                # Validate instance
                try:
                    model.validate(instance)
                    break
                except ValidationError as e:
                    e.errors()[0]["instance_loc"] = loc
                    errors.append(e)

        print(errors)
        return values



# class Jungle(BaseModel):
#     tree: PolyMorphList[Polygon, NoPolygon, Golygon, Lolygon]
#
#
# Jungle.validate({"tree" : [
#     {"type": "polygon", "other": 1},
#     {"type": "nopolygon", "other": "string"},
#     {"type": "golygon", "other": "some string"},
#     {"type": "golygon", "other": "some string"},
#     {"type": "golygon", "other1": "some string"},
# ]})








