import re
import csv
import csv_unicode
import datetime as dt
from datetime import datetime
import time
import random
import json
import pycurl
from error_log import error_log
#from lxml import etree
import urllib2
import os
from cStringIO import StringIO
import urllib 
import sys
from multiprocessing import Pool
import collections
import gzip

class DownloadError(Exception):
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def now_time():
   now=dt.datetime.now()
   return int(time.mktime(now.timetuple()))

def open_url_header(url, h):
	url = str(url)
	t = StringIO()
	curl = pycurl.Curl()
	header = h 
	curl.setopt(pycurl.HTTPHEADER, header)
	curl.setopt(pycurl.POST, 0)
	curl.setopt(curl.WRITEFUNCTION, t.write)

	curl.setopt(pycurl.URL, url) 
	curl.perform()
	http_code = int(curl.getinfo(pycurl.HTTP_CODE))	
	if http_code == 200:
		res = t.getvalue() 
		data = json.loads(res)	
		return data
	else:
		return {'rlt': 0}


def open_url(url):
	url = str(url)
	t = StringIO()
	curl = pycurl.Curl()
	header = ['Host: www.pinterest.com','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0','Accept: application/json, text/javascript, */*; q=0.01','Accept-Language: en-us,en;q=0.7,zh-cn;q=0.3','Accept-Encoding: deflate','DNT: 1','X-CSRFToken: zlBvfFlfiWQRk726c3LxcuVKEPkUmiwm','X-NEW-APP: 1','X-Requested-With: XMLHttpRequest','Referer: http://www.pinterest.com/all/food_drink/','''Cookie: _pinterest_sess="eJwz8fcIrrCsiizKyEoM8dAOyHHVj0pL1XapMrWwtY8vycxNtfUN8TXxqwqt8ndxNPBztLVVK04tLs5MsfXMisr2Cwk19A9xNfRzCS33rQqs8Mt1NQHyK/2qHE19XXKy/VwijSKrkss9021tAV3zIws="; __utma=229774877.717014847.1355236411.1386175531.1387537330.113; __utmz=229774877.1369761064.83.12.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __qca=P0-106563865-1357924876943; csrftoken=zlBvfFlfiWQRk726c3LxcuVKEPkUmiwm; __utmb=229774877.112.8.1387538043761; _track_cm=1; _pinterest_referrer="http://ipadpeek.com/"; logged_out=True; fba=True; prompt_views=3; prompt_seen=1; __utmc=229774877''','Connection: keep-alive']
	curl.setopt(pycurl.HTTPHEADER, header)
	curl.setopt(pycurl.POST, 0)
	curl.setopt(curl.WRITEFUNCTION, t.write)
	curl.setopt(pycurl.URL, url) 
	try_time = 5
	data = ''
	while try_time > 0:
		curl.perform()
		http_code = int(curl.getinfo(pycurl.HTTP_CODE))	
		if http_code == 200:
			res = t.getvalue() 
			json_num = len(list(re.finditer('page_info', res)))
			if json_num > 1:
				res = res[res.rfind('page_info')-2:]
			try:
				data = json.loads(res)	
				if data["resource_response"]["error"] == None:
					break
				else:
					try_time -= 1
			except Exception, e:
				print e
				try_time -= 1
		else:
			try_time -= 1
			if try_time > 0:
				slp = random.randint(0, 3)
				time.sleep(slp)
			else:
				raise DownloadError('Cannot download the page! Http_code: %s'%http_code)
		slp = random.randint(0, 3)
	t.close()
	return data

