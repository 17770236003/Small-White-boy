import requests
from lxml import etree
import csv
#创建爬虫
class Spider(object):
    # 初始化URL，请求头部信息
    def __init__(self,url):
        self.url=url
        self.headers={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
        ,'Cookie': 'GANJISESSID=2ne2jj1oqpcs8gasioe0ev2ok6; use_https=1; lg=1; ganji_uuid=2649999485670854618757; _gl_tracker=%7B%22ca_source%22%3A%22www.baidu.com%22%2C%22ca_name%22%3A%22-%22%2C%22ca_kw%22%3A%22-%22%2C%22ca_id%22%3A%22-%22%2C%22ca_s%22%3A%22seo_baidu%22%2C%22ca_n%22%3A%22-%22%2C%22ca_i%22%3A%22-%22%2C%22sid%22%3A72499990146%7D; __utmc=32156897; __utmz=32156897.1597320500.1.1.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ganji_xuuid=6a3997b5-ced7-43b7-f46a-8dbab0c4d6d6.1597320500222; gj_footprint=%5B%5B%22%5Cu79df%5Cu623f%22%2C%22http%3A%5C%2F%5C%2Fsz.ganji.com%5C%2Ffang1%5C%2F%22%5D%5D; citydomain=sz; __utma=32156897.1388972609.1597320500.1597320500.1597325585.2; __gads=ID=8946c401b429e5e7:T=1597325585:S=ALNI_Ma6qp4VXODCSGnL8RnMoQU78Ii1JA; __utmt=1; ganji_login_act=1597328162272; __utmb=32156897.18.10.1597325585'
        }
    #传入URL，发送请求，解析源文件
    def get_html(self,url):
        html = requests.get(url, headers=self.headers).content
        html = etree.HTML(html)
        return html
    #用xpath筛选信息
    def parse_html(self,html):
        houses = []
        items = html.xpath('//dl[@class="f-list-item-wrap min-line-height f-clear"]')
        for item in items:
            sigle_house = []
            title = item.xpath('./dd[@class="dd-item title"]/a')[0].text
            sigle_house.append(title)
            price = item.xpath('./dd[@class="dd-item info"]/div/span')[0].text
            sigle_house.append(price)
            address = item.xpath('./dd[@class="dd-item address"]/span/a')[0].text
            sigle_house.append(address)
            mes = item.xpath('./dd[@class="dd-item size"]/span')
            #用的xpath方法，这里房子简介位于不同的span标签，定义这个方法拼接简介信息
            m = ''
            for me in mes:
                if me.text:
                    m += str(me.text) + ' '
            sigle_house.append(m)
            houses.append(sigle_house)
        #最后一页获取不到URL，会报错，将NONE赋值
        try:
            next_url=html.xpath('//a[contains(@class,"next")]/@href')[0]
        except:
            next_url=None
        return houses,next_url
    #创建保存函数
    def save(self,houses):
        fp=open('ganji.csv','a+')
        writer = csv.writer(fp)
        #创建CSV文件头部信息
        house_head=["房子名称","房子价格","房子地段","房子简介"]
        writer.writerow(house_head)
        for house in houses:
            writer.writerow([house[0], house[1], house[2], house[3]])
        #用完关闭
        fp.close()


    def run(self):
        next_url=self.url
        #循环爬取
        while True:
            #判断next_url是否存在，在则执行，不存在则break
            if next_url:
                html=self.get_html(next_url)
                houses,next_url=self.parse_html(html)
                self.save(houses)
            else:
                break



if __name__ == '__main__':
    #初始URL
    url="http://sz.ganji.com/zufang"
    spider = Spider(url)
    spider.run()