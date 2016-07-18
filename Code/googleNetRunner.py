import numpy as np
import matplotlib.pyplot as plt
import json
import tables
import cPickle as Pickle


# The caffe module needs to be on the Python path;
#  we'll add it here explicitly.
import sys
caffe_root = '/work/sagarj/caffe'  # this file should be run from {caffe_root}/examples (otherwise change this line)
sys.path.insert(0, caffe_root + 'python')

import caffe
# If you get "No module named _caffe", either you have not built pycaffe or you have the wrong path.


model_root = "../Models/"
image_root = "../samples/"
image_list = "../Logs/samplevinesSorted.txt"
classprobs = "../Logs/sampledvineImagenetProbs2015_1.csv"
labelFile = "../Logs/sampledvineImagenetObjs2015_1.pk"


import os

if os.path.isfile(model_root + 'bvlc_googlenet.caffemodel'):
    print 'CaffeNet found.'
else:
    print 'Downloading pre-trained CaffeNet model...'

caffe.set_mode_gpu()

model_def = model_root+'deploy.prototxt' 
model_weights = model_root + 'bvlc_googlenet.caffemodel'

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

# load the mean ImageNet image (as distributed with Caffe) for subtraction
mu = np.load(caffe_root + '/python/caffe/imagenet/ilsvrc_2012_mean.npy')
mu = mu.mean(1).mean(1)  # average over pixels to obtain the mean (BGR) pixel values
print 'mean-subtracted values:', zip('BGR', mu)

# create transformer for the input called 'data'
transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})

transformer.set_transpose('data', (2,0,1))  # move image channels to outermost dimension
transformer.set_mean('data', mu)            # subtract the dataset-mean value in each channel
transformer.set_raw_scale('data', 255)      # rescale from [0, 1] to [0, 255]
transformer.set_channel_swap('data', (2,1,0))  # swap channels from RGB to BGR

# set the size of the input (we can skip this if we're happy
#  with the default; we can also change it later, e.g., for different batch sizes)
net.blobs['data'].reshape(1,        # batch size
                          3,         # 3-channel (BGR) images
                          224, 224)  # image size is 227x227

imageList = []
with open(image_list) as g:
    imageList = g.readlines()

# load ImageNet label
labels_file = caffe_root + '/data/ilsvrc12/synset_words.txt'
labels = []
synset_words = np.loadtxt(labels_file, str, delimiter='\t')
for sets in synset_words:
    labels.append(sets.split(' ')[1])

for line in imageList:    
    path = line.split(' ')[0]
    im = caffe.io.load_image(path)
    transformed_image = transformer.preprocess('data', im)
    # copy the image data into the memory allocated for the net
    net.blobs['data'].data[...] = transformed_image
    ### perform classification
    output = net.forward()
    output_prob = output['prob'][0].reshape(1,1000)  # the output probability vector for the first image in the batch
    print output_prob.shape
    with open(classprobs,'a') as f_handle:
        np.savetxt(f_handle, np.transpose(output_prob) , delimiter=',')
    print 'predicted class is:', output_prob.argmax()
    log = path + ',label,' + labels[output_prob.argmax()]
    print log
    f = open(labelFile, 'a+')
    Pickle.dump(log , f);
    f.close()