#!/usr/bin/env python3
import os
import errno

import fire
from src import VectorAnnotation
from src import VectorExportAnnotation
from src import PixelAnnotation
from src import PixelExportAnnotation
from src import DocumentAnnotation
from src import DocumentExportAnnotation
from src import VideoAnnotation
from src import VideoExportAnnotation


class CLIInterface:
    DEFAULT_PATH = "schemas"
    SCHEMAS = (
        VectorAnnotation, PixelAnnotation, DocumentAnnotation, VideoAnnotation, VideoExportAnnotation,
        VectorExportAnnotation, PixelExportAnnotation, DocumentExportAnnotation
    )

    def _create_folder(self, path: str):
        if not os.path.exists(os.path.dirname(path)):
            try:
                os.makedirs(os.path.dirname(path))
            except OSError as exc:  # Guard against race condition
                if exc.errno != errno.EEXIST:
                    raise

    def generate_schemas(self, path: str = None, indent: int = 2):
        path = f"{path}" if path else self.DEFAULT_PATH
        for schema in self.SCHEMAS:
            schema_path = f"{path}/{schema.__name__}.json"
            self._create_folder(schema_path)
            with open(schema_path, "w") as f:
                f.write(schema.schema_json(indent=indent))


def main():
    fire.Fire(CLIInterface)


if __name__ == "__main__":
    main()
