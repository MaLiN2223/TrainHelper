import logging
from .queuer import Queuer


class QsubQueuer(Queuer):
    def __init__(self, config):
        super().__init__(config)

    def queue(self, args=None):
        print('Running qsub')
        job = self.config.General.Name
        run_script = self.config.Queueing.ScriptName
        file_name = self.config.config_name
        a = self._execute_command('qstat')

        jobs = [q.strip(' ') for q in a.split('\n')[1:] if q.strip(' ') != '' and 'interacti {}'.format(job) in q]
        if len(jobs) > 0:
            print('Job with similar {} is already running'.format(job))
            return

        command = 'qsub -cwd -N {0} -e error-{0} -o output-{0} {1} {2} '.format(job, run_script, file_name)
        if args:
            command += args
        message = 'Will execute {}'.format(command)
        print(message)
        logging.info(message)
        self._execute_command(command)
