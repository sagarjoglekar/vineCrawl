import csv
import datetime as dt
from datetime import datetime
import time
import random
import json
import pycurl
from lxml import etree
import urllib2
import os
from cStringIO import StringIO
import sys
from multiprocessing import Pool
import collections
import gzip
import httplib, urllib, base64
class DownloadError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def now_time():
   now=dt.datetime.now()
   return int(time.mktime(now.timetuple()))


def save_json(res, rlt_dir, suffix):
        json_file = rlt_dir+'_json_'+suffix+'.csv.gz'
        with gzip.open(json_file, 'a') as f:
                json.dump(res, f)
                f.write('\n')

def vision1(url, rlt_dir, suffix):
	headers = {
	   # Basic Authorization Sample
	   #'Authorization': 'Basic %s' % base64.encodestring('{username}:{password}'),
	   'Content-type': 'application/json',
	}

	params = urllib.urlencode({
	   # Specify your subscription key
	   'subscription-key': '5e45a8119d6e44af96fb5048a047c548',
	   # Specify values for optional parameters, as needed
	   'visualFeatures': 'All',
	})

	try:
	   conn = httplib.HTTPSConnection('api.projectoxford.ai')
           data = json.dumps({"Url": "%s"%url})
	   conn.request("POST", "/vision/v1/analyses?%s" % params, data, headers)
	   response = conn.getresponse()
	   data = response.read()
	   conn.close()
	except Exception as e:
        print e
	    print("[Errno {0}] {1}".format(e.errno, e.strerror))
	save_json(data, rlt_dir+'vision', suffix)
def vision(url, rlt_dir, suffix):
	cmd = '''curl -sS 'https://www.projectoxford.ai/api/ForwardProxy/Analysis' -H 'Cookie: ai_user=16f3149b7e95429e89f756a5219a27f0|2015-07-01T09:28:44.1296046+00:00; ARRAffinity=3c256ddb5417a7e2c7bd5912d5dc15d26185f789b9f9ae2b5016c7c9540f33ad; __RequestVerificationToken=tMxL7bm1k8k_EXlF-5VP_kP_cwVsq95SVODmMObZyY30wPaRcHE-47I8IB5LadZzeMTeh5Qxna9QWwIzv6kPBkGk_8B_6jymcGAaUpE03d01; ai_session=02b09a2644944b0b9a22fe9c2f440d90|2015-07-13T15:16:50.0518800+00:00|2015-07-13T15:16:50.0830820+00:00' -H 'Origin: https://www.projectoxford.ai' -H 'Accept-Encoding: gzip, deflate' -H 'Accept-Language: en-US,en;q=0.8,zh-CN;q=0.6,zh;q=0.4' -H 'User-Agent: Mozilla/5.0 (X11; Linux i686 (x86_64)) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36' -H 'Content-Type: application/json' -H 'Accept: */*' -H 'Referer: https://www.projectoxford.ai/demo/visions' -H 'X-Requested-With: XMLHttpRequest' -H 'Connection: keep-alive' -H '__RequestVerificationToken: PaErq3k3eAelDv05yMJAqrX3HakmraC_fEJIuTFt7jI6KvnGFFkL0slJ_QqRjx2v086xUfvu-TNns6a3GDzaSGoeilqd-sGXOlFpYxgYSuw1' --data-binary '{"Url":"%s"}' --compressed '''%url
	f = os.popen(cmd)
	data = json.loads(f.read())
	img_name = url#.split('/')[-1].split('.')[0]
	data = {'img':img_name, 'res': data}
	save_json(data, rlt_dir+'vision', suffix)
def landmark(url, rlt_dir, suffix):
        s_url =  urllib.urlencode({'Data':url})
        cmd = '''curl -sS 'https://www.projectoxford.ai/Demo/Detect' -H 'Host: www.projectoxford.ai' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:40.0) Gecko/20100101 Firefox/40.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Content-Type: application/x-www-form-urlencoded; charset=UTF-8' -H 'X-Requested-With: XMLHttpRequest' -H 'Referer: https://www.projectoxford.ai/demo/face' -H 'Cookie: __RequestVerificationToken=HKE8PDM0bm08a6uOOAn7eBj9cGKyLAvldFXmRLzko_GZ5e_ioNF4txENybNkbVXYiGQwmSrFgEIfv-ZULAiiRVzoyefRQiuDsmxvtHPGRg41; ai_session=49c2398cc1274818b496e8374b0feff2|2015-10-12T15:47:47.2206750+00:00|2015-10-12T16:01:16.6749125+00:00; ai_user=8ca06b31b36842808a90bd97651776ed|2015-10-12T15:47:47.2206750+00:00; ARRAffinity=24e0488028b49b3000ef3cff0d95e0e684d4eab245e2fb9c87db1d192e7e4283' -H 'Connection: keep-alive' -H 'Pragma: no-cache' -H 'Cache-Control: no-cache' --data '%s&DataType=imageUrl&Time=Mon+Oct+12+2015+17%%3A04%%3A15+GMT%%2B0100+(BST)&ActionType=verification&__RequestVerificationToken=9G8t-NY0AIBvRbugfXBEXakqHpd4t_CdBsczwclnlDK_LvxU2kdwIXxo5U5KalpNDsX5ULLWx6eW8xTisKvm7ialpVXDpaDfA1yRFOnxgvY1' ''' %s_url
	f = os.popen(cmd)
	data = json.loads(f.read())
	img_name = url#.split('/')[-1].split('.')[0]
	data = {'img':img_name, 'res': data}
	save_json(data, rlt_dir+'vision_lankmark', suffix)

def vision_plus(url, rlt_dir, suffix):
	cmd = '''curl -sS 'http://apicn.faceplusplus.com/v2/detection/detect?api_key=DEMO_KEY&api_secret=DEMO_SECRET&%s&attribute=age%%2Cgender%%2Crace%%2Csmiling%%2Cpose%%2Cglass&mode=commercial' -H 'Host: apicn.faceplusplus.com' -H 'User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.10; rv:39.0) Gecko/20100101 Firefox/39.0' -H 'Accept: application/json, text/javascript, */*; q=0.01' -H 'Accept-Language: en-US,en;q=0.5' --compressed -H 'Referer: http://www.faceplusplus.com.cn/demo-detect/' -H 'Origin: http://www.faceplusplus.com.cn' -H 'Connection: keep-alive' ''' % urllib.urlencode({'url':url})
	f = os.popen(cmd)
	data = json.loads(f.read())
	if 'error' in data:
		print url
		print data['error']
		raise DownloadError(data['error'])
	img_name = url#.split('/')[-1].split('.')[0]
	data = {'img':img_name, 'res': data}
	save_json(data, rlt_dir+'faceplus', suffix)

if  __name__ == "__main__":
	landmark('https://fbcdn-profile-a.akamaihd.net/hprofile-ak-xtp1/v/t1.0-1/p200x200/11703358_10205745976942436_8031999280410217469_n.jpg?oh=d80437a6687ea7ab2ade2f9cf8dd17b1&oe=5641B765&__gda__=1446429373_f921be798e431b1a9ba5d742a89c9758', 'data/', '1')
