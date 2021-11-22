import copy
from abc import ABCMeta
from abc import abstractmethod
from typing import Any
from typing import Type

from src.utils import wrap_error
from schemas import PixelAnnotation
from schemas import VectorAnnotation
from schemas import VideoExportAnnotation
from schemas import DocumentAnnotation

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


class PixelValidator(BaseSchemaValidator):
    MODEL = PixelAnnotation


class VectorValidator(BaseSchemaValidator):
    MODEL = VectorAnnotation


class VideoValidator(BaseSchemaValidator):
    MODEL = VideoExportAnnotation


class DocumentValidator(BaseSchemaValidator):
    MODEL = DocumentAnnotation


class AnnotationValidator:
    @classmethod
    def get_pixel_validator(cls):
        return PixelValidator

    @classmethod
    def get_vector_validator(cls):
        return VectorValidator

    @classmethod
    def get_video_validator(cls):
        return VideoValidator

    @classmethod
    def get_document_validator(cls):
        return DocumentValidator
