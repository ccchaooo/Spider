#! -*-coding:utf-8 -*-

from urllib import request, parse

from bs4 import BeautifulSoup

import time

import datetime

import json


# boss直聘的url地址，默认成都

#循环查询应聘者列表
def read_page(page_num):  # 模仿浏览器

    url_search = r'https://www.zhipin.com/boss/search/geeks.json'

    page_headers = {

        'Host': 'www.zhipin.com',

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36 '

                      'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'cookie':'sid=sem_pz_bdpc_dasou_title; __g=sem_pz_bdpc_dasou_title; __c=1539183475; lastCity=101270100; JSESSIONID=""; t=qGrx2XdmwhVMgOAs; wt=qGrx2XdmwhVMgOAs; __l=r=https%3A%2F%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_title&l=%2Fsignup.zhipin.com%2F%3Fintent%3D1%26ka%3Dheader-boss&g=%2Fwww.zhipin.com%2F%3Fsid%3Dsem_pz_bdpc_dasou_ti; __a=68769265.1539183467.1539183467.1539183475.21.2.20.21; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1539183470; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1539186519',

        'Connection': 'keep-alive'

    }
    data = {}
    data['page'] = page_num
    data['source'] = ' 1'
    data['keywords'] = '客服'
    data['experience'] = 104
    data['degree'] = 202
    data['salary'] = 404
    data['school211'] = 0
    data['_'] = ' 1539184262242'

    page_data = parse.urlencode(data)

    req = request.Request(url_search, headers=page_headers)

    page = request.urlopen(req, data=page_data.encode('utf-8')).read()

    page = page.decode('utf-8')
    # print(page)

    htmlList = json.loads(page)['htmlList']
    return htmlList


#循环读取每个列表中的应聘者简历
def get_detail(htmlList):  # 模仿浏览器
    url_info = 'https://www.zhipin.com/boss/search/geek/info'
    page_headers = {

        'Host': 'www.zhipin.com',

        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36 '

                      'Chrome/45.0.2454.85 Safari/537.36 115Browser/6.0.3',
        'cookie':'sid=sem; __g=sem; Hm_lvt_194df3105ad7148dcf2b98a91b5e727a=1539220833; __c=1539220844; __l=r=https%3A%2F%2Fwww.zhipin.com%2Fuser%2Fsem7.html%3Fsid%3Dsem%26utm_source%3Dbaidu%26utm_medium%3Dcpc%26utm_campaign%3DPC-yixian-pinpaici-2C%26utm_content%3DBOSSzhipin-hexin%26utm_term%3DBOSSzhipinwangzhan&l=%2Flogin.zhipin.com%2F&g=%2Fwww.zhipin.com%2Fuser%2Fsem7.html%3Fsid%3Dsem%26utm_source%3Dbaidu%26utm_medium%3Dcpc%26utm_campaign%3DPC-yixian-pinpaici-2C%26utm_content%3DBOSSzhipin-hexin%26utm_term%3DBOSSzhipinwangzhan; lastCity=101270100; JSESSIONID=""; t=qGrx2XdmwhVMgOAs; wt=qGrx2XdmwhVMgOAs; Hm_lpvt_194df3105ad7148dcf2b98a91b5e727a=1539227846; __a=85195660.1539220841.1539220841.1539220844.17.2.16.17',
        'Connection': 'keep-alive'

    }
    # 存放该列表中每个用户的信息
    users = []

    soup = BeautifulSoup(htmlList,'lxml')

    link_a_list = soup.find_all('a')

    # 循环列表
    for index, item in enumerate(link_a_list):

        time.sleep(1)  # 休眠0.2秒

        # 以字面量的形式定义dict
        data = dict()
        # 获取数据

        data['jid'] = 0
        data['segs'] = '客服'
        data['suid'] = item.get('data-suid')
        data['lid'] = item.get('data-lid')
        data['expectId'] = item.get('data-expect')
        data['ka'] = item.get('ka')

        page_data = parse.urlencode(data)

        req = request.Request(url_info, headers=page_headers)

        # 详细数据
        page = request.urlopen(req, data=page_data.encode('utf-8')).read()

        page = page.decode('utf-8')

        users.append(page)

        break

    # 返回列表
    return users


def savefile(info, soup):
    t = time.time()

    nowTime = lambda: int(round(t * 1000))

    # title = '学历:%s_年龄:%s_工作年限:%s_状态:%.html' % (info['age'], info['experience'], info['degree'], info['status'])
    title = '学历_' + info['degree'] + '__年龄_' + info['age'] + '__工作年限_' + info['experience'] + '__状态_' + info[
        'status'] + str(nowTime()) + '.html'

    # 保存文件
    print(str(datetime.datetime.now()) + ': 正在保存简历....')

    try:
        with open(title, 'w') as f:  # 在当前路径下，以写的方式打开一个名为 title，如果不存在则创建
            f.write(str(soup))  # 将text里的数据写入到文本中
    except IOError:
        print('except:')
    else:
        f.close()


def startgrap():

    for j in range(1, 10):
      #循环列表 读取有效数据
        users = get_detail(read_page(j))
        for user in users:
            time.sleep(5)
            soup = BeautifulSoup(user, 'lxml')

            # 详细信息 ,命名
            info = dict()
            if len(soup.select('.info-labels ')) > 0:
                items = soup.select('.info-labels ')[0].find_all('span')
                if len(items) == 0:
                    continue
                info['age'] = str(items[0]).replace('<span class="label-text"><i class="fz fz-age"></i>', '').replace(
                    '</span>', '')
                if len(items) == 1:
                    savefile(info, soup)
                    continue
                info['experience'] = str(items[1]).replace('<span class="label-text"><i class="fz fz-experience"></i>',
                                                           '').replace('</span>', '')
                if len(items) == 2:
                    savefile(info, soup)
                    continue
                info['degree'] = str(items[2]).replace('<span class="label-text"><i class="fz fz-degree"></i>',
                                                       '').replace('</span>', '')
                if len(items) == 3:
                    savefile(info, soup)
                    continue
                info['status'] = str(items[3]).replace('<span class="label-text"><i class="fz fz-status"></i>',
                                                       '').replace('</span>', '')
                savefile(info, soup)

if __name__ == '__main__':

    startgrap()

    print('下载结束')
