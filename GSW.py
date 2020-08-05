import requests
from bs4 import BeautifulSoup
url="https://so.gushiwen.cn/user/login.aspx?from=http://so.gushiwen.cn/user/collect.aspx"
head={
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.105 Safari/537.36'
}
#发送请求的原因是获取登录接口，以及隐藏属性，验证码的 url。
#全程重点是保持请求跟下载的验证码一致。
res=requests.get(url,headers=head)
session=requests.session()

login_url='https://so.gushiwen.cn/user/login.aspx?from=http%3a%2f%2fso.gushiwen.cn%2fuser%2fcollect.aspx'
response=requests.get(url=login_url,headers=head)
response=response.content
soup=BeautifulSoup(response,"lxml")
#通过第一次访问发现登陆接口隐藏的两个属性，是动态变化的，所以获取属性的动态内容。
__VIEWSTATE=soup.select('#__VIEWSTATE')[0].attrs.get('value')
__VIEWSTATEGENERATOR=soup.select('#__VIEWSTATEGENERATOR')[0].attrs.get('value')

code_url='https://so.gushiwen.cn'+soup.select('#imgCode')[0].attrs.get('src')
#下载验证码图片。
with open('yzm.jpg',"wb")as f:
    f.write(session.get(code_url,headers=head).content)


code=input('验证码：')
#获取的动态属性内容作为参数传入。
data={
    "__VIEWSTATE": __VIEWSTATE,
    "__VIEWSTATEGENERATOR": __VIEWSTATEGENERATOR,
    "from": "http://so.gushiwen.cn/user/collect.aspx",
    "email": "#######",#账号
    "pwd": "######",#密码
    "code" :code ,
    "denglu": "登录"

}
resp=session.post(url,headers=head,data=data)
#有的浏览器返回的相应是bgk格式，这里统一为"UTF-8"。
resp.encoding='utf-8'
with open('gsw.html',"w",encoding='utf-8')as fp:
    fp.write(resp.text)
