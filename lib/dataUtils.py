#Python script that collects top 5 popular videos of every user that ranked in top 100 and post data of his timeline
import re
import json
import sys
import os
import pickle
import shutil

posts = "../vinedata/posts.txt"
sentimentFile = "../Logs/ANP_Sentiments.txt"
revisedSentimentFile = "../Logs/revised_ANP_sentiments.csv"

def getVisited(visitedList):
    visited = []
    try:
        f = open(visitedList, 'rb')
        visited = pickle.load(f)
    except IOError:
        f = open(visitedList,"a+")
        pickle.dump([],f)
    return visited


def updateVisited(visited,visitedList):
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

def getRecords(popular):
    records = popular['data']['records']
    return records

def find(lst, val):
    return [i for i, x in enumerate(lst) if x == val]

def readSentiments():
    with open(sentimentFile) as g:
        sentiList = g.readlines()
    sentiDict = dict()
    for line in sentiList:
        arr = line.split(' ')
        ANP = arr[0]
        sentiment = float(arr[2].replace(']',''))
        sentiDict[ANP] = sentiment
    return sentiDict

def readRevisedSentiments():
    with open(revisedSentimentFile) as g:
        List = g.readlines()
    sentiList = List[1:]
    sentiDict = dict()
    for line in sentiList:
        arr = line.split(',')
        ANP = arr[0]
        sentiment = float(arr[2])
        sentiDict[ANP] = sentiment
    return sentiDict

def readLists(fileName):
    fileList = []
    infile = open(fileName, 'rb')
    while 1:
        try:
            fileList.append(pickle.load(infile))
        except (EOFError):
            break
    infile.close()
    return fileList

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
                argsVideo = ['wget', '-r', '-l', '1', '-p', '-P' ,'-nd', videoDir, videoUrl[0]]
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

def getHistory(popular , dataRoot):
    records = popular['data']['records']
    timeline = dataRoot + "/" + userPastVideos
    posts = dataRoot + "/" + userPastVideoMeta
    if not os.path.exists(timeline):
        os.makedirs(timeline)
    if not os.path.exists(posts):
        os.makedirs(posts)
    print "now in : " + dataRoot
    for record in records:
        userId = record['userId']
        profile_file = dataRoot + "/userTimeline/" + str(userId) + ".json"
        print "Working on file:  "  + profile_file
        if os.path.exists(profile_file):
            usrProf = getJson(profile_file)
            getVideos(usrProf,userId, timeline)
            getPostMeta(usrProf,userId,posts)

def getList(textFile):
    lines = []
    ids = []
    with open(textFile) as f:
        lines = f.readlines()
    for line in lines:
        parts = line.split('/')
        ids.append(parts[-1])
    unique = list(set(ids))
    print len(unique)
    ulines = []
    for i in unique:
        ulines.append(lines[ids.index(i)].strip())
    print "%d reduced to %d"%(len(lines), len(ulines)) 
    return ulines

def copyFile(src, dest):
    if not os.path.exists(src): 
        return
    try:
        shutil.copy(src, dest)
    # eg. src and dest are the same file
    except shutil.Error as e:
        print('Error: %s' % e)
    # eg. source or destination doesn't exist
    except IOError as e:
        print('Error: %s' % e.strerror)
        
def getAllPosts():
    postList = getList(posts)
    allPosts = []
    allPostNames = []
    for p in postList:
        name = p.split('/')[-1]
        allPostNames.append(name)
        postJson = postDir + name
        f = open(postJson,'r')
        data = json.load(f)
        allPosts.append(data)
    return allPosts , allPostNames