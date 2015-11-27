#Class that starts everything

from multiprocessing import Pool
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
		self._procPool = Pool(12)

   	def getPopular(self):
		self._popular = requests.get("https://api.vineapp.com/timelines/popular")
		return self._popular

	def collectJSON(self,jsonObject):
		with open('popular_' + str(self.now_time()) + '.json', 'w') as outfile:
			json.dump(jsonObject.json(),outfile)
			print jsonObject.json()

class parsePopular(Exception):
	def __init__(self , popular , procPool):
		self._name = "Parse Popular"
		self._popular = popular
		self._procPool = procPool

	def decomposePopular(self):
		records = self._popular['data']['records']


		for i in range (0 , len(records)):
			subRecord = records[i]
			print subRecord
			filename = wget.download(subRecord['avatarUrl'])
			#videoname = wget.download(subRecord['permalinkUrl'])

