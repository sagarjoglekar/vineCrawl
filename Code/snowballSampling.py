#Python script that collects top 5 popular videos of every user that ranked in top 100 and post data of his timeline
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

visitedList = "../Logs/snowballUsers.data"
root ="../Data/"
userPastVideos = "snowball/videos"
userPastVideoMeta = "snowball/postData"

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

def getJson(jsonFile):
    f = open(jsonFile ,'r')
    data = json.load(f)
    return data

# Get Top 3 liked videos
def getVideos(usrProf, userId, vid ):
    videoDir = vid + "/" + str(userId)
    print "Working on Vids:  "  + videoDir
    if not os.path.exists(videoDir):
        os.makedirs(videoDir)
    if len(usrProf) < 2:
        return
    if not isinstance(usrProf['data'],dict):
        print "JSON Data not a dict"
        return
    records = usrProf['data']['records']
    likes = []
    for record in records:
        likes.append(record['likes']['count'])
    likes.sort(reverse=True)
    
    for record in records:
        if record['likes']['count'] in likes[:3]:
            videoString = record['videoDashUrl']
            if videoString:
                videoUrl = record['videoDashUrl'].split('?');
                argsVideo = ['wget', '-r', '-l', '1', '-p', '-P' , videoDir, videoUrl[0]]
                call(argsVideo);

def getPostMeta(usrProf, userId , post ):
    postDir = post + "/" + str(userId)
    print "Working on Post:  "  + postDir
    if not os.path.exists(postDir):
        os.makedirs(postDir)
    if not isinstance(usrProf['data'],dict):
        print "JSON Data not a dict"
        return
    records = usrProf['data']['records']
 
    for subRecord in records:
        postID = subRecord['postId']
        postData = requests.get("https://api.vineapp.com/timelines/posts/"+str(postID))
        post = open( postDir + "/" + str(postID) + '.json', 'w')
        json.dump(postData.json(), post)



if __name__ == '__main__':
    dirs,files = walkLevel1Dir(root)
    visited = getVisited()
    
    for dir in dirs:
        if dir not in visited:
            
            dataRoot = root + dir
            popular = getPopularFile(dataRoot)

            getHistory(popular , dataRoot)

            visited.append(dir)
            updateVisited(visited)
            print dir
            break







