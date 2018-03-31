from unittest import TestCase
from pathlib import Path


class TestBase(TestCase):

    def ensure_dir_exists(self, directory):
        Path(directory).mkdir(parents=True, exist_ok=True)
