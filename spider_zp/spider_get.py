#! -*-coding:utf-8 -*-

from urllib import request, parse

from bs4 import BeautifulSoup

import datetime

import json

starttime = datetime.datetime.now()

url = r'https://www.zhipin.com/boss/search/geeks.json'


# boss直聘的url地址，默认杭州


def read_page(url, page_num):  # 模仿浏览器

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
    data['jobs'] = '客服专员/助理'
    data['degree'] = 202
    data['_'] = ' 1539184262242'

    page_data = parse.urlencode(data)

    req = request.Request(url, headers=page_headers)

    page = request.urlopen(req, data=page_data.encode('utf-8')).read()

    page = page.decode('utf-8')
    print(page)

    htmlList = json.loads(page)['htmlList']
    print(htmlList)

    return json.dumps(htmlList)


if __name__ == '__main__':

    # for j in range(1, 2):
    # read_page(url, 1)
    soup = BeautifulSoup(read_page(url, 1))



    #
    # print('**********************************即将进行抓取**********************************')
    #
    # keyword = input('请输入您要搜索的职位：')
    #
    # workbook = xlwt.Workbook()
    #
    # sheet = workbook.add_sheet('sheet1')
    #
    # i = 0
    #
    # for j in range(1, 5):
    #
    #     soup = BeautifulSoup(read_page(url, j, keyword))
    #
    #     for link in soup.select('.company-text'):
    #         sheet.write(i, 0, link.get_text())
    #
    #         i = i + 1
    #
    # workbook.save("D:\\resultsLatest.xls")
    #
    # endtime = datetime.datetime.now()
    #
    # time = (endtime - starttime).seconds

    # print('总共用时：%s s' % time)
