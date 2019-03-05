import requests
import PyV8, re

headers = {
    'Host' : 'shfy.chinacourt.org',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.119 Safari/537.36',
    'Referer': 'http://shfy.chinacourt.org/paper/more/paper_mid/MzA0gAMA.shtml'
}

# 文章url
url = 'http://shfy.chinacourt.org/paper/detail/2018/11/id/1927107.shtml'

resp = requests.get(url, headers = headers)
content = resp.content.decode()
# 获取到文章的加密字段
encode_content = re.search(r'(var tm=new.*?html=\'\';)', content, re.S).group(1)



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

''' + eval('"{}"').format(encode_content) + '''

show=function(){
			html+=paperDecode(tm[n]);
			// document.getElementById('border_in').innerHTML+='. ';
			n++;
			if(n<tm.length){
				setTimeout(show,50);
			}else{
				// document.getElementById('border_in').innerHTML=html;
				return html;
			}
		}
show();
'''
# ''' + eval('"{}"').format(encode_content) + '''
# 上面这行代码的意思是先将正则匹配到的加密文本合并到js中、由于合并后的这个正则有双引号存在、如果直接运行则会报错、所以使用eval函数去掉
execute = PyV8.JSContext()
execute.enter()
result = execute.eval(hehe)
print(result)