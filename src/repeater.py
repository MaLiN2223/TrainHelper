# from src.functions import get_parameters
# from keras.callbacks import Callback
# import datetime
# print('SETTING START TIME')
# start = datetime.datetime.now()
# print('Start time {}'.format(start))
# config,file_name = get_parameters()
# from src.queuer_functions import *
# import logging
#
# class Repeater(Callback):
#     def __init__(self):
#         super(Callback, self).__init__()
#
#     def on_epoch_end(self, epoch, logs={}):
#         now = datetime.datetime.now()
#         delta = (now - start).seconds // 60
#         #if epoch >= 10:
#         #    logging.info('Repeating epoch >=10')
#         if delta >= 7*60: # 7 hrs
#             logging.info('Delta is bigger than expected')
#             queue(config,file_name,'run-autopixel','Y')
#             self.model.stop_training = True
#         if epoch == 99:
#             logging.info('Stopping at 99')
#             self.model.stop_training = True
