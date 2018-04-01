from . import BaseRunner
from src.functions import get_loggers
import logging


class Runner(BaseRunner):
    def __init__(self, model_generator, data_generator):
        self.model_generator = model_generator
        self.data_generator = data_generator

    def run(self, config):
        epochs = config['epochs']
        batch_size = config['batch_size']
        model = self.model_generator(config)
        (X_train, Y_train), valid_data = self.data_generator()
        loggers = get_loggers(config)
        message = 'X_train size = {}, Y_train size ={}'.format(X_train.shape, Y_train.shape)
        if valid_data:
            message += 'X_valid size = {}, Y_valid size = {}'.format(valid_data[0].shape, valid_data[1].shape)
        logging.info(message)
        model.fit(
            X_train,
            Y_train,
            epochs=epochs,
            batch_size=batch_size,
            shuffle=True,
            validation_data=valid_data,
            callbacks=loggers
        )
