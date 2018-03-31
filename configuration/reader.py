import configparser
import logging
from .config import Config


class Reader:
    @staticmethod
    def read(config_path, as_dictionary=None):
        config_data = configparser.ConfigParser()
        config_data.read(config_path)
        base_text = 'Reading configuration from {}'.format(config_path)
        if as_dictionary:
            logging.info('{} as dictionary'.format(base_text))
            sections = config_data.sections()
            conf = {}
            for section in sections:
                c = Reader.__configSectionMap(config_data, section)
                conf = {**conf, **c}
            return Config(conf)
        else:
            logging.info('{} as object'.format(base_text))
            configuration = Config()
            sections = config_data.sections()
            for section_name in sections:
                options = config_data.options(section_name)
                section = ConfigSection()
                for name, value in options.items():
                    val = Reader.__parse(value)
                    setattr(section, name, val)
                setattr(configuration, section_name, section)
            return configuration

    @staticmethod
    def __parse(s: str):  # TODO: support more types
        if s == 'True':
            return True
        if s == 'False':
            return False
        try:
            return int(s)
        except ValueError:
            try:
                return float(s)
            except ValueError:
                if s[0] == '[' and s[-1] == ']':
                    return map(float, s.split(','))
                else:
                    return s  # return as a string

    @staticmethod
    def __configSectionMap(config, section):
        _dict = {}
        options = config.options(section)
        for option in options:
            try:
                _dict[option] = Reader.__parse(config.get(section, option))
            except Exception as ex:
                logging.error(ex)
                _dict[option] = None
        return _dict


class ConfigSection:
    def __init__(self):
        pass
