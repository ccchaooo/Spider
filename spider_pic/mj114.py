#-*-coding: utf-8 -*-

import urllib.request
import requests
import re
from bs4 import BeautifulSoup
import os

'''
使用beautifulsoup下载图片
1、使用urllib.request 下载到网页内容
2、使用beautifulsoup匹配到所有的图片地址
3、指定文件路径
4、调用urllib.request.urlretrieve 下载图片
'''

# http://www.mj114.net/html/part/index21.html

class picDown:
    def __init__(self):
        self.image_couter = 1

    def grap_image(self):

        #手动link
        links = ['http://cache.imgespark.com/pics/20131217/b6617.jpg',
                'http://cache.imgespark.com/pics/20131217/b6617.jpg',
                'http://cache.imgespark.com/pics/20131217/b6618.jpg',
                'http://cache.imgespark.com/pics/20131217/b6619.jpg',
                'http://cache.imgespark.com/pics/20131217/b6620.jpg',
                'http://cache.imgespark.com/pics/20131217/b6621.jpg',
                'http://cache.imgespark.com/pics/20131217/b6622.jpg',
                'http://cache.imgespark.com/pics/20131217/b6623.jpg',
                'http://cache.imgespark.com/pics/20131217/b6624.jpg',
                'http://cache.imgespark.com/pics/20131217/b6625.jpg',
                'http://cache.imgespark.com/pics/20131217/b6626.jpg',
                'http://cache.imgespark.com/pics/20131217/b6627.jpg',
                'http://cache.imgespark.com/pics/20131217/b6628.jpg',
                'http://cache.imgespark.com/pics/20131217/b6629.jpg',
                'http://cache.imgespark.com/pics/20131217/b6630.jpg']

        title = '赛车模特铃南穗花和两个猛男的激战【25p】'

        #指定文件路径
        path = os.getcwd()
        new_path = os.path.join(path, 'pictures/')
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
        new_path += '/' #此处需要和windows系统区分开

        image_couter = 1
        # 下载图片

        for img_url in links:
            file_name = '%s.jpg' % self.image_couter
            urllib.request.urlretrieve(str(img_url), new_path + file_name)
            self.image_couter += 1


    def start(self):
        myurls = [{'href':'/html/article/index28156.html', 'title':'赛车模特铃南穗花和两个猛男的激战【25p】'},
                {'href':'/html/article/index28155.html', 'title':'立花瑠莉 穿着和服做爱【33p】'},
                {'href':'/html/article/index28154.html', 'title':'沙发上的宫崎爱莉秀给你看【15p】'},
                {'href':'/html/article/index28153.html', 'title':'绝品美少妇愛乃まほろ 掰开给你看【16p】'},
                {'href':'/html/article/index28152.html', 'title':'渋谷晴美有一只乖巧精状的性奴【43p】'},
                {'href':'/html/article/index28151.html', 'title':'美少女女仆神田流菜的贴身服务【63p】'},
                {'href':'/html/article/index28150.html', 'title':'千野久留美cosplay演出【37p】'},
                {'href':'/html/article/index28080.html', 'title':'献身给一群男人的女忧;;【22P】'},
                {'href':'/html/article/index28079.html', 'title':'エッチし酔っしてててキス【14P】'},
                {'href':'/html/article/index28078.html', 'title':'我们都爱小泽那清新多变的画风;;【15P】'},
                {'href':'/html/article/index28077.html', 'title':'学体操的美女各种高难度【28P】'},
                {'href':'/html/article/index28076.html', 'title':'極品小女友到萬達工地來露出【14P】'},
                {'href':'/html/article/index28075.html', 'title':'騷逼挺嫩的真的很好玩啊【14P】'},
                {'href':'/html/article/index28073.html', 'title':'有一個愛騎馬的騷妻是什么體驗【14P】'},
                {'href':'/html/article/index28074.html', 'title':'小穴還可以湊合著看【14P】'},
                {'href':'/html/article/index28072.html', 'title':'看來女同事也是個淫蕩賤婦啊，毛那么多【15P】'},
                {'href':'/html/article/index28070.html', 'title':'到酒店抱起來操到她呻吟直叫主人好【16P】'},
                {'href':'/html/article/index28071.html', 'title':'粉嫩小穴長腿爆乳妹子,附生活照【16P】'},
                {'href':'/html/article/index28069.html', 'title':'絲襪的美感絲絲入心，美感小騷逼【17P】'},
                {'href':'/html/article/index28068.html', 'title':'早熟你不喜歡的人【17P】'}]


if __name__ == '__main__':
    spider = picDown()
    spider.grap_image()
