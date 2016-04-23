import numpy as np
import matplotlib.pyplot as plt
import json
import tables
import cPickle as Pickle

# set display defaults
plt.rcParams['figure.figsize'] = (10, 10)        # large images
plt.rcParams['image.interpolation'] = 'nearest'  # don't interpolate: show square pixels
plt.rcParams['image.cmap'] = 'gray'  # use grayscale output rather than a (potentially misleading) color heatmap


# The caffe module needs to be on the Python path;
#  we'll add it here explicitly.
import sys
caffe_root = '/work/sagarj/caffe'  # this file should be run from {caffe_root}/examples (otherwise change this line)
sys.path.insert(0, caffe_root + 'python')

import caffe
# If you get "No module named _caffe", either you have not built pycaffe or you have the wrong path.


model_root = "/work/sagarj/Work/SentiBank/DeepSentiBank/"
import os
if os.path.isfile(model_root + 'caffe_sentibank_train_iter_250000'):
    print 'CaffeNet found.'
else:
    print 'Downloading pre-trained CaffeNet model...'
    

caffe.set_mode_gpu()

model_def = model_root + 'test.prototxt'
model_weights = model_root + 'caffe_sentibank_train_iter_250000'
imagenet_mean = model_root + 'imagenet_mean.binaryproto'
classes = model_root + 'classes.json'
imageListFile = model_root + 'test.txt'
classprobs = "../Logs/selfieSentibankProbs.csv"
labelFile = "../Logs/selfieSentibankANPS.pk"

imageList = []
with open(imageListFile) as g:
    imageList = g.readlines()

f = open(classes ,'r')
sentibankClasses = json.load(f)
f.close()
print len(sentibankClasses)

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape})
transformer.set_transpose('data', (2,0,1))
transformer.set_channel_swap('data', (2,1,0))
transformer.set_raw_scale('data', 255.0)

net.blobs['data'].reshape(1,3,227,227)

for line in imageList:
    
    path = line.split(' ')[0]
    im = caffe.io.load_image(path)
    net.blobs['data'].data[...] = transformer.preprocess('data', im)
    net.forward()
    out = net.blobs['prob']
    with open(classprobs,'a') as f_handle:
        np.savetxt(f_handle, out.data , delimiter=',')
    
    label = sentibankClasses[out.data.argmax()]
    
    f = open(labelFile, 'a+')
    Pickle.dump(label , f);
    f.close()
    
    print label