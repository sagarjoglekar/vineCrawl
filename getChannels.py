#Get Channels data to allow training datasets
#categories look something like this : 
#            'comedy'                => 1,
#            'art-and-experimental'  => 2,
#            'nature'                => 5,
#            'family'                => 7,
#            'special-fx'            => 8,
#            'sports'                => 9,
#            'food'                  => 10,
#            'music'                 => 11,
#            'beauty-and-fashion'    => 12,
#            'health-and-fitness'    => 13,
#            'news-and-politics'     => 14,
#            'animals'               => 17

from multiprocessing import Pool
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

visitedList = "visited.data"
root ="Channels/"
timeline = "userTimeline"
postData = "postData"

def now_time():
	now=dt.datetime.now()
	return int(time.mktime(now.timetuple()))

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

def getSocialData(popular , timeline , posts):
		records = popular['data']['records']
		for i in range (0 , len(records)):
			print "Getting Post data..."
			#get Post data
			postID = records[i]['postId']
			postData = requests.get("https://api.vineapp.com/timelines/posts/"+str(postID))
			post = open( posts + "/" + str(postID) + '.json', 'w')
			json.dump(postData.json(), post)

			#get USer Timeline
			print "Getting User data..."
			userId = records[i]['userId']
			userData = requests.get("https://api.vineapp.com/timelines/users/"+str(userId)+"?size=50");
			user = open( timeline + "/" + str(userId) + '.json', 'w')
			json.dump(userData.json(), user)





if __name__ == '__main__':
	dirs,files = walkLevel1Dir(root)
	visited = getVisited()
	
	for dir in dirs:
		if dir not in visited:
			timeline = root + dir + "/" + timeline
			posts = root + dir + "/" + postData

			if not os.path.exists(posts):
				os.makedirs(posts)
			if not os.path.exists(timeline):
				os.makedirs(timeline)
			
			dataRoot = root + dir
			popular = getPopularFile(dataRoot)

			getSocialData(popular , timeline , posts)

			visited.append(dir)
			updateVisited(visited)
			print dir
			break


			
			






