from threading import Thread
from queue import Queue
import requests
from lxml import etree
import headers
import csv
'''
思路：
<1 创建一个保存URL的队列容器，创建一个保存响应的队列容器
<2 创建请求类，返回响应，创建解析类，保存数据
<3 创建请求多线程，创建解析多线程

'''
#创建爬虫类，继承线程类
class Spider(Thread):
    def __init__(self,url_queue,parse_queue):
        #初始化线程
        Thread.__init__(self)
        self.url_queue=url_queue
        self.parse_queue=parse_queue

    def run(self):
        head=headers.head()
        #设置循环条件，如果队列中有URL，则循环继续
        while self.url_queue.empty()==False:
            response=requests.get(self.url_queue.get(),headers=head)
            self.parse_queue.put(response.content.decode('gb2312',"ignore"))


#创建解析类，继承线程类
class Parse(Thread):
    def __init__(self,parse_queue,writer):
        #初始化线程
        Thread.__init__(self)
        self.writer=writer
        self.parse_queue=parse_queue
    def run(self):
        #判断队列中是否有从上面传入的html，如果有则循环
        while self.parse_queue.empty()==False:
            html=self.parse_queue.get()
            html=etree.HTML(html)
            #xpath提取数据，获取每个同台图的标签，遍历解析
            heads=html.xpath('//div[@class="listgif-box"]')
            for head in heads:
                gifs=[]
                titles=head.xpath('./div[@class="listgif-title"]/h2/a/text()')[0]
                gifs.append(titles)
                goods=head.xpath('./div[@class="digg"]/a[1]/text()')[0]
                gifs.append(goods)
                bads=head.xpath('./div[@class="digg"]/a[3]/text()')[0]
                gifs.append(bads)
                img = head.xpath('./div[@class="listgif-giftu"]/p/img/@src')[0]
                gifs.append(img)
                #有的动态图没有标签描述，这里通过try将没有标签描述的赋值为None
                try:
                    bq=head.xpath('./div[@class="tagsinfo"]/div/a/text()')[0]
                    gifs.append(bq)
                except:
                    bq=None
                gifs.append(bq)
                #写入CSV文件
                self.writer.writerow([gifs[0],gifs[1],gifs[2],gifs[3],gifs[4]])

if __name__ == '__main__':
    url_queue=Queue()
    #为了不重复打开文件，这里创建传入writer
    fp = open('动态图/动态图.csv', 'a+')
    writer = csv.writer(fp)
    writer.writerow(['标题', '好评', '差评', '图片', '标签'])
    base_url="http://www.gaoxiaogif.com/index_{}.html"
    #传入多条URL
    for i in range(2,50):
        url=base_url.format(str(i))
        url_queue.put(url)
    parse_queue = Queue()
    spides=[]
    #创建5个线程来为爬虫类服务
    for i in range(5):
        spider=Spider(url_queue,parse_queue)
        spides.append(spider)
        spider.start()
    #线程插队，防止主进程结束线程
    for spider in spides:
        spider.join()

    parses=[]
    #创建5个线程为解析服务
    for i in range(5):
        parse=Parse(parse_queue,writer)
        parses.append(parse)
        parse.start()
    #同上
    for parse in parses:
        parse.join()
