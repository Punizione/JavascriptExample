import requests
import random
import time
import PyV8
import hashlib

# 用于翻译的post链接
post_url = 'http://fanyi.youdao.com/translate_o?smartresult=dict&smartresult=rule'

data = {
	'i': '',
	'from': 'en',
	'to': 'zh-CHS',
	'smartresult': 'dict',
	'client': 'fanyideskweb',
	# r + parseInt(10 * Math.random(), 10);
	'salt': '',
	# sign: n.md5("fanyideskweb" + e + i + "p09@Bn{h02_BIEe]$P^nG")
	'sign': '',
	# r = "" + (new Date).getTime()
	'ts': '',
	# md5(navigator.appVersion)
	'bv': '',
	'doctype': 'json',
	'version': '2.1',
	'keyfrom': 'fanyi.web',
	'action': 'FY_BY_REALTIME',
	'typoResult': 'false',
}

headers = {
	'User-Agent' : '5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36',
	'Referer': 'http://fanyi.youdao.com/',
	'Origin': 'http://fanyi.youdao.com',
	'Host': 'fanyi.youdao.com',
	'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
	'Content-Length': '256',
	'Connection': 'keep-alive',
	'Accept-Encoding': 'gzip, deflate',
	'Cookie': 'OUTFOX_SEARCH_USER_ID=-1355657466@10.168.8.64; OUTFOX_SEARCH_USER_ID_NCOO=562313514.4764107; JSESSIONID=aaakLrrDXSyNYe_8JpXIw; ___rl__test__cookies=1549183650766'
}

'''
发送post请求需要两个（salt、sign）参数 但这两个参数已经加密了。所以需要破解js
下面是生成sign参数的方法
sign: n.md5("fanyideskweb" + e + i + "p09@Bn{h02_BIEe]$P^nG")

r = "" + (new Date).getTime(),
i = r + parseInt(10 * Math.random(), 10)
上面个行函数是获取i的值 即是上面sign的i参数
'''

# 将13、14行代码转化为python代码
time_num = int(time.time()) * 10000
ctxt = PyV8.JSContext()
ctxt.enter()
func = ctxt.eval("""
    (function(){
        function hello(){
            return (new Date).getTime();
        }
        return hello();
    })
""")
js_time_num = str(int(func() + 4000)).split('.')[0]
print(js_time_num)
# 获取一个0 到 10 的随机数
func02 = ctxt.eval("""
    (function(){
        function hello(){
            return parseInt(10 * Math.random(), 10);
        }
        return hello();
    })
""")
js_random_num = str(func02())
print(js_random_num)
# 转化为python代码
random_nums = random.randint(0, 10)

salt = js_time_num + js_random_num
print(salt)
sign = "fanyideskweb" + 'ramsey' + str(salt) + "p09@Bn{h02_BIEe]$P^nG"
convert_method = 'en2zh-CHS'
def getMD5(string):
	md5 = hashlib.md5()
	md5.update(string.encode('utf8'))
	sign = md5.hexdigest()
	return sign
md5_sign = getMD5(sign)
navigator_appVersion = '5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.81 Safari/537.36'
bv = getMD5(navigator_appVersion)


data['i'] = 'ramsey'
data['salt'] = str(salt)
data['sign'] = md5_sign
data['ts'] = str(salt[:-1])
data['bv'] = bv

r = requests.post(url = post_url, headers = headers, data =data)
print(r.content.decode())
