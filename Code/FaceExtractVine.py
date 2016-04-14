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


visitedList = "../Logs/facesExtracted.data"
root = "../vinedata/Data/"
faces = "faces"
face_cascade = cv2.CascadeClassifier('../haarcascades/haarcascade_frontalface_default.xml')
selected = "popularVines.pkl"
loopThreshold = 1
faceNumber = "../Logs/numbersOfficial.pk"

def scaleSquare(image ,shape):
    resized = cv2.resize(image, shape, interpolation = cv2.INTER_AREA)
    return resized


def process_frame(frame, storeDir):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    cv2.waitKey(20)
    faces = []
    cropped = []
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    if len(faces) > 0:
        for i in range(len(faces)):
            cropped.append(gray[faces[i][1]:faces[i][1]+faces[i][3] , faces[i][0]:faces[i][0]+faces[i][2]])
        print "Saving image at %s" % storeDir
        cv2.imwrite( storeDir , frame)
    return cropped

    

def processVideo(videoPath , facesPath , postID):
    storeDir = facesPath + "/" + str(postID)
    csvFaces = facesPath + "/" + str(postID) + "/" +  str(postID) + ".csv"
    if not os.path.exists(storeDir):
        os.makedirs(storeDir)
    cap = cv2.VideoCapture(videoPath)
    videoFaces =  np.zeros((1,48*48) , dtype=np.uint8 )
    totFrames = 0
    faceFrames = 0
    i = 0
    while True:
        ret, frame = cap.read()
        if ret:
            totFrames += 1
            cv2.waitKey(20)
            imageName = storeDir + "/" + str(i) +".jpg"
            cropped = process_frame(frame, imageName)
            if len(cropped) > 0:
                faceFrames += 1
                for z in range(len(cropped)):
                    temp = np.zeros((1,48*48) , dtype=np.uint8 )
                    temp[0] = scaleSquare(cropped[z] , (48 , 48)).flatten()
                    videoFaces = np.concatenate((videoFaces , temp ) , axis = 0)
                    print "Faces CSV shape : " + str(videoFaces.shape)
            i += 1
            
        else:
            print "Done processing Video Number: %d , Saving csv"% postID
            logline = str(postID) + "," + str(totFrames) + "," + str(faceFrames) + "," + str(videoFaces.shape[0])
            print logline
            f = open(faceNumber, 'a+')
            cPickle.dump(logline , f);
            f.close()
            np.savetxt(csvFaces, videoFaces, delimiter=",")
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
                        processVideo(videoPath , faceDir , posts[i])

            visited.append(d)
            updateVisited(visited)
            break