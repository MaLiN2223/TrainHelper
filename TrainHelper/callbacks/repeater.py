from keras.callbacks import Callback
import datetime
import logging


class Repeater(Callback):
    def __init__(self, config, queuer):
        super(Callback, self).__init__()
        self.start = datetime.datetime.now()
        self.config = config
        self.queuer = queuer

    def on_train_begin(self, logs=None):
        logging.info('SETTING START TIME')
        self.start = datetime.datetime.now()
        logging.info('Start time {}'.format(self.start))

    def on_epoch_end(self, epoch, logs=None):
        now = datetime.datetime.now()
        delta = (now - self.start).seconds // 60
        time_max = self.config.Repeater.Time
        print(delta,time_max*60)
        if delta >= time_max * 60:  # time_max hrs
            logging.info('Delta is bigger than expected')
            self.queuer.queue(self.config, self.config.config_name, self.config.script, 'Y')
            self.model.stop_training = True
