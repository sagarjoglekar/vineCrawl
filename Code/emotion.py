

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

visitedList = "facesVisited.data"
root ="../Data/"
faces = "faces"
scores = "scores"
selected = "selected.datas"
loopThreshold = 150000

face_cascade = cv2.CascadeClassifier('../haarcascades/haarcascade_frontalface_default.xml')


def process_frame(frame, storeDir):
	print frame.shape
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
	cv2.waitKey(20)
	faces = []
	faces = face_cascade.detectMultiScale(frame, 1.3, 5)
	print faces
	if faces :
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





if __name__ == '__main__':
	dirs,files = walkLevel1Dir(root)
	visited = getVisited()
	
	for dir in dirs:
		if dir in visited:
			faceDir = root + dir + "/" + faces
			scoreDir = faceDir + "/" + scores
			selectedList = faceDir + "/" + selected
			if not os.path.exists(faceDir):
				break
			if not os.path.exists(scoreDir):
				print "Not doing what i am doing"
				os.makedirs(scoreDir)
			else:
				continue
			
			dataRoot = root + dir
			popular = getPopularFile(dataRoot)
			posts = getPopularPosts(popular , selectedList)
			print posts
			break

			
			






