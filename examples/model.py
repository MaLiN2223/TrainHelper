import keras
from keras.datasets import cifar100
from keras.layers import *
from keras.models import Model
from src.runners import Runner
from src.functions import load_config, download_splitted_dataset, load_data

def get_model():

    x = input = Input((32, 32, 3))
    x = Dense(12, input_dim=8, activation='relu')(x)
    x = Dense(8, activation='relu')(x)
    x = Dense(10, activation='sigmoid')(x)

    model = Model(input, x)
    model.compile(optimizer=keras.optimizers.RMSprop(lr=0.0003, rho=0.9, epsilon=None, decay=0.0),
                  metrics=['binary_accuracy', 'accuracy'],
                  loss='mean_squared_error')
    model.summary()
    return model


download_splitted_dataset(cifar100.load_data, 0.1)

config, config_name = load_config()
runner = Runner(get_model, load_data)
runner.run(config)
