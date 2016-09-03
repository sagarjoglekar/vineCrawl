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

root = "/datasets/sagarj/vine2016/Dataset/"
post_dir = root + "savedPosts/"
userProfile_Dir = root + "UserProfiles/"


def getUserProfile(userID, profileDir):
    userData = requests.get("https://api.vineapp.com/users/profiles/"+str(userID));
    user = open( profileDir + str(userID) + '.json', 'w')
    json.dump(userData.json(), user)
    print "Downloaded User %s to %s Directory"%(str(userID) , profileDir)
    
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

def getUniqueUsers(postList):
    userList = []
    for p in postList:
        userId = p['userId']
        if userId not in userList:
            userList.append(userId)
    return userList

if __name__ == '__main__':
    
    postList = getPosts(post_dir)
    users = getUniqueUsers(postList)
    print users
    print len(users)    
    for u in users: 
        getUserProfile(u , userProfile_Dir)