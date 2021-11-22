import copy
from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Type

from src.utils import wrap_error
from schemas.external import PixelAnnotation as ExternalPixelAnnotation
from schemas.external import VectorAnnotation as ExternalVectorAnnotation
from schemas.external import VideoAnnotation as ExternalVideoAnnotation
from schemas.external import DocumentAnnotation as ExternalDocumentAnnotation

from schemas.internal import PixelAnnotation as InternalPixelAnnotation
from schemas.internal import VectorAnnotation as InternalVectorAnnotation
from schemas.internal import VideoAnnotation as InternalVideoAnnotation
from schemas.internal import DocumentAnnotation as InternalDocumentAnnotation


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


class AnnotationValidator:

    @staticmethod
    def _get_default_schema():
        return type('CopyOfB', BaseSchemaValidator.__bases__, dict(BaseSchemaValidator.__dict__))

    @classmethod
    def get_pixel_validator(cls, external=True):
        schema = cls._get_default_schema()
        if external:
            schema.MODEL = ExternalPixelAnnotation
        else:
            schema.MODEL = InternalPixelAnnotation
        return schema

    @classmethod
    def get_vector_validator(cls, external=True):
        schema = cls._get_default_schema()
        if external:
            schema.MODEL = ExternalVectorAnnotation
        else:
            schema.MODEL = InternalVectorAnnotation
        return schema

    @classmethod
    def get_video_validator(cls, external=True):
        schema = cls._get_default_schema()
        if external:
            schema.MODEL = ExternalVideoAnnotation
        else:
            schema.MODEL = InternalVideoAnnotation
        return schema

    @classmethod
    def get_document_validator(cls, external=True):
        schema = cls._get_default_schema()
        if external:
            schema.MODEL = ExternalDocumentAnnotation
        else:
            schema.MODEL = InternalDocumentAnnotation
        return schema
