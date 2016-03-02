
#Class that starts everything

from subprocess import call
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

visitedList = "../Logs/facesVisited.data"
root ="../Data/"
faces = "faces"

face_cascade = cv2.CascadeClassifier('../haarcascades/haarcascade_frontalface_default.xml')

def process_faces(frame):
        #print frame.shape
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.waitKey(20)
        face = []
        face = face_cascade.detectMultiScale(frame, 1.3, 5)
        if (len(face) > 0):
            cropped = []
            for i in range(len(face)):
                cropped.append(gray[face[i][1]:face[i][1]+face[i][3] , face[i][0]:face[i][0]+face[i][2]])
            return cropped
        else :
            return gray

def scaleSquare(image ,shape):
    resized = cv2.resize(image, shape, interpolation = cv2.INTER_AREA)
    return resized

def saveFaces(ImagePaths , faceFileName):
    faceFile = faceFileName
    faces =  []
    i = 0
    for path in ImagePaths:
        image = cv2.imread(path)
        cropped = process_faces(image)
        if len(cropped) > 0:
            for z in range(len(cropped)):
                if len(faces == 0):
                    faces = np.array(scaleSquare(cropped , (48 , 48)).flatten(), dtype=np.uint8)
                else
                    np.append(faces , scaleSquare(cropped , (48 , 48)).flatten() , axis = 0)
    np.savetxt(faceFile, faces, delimiter=",")

def process_frame(frame, storeDir):
        print frame.shape
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        cv2.waitKey(20)
        faces = []
        faces = face_cascade.detectMultiScale(gray, 1.3, 5)
        print faces
        for i in range(len(faces)) :
            
            cv2.imwrite( storeDir , frame)
        return frame

def processVideo(videoPath , facesPath , postID):
    storeDir = facesPath + "/" + postID
    if not os.path.exists(faceDir):
        os.makedirs(storeDir)
    cap = cv2.VideoCapture(videoPath)
    i = 0
    while True:
        ret, frame = cap.read()
        cv2.waitKey(20)
        imageName = storeDir + "/" + str(i) +".jpg"
        process_frame(frame, imageName)
        i += 1
    

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

def getFaces(popular , faces):
		records = popular['data']['records']
                vidPaths=[]
		for i in range (0 , len(records)):
			postID = records[i]['postId']
			postURL = records[i]['videoDashUrl']
                        print "Post ID %d with url %s"% (postID, postURL)
                        if(postURL != None):
                            vidURL = postURL.split('//')
                            URLPaths = vidURL[1].split('?')
                            vidPath = URLPaths[0]
                            vidPaths.append(vidPath)
                            
                return vidPaths





if __name__ == '__main__':
	dirs,files = walkLevel1Dir(root)
	visited = getVisited()
	
	for dir in dirs:
		if dir not in visited:
			faceDir = root + dir + "/" + faces

			if not os.path.exists(faceDir):
				os.makedirs(faceDir)
			
			dataRoot = root + dir
			popular = getPopularFile(dataRoot)

			paths = getFaces(popular , faces)
                        print paths

			visited.append(dir)
			updateVisited(visited)
			print dir
			break


			
			






