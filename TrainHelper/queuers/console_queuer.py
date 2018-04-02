from .queuer import Queuer


class ConsoleQueuer(Queuer):
    def __init__(self, config):
        super().__init__(config)
        self.config = config

    def queue(self, args=None):
        print('Running on console')
        run_script = self.config.Queueing.ScriptName
        file_name = self.config.config_name
        print(run_script)
        exec(open("./"+run_script).read(),globals())
        #execfile('{} --config {}'.format(run_script, file_name))
