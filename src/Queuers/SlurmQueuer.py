import logging
from .Queuer import Queuer


class SlurmQueuer(Queuer):
    def __init__(self, config):
        super().__init__(config)

    def queue(self, args=None):
        print('Running slurm')
        job = self.config.General.Name
        run_script = self.config.Queueing.ScriptName
        file_name = self.config.config_name
        a = self._execute_command('squeue')

        if len(a) == 0:
            print('Something is wrong')
            return

        jobs = [q.strip(' ') for q in a.split('\n')[1:] if q.strip(' ') != '' and 'interacti {}'.format(job) in q]
        if len(jobs) > 0:
            print('Job with similar {} is already running'.format(job))
            return
        available = '--exclude='
        for i in range(10, 25):
            available += 'landonia{},'.format(i)
        available = available[:-1]
        command = 'sbatch --job-name {0} --error=error-{0} --output=output-{0} {3} {2}.sh {1} '.format(job, file_name,
                                                                                                       run_script,
                                                                                                       available)

        if args:
            command += args
        message = 'Will execute {}'.format(command)
        print(message)
        logging.info(message)
        self._execute_command(command)
