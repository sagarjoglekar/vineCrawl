import numpy as np
import os
import pandas as pd

datasets_dir = '/datasets/sagarj/MNIST'
faces_dir = '/datasets/sagarj/ImageDataSet/faces'

def one_hot(x,n):
	if type(x) == list:
		x = np.array(x)
	x = x.flatten()
	o_h = np.zeros((len(x),n))
	o_h[np.arange(len(x)),x] = 1
	return o_h

def mnist(ntrain=60000,ntest=10000,onehot=True):
	data_dir = os.path.join(datasets_dir,'mnist/')
	fd = open(os.path.join(data_dir,'train-images-idx3-ubyte'))
	loaded = np.fromfile(file=fd,dtype=np.uint8)
	trX = loaded[16:].reshape((60000,28*28)).astype(float)

	fd = open(os.path.join(data_dir,'train-labels-idx1-ubyte'))
	loaded = np.fromfile(file=fd,dtype=np.uint8)
	trY = loaded[8:].reshape((60000))

	fd = open(os.path.join(data_dir,'t10k-images-idx3-ubyte'))
	loaded = np.fromfile(file=fd,dtype=np.uint8)
	teX = loaded[16:].reshape((10000,28*28)).astype(float)

	fd = open(os.path.join(data_dir,'t10k-labels-idx1-ubyte'))
	loaded = np.fromfile(file=fd,dtype=np.uint8)
	teY = loaded[8:].reshape((10000))

	trX = trX/255.
	teX = teX/255.

	trX = trX[:ntrain]
	trY = trY[:ntrain]

	teX = teX[:ntest]
	teY = teY[:ntest]

	if onehot:
		trY = one_hot(trY, 10)
		teY = one_hot(teY, 10)
	else:
		trY = np.asarray(trY)
		teY = np.asarray(teY)

	return trX,teX,trY,teY


def faces(ntrain=28709,ntest=3589,onehot = True):
    data_dir = os.path.join(faces_dir,'fer2013/fer2013.csv')
    dataset = pd.read_csv( data_dir )
    
    trX = np.zeros((28709,48*48),dtype=np.uint8)
    trY = np.zeros((28709,7), dtype=np.int)
    for i in range(0,28709 ):
        trX[i] = np.asarray(dataset.values[i][1].split(" ") , dtype=np.uint8)
        label = dataset.values[i][0]
        trY[i][label] = 1;

    teX = np.zeros((3589,48*48),dtype=np.uint8)
    teY = np.zeros((3589,7), dtype=np.int)
    trainingBias = 28709
    for i in range(0,3589):
        teX[i] = np.asarray(dataset.values[trainingBias + i][1].split(" ") , dtype=np.uint8)
        label = dataset.values[trainingBias + i][0]
        teY[i][label] = 1; 
    
    return trX,teX,trY,teY

