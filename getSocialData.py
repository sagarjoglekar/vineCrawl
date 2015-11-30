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
import os
import wget

def now_time():
   		now=dt.datetime.now()
   		return int(time.mktime(now.timetuple()))

def walkLevel1Dir(root):
	count = 0
	for path, dirs, files in os.walk(root):
		if count > 0:
			return dirs , files
		for dir in dirs:
			print "Directory : " + dir
		count = count + 1

if __name__ == '__main__':

	dirs, files = walkLevel1Dir("Data/");
	print len(files)
	print len(dirs)