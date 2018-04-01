from os import popen


class Queuer:
    def __init__(self,config):
        self.config = config

    def _execute_command(self, command):
        return popen(command).read()

    def queue(self, args=None):
        raise NotImplementedError()
