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


###################################################################################################
#CRAWLER HELPERS
###################################################################################################

class vineCrawlerHelper:
    count = 0
    UserRec = ""
    PostRec = ""
    def __init__(self,UserRecords, PostRecords):
        self.count = 1;
        self.UserRec = UserRecords
        self.PostRec = PostRecords
        
    def getUsers(self):
        visited = []
        try:
            f = open(self.UserRec, 'rb')
            visited = pickle.load(f)
            f.close()
        except IOError:
            f = open(self.UserRec,"a+")
            pickle.dump([],f)
            f.close()
        return visited
    
    def getPosts(self):
        visited = []
        try:
            f = open(self.PostRec, 'rb')
            visited = pickle.load(f)
            f.close()
        except IOError:
            f = open(self.PostRec,"a+")
            pickle.dump([],f)
            f.close()
        return visited

    def updateUsers(self, users):
        with open(self.UserRec, 'wb') as f:
            pickle.dump(users, f)
            
    def updatePosts(self, posts):
        with open(self.PostRec, 'wb') as f:
            pickle.dump(posts, f)

    def getJson(self, jsonFile):
        f = open(jsonFile ,'r')
        data = json.load(f)
        return data

    def getPostMeta(self, postID , postDir):
        print "Writing to : %s"% postDir
        postData = requests.get("https://api.vineapp.com/timelines/posts/"+str(postID))
        post = open( postDir + str(postID) + '.json', 'w')
        json.dump(postData.json(), post)

    def getUserData(self, userID , userDir ):
        userData = requests.get("https://api.vineapp.com/timelines/users/"+str(userID)+"?size=50");
        user = open( userDir + str(userID) + '.json', 'w')
        json.dump(userData.json(), user)

    def getVideo(self, post , videoDir):
        if not isinstance(post,dict):
            print "Fault: JSON Data not a dict"
            return
        videoString = post['videoUrl']
        if videoString:
            videoName = videoString.split('?')[0].split('/')[-1]
            videoPath = videoDir + videoName
            argsVideo = ['wget','-nd', '-O' , videoPath , videoString]
            call(argsVideo)

###################################################################################################
#UTILS
###################################################################################################
def now_time():
    now=dt.datetime.now()
    return int(time.mktime(now.timetuple()))

def callCmd(args):
    call(args)


if __name__ == "__main__":
    
    root ="/datasets/sagarj/vine2016/Dataset/"
    postData = "savedPosts/"
    userData = "Users/"
    videoData = "Videos/"
    meta = "Meta/"

    visitedPosts = root + "2016visitedPosts.pk"
    visitedUsers = root + "2016visitedUsers.pk"
    postDir = root + postData
    videoDir = root + videoData
    userDir = root + userData
    metaDir = root + meta

    runTime = str(now_time());

    for i in range(1,18):
        channelRecent = requests.get("https://vine.co/api/timelines/channels/" + str(i) + "/recent" + "?size=100")
        channelJson = channelRecent.json()

        if not isinstance(channelJson['data'],dict):
            print "Fault: JSON Data not a dict"
            break
        
        f = open(metaDir + runTime + "_" + str(i) +'.json', 'w')
        json.dump(channelJson, f)
        data = channelJson['data']
        records = data['records']
        
        vc = vineCrawlerHelper(visitedUsers , visitedPosts)
        crawledPosts = vc.getPosts()
        crawledUsers = vc.getUsers()
        for i in range (0 , len(records)):
            subRecord = records[i]
            postid = subRecord['postId']

            if postid in crawledPosts:
                break
            else:
                crawledPosts.append(postid)
                vc.getPostMeta(subRecord['postId'],postDir)
                vc.getVideo(subRecord, videoDir)

            userid = subRecord['userId']
            

            if userid not in crawledUsers:
                vc.getUserData(userid,userDir)
                crawledUsers.append(userid)

        vc.updatePosts(crawledPosts)
        vc.updateUsers(crawledUsers)
            
        time.sleep(30)

    print "Done Crawling 18 channels for new videos , Sleeping now"