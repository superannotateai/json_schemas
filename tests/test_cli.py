from subprocess import Popen, PIPE
import os
from os.path import dirname
from tests import LIB_PATH
from pydantic import EmailStr

from unittest import TestCase


class TestCLI(TestCase):
    VALID_ANNOTATION_PATHS = "tests/data_set/sample_project_vector"
    INVALID_ANNOTATION_PATHS = "tests/data_set/sample_project_vector_invalid"
    IMAGE_1 = "example_image_1.jpg___objects.json"
    IMAGE_2 = "example_image_2.jpg___objects.json"


    @property
    def valid_json_path(self):
        return os.path.join(dirname(dirname(__file__)), self.VALID_ANNOTATION_PATHS)

    @property
    def invalid_json_path(self):
        return os.path.join(dirname(dirname(__file__)), self.INVALID_ANNOTATION_PATHS)

    def test_version_output(self):
        args = ["version"]
        p = Popen(["python3", f'{LIB_PATH}/bin/app.py', args[0]],  stdout=PIPE, stderr=PIPE)
        out, _ = p.communicate()
        self.assertIsNotNone(out)

    def test_single_annotation_validation(self):
        args = ["validate", "--project_type", "vector", f"{self.valid_json_path}/{self.IMAGE_1}"]
        p = Popen(["python3", f'{LIB_PATH}/bin/app.py', *args], stdout=PIPE, stderr=PIPE)
        out, _ = p.communicate()
        self.assertTrue(b"[]" in out)

    def test_multiple_annotation_validation(self):
        args = [
            "validate", "--project_type", "vector",
            f"{self.valid_json_path}/{self.IMAGE_1}",
            f"{self.valid_json_path}/{self.IMAGE_2}"
        ]
        p = Popen(["python3", f'{LIB_PATH}/bin/app.py', *args], stdout=PIPE, stderr=PIPE)
        out, _ = p.communicate()
        self.assertTrue(b"[]" in out)

    def test_single_invalid_annotation_validation(self):
        args = ["validate", "--project_type", "vector", f"{self.invalid_json_path}/{self.IMAGE_2}"]
        p = Popen(["python3", f'{LIB_PATH}/bin/app.py', *args], stdout=PIPE, stderr=PIPE)
        out, _ = p.communicate()
        self.assertIsNotNone(out)

    def test_single_invalid_annotation_validation__verbose(self):
        args = [
            "validate", "--project_type", "vector",
            f"{self.invalid_json_path}/{self.IMAGE_2}",
            "--verbose"
        ]
        p = Popen(["python3", f'{LIB_PATH}/bin/app.py', *args], stdout=PIPE, stderr=PIPE)
        out, _ = p.communicate()
        self.assertTrue(b"instances[0].points                              field required" in out)

    def test_multiple_invalid_annotation_validation(self):
        args = [
            "validate", "--project_type", "vector",
            f"{self.invalid_json_path}/{self.IMAGE_2}",
            f"{self.invalid_json_path}/{self.IMAGE_1}"
        ]
        p = Popen(["python3", f'{LIB_PATH}/bin/app.py', *args], stdout=PIPE, stderr=PIPE)
        out, _ = p.communicate()
        self.assertIsNotNone(out)


    def test_(self):
        # from email_validator import validate_email
        # import time
        # s = time.time()
        # for i in range(10):
        #     try:
        #         validate_email("vaghinak@superannotate.com", check_deliverability=True)
        #     except Exception:
        #         pass
        # print(time.time() - s)
        import datetime
        print((datetime.datetime.now(datetime.timezone.utc)).strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3] + 'Z')

