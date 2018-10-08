# -*- coding: utf-8 -*-
# !usr/bin/env/python
# encoding:UTF-8

import urllib
import requests
import json
import os
import re
import time
# !usr/bin/env/python
# encoding:UTF-8

import urllib
import requests
import json
import os
import re
import time


class MMSpider:

    def __init__(self):
        self.__code_type = 'gbk'
        self.__http = 'http:'
        # 美人库动态加载xhr数据的url
        self.__url = 'http://mm.taobao.com/tstar/search/tstar_model.do?_input_charset=utf-8'
        # 模特主页地址
        self.__person_url = 'http://mm.taobao.com/self/aiShow.htm?userId='
        # 相册地址
        self.__all_album_url = 'https://mm.taobao.com/self/album/open_album_list.htm?_charset=utf-8&user_id%20='
        # 具体相册地址
        self.__pic_url = "https://mm.taobao.com/album/json/get_album_photo_list.htm?user_id="
        # 存储照片的基地址
        self.__save_path = 'F:\Beauty'
        # 想要获取的页数
        self.__total_page = 1
        # 当前正在提取的页数
        self.__currentPage = 1
        # 找到具体album的id的正则表达式
        self.__album_id_pattern = re.compile('''<h4>.*?album_id=(.*?)&''', re.S)
        # album有多少的的正则表达式

        # 找到具体album的id的正则表达式
        self.__album_page_pattern = re.compile('''<input name="totalPage" id="J_Totalpage" value="(.*?)"''', re.S)

    # 根据动态请求获取需要的第X页的json数据，找出userId
    def get_person_dict(self, currentPage):
        try:
            data = {
                "currentPage": currentPage
            }
            data = urllib.parse.urlencode(data).encode('utf-8')
            request = urllib.request.Request(self.__url, data=data)
            response = urllib.request.urlopen(request)
            result = response.read().decode(self.__code_type)
            return json.loads(result)
        except urllib.error.URLError as e:
            print('美人动态加载信息出错', e.reason)

    # 根据得到的userID,找到相册的总页数
    def get_album_page(self, userId):
        try:
            all_album_url = self.__all_album_url + str(userId)
            res = urllib.request.urlopen(all_album_url)
            html = res.read().decode(self.__code_type)
            return re.search(self.__album_page_pattern, html).group(1)
        except urllib.error.URLError as e:
            print('动态加载相册总信息出错', e.reason)
            return None

    # 由得到的相册总页数范围内指定的页数，获取该页所有相册的ID
    def get_album_ids(self, userId, page):
        try:
            all_album_url = self.__all_album_url + str(userId) + "&" + str(page)
            request = urllib.request.Request(all_album_url)
            response = urllib.request.urlopen(request)
            html = response.read().decode(self.__code_type)
            # 提取该页中album的id
            return re.findall(self.__album_id_pattern, html)
        except urllib.error.URLError as e:
            print("提取相册id出错了！", e.reason)

    # 找到一个相册内的图片有多少页
    def get_pic_page(self, userId, albumId):
        try:
            # 先得到这个相册一共有多少页
            url = self.__pic_url + str(userId) + "&album_id=" + str(albumId)
            response = urllib.request.urlopen(url)
            result = json.loads(response.read().decode(self.__code_type))
            return result["totalPage"]
        except urllib.error.URLError as e:
            print(e.reason)
            return None

    # 根据相册图片页数获取指定页数的图片信息
    def get_img_url(self, person, j, album_id):
        url = self.__pic_url + str(person["userId"]) \
              + "&album_id=" + str(album_id) \
              + "&page=" + str(j)
        try:
            response = urllib.request.urlopen(url, timeout=5)
            result = response.read().decode(self.__code_type)
            imgs_url = json.loads(result)["picList"]
            return imgs_url
        except TimeoutError as e:
            print('1', e.strerror)
        except urllib.error.URLError as e:
            print('2', e.reason)
        except BaseException as e:
            print('3', e.args)

    # 保存model的个人信息
    def save(self, searchDOList):
        for person in searchDOList:
            dir_path = self.__save_path + '\\' + person['realName']
            if self.mkdir(dir_path):
                txt_path = dir_path + '\\' + person['realName'] + '.txt'
                self.write_txt(txt_path, person)
                self.save_imgs(person, dir_path)

    def mkdir(self, dir_path):
        if (os.path.exists(dir_path)):
            return False
        else:
            os.mkdir(dir_path)
            return True

    def write_txt(self, txt_path, person):
        person_url = self.__person_url + str(person['userId'])
        content = "姓名：" + person["realName"] + "  城市：" + person["city"] \
                  + "\n身高：" + str(person["height"]) + "  体重：" + str(person["weight"]) \
                  + "\n喜欢：" + str(person["totalFavorNum"]) \
                  + "\n个人主页：" + person_url
        with open(txt_path, 'w', encoding='utf-8')as file:
            print('正在保存%s的文字信息' % (person['realName']))
            file.write(content)
            file.close()

    def save_imgs(self, person, dir_path):
        album_page = self.get_album_page(person['userId'])
        print(album_page)
        img_index = 1
        for i in range(1, int(album_page) + 1):
            album_ids = self.get_album_ids(person["userId"], i)

            for album_id in album_ids:
                pic_page = self.get_pic_page(person["userId"], album_id)

                for j in range(1, int(pic_page) + 1):
                    img_urls = self.get_img_url(person, j, album_id)

                    for img_url in img_urls:
                        try:
                            url = self.__http + img_url["picUrl"]
                            res = urllib.request.urlopen(url, timeout=5)

                            with open(dir_path + '\\' + str(img_index) + '.jpg', 'wb') as file:
                                file.write(res.read())
                                if img_index % 10 == 0:
                                    print('sleep 1 second')
                                    time.sleep(1)
                                if img_index >= 11:
                                    print('%s已保存11张辣照' % person['realName'])
                                    file.close()
                                    return
                                img_index += 1
                        except TimeoutError as e:
                            print('1', e.strerror)
                        except urllib.error.URLError as e:
                            print('2', e.reason)

    def start(self):
        print("开始！")
        opener = urllib.request.build_opener()
        opener.addheaders = [("User-Agent",
                              "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.96 Safari/537.36")]
        urllib.request.install_opener(opener)
        for i in range(self.__total_page):
            dict_result = self.get_person_dict(self.__currentPage)
            searchDOList = dict_result["data"]["searchDOList"]

            # 保存所有本页中MM的信息
            self.save(searchDOList)
            self.__currentPage += 1


if __name__ == "__main__":
    spider = MMSpider()
    spider.start()

