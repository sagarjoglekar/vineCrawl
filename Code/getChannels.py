#Get Channels data to allow training datasets
#categories look something like this : 
#            'comedy'                => 1,
#            'art-and-experimental'  => 2,
#            'cats'                  => 3,
#            'dogs'                  => 4,
#            'nature'                => 5,
#            'urban'                 => 6,
#            'family'                => 7,
#            'special-fx'            => 8,
#            'sports'                => 9,
#            'food'                  => 10,
#            'music'                 => 11,
#            'beauty-and-fashion'    => 12,
#            'health-and-fitness'    => 13,
#            'news-and-politics'     => 14,
#            'weird'                 => 15,
#            'scary'                 => 16,
#            'animals'               => 17
# https://vine.co/api/timelines/channels/1/recent

from multiprocessing import Pool
from subprocess import call
import re
import datetime as dt
from datetime import datetime
import time
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

def callCmd(args):
		call(args)


if __name__ == '__main__':

	workingDir = root + str( now_time()) 
	
	os.makedirs( workingDir )

	for i in range(1,18):
		
		typeDir = workingDir + "/" + str(i)
		videoDir = typeDir + "/videos"
		avatarDir = typeDir + "/avatars"
		os.makedirs( typeDir )
		os.makedirs( videoDir )
		os.makedirs( avatarDir )
		
		channelRecent = requests.get("https://vine.co/api/timelines/channels/" + str(i) + "/recent" + "?size=100")
		f = open(typeDir + "/" + str(i) +'.json', 'w')
		channelJson = channelRecent.json()
		json.dump(channelJson, f)

		data = channelJson['data']
		records = data['records']

		for i in range (0 , len(records)):
			subRecord = records[i]
			print subRecord
			
			argsProfile = ['wget', '-r', '-nd', '-l', '1', '-p', '-P', avatarDir, subRecord['avatarUrl']]
			callCmd(argsProfile);

			videoString = subRecord['videoDashUrl']
                        if videoString:
                            videoUrl = subRecord['videoDashUrl'].split('?');
			    argsVideo = ['wget', '-r', '-nd', '-l', '1', '-p', '-P' , videoDir, videoUrl[0]]
			    callCmd(argsVideo);
		time.sleep(30)



	

			
			






