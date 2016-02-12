import csv
from oxford import vision, vision_plus, landmark 
from multiprocessing import Pool
import multiprocessing as mp
from error_log import error_user, error_log
from random import randrange
import time
import sys
import gzip
import cfg

mode = ''
def vision_process(l):
	time.sleep(randrange(8))
	try:
		landmark(l[0], l[1], str(mp.current_process()._identity[0]))
	except Exception, e:
		error_user(l[0], mode)
		error_log(0, l[0], mode, e)
	with open(cfg.log_dir+mode+'_finished.csv', 'a') as f:
		w = csv.writer(f, delimiter='|')
		w.writerow([l[0]])
def vision_process_plus(l):
	time.sleep(randrange(8))
	try:
		vision_plus(l[0], l[1], str(mp.current_process()._identity[0]))
	except Exception, e:
		error_user(l[0], mode)
		error_log(0, l[0], mode, e)
	with open(cfg.log_dir+mode+'_finished.csv', 'a') as f:
		w = csv.writer(f, delimiter='|')
		w.writerow([l[0]])

def vision_main(mode='oxford'):
	users = set()
	n = 0
	pool = Pool(cfg.vision_process_num)
	input_list = []
	finished = set()
	finished_file = cfg.log_dir+mode+'_finished.csv'
	try:
		with open(finished_file, 'r') as f:
			r = csv.reader(f, delimiter='|')
			for line in r:
				finished.add(line[0])
	except Exception, e:
		print e
	with gzip.open(cfg.vision_data_file, 'r') as f:
		freader = csv.reader(f, delimiter='|')
		for line in freader:
			n+=1
			if n <= cfg.vision_start_num:
				continue
			
			if len(line) <= 1 or  line[1] in finished:
				continue
			input_list.append([line[1], cfg.vision_save_dir])
			if len(input_list)%1000==0:
				if mode == 'oxford':
					outp = pool.map(vision_process, input_list)
				elif mode =='plus':
					outp = pool.map(vision_process_plus, input_list)
				input_list = []
				error_log('system', 'user', mode, 'n=%d'%n)
				time.sleep(randrange(2))
		if len(input_list) > 0:
			if mode == 'oxford':
				outp = pool.map(vision_process, input_list)
			elif mode =='plus':
				outp = pool.map(vision_process_plus, input_list)
			input_list = []
			error_log('system', 'user', mode, 'n=%d'%n)
if __name__ == '__main__':
	if len(sys.argv) < 0:
		print 'Error: please define mode.'
	else:
		mode = sys.argv[1]
		if mode== 'vision':
			vision_main()
		if mode== 'plus':
			vision_main(mode='plus')
		else:
			print 'Error: mode are not correct!'
