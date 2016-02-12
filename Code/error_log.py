#! /usr/bin/env python
#coding=utf-8
import csv
from datetime import datetime
from cfg import log_dir

def error_user(u, mode):
	with open(log_dir+mode+'_error_users.csv', 'a') as f:
		w = csv.writer(f, delimiter='|')
		w.writerow([str(datetime.now()), u])
	

def error_log(thread, id, mode, e):
    filename = log_dir + mode+ '-%s-%s-%s.log'%(datetime.now().year, datetime.now().month, datetime.now().day)
    f = open(filename, "a") 
    s = '%s| thread %s| %s \n \t\t\t%s\n'%(str(datetime.now()), thread, id, e)
#    print s
    f.write(s) 
    f.flush()
    
