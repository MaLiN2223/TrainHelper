class ConfigSection:
    def __init__(self):
        pass

    def __getattribute__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            return None

    def __bool__(self):
        return len([a for a in dir(self) if a[0:2] != "__"]) > 0  # meaning it has some properties

class Config:
    def __init__(self, config_name):
        self.config_name = config_name

    def __getattribute__(self, item):
        try:
            return object.__getattribute__(self, item)
        except AttributeError:
            return ConfigSection()

