from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings

import test2
import rz7

user_name = ""
user_pw = ""

def login(request):
  return render_to_response('login.html')

@csrf_exempt
def search(request):
	error_name = False
	error_pw = False
	judge = True
	if 'username' in request.POST:
		if 'userpw' in request.POST:
			user_name = request.POST['username']
			user_pw = request.POST['userpw']
			if not user_name:
				error_name = True
			if not user_pw:
				error_pw = True
			if user_pw == "fuck":
                                judge = False
	if error_name or error_pw:
		return render_to_response('login.html', {'error_name' : error_name, 'error_pw' : error_pw})
	back = 'back'
	if 'back' in request.POST:
		back = request.POST['back']
	if back == 'back' and judge:
		test2.log_in()
	return render_to_response('newsearch.html', {'face' : rz7.PIC_URL, 'weibo_name' : rz7.NAME})

@csrf_exempt
def result(request):
	error_img = False
	if 'image' not in request.FILES:
		error_img = True;
		return render_to_response('newsearch.html', {'error_img' : error_img})
	image = request.FILES.get('image', None)
	fname = image.name
	destname = "0"
	destname += fname[fname.rfind('.'):]
	dest = open('static/' + destname, 'wb+')
	for chunk in request.FILES['image'].chunks():
		dest.write(chunk)
	dest.close()
	data = test2.search(settings.STATIC_URL + '/', request.POST['label'])
	return render_to_response('newresult.html', {'face' : rz7.PIC_URL, 'weibo_name': rz7.NAME, 'data_list' : data})

@csrf_exempt
def final(request):
	test2.learn(request.POST['str'])
	return render_to_response('final.html')

def tmpui(request):
	return render_to_response('newsearch.html', {'face' : 'http://tp4.sinaimg.cn/3171368547/50/40010119271/1', 'weibo_name' : 'God Damn Fuck'})

def tmpresult(request):
	data_list = [];
	for i in range (0, 11):
		tmp = '/static/' + str(i) + '.jpg'
		item = {'face' : 'http://tp4.sinaimg.cn/3171368547/50/40010119271/1', 'name' : 'God Damn Fuck', 'picture' : tmp, 'text' : 'God Damn Fuck!!!!!!!!'}
		data_list.append(item)
	return render_to_response('newresult.html', {'face' : 'http://tp4.sinaimg.cn/3171368547/50/40010119271/1', 'weibo_name' : 'God Damn Fuck', 'data_list' : data_list})
