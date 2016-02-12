import re
import json
import sys
import os.path
import random
import json
import sys
import requests
import os
import wget
import pickle



visitedList = "visited.data"
root ="Channels/"

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

