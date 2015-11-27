#Trying to use Vine API to get some videos

import re
import json
import sys
import os.path
from getPopular import vineCrawler
from getPopular import parsePopular	
from multiprocessing import Pool



if __name__ == '__main__':
	print "initiating Vine Crawler from the popualr ones"
	procPool = Pool(12)
	crawler = vineCrawler(procPool)
	files = [f for f in os.listdir('.') if re.match(r'popular*', f)]
	if not files :
		popular = crawler.getPopular()
		crawler.collectJSON(popular)
	else :
		with open(files[0]) as data_file:
			popular = json.load(data_file)
			#print popular
			print popular['data']['count']
			print popular['data']['records'][1]


	parser = parsePopular(popular,procPool)
	parser.decomposePopular()






	



