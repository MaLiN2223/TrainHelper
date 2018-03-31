import numpy as np
import tensorflow as tf
import random as rn
import logging
import os
os.environ['PYTHONHASHSEED'] = '0'

np.random.seed(42)

rn.seed(12345)

session_conf = tf.ConfigProto(intra_op_parallelism_threads=1, inter_op_parallelism_threads=1)

import keras
#from sklearn.model_selection import train_test_split
from keras import backend as k
from keras.applications import ResNet50
from keras.applications import InceptionV3
from keras.applications import Xception # TensorFlow ONLY
from keras.applications import VGG16
from keras.applications import VGG19
from keras.regularizers import l2,l1
from keras.callbacks import ModelCheckpoint, TensorBoard, EarlyStopping,CSVLogger
from keras.datasets import cifar10, cifar100
from sklearn.model_selection import train_test_split
#import cv2
tf.set_random_seed(1234)

sess = tf.Session(graph=tf.get_default_graph(), config=session_conf)
k.set_session(sess)


import argparse
import os

from src.configuration import read_config
validation_data_dir = 'images-valid'
train_data_dir = 'images'
num_classes = 10
MODELS = {
	"vgg16": VGG16,
	"vgg19": VGG19,
	"inception": InceptionV3,
	"xception": Xception,
	"resnet": ResNet50
}
REGULARIZERS = {
	'l1': l1,
	'l2': l2
}

def get_regularizer(reg):
	if reg not in REGULARIZERS:
		return None
	return REGULARIZERS[reg](0.01)

def get_parameters():
	print('PARSING ARGUMENTS')
	parser = argparse.ArgumentParser(description='Inputs')
	parser.add_argument('--name', help='file_name')
	parser.add_argument('--append', help='file_name', default='N')
	args, leftovers = parser.parse_known_args()
	config_name = args.name
	config = read_config(config_name)
	append = True if args.append == 'Y' else False
	config.append = append
	log_file = 'logs/{}.log'.format(config['name'])
	if not append:
		with open(log_file, 'w'):
			pass

	logging.basicConfig(filename=log_file,level=logging.DEBUG)
	logging.info('Working in mode {}'.format(append))
	logging.info(config.config)

	return config, config_name

def download_dataset():
	print('Downloading dataset')
	(x_train, y_train), (x_test, y_test) = cifar10.load_data()
	x_valid, x_test, y_valid, y_test = train_test_split(x_test,y_test,test_size = .5, random_state=1)
	print('Saving x_train')
	np.save('x_train',x_train)
	print('Saving x_valid')
	np.save('x_valid',x_valid)
	print('Saving x_test')
	np.save('x_test',x_test)

	print('Saving y_train')
	np.save('y_train',y_train)
	print('Saving y_valid')
	np.save('y_valid',y_valid)
	print('Saving y_test')
	np.save('y_test',y_test)

def download_cifar_100():
	print('Downloading dataset')
	(x_train, y_train), (x_valid, y_valid) = cifar100.load_data()
	#x_valid, x_test, y_valid, y_test = train_test_split(x_test,y_test,test_size = .5, random_state=1)

	print('Saving cifar100_x_train')
	np.save('cifar100_x_train',x_train)

	print('Saving x_valid')
	np.save('cifar100_x_valid',x_valid)

	print('Saving cifar100_y_train')
	np.save('cifar100_y_train',y_train)

	print('Saving cifar100_y_valid')
	np.save('cifar100_y_valid',y_valid)

def load_cifar_100_data():
	up ='../'
	ex = '.npy'
	print('loading x_train')
	x_train = np.load('{}cifar100_x_train{}'.format(up,ex))
	print('loading x_valid')
	x_valid = np.load('{}cifar100_x_valid{}'.format(up,ex))

	print('loading y_train')
	y_train = np.load('{}cifar100_y_train{}'.format(up,ex))
	print(y_train.shape)
	print('loading y_valid')
	y_valid = np.load('{}cifar100_y_valid{}'.format(up,ex))

	return (x_train,y_train), (x_valid,y_valid)

