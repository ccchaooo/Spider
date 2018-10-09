#-*-coding: utf-8 -*-

import urllib.request
from bs4 import BeautifulSoup
import os

'''
使用beautifulsoup下载图片
1、使用urllib.request 下载到网页内容
2、使用beautifulsoup匹配到所有的图片地址
3、指定文件路径
4、调用urllib.request.urlretrieve 下载图片
'''


class picDown:
    def __init__(self):
        self.nowPage = 1
        self.endpage = 266
        self.image_couter = 1


    def grap_image(self):
        # 下载网页
        url = 'http://www.7160.com/qingchunmeinv/list_2_'+str(self.nowPage)+'.html'
        html = urllib.request.urlopen(url)
        content = html.read()
        html.close()

        # 使用beautifulsoup匹配图片
        html_soup = BeautifulSoup(content, 'lxml')
        all_img_links = html_soup.find_all('img',)
        # print(all_img_links)

        #指定文件路径
        path = os.getcwd()
        new_path = os.path.join(path, 'pictures')
        if not os.path.isdir(new_path):
            os.mkdir(new_path)
        new_path += '/' #此处需要和windows系统区分开

        # 下载图片
        for img_link in all_img_links:

            file_name = '%s.jpg' % self.image_couter
            img_url = img_link['src']
            if len(img_url) > 0:
                urllib.request.urlretrieve(img_url, new_path + file_name)
                self.image_couter += 1

    def start(self):
        while self.nowPage < self.endpage:
            self.nowPage += 1
            self.grap_image()
        print('下载完成')
        return


if __name__ == '__main__':
    spider = picDown()
    spider.start()

