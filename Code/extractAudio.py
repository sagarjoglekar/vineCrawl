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


root = "/datasets/sagarj/instaSample6000/"
AudioDest = root + "audio/"
videoDir = root + "videos/"


def sampleAudio(videoPath , AudioPath , postID ):
    destPath = AudioPath + str(postID)
    command1 = "ffmpeg -i "+ videoPath + " -ab 160k -ac 2 -ar 44100 -vn " + destPath + ".wav"
    #command2 = "ffmpeg -i "+ videoPath + " " + destPath + ".mp3"
    ret1 = subprocess.call(command1, shell=True)
    #ret2 = subprocess.call(command2, shell=True)
    ret2 = 0
    if ret1 != 0:
        print ".WAV extraction failed for post %s"%str(postID)
    elif ret2 != 0:
        print ".mp3 extraction failed for post %s"%str(postID)
    else:
        print "Success in extracting audio for post %s"%str(postID)
    return
    

def getVideos(postsDir):
    crawledPosts = os.listdir(postsDir)
    posts = []
    for post in crawledPosts:
        extension = post[-3:]
        if extension == "mp4":
            posts.append(post)
    return posts

if __name__ == '__main__':
    
    postList = getVideos(videoDir)
    print postList
#     mappingDict = getMappingDict(postList)
    
    for k in postList: 
        videoName = videoDir+k
        postID = k.split('.')[0]
        sampleAudio( videoName ,AudioDest , postID)