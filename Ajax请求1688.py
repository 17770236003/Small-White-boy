# import requests
# from lxml import etree
# import re
# import csv
# from bs4 import BeautifulSoup
# import selenium
# class Spider(object):
#     def __init__(self,url):
#         self.url=url
#         self.headers={
#             'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36',
#             'cookie': 'cna=8EWoF1lA7yACAToX7qozIwqE; UM_distinctid=173afe36483b3-07a6b1c5426649-31657305-13c680-173afe36484d60; taklid=5aeb1821673c4a578f4f81babbe16b82; ali_ab=58.23.238.170.1596655288254.6; cookie2=186bb92887e7f1d15c5d1170b0a58834; t=6067f446e49c540aa4a6ad941b7fac43; _tb_token_=38e636537ee33; __cn_logon__=false; _csrf_token=1597462879701; alicnweb=touch_tb_at%3D1597603936901; tfstk=cdklB3gIJr_6BVNm1LwSYgRMqPROZGs4y2uS3YQH2bAuyoDViJ1V_X-Bir0op61..; l=eBOjUPImOapFEu2LBOfaourza779LIRYSuPzaNbMiOCPO3fH5Y8OWZu15jYMCnhVh6akR3rsvp1MBeYBcIvdDNPfCgpMGQkmn; isg=BEREMZY-xw5a_3Nd0vMJ6m0yFcQ2XWjHPsRGY17lg4_SieRThm_YV3YrzCFRlKAf'
#         }
#     def get_html(self,url):
#         response=requests.get(url,headers=self.headers)
#         return response.content
#     def parser(self,html):
#         # html=BeautifulSoup(html,'lxml')
#         # html.select()
#         # html.find_all()
#         html=etree.HTML(html)
#         # html.xpath()
#         print(etree.tostring(html))
#         # return mes
#     def save(self,mes):
#         fp=open('1688.csv','w')
#         writer=csv.writer(fp)
#         writer.writerow([])
#     def run(self):
#         if 1:
#             pass
#         self.get_html()
#         self.parser()
#         self.save()
# if __name__ == '__main__':
#     url="https://show.1688.com/pinlei/industry/pllist.html?spm=a260j.12536015.jr60bfo3.1.293d700epQXSha&&sceneSetId=857&sceneId=2140&bizId=4386"
#     spider = Spider(url)
#     spider.parser(spider.get_html(url))
import requests
import json
from jsonpath import jsonpath
import csv
import headers
import re
import pandas as pd

'''
思路：
1.分析1688网站，数据都是通过ajax异步请求
2.找到xhr接口获取数据URL，找到URL规律
3.请求URL获取json数据
4.提取数据
5.保存数据

'''


# 创建爬虫
class Spider(object):
    def __init__(self, url):
        self.url = url

    # 封装公用函数
    def comment(self):
        data = json.loads(requests.get(self.url, headers=headers.head()).content.decode())
        titles = jsonpath(data, '$..information.subject')
        goods_titles = []
        # 获取的title中间有标签，用正则替换，重新加入空列表
        for title in titles:
            title = str(title)
            name = re.sub(re.compile('<.*?>'), '', title)
            goods_titles.append(name)
        images = jsonpath(data, '$..offerList..image.imgUrl')
        prices = jsonpath(data, '$..offerPrice.valueString')
        detail_url = jsonpath(data, '$..information.detailUrl')
        # 写入CSV
        writer.writerows([[goods_titles], [images], [prices], [detail_url]])
        # data_fram = pd.DataFrame({'商品名': goods_titles, '商品图片': images, '商品价格': prices, '商品链接': detail_url})
        # data_fram.to_csv(r'1688.csv', sep='，')

    def run(self):
        for i in range(1, 8):
            index = 0
            self.url = base_url.format(str(i), str(index))
            self.comment()
            while index < 2:
                index += 1
                self.url = base_url.format(str(i), str(20 * index))
                self.comment()


if __name__ == '__main__':
    base_url = 'https://search.1688.com/service/marketOfferResultViewService?select-faker=products&keywords=%C5%AE%D7%B0&n=y&mastheadtype=&from=industrySearch&industryFlag=&beginPage={}&async=true&asyncCount=20&pageSize=60&startIndex={}&offset=8'
    fp = open('1688.csv', 'a+')
    writer = csv.writer(fp)
    writer.writerow(['商品名称', '商品图片', '商品价格', '商品链接'])
    spider = Spider(base_url)
    spider.run()
