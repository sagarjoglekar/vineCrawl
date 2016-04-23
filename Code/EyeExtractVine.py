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


visitedList = "../Logs/eyesExtracted.data"
root = "../vinedata/Data/"
#root = root = "../Data/"
faces = "faces"

frontal_face_cascade = cv2.CascadeClassifier('../haarcascades/haarcascade_frontalface_default.xml')
profile_face_cascade = cv2.CascadeClassifier('../haarcascades/haarcascade_profileface.xml')

selected = "popularVines.pkl"
loopThreshold = 1
faceNumber = "../Logs/faceNumbersPass2.pk"


def process_frontal(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.waitKey(20)
    faces = []
    faces = frontal_face_cascade.detectMultiScale(gray, 1.3, 5)
    return len(faces)
    

def process_eyes(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.waitKey(20)
    eyes = []
    eyes = profile_face_cascade.detectMultiScale(gray)
    return len(eyes)

def processVideo(videoPath , facesPath , postID , pool):
    cap = cv2.VideoCapture(videoPath)
    totFrames = 0
    faceFrames = 0
    profileFrames = 0
    eyeFrames = 0
    i = 0
    while True:
        ret, frame = cap.read()
        if ret:
            procs = []
            result = {}
            totFrames += 1
            cv2.waitKey(20)
            
            faces = pool.apply_async(process_frontal, (frame,))
            eyes = pool.apply_async(process_eyes, (frame,))

            faceFrames += faces.get(timeout=1) 
            eyeFrames += eyes.get(timeout=1)
            
        else:
            logline = str(postID) + "," + str(totFrames) + "," + str(faceFrames) + "," +str(eyeFrames)
            print logline
            f = open(faceNumber, 'a+')
            cPickle.dump(logline , f);
            f.close()
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

    
    
def getPopularPosts(popular , listFile):
    records = popular['data']['records']
    posts=[]
    for i in range (0 , len(records)):
        postID = records[i]['postId']
        loopCount = records[i]['loops']['count']
        if(loopCount > loopThreshold):
            posts.append(postID)
    
    with open(listFile, 'wb') as f:
        pickle.dump(posts, f)
    return posts



def getFaces(popular , faces):
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


def getVidPaths():
    with open(vidpaths) as f:
        content = f.readlines()
    return content


#MAin Loop: Runs only once and is reculated using Cron jobs
if __name__ == '__main__':
    dirs,files = walkLevel1Dir(root)
    visited = getVisited()
    pool = mp.Pool(processes=8) 
    
    for d in dirs:
        if d not in visited:
            faceDir = root + d + "/" + faces
            selectedList = faceDir + "/" + selected

            if not os.path.exists(faceDir):
                os.makedirs(faceDir)
            
            dataRoot = root + d
            popular = getPopularFile(dataRoot)
            selectedPosts = getPopularPosts(popular , selectedList)

            paths, posts = getFaces(popular , faces)
            for i in range(len(posts)):
                if posts[i] in selectedPosts:
                    videoPath = root + d + "/videos/" + paths[i]
                    if os.path.exists(videoPath):
                        print "Processing Post ID %d with url %s"% (posts[i], paths[i])
                        processVideo(videoPath , faceDir , posts[i] , pool)

            visited.append(d)
            updateVisited(visited)
            break