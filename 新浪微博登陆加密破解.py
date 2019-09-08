# -*- coding: utf-8 -*-
import requests, json, re, execjs
'''
微博登陆密文破解
prelogin：https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.19)&_=1567929183383
url：https://login.sina.com.cn/sso/login.php?client=ssologin.js(v1.4.19)&_=1567929229327
通过输入一个错误的密码捉包发现有两个参数是经过加密生成的，一个是su、另一个是sp，通过观察发现，su是通过base64加密而成的，所以将重点放在sp上，然后通过搜索su或sp这两个关键字发现第790行附近看到publickey这种字眼，应该就是通过rsa方法加密的，然后通过断点调试，var f = new sinaSSOEncoder.RSAKey; b = f.encrypt([st, nonce].join("\t") + "\n" + password); 这行代码就是最后生成密码的js，然后将相关的js代码抠出来，其中st，nonce等参数就是通过请求上面的prelogin获取的，而new sinaSSOEncoder则是新浪自带的方法，通过全局搜索将这段函数整段复制出来，然后便生成了 新浪.js 这个文件，首先通过请求prelogin获取所需的请求参数，还有调用js的参数，然后通过execjs调用该js便可以获取到最后的加密密码。
'''

headers = {
"Referer":"https://weibo.com/",
"Sec-Fetch-Mode":"no-cors",
"User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/76.0.3809.132 Safari/537.36",
}
url = 'https://login.sina.com.cn/sso/prelogin.php?entry=weibo&callback=sinaSSOController.preloginCallBack&su=&rsakt=mod&client=ssologin.js(v1.4.19)&_=1567929183383'
s = requests.session()

# 请求prelogin
resp = s.get(url, headers = headers).content.decode()
# 正则获取json数据
json_data = re.search(r'CallBack\((.*?)\)', resp, re.S).group(1)
# 提取
json_data = json.loads(json_data)
pubkey = json_data['pubkey']
servertime = json_data['servertime']
nonce = json_data['nonce']
# print(servertime, pubkey, nonce)

with open('微博.js', 'r')as f:
    sina = f.read()


ctx = execjs.compile(sina)
result = ctx.call('get_sp', pubkey, servertime, nonce, '18859915511nat.')
print(result)


