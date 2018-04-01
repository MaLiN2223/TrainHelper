from src.functions import load_config
from src.queuers.console_queuer import ConsoleQueuer

config, config_name = load_config()
queuer = ConsoleQueuer(config)
queuer.queue()
