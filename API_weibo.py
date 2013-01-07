from weibo import APIClient
from re import split
import urllib,httplib
import webbrowser
import searcherAI as searcher
import learning
from urllib import urlretrieve

import rz7

APP_KEY = "XXXXX"
APP_SECRET = "XXXXXXXXXXXXXXXXXXX"
CALLBACK_URL = "http://api.weibo.com/oauth2/default.html"

def get_code(ACCOUNT,PASSWORD):
        #get url
  client = APIClient(app_key = APP_KEY,app_secret = APP_SECRET,redirect_uri=CALLBACK_URL)
	url = client.get_authorize_url()
	
        #get code
	conn = httplib.HTTPSConnection('api.weibo.com')
	postdata = urllib.urlencode     ({'client_id':APP_KEY,'response_type':'code','redirect_uri':CALLBACK_URL,'action':'submit','userId':ACCOUNT,'passwd':PASSWORD,'isLoginSina':0,'from':'','regCallback':'','state':'','ticket':'','withOfficalFlag':0})
	conn.request('POST','/oauth2/authorize',postdata,{'Referer':url,'Content-Type': 'application/x-www-form-urlencoded'})
	res = conn.getresponse()
	location = res.getheader('location')
	code = location.split('=')[1]
	conn.close()

	#get client		
	r = client.request_access_token(code)
	access_token = r.access_token 
	expires_in = r.expires_in 
	client.set_access_token(access_token, expires_in)
	
	all_tmp = client.users__show(uid = client.account__get_uid()['uid'])
	rz7.PIC_URL = all_tmp['profile_image_url']
	rz7.NAME = all_tmp['screen_name']
	all = {}
	#a count
	flag = 0
	data = []
	all = client.statuses__home_timeline(count = 200)
	d = dict(all)
	
	#fobj = open("api_data","w")

	tar = ''
	
	for i in range(len(d['statuses'])):	
		if 'bmiddle_pic' in d['statuses'][i]:
			tmp = {}
			tmp['name'] = d['statuses'][i]['user']['screen_name']
			tmp['text'] = d['statuses'][i]['text']
			tmp['picture'] = d['statuses'][i]['bmiddle_pic']
			tmp['face'] = d['statuses'][i]['user']['profile_image_url']

			fn = tar + (str)(flag) + '.jpg'
			urlretrieve(d['statuses'][i]['bmiddle_pic'],fn)
			flag = flag + 1
			data.append(tmp)	
	return data,flag

def log_in():
	rz7.DATA, rz7.FLAG = get_code("XXXXXXXXXXXX","XXXXXXXXXX")
	return rz7.PIC_URL,rz7.NAME

def search( src_address, label ):
	array1 = []
	b = []
	rz7.LABEL = label
	if rz7.FLAG < 10:
		array1,rz7.RES = searcher.searcher(src_address,"",label, rz7.FLAG, rz7.FLAG)
	else:	
		array1,rz7.RES = searcher.searcher(src_address,"",label, rz7.FLAG,10)
	for i in array1:
		b.append(rz7.DATA[i])
	return b
    
def learn( imgStr):
	searcher.machineLearning(imgStr,rz7.LABEL,rz7.RES)


	
	
