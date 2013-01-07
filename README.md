DIP-with-ML-in-weibo
====================
-------------------------------------------------------

首先 安装 PIL, python的图像处理库
http://www.pythonware.com/products/pil/
然后 安装 Django框架
https://www.djangoproject.com/download/

-------------------------------------------------------

完成以上设置后
将本文件夹，即 AIProject 文件夹的绝对路径
  加入python的模块路径中
	使用 import sys
		 print sys.path;
	可以查看目前python的模块路径。
	
	--------------方法：---------------
	在python安装路径的Lib文件夹下的site-packages文件夹
	中创建一个文件，如django.pth，
	在里面加入本文件夹的绝对路径即可。
	我的路径是：
	E:\Program Files\Coding\Python2.7\Lib\site-packages
	
-------------------------------------------------------

然后修改aidemo文件夹中的settings.py文件

	63行：
	修改为static文件夹的绝对路径
	107行：
	修改为templates文件夹的绝对路径
	
	注意：
	在Windows下的路径中需要将\修改为/
	
-------------------------------------------------------

运行方法：

	cd到AIProject文件夹，
	python manage.py runserver 8888
	运行服务器，上面命令为监听8888端口
	或：
	python manage.py runserver 0.0.0.0:8888
	上述命令为监听本子网下对本机8888端口的访问
  
	
	然后在浏览器输入
	localhost:8888
	即可使用本应用
	
-------------------------------------------------------
CODE:PAN,WU,LIAN
