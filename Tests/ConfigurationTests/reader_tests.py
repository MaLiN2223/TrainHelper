import sys
from unittest import TestCase
from mock import Mock
from src.configuration import Reader


class ReaderTests(TestCase):
    def givenPathAndAsDictionary_willReadGoodFile(self):
        parser = Mock()
        parser.sections = Mock(return_value=[])
        sys.modules['configparser'] = parser
        config_path = 'config_path'
        reader = Reader()

        # Act
        reader.read(config_path, True)

        # Assert
        self.assertTrue(parser.sections.called)
        parser.sections.assert_called_with(config_path)
