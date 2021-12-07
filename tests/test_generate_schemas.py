import glob
from unittest import TestCase
from tempfile import TemporaryDirectory

from src.bin.interface import CLIInterface


class TestGenerateSchemas(TestCase):

    def test_generate(self):
        with TemporaryDirectory() as tmp_dir:
            CLIInterface().generate_schemas(tmp_dir)
            self.assertEqual(8, len(glob.glob(f"{tmp_dir}/*.json")))