def load_data():
	up ='../'
	ex = '.npy'
	print('loading x_train')
	x_train = np.load('{}x_train{}'.format(up,ex))
	print('loading x_valid')
	x_valid = np.load('{}x_valid{}'.format(up,ex))
	print('loading x_test')
	x_test = np.load('{}x_test{}'.format(up,ex))

	print('loading y_train')
	y_train = np.load('{}y_train{}'.format(up,ex))
	print('loading y_valid')
	y_valid = np.load('{}y_valid{}'.format(up,ex))
	print('loading y_test')
	y_test = np.load('{}y_test{}'.format(up,ex))

	return (x_train,y_train), (x_valid,y_valid), (x_test, y_test)

def load_data2():
	up ='../'
	ex = '.npy'
	print('loading x_train')
	x_train = np.load('{}x_train{}'.format(up,ex))
	print('loading x_valid')
	x_valid = np.load('{}x_valid{}'.format(up,ex))

	print('loading y_train')
	y_train = np.load('{}y_train{}'.format(up,ex))
	print('loading y_valid')
	y_valid = np.load('{}y_valid{}'.format(up,ex))

	return (x_train,y_train), (x_valid,y_valid)

def load_c10_labels():
	up ='../'
	ex = '.npy'
	print('loading x_train')
	x_train = np.load('{}x_train{}'.format(up,ex)) / 255
	print('loading x_valid')
	x_valid = np.load('{}x_valid{}'.format(up,ex)) / 255

	print('loading y_train')
	y_train = np.load('{}y_train{}'.format(up,ex))
	print('loading y_valid')
	y_valid = np.load('{}y_valid{}'.format(up,ex))

	y_train = keras.utils.to_categorical(y_train, num_classes=10)
	y_valid = keras.utils.to_categorical(y_valid, num_classes=10)
	return (x_train,y_train), (x_valid,y_valid)

def get_loggers(config, monitor='val_acc'):

	from src.repeater import Repeater
	early_stop = config['early_stop']
	if early_stop is None:
		early_stop = 10

	base_name = config.results_dir+'/'+config.name
	base = keras.callbacks.BaseLogger()
	checkpoint = ModelCheckpoint(base_name+'_best.h5', monitor=monitor, verbose=1, save_best_only=True, save_weights_only=False, mode='auto', period=1)
	checkpoint2 = ModelCheckpoint(base_name+'.h5', monitor=monitor, verbose=1, save_weights_only=True, mode='auto', period=1)

	repeater = Repeater()
	if early_stop is not False:
		print('Doing early stoping with {}'.format(early_stop))
		early = EarlyStopping(monitor='val_acc', min_delta=0, patience=early_stop, verbose=1, mode='auto')
	board = TensorBoard(log_dir=base_name, histogram_freq=0, batch_size=config.batch_size, write_graph=True, write_grads=False, write_images=False, embeddings_freq=0, embeddings_layer_names=None, embeddings_metadata=None)
	csv = CSVLogger(base_name+'.log')
	return [base,checkpoint,checkpoint2,early,board,csv,repeater]

def create_dir(name):
	if not os.path.exists(name):
		os.makedirs(name)

def preprocess_images(to_size):
	print('PREPROCESSING IMAGES')
	(x_train, y_train), (x_test, y_test) = cifar10.load_data()
	#x_test = x_test[:5000]
	#y_test = y_test[:5000]
	print('x_train shape:', x_train.shape)
	print(x_train.shape[0], 'train samples')
	print(x_test.shape[0], 'test samples')

	# Convert class vectors to binary class matrices.
	y_train = keras.utils.to_categorical(y_train, 10)
	y_test = keras.utils.to_categorical(y_test, 10)

	create_dir(train_data_dir)
	create_dir(validation_data_dir)
	for i in range(num_classes):
		create_dir(train_data_dir+'/'+str(i))
		create_dir(validation_data_dir+'/'+str(i))
	process_set_of_images(x_train,train_data_dir,y_train,to_size)
	process_set_of_images(x_test, validation_data_dir,y_test,to_size)

def process_set_of_images(images, dir,labels,size):
	for i, img in enumerate(images):
		large_img = cv2.resize(img, dsize=size, interpolation=cv2.INTER_CUBIC)
		large_img = large_img.astype(np.uint8)
		path = dir+'/'+str(number(labels[i]))+'/'+str(i)+'.png'
		cv2.imwrite(path,large_img)

def number(array):
	for i,item in enumerate(array):
		if item !=0 :
			return i
