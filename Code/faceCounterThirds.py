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


root = "/datasets/sagarj/Pop2016/"

post_dir = root + "meta/"
videos_dir = root + "videos/"
frame_dir = root + "faces/"

frontal_face_cascade = cv2.CascadeClassifier('../haarcascades/haarcascade_frontalface_default.xml')
profile_face_cascade = cv2.CascadeClassifier('../haarcascades/haarcascade_profileface.xml')

faceNumber = "../Logs/Pop2016Thirds.pk"


def process_frontal(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.waitKey(20)
    faces = []
    faces = frontal_face_cascade.detectMultiScale(gray, 1.3, 5)
    return len(faces)
    

def process_profile(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.waitKey(20)
    eyes = []
    eyes = profile_face_cascade.detectMultiScale(gray)
    return len(eyes)

def processVideo(videoPath , facesPath , postID , pool):
    if not os.path.exists(videoPath):
        print "File Missing, skipping this one"
        return
    cap = cv2.VideoCapture(videoPath)
    rate = 2
    framesRead = 0
    thirdFaceNumbers = [0 , 0 ,0 , 0]
    frameRate = cap.get(cv2.cv.CV_CAP_PROP_FPS)

    if math.isnan(frameRate):
        frameRate = int(24 * rate)
    frameRate = int(frameRate*rate)
    if frameRate == 0:
        frameRate = int(24 * rate)
        
    totFrames = 0
    flaggedFrames = 0
    faces = 0
    profiles = 0
    i = 0
    while True:
        ret, frame = cap.read()
        if ret:
            framesRead +=1 
            if framesRead%frameRate == 0:
                if i < 4:
                    thirdFaceNumbers[i] = (float(flaggedFrames)/float(frameRate))
                    i+=1
                    flaggedFrames = 0
            procs = []
            totFrames += 1
            cv2.waitKey(20)
            
            f = pool.apply_async(process_frontal, (frame,))
            p = pool.apply_async(process_profile, (frame,))

            num_front= f.get(timeout=1) 
            num_profile = p.get(timeout=1)
            
            faces+= num_front
            profiles+=num_profile
            
            
            if(num_front>0 or num_profile>0):
                flaggedFrames+=1
        else:
            logline = str(postID) + "," + str(thirdFaceNumbers[0]) + "," + str(thirdFaceNumbers[1]) + "," + str(thirdFaceNumbers[2]) + ","+ str(thirdFaceNumbers[3])
            print logline
            logfile = open(faceNumber, 'a+')
            cPickle.dump(logline , logfile);
            logfile.close()
            break
    

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


#MAin Loop: Runs only once and is reculated using Cron jobs
if __name__ == '__main__':
    
    postList = getPosts(post_dir)
    mappingDict = getMappingDict(postList)
    pool = mp.Pool(processes=2) 
    
    for k in mappingDict: 
        postID = k
        print "Processing video %s" %(str(k))
        processVideo(videos_dir+mappingDict[k] ,frame_dir , postID ,pool)
    print "Done Counting faces from %d Videos" %(len(mappingDict.keys()))