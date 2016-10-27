#####SIMPLE UTILITY TO SAMPLE .Wav files from videos in a folder #####################

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
import subprocess


root = "/datasets/sagarj/vineData/Dataset/"

post_dir = root + "savedPosts/"
videos_dir = root + "Videos/"
audio_dir = root + "Audio/"


def sampleAudio(videoPath , AudioPath , postID ):
    destPath = AudioPath + str(postID)
    command1 = "ffmpeg -i "+ videoPath + " -ab 160k -ac 2 -ar 44100 -vn " + destPath + ".wav"
    command2 = "ffmpeg -i "+ videoPath + " " + destPath + ".mp3"
    ret1 = subprocess.call(command1, shell=True)
    #ret2 = subprocess.call(command2, shell=True)
    ret2 = 1
    if ret1 != 0:
        print ".WAV extraction failed for post %s"%str(postID)
    elif ret2 != 0:
        print ".mp3 extraction failed for post %s"%str(postID)
    else:
        print "Success in extracting audio for post %s"%str(postID)
    return
    

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

if __name__ == '__main__':
    
    postList = getPosts(post_dir)
    mappingDict = getMappingDict(postList)
    
    for k in mappingDict: 
        postID = k
        sampleAudio(videos_dir+mappingDict[k] ,audio_dir , postID)