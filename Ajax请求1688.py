
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
        #突然发现pandas写更好。
        data = pd.DataFrame({'商品名称': goods_titles, '商品图片': images, '商品价格': prices, '商品链接': detail_url})
        data.to_csv('1688.csv', sep=',', mode='a')
        # 写入CSV
#         writer.writerows([[goods_titles], [images], [prices], [detail_url]])
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
#     fp = open('1688.csv', 'a+')
#     writer = csv.writer(fp)
#     writer.writerow(['商品名称', '商品图片', '商品价格', '商品链接'])
    spider = Spider(base_url)
    spider.run()
