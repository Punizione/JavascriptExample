import requests
import re
import PyV8
from chaojiying import chaojiying

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
    'Referer': 'https://passport.kongzhong.com/'
}
url = 'https://sso.kongzhong.com/ajaxLogin?j=j&jsonp=j&service=https://passport.kongzhong.com/&_=1551868428390'
session = requests.session()
r = session.get(url, headers = headers)
dc = re.search(r'dc\":\"(.*?)\"', r.content.decode(), re.S).group(1)
print(dc)

hehe = '''
function encode(str, pwd) {
		if (pwd == null || pwd.length <= 0) {
			return null
		};
		var prand = "";
		for (var i = 0; i < pwd.length; i++) {
			prand += pwd.charCodeAt(i).toString()
		};
		var sPos = Math.floor(prand.length / 5);
		var mult = parseInt(prand.charAt(sPos) + prand.charAt(sPos * 2) + prand.charAt(sPos * 3) + prand.charAt(sPos * 4) + prand.charAt(sPos * 5));
		var incr = Math.ceil(pwd.length / 2);
		var modu = Math.pow(2, 31) - 1;
		if (mult < 2) {
			return null
		};
		var salt = Math.round(Math.random() * 1000000000) % 100000000;
		prand += salt;
		while (prand.length > 10) {
			var a = prand.substring(0, 1);
			var b = prand.substring(10, prand.length);
			if (b.length > 10) {
				prand = b
			} else {
				prand = (parseInt(a) + parseInt(b)).toString()
			}
		};
		prand = (mult * prand + incr) % modu;
		var enc_chr = "";
		var enc_str = "";
		for (var i = 0; i < str.length; i++) {
			enc_chr = parseInt(str.charCodeAt(i) ^ Math.floor((prand / modu) * 255));
			if (enc_chr < 16) {
				enc_str += "0" + enc_chr.toString(16)
			} else enc_str += enc_chr.toString(16);
			prand = (mult * prand + incr) % modu
		};
		salt = salt.toString(16);
		while (salt.length < 8) salt = "0" + salt;
		enc_str += salt;
		return enc_str
	};
encode('liang2770', ''' + '"{}"'.format(dc) + ''');
'''

execute = PyV8.JSContext()
execute.enter()
result = execute.eval(hehe)
print(result)
# print(result[-20:])

# 验证码
aaaa = '''
    function hehe(){
    a = Math.random();
    return a;
    }
    hehe()
'''
random_time = execute.eval(aaaa)
vcode = 'https://sso.kongzhong.com/createVCode?w=80&h=30&{}'.format(random_time)
print(vcode)
login_url = 'https://sso.kongzhong.com/ajaxLogin?j=j&&type=1&service=https://passport.kongzhong.com/&username=13316214395&password={}&vcode={}&toSave=0&_=1551876978946'

data = {
    'j': 'j',
    'type': '1',
    'service': 'https://passport.kongzhong.com/',
    'username' : '13316214395',
    'password' : result,
    'toSave' : '0',
    '_' : '1551876978946'
}

img = session.get(vcode, headers = headers).content
with open('vcode.jpg', 'wb')as f:
    f.write(img)

im = open('vcode.jpg', 'rb').read()			#本地图片文件路径 来替换 a.jpg 有时WIN系统须要//
captcha = chaojiying.PostPic(im, 1004)['pic_str']		#1902 验证码类型  官方网站>>价格体系 3.4+版 print 后要加()

url = login_url.format(result, captcha)
print(url)

user_page = session.get(url, headers = headers).content.decode()
print(user_page)

user_login_url = 'https://passport.kongzhong.com/v/user/userindex?validate=true'
user_page = session.get(user_login_url, headers = headers)
print(user_page.content.decode())