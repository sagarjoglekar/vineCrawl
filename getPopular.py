#Class that starts everything

from multiprocessing import Pool
from subprocess import Popen
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
	def __init__(self, procPool , rootDir):
		self._name = "Vine Crawler"
		self._popular = None
		self._procPool = Pool(12)
		self._root = rootDir

   	def getPopular(self):
		self._popular = requests.get("https://api.vineapp.com/timelines/popular")
		f = open(self._root + '/popular' + '.json', 'w')
		json.dump(self._popular.json(), f)
		return self._popular.json()


class parsePopular(Exception):
	def __init__(self , popular , procPool , rootDir):
		self._name = "Parse Popular"
		self._root = rootDir
		self._popular = popular
		self._procPool = procPool
		self._profileDir = self._root + '/profile'
		self._videoDir = self._root + '/videos'
		self._pageDir = self._root + '/pages'

	def decomposePopular(self):
		data = self._popular['data']
		records = data['records']
		#empty list to cache proc ids of everthing being done here
		procRegister = [];


		for i in range (0 , len(records)):
			subRecord = records[i]
			print subRecord
			
			argsProfile = ['wget', '-r', '-l', '1', '-p', '-P', self._profileDir, subRecord['avatarUrl']]
			procRegister.append(Popen(argsProfile))

			videoUrl = subRecord['videoDashUrl'].split('?');
			argsVideo = ['wget', '-r', '-l', '1', '-p', '-P' , self._videoDir, videoUrl[0]]
			procRegister.append(Popen(argsVideo))

			argsPage = ['wget', '-r', '-l', '1', '-p', '-P', self._profileDir, subRecord['permalinkUrl']]
			procRegister.append(Popen(argsPage))

		print "Created " + str(len(procRegister)) + 'processes'

		return procRegister

			
			

