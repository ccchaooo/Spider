# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup


resp = requests.get('https://item.taobao.com/item.htm?spm=a230r.1.14.13.3bfe3d48TroW11&id=561267118940&ns=1&abbucket=4#detail')

bsobj = BeautifulSoup(resp.content,'lxml') #将网页源码构造成BeautifulSoup对象，方便操作
print(bsobj.select('#review-1019130227196'))

# MainReviews=bsobj.find_all('J_KgRate_MainReviews')

# print(MainReviews)

# a_list=bsobj.find_all('a') #获取网页中的所有a标签对象
# text='' # 创建一个空字符串
# for a in a_list:
#     href=a.get('href') #获取a标签对象的href属性，即这个对象指向的链接地址
#     text+=href+'\n' #加入到字符串中，并换行
#     print(text)


