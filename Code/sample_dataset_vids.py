import re
import datetime as dt
from datetime import datetime
import time
import random
import json
import sys
import requests
import os
import wget
import pickle
import cv2
import numpy as np
import cPickle
import multiprocessing as mp

root = "/datasets/sagarj/vineData/Dataset/"

videos_dir = root + "Videos/"
frame_dir = root + "fineSamples/"

sampled = "../Logs/fineSampledVines.pk"
sampledLog = "../Logs/sampledLog.txt"
mapping_file = "../Logs/postsMapping.csv"


def sampleVideo(videoPath , facesPath , postID):
    cap = cv2.VideoCapture(videoPath)
    #print videoPath
    totFrames = 0
    i = 0
    framesRead = 0
    framesSaved = 0
    frameRate = int(cap.get(cv2.cv.CV_CAP_PROP_FPS))
    frameRate /= 2
    while True:
        ret, frame = cap.read()
        if ret:
            framesRead += 1
            procs = []
            totFrames += 1
            cv2.waitKey(20)
            if totFrames%frameRate == 0:
                i = int(totFrames/frameRate)
                framesSaved +=1
                imageName = facesPath + "/" + str(postID) + "_" + str(i) + ".jpg"
                cv2.imwrite( imageName , frame)
                logline = str(postID) + "," + imageName
                #print logline
                logfile = open(sampledLog, 'a+')
                cPickle.dump(logline , logfile);
                logfile.close()
                
        else:
            print "Done processing Post: %s with %d frames Read  and %d saved at %d FPS"%(postID,framesRead,framesSaved,frameRate)
            return framesSaved

def readSampledList():
    visited = []
    try:
        f = open(sampled, 'rb')
        visited = pickle.load(f)
    except IOError:
        f = open(sampled,"a+")
        pickle.dump([],f)
    return visited

def updateSampledList(visited):
    with open(sampled, 'wb') as f:
        pickle.dump(visited, f)

if __name__ == '__main__':
    vidDict = {}
    vidList = []
    
    with open(mapping_file, 'rb') as f:
        lines = f.readlines()
    
    for line in lines:
        comp = line.split(',')
        vidDict[comp[0]] = comp[1]
        vidList.append(comp[0])

    for vid in vidList:
        visited = readSampledList()
        if vid not in visited:
            postID = vidDict[vid].split('.')[0]
            sampledNumbers = sampleVideo(videos_dir+vid ,frame_dir , postID)
            visited.append(vid)
            updateSampledList(visited)
            
    
    