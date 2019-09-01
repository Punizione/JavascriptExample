""" ------------------------------------------------- File Name： demo_1.py.py Description : Python爬虫—破解JS加密的Cookie 快代理网站为例：http://www.kuaidaili.com/proxylist/1/ Document: Author : JHao date： 2017/3/23 ------------------------------------------------- Change Activity: 2017/3/23: 破解JS加密的Cookie ------------------------------------------------- """
__author__ = 'JHao'

import re
import PyV8
import requests

TARGET_URL = "http://www.kuaidaili.com/proxylist/1/"

def getHtml(url, cookie=None):
    header = {
        "Host": "www.kuaidaili.com",
        'Connection': 'keep-alive',
        'Cache-Control': 'max-age=0',
        'Upgrade-Insecure-Requests': '1',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.87 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
        'Accept-Encoding': 'gzip, deflate, sdch',
        'Accept-Language': 'zh-CN,zh;q=0.8',
    }
    html = requests.get(url=url, headers=header, timeout=30, cookies=cookie).content
    return html

def executeJS(js_func_string, arg):
	# 创建一个jsContext对象并进入
    ctxt = PyV8.JSContext()
    ctxt.enter()
    # 然后eval一下想要执行的js的代码，或者包含你需要的js代码的源文件
    func = ctxt.eval("({js})".format(js=js_func_string))
    return func(arg)

def parseCookie(string):
    string = string.replace("document.cookie='", "")
    clearance = string.split(';')[0]
    return {clearance.split('=')[0]: clearance.split('=')[1]}

# 第一次访问获取动态加密的JS 该变量是一个js代码的字符串
first_html = getHtml(TARGET_URL)


# 提取其中的JS加密函数 获取整段
js_func = ''.join(re.findall(r'(function .*?)</script>', first_html))

print('get js func:\n', js_func)

# 提取其中执行JS函数的参数
js_arg = ''.join(re.findall(r'setTimeout\(\"\D+\((\d+)\)\"', first_html))

print('get ja arg:\n', js_arg)

# 修改JS函数，使其返回Cookie内容 由于我们需要的是po的这个参数。但js代码中的eval在python解释器中没有返回的功能、所以使用return替代
js_func = js_func.replace('eval("qo=eval;qo(po);")', 'return po')

# 执行JS获取Cookie
cookie_str = executeJS(js_func, js_arg)

# 将Cookie转换为字典格式
cookie = parseCookie(cookie_str)

print(cookie)

# 带上Cookie再次访问url,获取正确数据
print(getHtml(TARGET_URL, cookie)[0:500])
