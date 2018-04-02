import sys
from unittest import TestCase
from mock import Mock
mocked_configparser = Mock()
mocked_configparser_module = Mock()
mocked_configparser.sections = Mock(return_value=[])
mocked_configparser_module.ConfigParser = Mock(return_value=mocked_configparser)
sys.modules['configparser'] = mocked_configparser_module
from TrainHelper.configuration.reader import Reader


class ReaderTests(TestCase):
    def test_givenPathAndAsDictionary_willReadGoodFile(self):
        parser = Mock()
        config_path = 'config_path'


        # Act
        Reader.read(config_path, True)

        # Assert
        self.assertTrue(parser.sections.called)
        parser.sections.assert_called_with(config_path)
