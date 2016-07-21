import json
import os
import sys
from subprocess import call

viral_meta = "../Logs/viral_meta.csv"
youtube_prefix = "https://www.youtube.com/watch?v="
youtube_dir = "../Youtube_videos/"


def readYouTubeMeta():
    with open(viral_meta) as g:
        metaLines = g.readlines()
    return metaLines


def dequote(s):
    """
    If a string has single or double quotes around it, remove them.
    Make sure the pair of quotes match.
    If a matching pair of quotes is not found, return the string unchanged.
    """
    if (s[0] == s[-1]) and s.startswith(("'", '"')):
        return s[1:-1]
    return s

if __name__ == "__main__":
    
    metaLines = readYouTubeMeta()
    comedyIds = []
    comedyMeta = []
    for line in metaLines:
        if dequote(line.split(',')[3]) =='Comedy':
            comedyMeta.append(line)
            comedyIds.append(dequote(line.split(',')[0]))
    
    for Id in comedyIds:
        url = youtube_prefix + Id
        opPattern = youtube_dir +'%(id)s.mp4'
        command = ['youtube-dl', '-o' , opPattern, url]
        call(command)

    