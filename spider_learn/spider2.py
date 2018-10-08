# -*- coding: utf-8 -*-
import requests
resp = requests.get('https://www.baidu.com') #请求百度首页
print(resp) #打印请求结果的状态码
print(resp.content) #打印请求到的网页源码

bsobj=BeautifulSoup(resp.content,'lxml') #将网页源码构造成BeautifulSoup对象，方便操作
a_list=bsobj.find_all('a') #获取网页中的所有a标签对象
for a in a_list:
    print(a.get('href')) #打印a标签对象的href属性，即这个对象指向的链接地址
