import requests, execjs, jsbeautifier, re

# 工商信息网首页 请求该主页需要5个cookie  tlb_cookie __jsluid_h JSESSIONID SECTOKEN __jsl_clearance
url = 'http://www.gsxt.gov.cn/corp-query-homepage.html'

headers = {
    'Host': 'www.gsxt.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
    'Cookie' : 'tlb_cookie=S172.16.12.130; '
}

session = requests.session()

# 请求第一次主页会首先返回一个__jsluid_h 并且 响应文本返回一段js代码 该代码用于获取 __jsl_clearance
r = session.get(url, headers = headers)
# 获取到第一个请求的cookie
cookies01 = '__jsluid_h' + '=' + r.cookies['__jsluid_h'] + '; '
headers['Cookie'] += cookies01
# 截取有用的js代码 并且修改部分字段
cookiesJs = r.content.decode().split('</script>')[0][8:]
cookiesJs = r.content.decode().split('</script>')[0][8:].replace('{eval', '{var hehe = ')

# 对js中没用的字段进行清洗
node = execjs.get()
ctx = node.compile(cookiesJs)
js2 = ctx.eval('hehe').replace('document.cookie', 'cookie')
js2 = js2.split(';if(')[0]
js2 = js2[:-1] + 'return cookie;\n}'
js2 = jsbeautifier.beautify(js2).replace('setTimeout', '// setTimeout')
# print(js2)
# 获取该js的函数名 用于接下来的调用
funcName = re.search(r'var(.*?)=', js2, re.S).group(1).strip()
print(funcName)

# 使用execjs方法执行上面清洗过后的js代码
ctx = execjs.compile(js2)
# 通过js获取到第二个必要cookie __jsl_clearance
cookies02 = ctx.call(funcName) + ' '
headers['Cookie'] += cookies02
print(headers)


# 现在已获取到 tlb_cookie __jsluid_h __jsl_clearance 就可以再次请求该主页 带着这三个cookie就可以从主页中获取到另外的两个cookie SECTOKEN JSESSIONID
resp02 = session.get(url, headers = headers)
headers['Cookie'] += 'JSESSIONID' + '=' + resp02.cookies['JSESSIONID'] + '; '
headers['Cookie'] += 'SECTOKEN' + '=' + resp02.cookies['SECTOKEN']
print(resp02.cookies)
print(headers)

