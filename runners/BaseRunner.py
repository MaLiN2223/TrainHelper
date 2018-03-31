class BaseRunner:
    def __init__(self):
        raise NotImplementedError()

    def run(self, config):
        raise NotImplementedError()