#####SIMPLE UTILITY TO SAMPLE A LIST OF VIDEOS AT THEIR FRAM RATES INTO A KNOWN FOLDER #####################

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
import math

root = "/datasets/sagarj/UnPopular2016/"

post_dir = root + "Posts/"
videos_dir = root + "Videos/"
frame_dir = root + "AesthicSamples/"

sampledLog = "../Logs/unPopularSamplingLog.txt"


def sampleVideo(videoPath , facesPath , postID):
    cap = cv2.VideoCapture(videoPath)
    #print videoPath
    totFrames = 0
    i = 0
    framesRead = 0
    framesSaved = 0
    frameRate = cap.get(cv2.cv.CV_CAP_PROP_FPS)
    if math.isnan(frameRate):
        frameRate = 24
    else:
        frameRate = int(frameRate)
    
    frameRate = frameRate * 3
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

def readJson(path):
    f = open(path)
    data = json.loads(f.read())
    return data

def getPosts(postsDir):
    crawledPosts = os.listdir(postsDir)
    posts = []
    for post in crawledPosts:
        record = readJson(postsDir + post)
        p = record['data']
        if isinstance(p,dict):
            posts.append(p['records'][0])
    return posts

def getMappingDict(postList):
    mapping = dict()
    for p in postList:
        postId = p['postId']
        vidName = p['videoUrl'].split('/')[5].split('?')[0]
        mapping[postId] = vidName
    return mapping

if __name__ == '__main__':
    
    postList = getPosts(post_dir)
    mappingDict = getMappingDict(postList)
    
    for k in mappingDict: 
        postID = k
        sampledNumbers = sampleVideo(videos_dir+mappingDict[k] ,frame_dir , postID)