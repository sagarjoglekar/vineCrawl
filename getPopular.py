#Class that starts everything

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
import os.path
import wget

def now_time():
   		now=dt.datetime.now()
   		return int(time.mktime(now.timetuple()))

class vineCrawler(Exception):
	def __init__(self, procPool):
		self._name = "Vine Crawler"
		self._popular = None
		self._procPool = procPool

   	def getPopular(self, rootDir):
		self._popular = requests.get("https://api.vineapp.com/timelines/popular")
		f = open(rootDir + '/popular' + '.json', 'w')
		json.dump(self._popular.json(), f)
		return self._popular.json()


class parsePopular(Exception):
	def __init__(self, procPool ):
		self._name = "Parse Popular"
		self._procPool = procPool

	def callCmd(self,args):
		call(args)

	def decomposePopular(self,popular,rootDir):
		
		profileDir = rootDir + '/profile'
		videoDir = rootDir + '/videos'
		pageDir = rootDir + '/pages'
		data = popular['data']
		records = data['records']
		#empty list to cache proc ids of everthing being done here
		procRegister = [];


		for i in range (0 , len(records)):
			subRecord = records[i]
			print subRecord
			
			argsProfile = ['wget', '-r', '-l', '1', '-p', '-P', profileDir, subRecord['avatarUrl']]
			#procRegister.append(Popen(argsProfile))
			self.callCmd(argsProfile);

			videoUrl = subRecord['videoDashUrl'].split('?');
			argsVideo = ['wget', '-r', '-l', '1', '-p', '-P' , videoDir, videoUrl[0]]
			#procRegister.append(Popen(argsVideo))
			self.callCmd(argsVideo);

		#	argsPage = ['wget', '-r', '-l', '1', '-p', '-P', self._profileDir, subRecord['permalinkUrl']]
		#	procRegister.append(Popen(argsPage))

		print "Created " + str(len(procRegister)) + 'processes'

		return procRegister

			
			

