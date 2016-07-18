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


visitedList = "../Logs/sampledVids.data"
root = "../vinedata/Data/"
faceStoreRoot = "../vinedata"
#root = "../Data/"
faces = "sampledFrames"

frameRate = 24

selected = "sampledVines.pkl"
loopThreshold = 0
sampledLog = "../Logs/sampledFrames.pk"


def sampleVideo(videoPath , facesPath , postID):
    cap = cv2.VideoCapture(videoPath)
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

def getVisited():
    visited = []
    try:
        f = open(visitedList, 'rb')
        visited = pickle.load(f)
    except IOError:
        f = open(visitedList,"a+")
        pickle.dump([],f)
    return visited


def updateVisited(visited):
    with open(visitedList, 'wb') as f:
        pickle.dump(visited, f)


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


def getPopularFile(rootDir):
    f = open(rootDir + '/popular.json' ,'r')
    data = json.load(f)
    return data

    
    
def getPopularPosts(popular):
    records = popular['data']['records']
    posts=[]
    for i in range (0 , len(records)):
        postID = records[i]['postId']
        loopCount = records[i]['loops']['count']
        if(loopCount > loopThreshold):
            posts.append(postID)
    return posts



def getVideoPaths(popular):
    records = popular['data']['records']
    vidPaths=[]
    postIds=[]
    for i in range (0 , len(records)):
        postID = records[i]['postId']
        postURL = records[i]['videoDashUrl']
        if(postURL != None):
            vidURL = postURL.split('//')
            URLPaths = vidURL[1].split('?')
            vidPath = URLPaths[0]
            vidPaths.append(vidPath)
            postIds.append(postID)                            
    return vidPaths, postIds


#MAin Loop: Runs only once and is reculated using Cron jobs
if __name__ == '__main__':
    dirs,files = walkLevel1Dir(root)
    visited = getVisited()
    
    for d in dirs:
        if d not in visited:
            faceDir = faceStoreRoot + "/" + faces
            
            if not os.path.exists(faceDir):
                os.makedirs(faceDir)
            
            dataRoot = root + d
            popular = getPopularFile(dataRoot)
            selectedPosts = getPopularPosts(popular)

            paths, posts = getVideoPaths(popular)
            for i in range(len(posts)):
                if posts[i] in selectedPosts:
                    videoPath = root + d + "/videos/" + paths[i]
                    if os.path.exists(videoPath):
                        print "Sampling Post ID %d with url %s"% (posts[i], paths[i])
                        sampleVideo(videoPath , faceDir , posts[i])

            visited.append(d)
            updateVisited(visited)
            break