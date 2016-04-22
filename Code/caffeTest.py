import numpy as np
import matplotlib.pyplot as plt
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

caffe.set_mode_cpu()

model_root = "/work/sagarj/Work/SentiBank/DeepSentiBank/"
import os
if os.path.isfile(model_root + 'caffe_sentibank_train_iter_250000'):
    print 'CaffeNet found.'
else:
    print 'Downloading pre-trained CaffeNet model...'
    

caffe.set_mode_cpu()

model_def = model_root + 'test.prototxt'
model_weights = model_root + 'caffe_sentibank_train_iter_250000'
imagenet_mean = model_root + 'imagenet_mean.binaryproto '

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)