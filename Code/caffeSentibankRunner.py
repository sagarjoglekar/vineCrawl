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


#model_root = "/work/sagarj/Work/SentiBank/DeepSentiBank/"
model_root = "/work/sagarj/Work/SentiBank/english/"
imageRoot = "/work/sagarj/Work/vineCrawl/Logs/"
import os
if os.path.isfile(model_root + 'english_lr10_iter_210000.caffemodel'): #'caffe_sentibank_train_iter_250000'):
    print 'CaffeNet found.'
else:
    print 'Cannot find model'
    exit(1)
    

caffe.set_mode_gpu()

model_def = model_root + 'english_lr10_iter_210000.prototxt'#'test.prototxt'
model_weights = model_root + 'english_lr10_iter_210000.caffemodel'#'caffe_sentibank_train_iter_250000'
imagenet_mean = model_root + 'imagenet_mean.binaryproto'
#classes = model_root + 'classes.json'
classes = model_root + 'english_label.txt'

# imageListFile = imageRoot + 'sampled_sentibank_labelled.txt'
# classprobs = "../Logs/sentibank_baseline_final.csv"
# labelFile = "../Logs/sentibank_baseline_ANPS_final.pk"

imageListFile = imageRoot + 'sampleInsta6000.txt'
classprobs = "../Logs/insta6000_probs.csv"
labelFile = "../Logs/insta6000_ANPs.pk"

imageList = []
with open(imageListFile) as g:
    imageList = g.readlines()

#JSON CLASSES 
# f = open(classes ,'r')
# sentibankClasses = json.load(f)
# f.close()

#Text classes for MVSO
f = open(classes ,'r')
sentibankClasses = f.readlines()
f.close()

print "Running Sentibank for %d Classes"%(len(sentibankClasses))

net = caffe.Net(model_def,      # defines the structure of the model
                model_weights,  # contains the trained weights
                caffe.TEST)     # use test mode (e.g., don't perform dropout)

transformer = caffe.io.Transformer({'data': net.blobs['data'].data.shape}) 
transformer.set_transpose('data', (2,0,1))
transformer.set_channel_swap('data', (2,1,0))
transformer.set_raw_scale('data', 255.0)

net.blobs['data'].reshape(1,3,227,227)
matched = 0
for line in imageList:
    
    path = line.split(' ')[0]
    #true_label = path.split('/')[5]
    im = caffe.io.load_image(path)
    net.blobs['data'].data[...] = transformer.preprocess('data', im)
    net.forward()
    out = net.blobs['prob'].data
    with open(classprobs,'a') as f_handle:
        np.savetxt(f_handle, out , delimiter=',')
    log = path   
    # get Top 5 labels
    values = out
    for i in range(5):
        index = values.argmax()
        label = sentibankClasses[index]
#         if str(label) == str(true_label):
#             print "Matched!!!"
#             matched+=1
        value = values.max()
        log = log + "," + label.strip() + "," + str(value)
        values[0][index] = 0.0
    
    print log    
    
    f = open(labelFile, 'a+')
    Pickle.dump(log , f);
    f.close()
print "Total matched labels : %d"%(matched)
