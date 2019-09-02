import requests, re, execjs


headers = {
    'Host' : 'shfy.chinacourt.gov.cn',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    'Referer': 'http://shfy.chinacourt.org/paper/more/paper_mid/MzA0gAMA.shtml'
}

# 文章url
url = 'http://shfy.chinacourt.gov.cn/paper/detail/2018/11/id/1927107.shtml'

resp = requests.get(url, headers = headers)
content = resp.content.decode()
# print(content)
# 获取到文章的加密字段
encode_content = re.search(r'tm\[0\]="(.*?)";var', content, re.S).group(1)
# print(encode_content)

# 下面js代码通过上面的content返回值找到加密字段是通过paperDecode的js文件来处理的、然后搜索到该js(混淆js)，需要通过解密(需要解密两次)获取到最终的js代码
hehe = '''
function disableCopy() {
	return false
}
// document.body.onselectstart = disableCopy;
// document.body.oncopy = disableCopy;
// document.body.oncut = disableCopy;
function paperDecode(paperString) {
	var ret = '';
	paperString = unescape(paperString);
	for (var i = paperString.length; i > 0; i--) {
		ret += paperString.substr(i - 1, 1)
	}
	return ret
}
function jsPaperDecode(paperString) {
	document.write(paperDecode(paperString))
}
'''

# 最后只需要将刚刚获取到的加密文本作为参数、传入该js函数中、所得的返回值便是解密后的数据
ctx = execjs.compile(hehe)
result = ctx.call('paperDecode', encode_content)
print(result)
