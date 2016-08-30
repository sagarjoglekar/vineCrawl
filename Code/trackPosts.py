import json
import os
from datetime import datetime
import requests

recentRoot = "/datasets/sagarj/vine2016/Dataset/"
postDir = "savedPosts/"
trackingDir = "postTracking/"

def readJson(path):
    f = open(path)
    data = json.loads(f.read())
    return data

def getCrawled():
    crawledDir = recentRoot + postDir
    crawledPosts = os.listdir(crawledDir)
    posts = []
    for post in crawledPosts:
        record = readJson(crawledDir + post)
        p = record['data']
        if isinstance(p,dict):
            posts.append(p['records'][0])
    return posts

def createDestination(base):
    today = datetime.now()
    daysSince = (today - base).days
    dirname = "Day"+str(daysSince)
    print "Creating destination directory : %s"%dirname
    destDirectory = recentRoot + trackingDir + dirname
    if not os.path.exists(destDirectory):
        os.makedirs(destDirectory)
    return destDirectory

def findTrackingPosts(postList, base):
    trackingList = []
    for vine in postList:
        timestamp = (datetime.strptime(vine['created'], '%Y-%m-%dT%H:%M:%S.%f'))
        daysSince = (timestamp - base).days
        if daysSince > 2:
            trackingList.append(vine['postId'])
    return trackingList

def getPostMeta( postID , postDir):
    print "Writing to : %s"% postDir
    postData = requests.get("https://api.vineapp.com/timelines/posts/"+str(postID))
    post = open( postDir + "/" + str(postID) + '.json', 'w')
    json.dump(postData.json(), post)

if __name__ == "__main__":
    
    #Time when the first post was crawled
    base = datetime.strptime("2016-08-16T13:03:34.00000" , '%Y-%m-%dT%H:%M:%S.%f')
    
    recentList = getCrawled()
    trackingPosts = findTrackingPosts(recentList , base)
    print "Found %d Posts older than a week, Scraping"%len(trackingPosts)
    
    destinationDir = createDestination(base)
    for post in trackingPosts:
        getPostMeta(post , destinationDir)
    