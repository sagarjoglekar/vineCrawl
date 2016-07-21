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


visitedList = "../Logs/sampledVirals.data"
root = "../Youtube_videos/"
faceStoreRoot = "../Youtube_videos"
#root = "../Data/"
faces = "sampledFrames"

frameRate = 24

selected = "sampledVirals.pkl"
loopThreshold = 0
sampledLog = "../Logs/sampledVirals.pk"


def sampleVideo(videoPath , facesPath , postID):
    cap = cv2.VideoCapture(videoPath)
    frameRate = cv.GetCaptureProperty(cap, CV_CAP_PROP_FPS)
    totFrames = 0
    i = 0
    while True:
        ret, frame = cap.read()
        if ret:
            procs = []
            totFrames += 1
            cv2.waitKey(20)
            if totFrames%frameRate == 0:
                i = totFrames/frameRate
                imageName = facesPath + "/" + str(postID)+"_"+str(i) +".jpg"
                cv2.imwrite( imageName , frame)
                logline = str(postID) + "," + imageName
                print logline
                logfile = open(sampledLog, 'a+')
                cPickle.dump(logline , logfile);
                logfile.close()
                
        else:
            print "Done processing Post: %d" %postID
            break
            
            
            
            
def walkLevel1Dir(root):
    count = 0
    dirList = []
    filesList = []
    for path, dirs, files in os.walk(root):
        if count > 0:
            return dirList , fileList
        dirList = dirs
        fileList = files
        count = count + 1



#MAin Loop: Runs only once and is reculated using Cron jobs
if __name__ == '__main__':
    dirs,files = walkLevel1Dir(root)
    print files
    