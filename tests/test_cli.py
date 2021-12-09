from subprocess import Popen, PIPE

from tests import LIB_PATH

from unittest import TestCase
class TestCLI(TestCase):
    VALID_ANNOTATION_PATHS = "/Users/vaghinak.basentsyan/www/superannotate-python-sdk/tests/data_set/sample_project_vector"
    INVALID_ANNOTATION_PATHS = "/Users/vaghinak.basentsyan/www/superannotate-python-sdk/tests/data_set/sample_project_vector_invalid"
    IMAGE_1 = "example_image_1.jpg___objects.json"
    IMAGE_2 = "example_image_2.jpg___objects.json"

    def test_version_output(self):
        args = ["version"]
        p = Popen(["python3", f'{LIB_PATH}/bin/app.py', args[0]],  stdout=PIPE, stderr=PIPE)
        out, _ = p.communicate()
        self.assertIsNotNone(out)

    def test_single_annotation_validation(self):
        args = ["validate", "--project_type", "vector", f"{self.VALID_ANNOTATION_PATHS}/{self.IMAGE_1}"]
        p = Popen(["python3", f'{LIB_PATH}/bin/app.py', *args], stdout=PIPE, stderr=PIPE)
        out, _ = p.communicate()
        self.assertTrue(b"[]" in out)

    def test_multiple_annotation_validation(self):
        args = [
            "validate", "--project_type", "vector",
            f"{self.VALID_ANNOTATION_PATHS}/{self.IMAGE_1}",
            f"{self.VALID_ANNOTATION_PATHS}/{self.IMAGE_2}"
        ]
        p = Popen(["python3", f'{LIB_PATH}/bin/app.py', *args], stdout=PIPE, stderr=PIPE)
        out, _ = p.communicate()
        self.assertTrue(b"[]" in out)

    def test_single_invalid_annotation_validation(self):
        args = ["validate", "--project_type", "vector", f"{self.INVALID_ANNOTATION_PATHS}/{self.IMAGE_2}"]
        p = Popen(["python3", f'{LIB_PATH}/bin/app.py', *args], stdout=PIPE, stderr=PIPE)
        out, _ = p.communicate()
        self.assertIsNotNone(out)

    def test_single_invalid_annotation_validation__verbose(self):
        args = [
            "validate", "--project_type", "vector",
            f"{self.INVALID_ANNOTATION_PATHS}/{self.IMAGE_2}",
            "--verbose"
        ]
        p = Popen(["python3", f'{LIB_PATH}/bin/app.py', *args], stdout=PIPE, stderr=PIPE)
        out, _ = p.communicate()
        self.assertTrue(b"instances[0].points                              field required" in out)

    def test_multiple_invalid_annotation_validation(self):
        args = [
            "validate", "--project_type", "vector",
            f"{self.INVALID_ANNOTATION_PATHS}/{self.IMAGE_2}",
            f"{self.INVALID_ANNOTATION_PATHS}/{self.IMAGE_1}"
        ]
        p = Popen(["python3", f'{LIB_PATH}/bin/app.py', *args], stdout=PIPE, stderr=PIPE)
        out, _ = p.communicate()
        self.assertIsNotNone(out)

