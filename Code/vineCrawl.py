#Trying to use Vine API to get some videos

import re
import json
import sys
import os.path
from getPopular import *
from multiprocessing import Pool

def now_time():
   		now=dt.datetime.now()
   		return int(time.mktime(now.timetuple()))

if __name__ == '__main__':
	print "initiating Vine Crawler from the popualr ones"
	procPool = Pool(1)
	procRegister = []
	crawler = vineCrawler(procPool)
	parser = parsePopular(procPool)

	timeStamp = now_time()
	rootDir = "Data/" + str(timeStamp)
	os.makedirs(rootDir)
	popular = crawler.getPopular(rootDir)		
	procRegister = parser.decomposePopular(popular, rootDir)
	for i in range(0 , len(procRegister)):
		Popen.kill(procRegister[i])
		print "Proceess Killed"
	procRegister = [];
	print "Cleaned up past processes : " + str(len(procRegister))
	time.sleep(10)







	


