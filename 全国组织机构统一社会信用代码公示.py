# coding=utf-8
import re
import time
import json
import requests


'''
一、首先清空该网站所有cookies， 然后在搜索框输入任意关键字(例如 土豆)然后点击搜索开始捉包、并且点解怕preserve log进行日志保存
二、然后点击搜索之后会弹出一个滑动验证码、该验证码由极验提供
三、验证码通过后就会看到最终需要请求的网页https://ss.cods.org.cn/latest/searchR?q=%25E5%259C%259F%25E8%25B1%2586&t=common&currentPage=1&searchToken=&geetest_challenge=aded20c94d8c571619b401f6e8670c2a95&geetest_validate=4134ebbc5895f35bde0505adabb6572b&geetest_seccode=4134ebbc5895f35bde0505adabb6572b|jordan

	这里个url需要传入5个参数、第一个参数q为关键字即土豆、第二个关键字currentPage为页数、第三个参数geetest_challenge
	geetest_challenge这个参数是通过对https://ss.cods.org.cn/isearch进行post请求获取的、并且有两个参数sign和jsonString、而这两个参数又需要通过对https://www.cods.org.cn/cods/ajax/invoke该url进行post请求从而得到response信息、从信息中获取这两个参数

		所以流程就是：
			一、先get请求首页https://www.cods.org.cn
			二、然后post请求https://www.cods.org.cn/cods/ajax/invoke并且带上四个固定参数、keywordk为关键字 然后返回sign和jsonString
			三、再然后post请求https://ss.cods.org.cn/isearch、带上刚刚返回的sign和jsonString作为参数、并通过正则表达式得到返回值challenge和gt两个参数


'''


headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.25 Safari/537.36 Core/1.70.3704.400 QQBrowser/10.4.3587.400"
}


def get_detail(word, page):
    """
    :param word: 关键词
    :param page: 页数
    :return:
    """
    s = requests.Session()
    # 请求首页
    r = s.get('https://www.cods.org.cn', headers=headers)
    # r.encoding = "utf-8"
    # print(r.content.decode('gbk', 'ignore'))
    # print(r.headers)

    data = {
        "_ZVING_METHOD": "search/query",
        "_ZVING_URL": "%2F",
        "_ZVING_DATA": """{{"type":"1","keywords":"{}"}}""".format(word),
        "_ZVING_DATA_FORMAT": "json"
    }

    r = s.post('https://www.cods.org.cn/cods/ajax/invoke', headers=headers, data=data)
    # print(r.text)
    sign = json.loads(r.text).get('sign')
    jsonString = json.loads(r.text).get('jsonString')
    # print(sign)
    # print(jsonString)

    data = {
        "sign": sign,
        "jsonString": jsonString
    }

    r = s.post('https://ss.cods.org.cn/isearch', headers=headers, data=data)
    # print(r.text)
    challenge, gt = re.findall('eval\(\'\({"challenge":"(.*?)","gt":"(.*?)",', r.text)[0]
    print("challenge:", challenge)
    print("gt:", gt)

    # validate = input('validate:')
    # seccode = validate + "|jordan"
    # url = "https://ss.cods.org.cn/latest/searchR?q={3}&t=common&currentPage={4}&searchToken=&geetest_challenge={0}&geetest_validate={1}&geetest_seccode={2}".format(challenge, validate, seccode, word, page)

    # headers1 = {
    #     "Accept":"text/html, application/xhtml+xml, image/jxr, */*",
    #     "Accept-Encoding":"gzip, deflate",
    #     "Accept-Language":"zh-CN",
    #     "Connection":"Keep-Alive",
    #     "Host":"ss.cods.org.cn",
    #     "Referer":"https://ss.cods.org.cn/isearch",
    #     "User-Agent":"Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko Core/1.70.3704.400 QQBrowser/10.4.3587.400",
    # }
    # r = s.get(url, headers=headers1)
    # print(r.text)
    # print(url)
    # print(r.url)


if __name__ == '__main__':
    word = "土豆"
    get_detail(word, 2)
