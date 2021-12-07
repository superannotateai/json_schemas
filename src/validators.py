import copy
from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Type
from typing import Tuple

from src.utils import wrap_error
from src.schemas.external import PixelAnnotation as ExternalPixelAnnotation
from src.schemas.external import VectorAnnotation as ExternalVectorAnnotation
from src.schemas.external import VideoAnnotation as ExternalVideoAnnotation
from src.schemas.external import DocumentAnnotation as ExternalDocumentAnnotation

from src.schemas.internal import PixelAnnotation as InternalPixelAnnotation
from src.schemas.internal import VectorAnnotation as InternalVectorAnnotation
from src.schemas.internal import VideoAnnotation as InternalVideoAnnotation
from src.schemas.internal import DocumentAnnotation as InternalDocumentAnnotation


from pydantic import BaseModel
from pydantic import Extra
from pydantic import ValidationError


class BaseValidator(metaclass=ABCMeta):
    MODEL: Type[BaseModel]

    def __init__(self, data: Any, allow_extra: bool = True):
        self.data = data
        self._validation_output = None
        self._extra = Extra.allow if allow_extra else Extra.forbid

    @classmethod
    def validate(cls, data: Any, extra=True):
        return cls.MODEL(**data)

    def _validate(self):
        model = copy.deepcopy(self.MODEL)
        model.Config.extra = self._extra
        self.data = model(**self.data).dict(by_alias=True, exclude_none=True)

    @abstractmethod
    def is_valid(self) -> bool:
        raise NotImplementedError

    @abstractmethod
    def generate_report(self) -> str:
        raise NotImplementedError


class BaseSchemaValidator(BaseValidator):
    MODEL = BaseModel()

    def is_valid(self) -> bool:
        try:
            self._validate()
        except ValidationError as e:
            self._validation_output = e
        return not bool(self._validation_output)

    def generate_report(self) -> str:
        return wrap_error(self._validation_output)


class ValidatorFactory:
    @staticmethod
    def _get_default_schema():
        return type('CopyOfB', BaseSchemaValidator.__bases__, dict(BaseSchemaValidator.__dict__))

    @staticmethod
    def get_validator(model: BaseModel):
        schema = ValidatorFactory._get_default_schema()
        schema.MODEL = model
        return schema

    def __class_getitem__(cls, item):
        return cls.get_validator(item)


class AnnotationValidators:
    VALIDATORS = {
        "pixel": (
            ValidatorFactory[ExternalPixelAnnotation],
            ValidatorFactory[InternalPixelAnnotation]
        ),
        "vector": (
            ValidatorFactory[ExternalVectorAnnotation],
            ValidatorFactory[InternalVectorAnnotation]
        ),
        "video": (
            ValidatorFactory[ExternalVideoAnnotation],
            ValidatorFactory[InternalVideoAnnotation]
        ),
        "document": (
            ValidatorFactory[ExternalDocumentAnnotation],
            ValidatorFactory[InternalDocumentAnnotation]
        )
    }

    def __class_getitem__(cls, item) -> Tuple[BaseModel, BaseModel]:
        return cls.VALIDATORS.get(item)

    def __getitem__(self, item) -> Tuple[BaseModel, BaseModel]:
        return AnnotationValidator[item]