def open_url_lxml(url):
	opener = urllib2.build_opener(urllib2.HTTPHandler(), urllib2.HTTPSHandler())
	opener.addheaders = [('User-agent', 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.8; rv:19.0) Gecko/20100101 Firefox/19.0')]
	try_time = 2
	while try_time > 0:
		try:
			res = opener.open(url)
			try_time = -1
		except Exception, e:
			try_time -= 1
			if try_time <= 0:
				print e
				raise DownloadError('Cannot download the page: %s'%e)

	res_s = res.read()
	start_i = res_s.index("P.start.start(")+14
	end_i = res_s.index(''');
    </script>
</body>
</html>''')
	data = json.loads(res_s[start_i:end_i])	
	return data

def grab_user_basic(username, store_path):
	url = 'http://pinterest.com/%s/'%username
	res = open_url_lxml(url)
	data = res['tree']['data']
	boards = data['board_count'] 
	pins = data['pin_count'] 
	likes = data['like_count'] 
	followers = data['follower_count'] 
	following = data['following_count'] 
	name = data['full_name']
	about = data['about']
	user_id = data['id'] 
	domain = data['domain_verified']
	secret_board = 0
	if 'secret_board_count' in data:
		secret_board = data['secret_board_count']
	with open(store_path+'users.csv', 'a') as wf:
		user_w = csv.writer(wf, delimiter = '|')
		user_w.writerow([now_time(), user_id, username, boards, secret_board, pins, likes, followers, following, domain])
	with open(store_path+'user_des.csv', 'a') as wf:
		user_w = csv_unicode.UnicodeWriter(wf, delimiter='|')
		user_w.writerow([str(now_time()), user_id, username, name, about])
	
	#facebook
	fb = data['facebook_url']
	if fb != None:
		with open(store_path+'user_facebook.csv', 'a') as f:
			w = csv.writer(f, delimiter='|')
			w.writerow([username, fb])
	#location
	lc = data['location']
	if len(lc) > 0:
		with open(store_path+'user_location.csv', 'a') as f:
			w = csv_unicode.UnicodeWriter(f, delimiter='|')
			w.writerow([username, lc])
	#twitter
	tw = data['twitter_url']
	if tw != None:
		with open(store_path+'user_twitter.csv', 'a') as f:
			w = csv.writer(f, delimiter='|')
			w.writerow([username, tw])
	
        #website
	web = data['website_url']
	if web != None:
		with open(store_path+'user_website.csv', 'a') as f:
			w = csv.writer(f, delimiter='|')
			w.writerow([username, web])
def save_json_with_url(res, rlt_dir, prefix):
        json_file = rlt_dir+'json/'+prefix+'_json-%s%s%s.csv.gz'%(datetime.now().year, datetime.now().month, datetime.now().day)
        url_file = rlt_dir+'url/'+prefix+'_url-%s%s%s.csv'%(datetime.now().year, datetime.now().month, datetime.now().day)
	with gzip.open(json_file, 'a') as f:
		json.dump(res, f)
		f.write('\n')
#	with open(url_file, 'a') as f:
#		for basic_data in res['resource_response']['data']:
#			w = csv.writer(f, delimiter='|')
#			w.writerow([now_time(), basic_data['id'], basic_data['link']])

def grab_domain_pins(domain, rlt_dir, prefix):
	ori_url='http://www.pinterest.com/resource/DomainFeedResource/get/?source_url=/source/ebay.com/&data={"options":{"domain":"%s","page_size":200},"context":{},"module":{"options":{"item_options":{"show_pinner":true,"show_pinned_from":true,"show_board":true,"squish_giraffe_pins":false},"layout":"variable_height"}}}'
	next_url='http://www.pinterest.com/resource/DomainFeedResource/get/?source_url=/source/ebay.com/&data={"options":{"domain":"%s","bookmarks":["%s"],"page_size":200},"context":{},"module":{"options":{"item_options":{"show_pinner":true,"show_pinned_from":true,"show_board":true,"squish_giraffe_pins":false},"layout":"variable_height"}}}'
        url = ori_url%(domain)
	print url
        try:
                res = open_url(url)
		save_json_with_url(res, rlt_dir, prefix)
        except DownloadError, e:
                print e
		error_log('domain_pins', domain, 'pin', e)
                return
	bookmarks = (res['resource']['options']['bookmarks'][0])
        while bookmarks <> "-end-":
                url = next_url%(domain, bookmarks)
		try:
			res = open_url(url)
			save_json_with_url(res, rlt_dir, prefix)
		except DownloadError, e:
			print e
			error_log('domain_pins', domain, 'pin', e)
			return
                bookmarks = (res['resource']['options']['bookmarks'][0])
                slp = random.randint(0, 1)
                time.sleep(slp)	

def grab_user_pins(username, rlt_dir):
	ori_url='https://www.pinterest.com/resource/UserPinsResource/get/?source_url=/%s/pins/&data={"options":{"username":"%s","page_sie":200},"context":{},"module":{"name":"GridItems","options":{"scrollable":true,"show_grid_footer":true,"centered":true,"reflow_all":true,"virtualize":true,"item_options":{"show_pinner":true,"show_pinned_from":false,"show_board":true,"squish_giraffe_pins":false},"layout":"variable_height"}},"append":true,"error_strategy":1}'
	next_url='https://www.pinterest.com/resource/UserPinsResource/get/?source_url=/%s/pins/&data={"options":{"username":"%s","page_sie":200,"bookmarks":["%s"]},"context":{},"module":{"name":"GridItems","options":{"scrollable":true,"show_grid_footer":true,"centered":true,"reflow_all":true,"virtualize":true,"item_options":{"show_pinner":true,"show_pinned_from":false,"show_board":true,"squish_giraffe_pins":false},"layout":"variable_height"}},"append":true,"error_strategy":1}'
        url = ori_url%(username, username)
        try:
                res = open_url(url)
		save_board_pins(res, rlt_dir)
        except DownloadError, e:
                print e
		error_log('user_pins', username, 'pin', e)
                return
        bookmarks = res['module']['tree']['resource']['options']['bookmarks'][0]
        while bookmarks <> "-end-":
                url = next_url%(username, username, bookmarks)
                try:
                        res = open_url(url)
			save_board_pins(res, rlt_dir)
                except DownloadError, e:
                        print e
			error_log('user_pins', username, 'pin', e)
                        return 
                bookmarks = (res['module']['tree']['resource']['options']['bookmarks'][0])
                slp = random.randint(0, 1)
                time.sleep(slp)	

def grab_user_boards(username, rlt_dir):
	ori_url='http://www.pinterest.com/resource/ProfileBoardsResource/get/?source_url=/%s/&data={"options":{"field_set_key":"detailed","username":"%s","page_sie":200},"context":{},"module":{"name":"GridItems","options":{"scrollable":true,"show_grid_footer":false,"centered":true,"reflow_all":true,"virtualize":true,"item_options":{"show_board_context":false,"show_user_icon":false},"layout":"fixed_height"}},"render_type":3,"error_strategy":1}'
	next_url='http://www.pinterest.com/resource/ProfileBoardsResource/get/?source_url=/%s/&data={"options":{"field_set_key":"detailed","username":"%s","bookmarks":["%s"],"page_sie":200},"context":{},"module":{"name":"GridItems","options":{"scrollable":true,"show_grid_footer":false,"centered":true,"reflow_all":true,"virtualize":true,"item_options":{"show_board_context":false,"show_user_icon":false},"layout":"fixed_height"}},"render_type":3,"error_strategy":1}'
        url = ori_url%(username, username)
        try:
                res = open_url(url)
		save_board_basic(res, rlt_dir)
        except DownloadError, e:
                print e
		error_log('user_pins', username, 'pin', e)
                return
        bookmarks = res['module']['tree']['resource']['options']['bookmarks'][0]
        while bookmarks <> "-end-":
                url = next_url%(username, username, bookmarks)
                try:
                        res = open_url(url)
			save_board_basic(res, rlt_dir)
                except DownloadError, e:
                        print e
			error_log('user_pins', username, 'pin', e)
                        return 
                bookmarks = (res['module']['tree']['resource']['options']['bookmarks'][0])
                slp = random.randint(0, 1)
                time.sleep(slp)	

def save_board_basic(res, rlt_dir):
	pin_file = rlt_dir+'boards.csv'
	des_file = rlt_dir+'board_des.csv'
	if 'data' not in res['module']['tree']:
		return
	for basic_data in res['module']['tree']['data']:
		with open(des_file, 'a') as df, open(pin_file, 'a') as f:
			w = csv.writer(f, delimiter='|')
			dw = csv_unicode.UnicodeWriter(df, delimiter='|')
			name = basic_data['name']
			if name == None:
				name = ''
			des = basic_data['description']
			if des == None:
				des = ''
			dw.writerow([basic_data['url'], name, des])
			w.writerow([now_time(), basic_data['id'], basic_data['owner']['username'], basic_data['url'], basic_data['category'], basic_data['is_collaborative'], basic_data['collaborator_count'], basic_data['pin_count'], basic_data['follower_count']])

def save_board_pins(res, rlt_dir):
	pin_file = rlt_dir+'pins.csv'
	des_file = rlt_dir+'pin_des.csv'
	if 'data' not in res['module']['tree']:
		return
	for basic_data in res['module']['tree']['data']:
		with open(des_file, 'a') as df, open(pin_file, 'a') as f:
			w = csv.writer(f, delimiter='|')
			dw = csv_unicode.UnicodeWriter(df, delimiter='|')
			pin_id =  basic_data['id']
			link = basic_data['link'].encode('ascii', 'ignore')
			img = basic_data['images']['orig']
			dw.writerow([pin_id, basic_data['description']])
			w.writerow([now_time(), pin_id, basic_data['pinner']['username'], basic_data['board']['id'], basic_data['board']['url'], basic_data['is_repin'], basic_data['dominant_color'], basic_data['price_currency'], basic_data['price_value'], basic_data['is_video'], basic_data['created_at'], img['width'], img['height'], img['url'], basic_data['domain'], link])

		stat_file = rlt_dir+'pin_stat.csv'
		with open(stat_file, 'a') as f:
			w = csv.writer(f, delimiter='|')
			w.writerow([now_time(), pin_id, basic_data['repin_count'], basic_data['like_count'], basic_data['comment_count']])

def blocked_urls(domain, rlt_dir):
	e = random.randint(100, 999)
	f = random.randint(100, 999)
	ori_url = 'http://www.pinterest.com/offsite/?token=%s-%s&url=%s&pin=184155072237278966'%(e, f, domain)
	h = ['Host: www.pinterest.com','User-Agent: Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:26.0) Gecko/20100101 Firefox/26.0','Accept: application/json, text/javascript, */*; q=0.01','Accept-Language: en-us,en;q=0.7,zh-cn;q=0.3','Accept-Encoding: deflate','DNT: 1','X-CSRFToken: zlBvfFlfiWQRk726c3LxcuVKEPkUmiwm','X-NEW-APP: 1','X-Requested-With: XMLHttpRequest','Referer: http://www.pinterest.com/all/food_drink/','''Cookie: _pinterest_sess="eJwz8fcIrrCsiizKyEoM8dAOyHHVj0pL1XapMrWwtY8vycxNtfUN8TXxqwqt8ndxNPBztLVVK04tLs5MsfXMisr2Cwk19A9xNfRzCS33rQqs8Mt1NQHyK/2qHE19XXKy/VwijSKrkss9021tAV3zIws="; __utma=229774877.717014847.1355236411.1386175531.1387537330.113; __utmz=229774877.1369761064.83.12.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided); __qca=P0-106563865-1357924876943; csrftoken=zlBvfFlfiWQRk726c3LxcuVKEPkUmiwm; __utmb=229774877.112.8.1387538043761; _track_cm=1; _pinterest_referrer="http://ipadpeek.com/"; logged_out=True; fba=True; prompt_views=3; prompt_seen=1; __utmc=229774877'''+'''; offsite_%s=%s'''%(e, f),'Connection: keep-alive']
        try:
		data = open_url_header(ori_url, h)
        except DownloadError, e:
                print e
		error_log('block-domain', domain, 'block-domain', e)
                return
	if 'rlt' in data:
		s = 'trust'
	else:
		s = data['module']['tree']['options']['redirect_status']
	url_file = rlt_dir+'blocked_url.csv'
	with open(url_file, 'a') as f:
		w = csv.writer(f, delimiter='|')
		w.writerow([now_time(), domain, s])
def check_url(url, filename):
	url = str(url)
	a=urllib.urlopen(url)
	http_code = a.getcode() 
	with open(filename, 'a') as f:
		w = csv.writer(f, delimiter='|')
		w.writerow([now_time(), url, http_code])

def grab_user_follower(username, filename):
	return harvest_users(username, filename, mode='follower')

def grab_user_following(username, filename):
	return harvest_users(username, filename, mode='following')

def save_csv(filename, data):
	with open(filename, 'a') as f:
		wf = csv.writer(f, delimiter='|')
		for d in data:
			wf.writerow(d)

def harvest_users(username, filename, mode):
	m = 0
	rlt = set()
	if mode == 'follower':
		m = 0
		ori_url = 'http://www.pinterest.com/resource/UserFollowersResource/get/?data={"options":{"username":"%s","page_size":200},"module":{"name":"GridItems"}}'
		next_url = 'http://www.pinterest.com/resource/UserFollowersResource/get/?data={"options":{"username":"%s","page_size":200,"bookmarks":["%s"]},"module":{"name":"GridItems"}}'
	elif mode == 'following':
		m = 1
		ori_url = 'http://www.pinterest.com/resource/UserFollowingResource/get/?data={"options":{"username":"%s","page_size":200},"module":{"name":"GridItems"}}'
		next_url = 'http://www.pinterest.com/resource/UserFollowingResource/get/?data={"options":{"username":"%s","page_size":200,"bookmarks":["%s"]},"module":{"name":"GridItems"}}'
	url = ori_url%username
	try:
		res = open_url(url)	
	except DownloadError, e:
		raise
	fer = []
	for data in res['module']['tree']['data']:	
		if m == 0:
			fer.append([username, data['username']])
		elif m == 1:
			fer.append([data['username'], username])
			
	save_csv(filename, fer)
	bookmarks = (res['module']['tree']['resource']['options']['bookmarks'][0]).encode('ascii','ignore')
	while bookmarks <> "-end-":
		url = next_url%(username, bookmarks)
		try:
			res = open_url(url)	
		except DownloadError, e:
			raise
		fer = []
		for data in res['module']['tree']['data']:	
			if m == 0:
				fer.append([username, data['username']])
			elif m == 1:
				fer.append([data['username'], username])
			
		save_csv(filename, fer)
		bookmarks = (res['module']['tree']['resource']['options']['bookmarks'][0]).encode('ascii','ignore')
		slp = random.randint(0, 3)
		time.sleep(slp)
	return rlt
def grab_repins(pin_id, rlt_dir):
        new_down = []
	repin_file = rlt_dir+'repins.csv'
	ori_url = 'http://www.pinterest.com/resource/RepinFeedResource/get/?source_url=/pin/%s/repins/&data={"options":{"pin_id":"%s","page_size":200},"context":{"app_version":"18ad338"},"module":{"name":"GridItems","options":{"scrollable":true,"show_grid_footer":false,"centered":true,"reflow_all":true,"virtualize":true,"item_options":{"user_in_rep_title":true},"layout":"fixed_height"}},"append":true,"error_strategy":2}' 
	next_url = 'http://www.pinterest.com/resource/RepinFeedResource/get/?source_url=/pin/%s/repins/&data={"options":{"pin_id":"%s","bookmarks":["%s"],"page_size":200},"context":{"app_version":"18ad338"},"module":{"name":"GridItems","options":{"scrollable":true,"show_grid_footer":false,"centered":true,"reflow_all":true,"virtualize":true,"item_options":{"user_in_rep_title":true},"layout":"fixed_height"}},"append":true,"error_strategy":2}' 
	with open(repin_file, 'a') as f:
		w = csv.writer(f, delimiter='|')
		url = ori_url%(pin_id, pin_id)
		try:
			res = open_url(url)
		except DownloadError, e:
			print e
	#               error_log('cate', catename, e)
			return
		if 'data' in res['module']['tree']:
			for data in res['module']['tree']['data']:
				w.writerow([now_time(), pin_id, data['url']])
		bookmarks = (res['module']['tree']['resource']['options']['bookmarks'][0]).encode('ascii','ignore')
		n = 1
		while bookmarks <> "-end-":
			url = next_url%(pin_id, pin_id, bookmarks)
			try:
				res = open_url(url)
			except DownloadError, e:
				print e
	#                       error_log('cate', catename, e)
				return
			if 'data' in res['module']['tree']:
				for data in res['module']['tree']['data']:
					w.writerow([now_time(), pin_id, data['url']])

			bookmarks = (res['module']['tree']['resource']['options']['bookmarks'][0]).encode('ascii','ignore')
			slp = random.randint(0, 1)
			n += 1
			time.sleep(slp)	
		

def grab_likes(pin_id, rlt_dir):
        new_down = []
        like_file = rlt_dir+ 'likes.csv'
        ori_url = 'http://www.pinterest.com/resource/PinLikesResource/get/?source_url=/pin/%s/repins/&data={"options":{"pin_id":"%s","page_size":200},"context":{"app_version":"18ad338"},"module":{"name":"GridItems","options":{"scrollable":true,"show_grid_footer":false,"centered":true,"reflow_all":true,"virtualize":true,"item_options":{"user_in_rep_title":true},"layout":"fixed_height"}},"append":true,"error_strategy":2}'
        next_url = 'http://www.pinterest.com/resource/PinLikesResource/get/?source_url=/pin/%s/repins/&data={"options":{"pin_id":"%s","bookmarks":["%s"],"page_size":200},"context":{"app_version":"18ad338"},"module":{"name":"GridItems","options":{"scrollable":true,"show_grid_footer":false,"centered":true,"reflow_all":true,"virtualize":true,"item_options":{"user_in_rep_title":true},"layout":"fixed_height"}},"append":true,"error_strategy":2}'
        with open(like_file, 'a') as f:
                w = csv.writer(f, delimiter='|')
		url = ori_url%(pin_id, pin_id)
		try:
			res = open_url(url)
		except DownloadError, e:
			print e
			return
		if 'data' in res['module']['tree']:
			for data in res['module']['tree']['data']:
				w.writerow([now_time(), pin_id, data['username']])
		bookmarks = (res['module']['tree']['resource']['options']['bookmarks'][0]).encode('ascii','ignore')
		n = 1
		while bookmarks <> "-end-":
			url = next_url%(pin_id, pin_id, bookmarks)
			try:
				res = open_url(url)
			except DownloadError, e:
				print e
				return
			if 'data' in res['module']['tree']:
				for data in res['module']['tree']['data']:
					w.writerow([now_time(), pin_id, data['username']])
			bookmarks = (res['module']['tree']['resource']['options']['bookmarks'][0]).encode('ascii','ignore')
			slp = random.randint(0, 1)
			n += 1
			time.sleep(slp)
def repin(l):
	pin_id =l[0]
	err_file = l[1]+'error_repin.csv'
	with  open(err_file, 'a') as wf:
		w =  csv.writer(wf, delimiter='|')
		try:
			grab_repins(l[0], l[1])
			w.writerow([pin_id, 'succ'])
		except Exception, e:
			w.writerow([pin_id, 'err'])
def like(l):
	pin_id =l[0]
	err_file = l[1]+'error_like.csv'
	with  open(err_file, 'a') as wf:
		w =  csv.writer(wf, delimiter='|')
		try:
			grab_likes(l[0], l[1])
			w.writerow([pin_id, 'succ'])
		except Exception, e:
			w.writerow([pin_id, 'err'])
def rl_process():
	pool = Pool(25)
	rlt_dir = '/home/changtao/changtao/pnt_activity/data/addmefast/'
	data_file = rlt_dir+'downloaded.csv'
	data_file = rlt_dir+'email.csv'
	in_list = []
	err_repin= ['171488698284027741', '253468285248299501']
	for p in err_repin:
		in_list.append([p, rlt_dir])
	pool.map(repin, in_list)
	in_list = []
	err_like = []
	for p in err_like:
		in_list.append([p, rlt_dir])
	pool.map(like, in_list)
	in_list = []
	return
	with open(data_file, 'r') as f:
		r =  csv.reader(f, delimiter='|')
		for line in r:
			pin_id = line[0].split('/')[-1]
			print pin_id
			in_list.append([pin_id, rlt_dir])
			if len(in_list) %50 == 0:
				print in_list
				pool.map(repin, in_list)
				pool.map(like, in_list)
				in_list = []
		if len(in_list) > 0:
			pool.map(repin, in_list)
			pool.map(like, in_list)
			in_list = []
if __name__ == "__main__":
	print datetime.now()
	grab_domain_pins('ebay.com', 'data/', 'ebaycom')
	print datetime.now()
