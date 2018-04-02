import argparse
import logging

from ..utils.functions import load_config, setup_logging
from ..queuers import SlurmQueuer, Queuer, ConsoleQueuer


def queue():
    config, config_name = load_config()
    setup_logging(config)

    logging.info('Starting queuer')
    parser = argparse.ArgumentParser(description='Process')
    parser.add_argument('--script', help='sh file name', default='run')

    args, leftovers = parser.parse_known_args()
    script = args.script

    queue_type = config.Queueing.QueueType.lower()
    q = Queuer
    if queue_type == 'slurm':
        q = SlurmQueuer
    if queue_type == 'console':
        q = ConsoleQueuer
    q = q(config)
    message = 'Running with config {}, script {}, using {}'.format(config_name, script, queue_type)
    print(message)
    logging.info(message)
    config.queuer = q
    q.queue(config)
