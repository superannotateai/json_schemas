import os
import json
import errno

from src.schemas.external import PixelAnnotation as ExternalPixelAnnotation
from src.schemas.external import VectorAnnotation as ExternalVectorAnnotation
from src.schemas.external import VideoAnnotation as ExternalVideoAnnotation
from src.schemas.external import DocumentAnnotation as ExternalDocumentAnnotation

from src.schemas.internal import PixelAnnotation as InternalPixelAnnotation
from src.schemas.internal import VectorAnnotation as InternalVectorAnnotation
from src.schemas.internal import VideoAnnotation as InternalVideoAnnotation
from src.schemas.internal import DocumentAnnotation as InternalDocumentAnnotation
from src.exceptions import InvalidInput

from src.validators import AnnotationValidators


class CLIInterface:
    DEFAULT_PATH = "schemas/"
    EXTERNAL_SCHEMAS = (
        ExternalPixelAnnotation, ExternalVectorAnnotation, ExternalDocumentAnnotation, ExternalVideoAnnotation
    )
    INTERNAL_SCHEMAS = (
        InternalPixelAnnotation, InternalVectorAnnotation, InternalDocumentAnnotation, InternalVideoAnnotation
    )

    @staticmethod
    def _create_folder(path: str):
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc:
                if exc.errno != errno.EEXIST:
                    raise

    def generate_schemas(self, path: str = None, indent: int = 2):
        path = f"{path}" if path else self.DEFAULT_PATH
        self._create_folder(path)
        for schema in self.INTERNAL_SCHEMAS:
            schema_path = f"{path}/internal_{schema.__name__}.json"
            with open(schema_path, "w") as f:
                f.write(schema.schema_json(indent=indent))
        for schema in self.INTERNAL_SCHEMAS:
            schema_path = f"{path}/external_{schema.__name__}.json"
            with open(schema_path, "w") as f:
                f.write(schema.schema_json(indent=indent))

    def validate(self, *paths, project_type, internal=False, verbose=False, report_path=None):
        validators = AnnotationValidators[project_type.lower()]
        if not validators:
            raise InvalidInput(
                f"Invalid project type, valid types are: {', '.join(AnnotationValidators.VALIDATORS.keys())}"
            )
        external_validator, internal_validator = validators
        validator = internal_validator if internal else external_validator
        for path in paths:
            with open(path, "r") as file:
                data = json.load(file)
                if not validator(data).is_valid():
                    print(validator.generate_report)





