# 导入需要用到的库#####

import requests
import re
from bs4 import BeautifulSoup
from lxml import etree
import sqlite3

#获取请求头，防止被网页当作爬虫而被拒绝访问
head={'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
,'Cookie': '__mta=142472077.1596036514995.1596036514995.1596036943584.2; uuid_n_v=v1; uuid=29C64390D1B011EA915A0DDBDFA8C0BC14F15ACF43AA4637BDD9BB685B2A0DE6; _csrf=9e3eb1f7bcac759957631d2419179e073d68c1f14d8d7785211d3a6bee549b5b; Hm_lvt_703e94591e87be68cc8da0da7cbd0be2=1596036514; mojo-uuid=9c0ad753bc911528ca871291d6556bb3; _lxsdk_cuid=1739b308494c8-006eaee26f535e-31657305-13c680-1739b308494c8; _lxsdk=29C64390D1B011EA915A0DDBDFA8C0BC14F15ACF43AA4637BDD9BB685B2A0DE6; mojo-session-id={"id":"b9361f0ff1b2dff8bcfaee7f49432ad0","time":1596036514974};'
           ' Hm_lpvt_703e94591e87be68cc8da0da7cbd0be2=1596036943; mojo-trace-id=3; _lxsdk_s=1739b308496-04b-643-594%7C%7C4'

}
posters=re.compile('<img alt=".*class="avatar" src="(.*?)"/>',re.S)#正则提取海报链接
names=re.compile('<h1 class="name">(.*?)</h1>',re.S)                #提取电影名称
synopsis=re.compile('<span class="dra">(.*?)</span>',re.S)          #提取电影简介

base_url="https://maoyan.com"                                       #先获取网站的首页URL，用来下面拼接
#定义获取所有页面的URL方法
def get_url():
    urls=[]
    for i in range(10):
        #找到URL的规律，用循环十次的方法找到URL
        url="https://maoyan.com/board/4?offset={}"
        url=url.format(i*10)
        resp = requests.get(url, headers=head)
        html = resp.content.decode('utf-8')         #将获取的网页内容编码

        html = etree.HTML(html)                     #用etree解析获取的网页
        hrefs = html.xpath('//p[@class="name"]/a/@href')#用xpath方法提取网页中的一部电影的url，此时不完整
        for href in hrefs:
            href=base_url+href                      #通过网页首页的baseurl拼接成一个电影详情URL
            urls.append(href)
    return urls




#定义获取电影详情的函数
def get_detail_mes():
    movies=[]
    urls=get_url()                       #将retur出来的URL传入函数
    for url in urls:                     # for url in urls:#一个URL一部电影
        movie = []                       #创建一个空列表用来把下面爬到的数据作为movies列表里面的一个元素，方便遍历存入数据库
        movie.append(url)
        response=requests.get(url,headers=head)
        html=response.content.decode('utf-8')
        html=BeautifulSoup(html,"lxml")
        items_1=str(html.find_all('div',class_="wrapper clearfix"))#正则表达式是对字符串进行操作，这里转成str
        poster=posters.findall(items_1)[0]                          #利用上面的正则规则进行提取
        movie.append(poster)
        name=names.findall(items_1)[0]
        movie.append(name)
        items_2=str(html.find_all('div',class_="main-content"))
        synopsi=synopsis.findall(items_2)[0]
        movie.append(synopsi)
        movies.append(movie)
    return movies
def creatdb():
    conn=sqlite3.connect("cat_movie.db")
    cur=conn.cursor()
    sql='''
    create table cat(id int AUTO_INCREMENT ,
    movieurl varchar not null,
    moviepost varchar no null ,
    moviesynopsis varchar not null 
    )
    
    '''
    cur.execute(sql)
    conn.commit()
    cur.close()
    conn.close()
def save_movies():
    movies=get_detail_mes()
    conn=sqlite3.connect("cat_movie.db")
    cur=conn.cursor()
    for movie in movies:
        sql='''
        insert into cat(movieurl,moviepost,moviesynopsis)
        values ("%s","%s","%s")'''%(movie[0],movie[1],movie[2])
        cur.execute(sql)
        conn.commit()
    cur.close()
    conn.close()












if __name__ == '__main__':
    # creatdb()
    # get_detail_mes()
    save_movies()

