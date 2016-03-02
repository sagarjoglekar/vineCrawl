import numpy
import timeit
import theano
import theano.tensor as T
import os
import pickle
try:
    import PIL.Image as Image
except ImportError:
    import Image
    
from theano.tensor.shared_randomstreams import RandomStreams

import sys
sys.path.append("../lib")
from load import mnist
from load import faces
from load import getValData
from utils import tile_raster_images
from rbm import RBM
from dbn import DBN
from IPython.display import Image, display
from matplotlib.pyplot import imshow
import matplotlib.cm as cm
import dlib

currentDir =  os.getcwd();
parampickle = currentDir + "/../Logs/parametersDBNV1.pickle"
logPickle = currentDir + "/../Logs/errorPickleDBNV1.pickle"

TrX, teX, TrY, teY  = faces(onehot=False)
#valX , valY = getValData()
trX = TrX[:25000]
valX =TrX[25000:]
trY = TrY[:25000]
valY = TrY[25000:]

train_set_x = theano.shared(numpy.asarray(trX, dtype=theano.config.floatX),borrow=True)
test_set_x = theano.shared(numpy.asarray(teX, dtype=theano.config.floatX),borrow=True)
train_set_y = theano.shared(numpy.asarray(trY, dtype="int32"),borrow=True)
test_set_y = theano.shared(numpy.asarray(teY, dtype="int32"),borrow=True)

val_set_x = theano.shared(numpy.asarray(valX, dtype=theano.config.floatX),borrow=True)
val_set_y = theano.shared(numpy.asarray(valY, dtype="int32"),borrow=True)


datasets = [(train_set_x, train_set_y), (val_set_x, val_set_y),(test_set_x, test_set_y)]

finetune_lr=0.001 
pretraining_epochs=500
pretrain_lr=0.05
k=15 
training_epochs=1000
batch_size=14

# compute number of minibatches for training, validation and testing
n_train_batches = train_set_x.get_value(borrow=True).shape[0] / batch_size

# numpy random generator
numpy_rng = numpy.random.RandomState(23455)
print '... building the model'
logline = "... building the model"
f2 = open(logPickle, 'a+')
pickle.dump(logline , f2);
f2.close()

# construct the Deep Belief Network
dbn = DBN(numpy_rng=numpy_rng, theano_rng=None, n_ins=48 * 48, hidden_layers_sizes=[500, 500 , 500 , 500], n_outs=7)

# start-snippet-2
#########################
# PRETRAINING THE MODEL #

#########################
print '... getting the pretraining functions'
logline = "... getting the pretraining functions"
f2 = open(logPickle, 'a+')
pickle.dump(logline , f2);
f2.close()
pretraining_fns = dbn.pretraining_functions(train_set_x=train_set_x,
                                                batch_size=batch_size,
                                                k=k)

print '... pre-training the model'
logline = "... pre-training the model"
f2 = open(logPickle, 'a+')
pickle.dump(logline , f2);
f2.close()
    
start_time = timeit.default_timer()
## Pre-train layer-wise
for i in xrange(dbn.n_layers):
    # go through pretraining epochs
    for epoch in xrange(pretraining_epochs):
        # go through the training set
        c = []
        for batch_index in xrange(n_train_batches):
            c.append(pretraining_fns[i](index=batch_index,
                                            lr=pretrain_lr))
        print 'Pre-training layer %i, epoch %d, cost ' % (i, epoch),
        print numpy.mean(c)
            
        logline = "Pre-training layer: " + str(i) +"epoch: " + str(epoch) + "mean: " + str(numpy.mean(c))
        f2 = open(logPickle, 'a+')
        pickle.dump(logline , f2);
        f2.close()

end_time = timeit.default_timer()

print '... Finished pre-training in :' + str((end_time-start_time)/60) + "min"
logline = '... Finished pre-training in :' + str((end_time-start_time)/60) + "min"
f2 = open(logPickle, 'a+')
pickle.dump(logline , f2);
f2.close()
    
    
 


