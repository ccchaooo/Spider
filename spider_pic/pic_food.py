import urllib.request
import re


class qsbkClassCrawler:
    # 初始化方法，定义一些变量
    def __init__(self):
        self.pageIndex = 1
        self.user_agent = 'Mozilla/4.0 (compatible; MSIE 5.5; Windows NT)'
        # 初始化headers
        self.headers = {'User-Agent': self.user_agent}
        # 存放段子的变量，每一个元素是每一页的段子们
        self.stories = []
        # 存放程序是否继续运行的变量
        self.enable = False

        # 传入某一页的索引获得页面代码
    def getPage(self, pageIndex):
            try:
                url = 'http://www.qiushibaike.com/hot/page/' + str(pageIndex)
                # 构建请求的request
                request = urllib.request.Request(url, headers=self.headers)
                # 利用urlopen获取页面代码
                response = urllib.request.urlopen(request)
                # 将页面转化为UTF-8编码
                pageCode = response.read().decode('utf-8')
                return pageCode

            except urllib.request.URLError as e:
                if hasattr(e, "reason"):
                    print(u"连接糗事百科失败,错误原因", e.reason)
                    return None


    # 传入某一页代码，返回本页不带图片的段子列表
    def getPageItems(self, pageIndex):

        pageCode = self.getPage(pageIndex)
        if not pageCode:
            print("页面加载失败...")
            return None
        pattern = re.compile(
            '<h2>(.*?)</h2>.*?<div class="content">.*?<span>(.*?)</span>.*?<div class="stats.*?class="number">(.*?)</i>',
            re.S)
        items = re.findall(pattern, pageCode)
        pageStories=[]
        for item in items:
            pageStories.append([item[0].strip(),item[1].strip(), item[2].strip()])
        return pageStories

    # 加载并提取页面的内容，加入到列表中
    def loadPage(self):
        # 如果当前的页数少于两页，则加载新的一页
        if self.enable == True:
            if len(self.stories) < 2:
                #获取新的一页
                pageStories = self.getPageItems(self.pageIndex)
                # 将该页的段子存放到全局list中
                if pageStories:
                    self.stories.append(pageStories)
                    # 获取完之后页码索引加一，表示下次读取下一页
                    self.pageIndex += 1


    def getOneStory(self, pageStories, page):
        # 遍历一页的段子
        for story in pageStories:
            income = input('Please Input')
            # 每当输入回车一次，判断一下是否要加载新页面
            self.loadPage()
            if income == 'Q':
                self.enable = False
                return
            print("第%d页 作者%s段子内容%s 点赞数%s" % (page,story[0],story[1].replace("<br/>", "\n"),story[2]))
            # 记录下段子
            with open('文本.txt', 'a',encoding='utf-8') as f:  # 在当前路径下，以写的方式打开一个名为'文本.txt'，如果不存在则创建
                f.write("第%d页 作者%s \n段子内容:\n %s \n\n" % (page, story[0], story[1].replace("<br/>", "\n")))  # 将text里的数据写入到文本中

    def start(self):
        print("正在读取糗事百科，按回车查看新段子，Q退出")
        #使变量为true,程序可以正常运行
        self.enable=True
        #先加载一页内容
        self.loadPage()
        #局部变量，控制当前读了几页
        nowPage =0
        while self.enable:
            if len(self.stories) > 0:
                #从全局list中获取一页的段子
                pageStories= self.stories[0]
                #当前读到的页数加一
                nowPage +=1
                #将全局list中第一个元素删除,因为已经取出
                del self.stories[0]
                #输出该页的段子
                self.getOneStory(pageStories,nowPage)

if __name__ == "__main__":
    spider = qsbkClassCrawler()
    spider.start()
