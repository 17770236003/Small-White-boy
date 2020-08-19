import random
import time
import requests
import re
import csv
from lxml import etree
class DZ(object):
    #初始化信息
    def __init__(self,headers,url):
        self.headers=headers
        self.url=url
    #创建获取免费代理的方法，这里只获取快代理第一页
    def  get_ip(self):
        url='https://www.kuaidaili.com/free/'
        resp=requests.get(url,headers=self.headers).content.decode('utf-8')
        html=etree.HTML(resp)
        ips=html.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr/td[1]/text()')
        ports=html.xpath('//table[@class="table table-bordered table-striped"]/tbody/tr/td[2]/text()')
        dls=list(zip(ips,ports))
        nums=[]
        #访问百度，验证代理是否可用
        for ip,port in dls:
            num={'http':'{}:{}'.format(ip,port)}
            print(num)
            try:
                response=requests.get('http://www.baidu.com',proxies=num,timeout=3)
                if response.status_code==200:
                    print('代理可用')
                    nums.append(num)
            except:
                print('这个代理无效')
                continue
        return nums
    #传入URL获取源代码
    def get_html(self,url):
        nums=self.get_ip()
        #从代理池中随机选出一个代理
        ip=random.sample(nums,1)
        try:
            html=requests.get(url,headers=self.headers,proxies=ip,timeout=5)
            if html.status_code==200:
                return html.content.decode('utf-8')
        except:
            print('请求失败！')
    #解析源代码，提取信息
    def parse(self, html):
        messages=[]
        html = etree.HTML(html)
        items = html.xpath('//div[@id="shop-all-list"]/ul/li')
        #一个li标签就是一个商家信息
        for item in items:
            message = []
            #获取店铺名称
            title = item.xpath('./div[@class="txt"]/div/a/h4/text()')[0]
            message.append(title)
            #获取介绍图
            pic = item.xpath('./div[@class="pic"]/a/img')[0].get('src')
            #这里图片有两种，一种JPG结尾的是高清大图，有后缀的是缩略图，取大图，判断
            if pic.endswith('jpg') or pic.endswith('png'):
                img = pic
                message.append(img)
            else:
                img = re.compile(r'(.*?)%.*', re.S)
                img = img.findall(pic)[0]
                message.append(img)
            #获取店铺评分
            score = item.xpath('./div[@class="txt"]/div[@class="comment"]/div/div[2]/text()')[0]
            message.append(score)
            #获取商家推荐菜品
            dishs= item.xpath('./div[@class="txt"]/div[@class="recommend"]/a[@class="recommend-click"]/text()')
            message.append(dishs)
            #获取商家链接
            link = item.xpath('./div[@class="txt"]/div[@class="tit"]/a')[0].get('href')
            message.append(link)
            messages.append(message)
        #判断是否是最后一页，不是则继续，是就返回空
        try:
            next_url=html.xpath('//a[@class="next"]')[0].get('href')
        except:
            next_url=None
        return messages,next_url
    #创建一个保存数据的CSV文件，先创建表头防止后面重复创建
    def creat_head(self):
        fp = open('大众点评美食篇.csv', 'a+')
        writer = csv.writer(fp)
        writer.writerow(["店名", "图片", "评分", "菜类推荐", "店铺链接"])
        fp.close()
        return fp,writer
    #创建保存数据方法，保存数据
    def save(self,messages):
        fp = open('大众点评美食篇.csv', 'a+')
        writer=csv.writer(fp)
        for message in messages:
            print('正在保存。。。')
            writer.writerow([message[0],message[1],message[2],message[3],message[4]])
        fp.close()
    #创建运行函数
    def run(self):
        next_url=self.url
        self.creat_head()
        while True:
            if next_url:
                try:
                    html = self.get_html(next_url)
                    messages, next_url = self.parse(html)
                    self.save(messages)
                    time.sleep(2)
                except:
                    print('请求网页出错！')
                    break
            else:
                print('保存完毕！！')
                break


if __name__ == '__main__':
    headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.125 Safari/537.36'
,'Cookie': 'fspop=test; cy=15; cye=xiamen; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_cuid=17404b76642c8-0cc82828a8b0c4-31677305-13c680-17404b76642c8; _lxsdk=17404b76642c8-0cc82828a8b0c4-31677305-13c680-17404b76642c8; _hc.v=c4bdedb1-2fdd-f249-109f-ddde9402ac4b.1597806962; Hm_lvt_602b80cf8079ae6591966cc70a3940e7=1597806964; s_ViewType=10; Hm_lpvt_602b80cf8079ae6591966cc70a3940e7=1597806981; _lxsdk_s=17404b76643-ce8-70b-050%7C%7C65'
    }
    url = 'http://www.dianping.com/xiamen/ch10'
    spider=DZ(headers=headers,url=url)
    spider.run()
