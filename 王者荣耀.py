import requests
import json
import csv

'''
思路：
1.分析网页
2.找到英雄列表的json数据
3.找到英雄名称，皮肤个数
4.手动构造皮肤链接地址
5.下载皮肤，保存
'''


class WZ:
    def __init__(self, url):
        self.url = url

    def get_data(self):
        fp = open('王者荣耀皮肤.csv', 'a')
        writer = csv.writer(fp)
        writer.writerow(['英雄编号', '英雄名称', '英雄皮肤'])
        json_data = json.loads(requests.get(self.url).text)
        for data in json_data:
            try:
                skin_names = data['skin_name'].split('|')
                ename = data['ename']
                cname = data['cname']
            except Exception as e:
                print(e)
            for skin_num in range(len(skin_names)):
                img_url = 'http://game.gtimg.cn/images/yxzj/img201606/skin/hero-info/{}/{}-bigskin-{}.jpg'.format(ename, ename,skin_num + 1)
                img = requests.get(img_url).content
                with open('王者荣耀皮肤/' + '{}{}.jpg'.format(cname, skin_names[skin_num]), 'wb')as fp:
                    print('正在下载', cname, skin_names[skin_num])
                    fp.write(img)

    def run(self):
        self.get_data()


if __name__ == '__main__':
    url = 'https://pvp.qq.com/web201605/js/herolist.json'
    wz = WZ(url)
    wz.get_data()
