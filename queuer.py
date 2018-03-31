import argparse
from configuration.reader import read_config
import os
from queuer_functions import *
import logging

parser = argparse.ArgumentParser(description='Process')
parser.add_argument('--config', help='file_name',default='default.cfg')
parser.add_argument('--script', help='sh file name',default='run')
parser.add_argument('--append', help='append',default='N')

args, leftovers = parser.parse_known_args()
file_name = args.config
script = args.script
if not file_name.startswith('configs/'):
    file_name = os.path.join('configs',file_name)
logging.info(file_name)
logging.info('Running {}.sh'.format(script))

config = read_config(file_name)
queue(config,file_name,script)
