import os
import configparser
import logging
import ntpath
from .config import Config, ConfigSection


class Reader:

    @staticmethod
    def path_leaf(path):
        head, tail = ntpath.split(path)
        return tail or ntpath.basename(head)

    @staticmethod
    def validate_path(path):
        possible = ["", "config", "configs", "conf"]
        for p in possible:
            src = "{}/{}".format(p, path)
            if os.path.exists(src):
                return src
        return path

    @staticmethod
    def read(config_path):
        config_data = configparser.ConfigParser()
        config_data.optionxform = str
        config_path = Reader.validate_path(config_path)
        config_data.read(config_path)
        file_name = Reader.path_leaf(config_path)
        base_text = 'Reading configuration from {}'.format(config_path)
        logging.info('{} as object'.format(base_text))
        configuration = Config(file_name)
        sections = config_data.sections()
        for section_name in sections:
            options = config_data.options(section_name)
            section = ConfigSection()
            for option in options:
                value = config_data[section_name][option]
                val = Reader.__parse(value)
                setattr(section, option.lower(), val)
            setattr(configuration, section_name.lower(), section)
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

    # @staticmethod
    # def __configSectionMap(config, section):
    #     _dict = {}
    #     options = config.options(section)
    #     for option in options:
    #         try:
    #             _dict[section+'.'+option] = Reader.__parse(config.get(section, option))
    #         except Exception as ex:
    #             logging.error(ex)
    #             _dict[option] = None
    #     return _dict

