from .base_runner import BaseRunner
import logging
from ..utils.utils import ensure_dir_exists

class Runner(BaseRunner):
    def __init__(self, model_generator, data_generator):
        super().__init__()
        self.model_generator = model_generator
        self.data_generator = data_generator

    def run(self, config):
        epochs = config.Training.Epochs
        batch_size = config.Training.BatchSize
        model = self.model_generator(config)
        (X_train, Y_train), valid_data = self.data_generator()
        if config.General.ResultsDir:
            ensure_dir_exists(config.General.ResultsDir)
        if config.EarlyStopping or config.ModelCheckpoint:
            from ..keras_utils.keras_functions import get_keras_callbacks
            callbacks = get_keras_callbacks(config)
        else:
            callbacks = None
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
            callbacks=callbacks
        )
