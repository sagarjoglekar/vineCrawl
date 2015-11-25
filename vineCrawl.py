#Trying to use Vine API to get some videos

import re
import datetime as dt
from datetime import datetime
import time
import random
import json
import sys
import requests
from multiprocessing import Pool


class vineCrawler(Exception):
	def __init__(self):
		self.name = "Vine Crawler"
		self.popular = None

	def now_time(self):
   		now=dt.datetime.now()
   		return int(time.mktime(now.timetuple()))

   	def getPopular(self):
		self.popular = requests.get("https://api.vineapp.com/timelines/popular")
		return self.popular


if __name__ == '__main__':
	print "initiating Vine Crawler from the popualr ones"
	procPool = Pool(12)

	crawler = vineCrawler();
	popular = crawler.getPopular();
	print popular



