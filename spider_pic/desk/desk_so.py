#-*-coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
from lxml import etree
import os

'''
使用beautifulsoup下载图片
1、使用urllib.request 下载到网页内容
2、使用beautifulsoup匹配到所有的图片地址
3、指定文件路径
4、调用urllib.request.urlretrieve 下载图片
'''
# http://desk.zol.com.cn/fengjing/1366x768/

class picDown:
    def __init__(self):
        self.appname = 'http://desk.zol.com.cn'
        self.nextPage = None
        self.firstPage = 'http://desk.zol.com.cn/fengjing/1366x768/'
        self.image_couter = 1
        self.page_counter = 0


    def getpics(self, url,name):
        # 如果第一次下载,则从首页开始
        html = urllib.request.urlopen(self.appname + url)
        content = html.read()
        html.close()

        # 使用beautifulsoup匹配图片
        html_soup = BeautifulSoup(content, 'lxml')
        all_img_links = html_soup.select('#showImg img')

        #指定文件路径
        path = os.getcwd()
        new_path = os.path.join(path, 'pictures')
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
        new_path += '/' #此处需要和windows系统区分开

        # 下载图片
        self.image_couter = 1
        for img_link in all_img_links:
            # 判断属性src/srcs是否村子
            if img_link.get('src') is not None:
                img = img_link.get('src')
            elif img_link.get('srcs') is not None:
                img = img_link.get('srcs')
            else:
                continue

            file_name = '%s.jpg' % (name + str(self.image_couter))

            #缩略图替换成原图
            img_url = img.replace('t_s144x90c5', 't_s960x600c5')
            if len(img_url) > 0:
                urllib.request.urlretrieve(img_url, new_path + file_name)
                self.image_couter += 1

    # 获取所有相册
    def getallclass(self, url):
        html = urllib.request.urlopen(url)
        content = html.read()
        html.close()

        # 使用beautifulsoup匹配图片
        soup = BeautifulSoup(content, 'lxml')
        classes = soup.select('.photo-list-padding')
        for x in classes:
            self.getpics(x.find('a').get('href'), x.find('img').get('alt'))

    def start(self):
        while self.page_counter < 2:
            if self.nextPage is None:
                url = self.firstPage
            else:
                url = self.nextPage

            #获取当前页所有相册的地址
            self.getallclass(url)

            html = urllib.request.urlopen(url)
            content = html.read()
            html.close()

            soup = BeautifulSoup(content, 'lxml')
            next = soup.select('#pageNext')
            if len(next) > 0:
                self.nextPage = self.appname + next[0].get('href')
                # print(self.nextPage)

            self.page_counter += 1


if __name__ == '__main__':
    spider = picDown()
    spider.start()
