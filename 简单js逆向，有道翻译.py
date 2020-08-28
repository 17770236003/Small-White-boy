import random
import time
from hashlib import md5
from jsonpath import jsonpath
import requests

'''
思路：
1.分析有道翻译的网页
2.找到翻译动作接口，发现是post请求，分析参数
3.通过几次点击翻译按钮，发现变化的三个参数 lts、salt、sign
4.lts、salt都是时间戳函数 r = "" + (new Date).getTime() ,salt: i, sign: n.md5("fanyideskweb" + e + i + "]BjuETDhU)zqSxf-=B#7m")
5、sign与bv参数都是通过md5函数加密，但是bv不变，不必分析。
6.分步复写pytho代码，生成参数
7.发送请求，获取数据
'''


def get_data(word):
    # 获取数据生成方法，模拟生成，python时间戳是10位数，这里是13位，所以乘1000
    lts = str(int(time.time() * 1000))
    # i = r + parseInt(10 * Math.random(), 10)，此处是0，9之间转str，js是字符串加上任意类型都是字符串，NAN等除外
    salt = lts + str(random.randint(0, 9))
    return {
        "ts": lts,
        "salt": salt,
        # 模拟加密
        "sign": md5(str("fanyideskweb" + word + salt + "]BjuETDhU)zqSxf-=B#7m").encode()).hexdigest()
    }


def fan_yi(word):
    data = get_data(word)
    # 重点：一定注意双引号，中间不能包含空格，本人debug花了将近两天才搞出来，汗颜~~
    pars = {
        "i": word,
        "from": "AUTO",
        "to": "AUTO",
        "smartresult": "dict",
        "client": "fanyideskweb",
        "salt": data["salt"],
        "sign": data["sign"],
        "lts": data["ts"],
        "bv": "8383a5327f9285a941fdc7ae1aec5449",
        "doctype": "json",
        "version": "2.1",
        "keyfrom": "fanyi.web",
        "action": "FY_BY_REALTlME",

    }
    # 用jsonpath函数直接提取，更加方便
    resp = requests.post(url=url, data=pars, headers=headers).json()
    print("待翻译的内容：", jsonpath(resp, "$..tgt")[0], "\n", "翻译后的内容：", jsonpath(resp, "$..src")[0])


if __name__ == '__main__':
    url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'
    #三个参数都要带
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.135 Safari/537.36",
        "Cookie": "OUTFOX_SEARCH_USER_ID=-389257787@10.108.160.100; OUTFOX_SEARCH_USER_ID_NCOO=1759635714.0944908; JSESSIONID=aaaOgGagLGPWs_pe4L1qx; ___rl__test__cookies=1598626971658",
        "Referer": "http://fanyi.youdao.com/"
    }
    while True:
        word = input('请输入要翻译的内容：')
        fan_yi(word)
