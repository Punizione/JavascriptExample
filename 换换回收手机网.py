# -*- coding: utf-8 -*-
import execjs
import requests

'''
查找价格js的入口
第一步：打开Chrome浏览器，地址栏输入网址，并按下F12，打开调试器，切换到Network面板，再按下回车，进行访问。
先全局搜索商品价格：4440，发现搜索不到，那只有去一个一个页面看了。
在这里，我们只查看 XHR加载的页面：并且发现一个getEvaluateData?goods_id=47这个请求
看见这个返回信息是加密后的信息
这个时候一般已经卡死、但可以尝试新方法、鼠标移到getEvaluateData?goods_id=47的Initiator选项卡上并点击第一个send，并且在代码里面打上断点、因为send是获得所有请求后再调用的、所以所有参数应该都准备好才调用该方法、所以在call stack堆栈中逐个逐个往上找、当找到jsonCall这个栈时、便可以看见decode这个可疑的方法、然后就把之前send方法的断点取消在调用decode方法的代码上打上新的断点并刷新网页。
可以看到decode调用时有两个参数decode(res, code) 鼠标指着res可以看到res便是之前找到的加密代码、 code则是从Response.headers中的content-text中获取
接下来按f11追进去看 发现该函数最后返回的值便包含该商品的所有信息。
在抠js代码的时候注意
先把decode函数拿出来
然后把decode函数所用到的函数也抠出来、这里包含str_replace、str_split、Base64
利用execjs执行这段js就可以得到结果

最后注意两点：
一、当抠出完整js代码，并且在webstrom调试完成之后，尽量使用文件导入的方式导入js代码，避免引起不必要的奇怪问题
二、对于使用python调用js时，有时候会出现一些转义上的错误。例如：
修改前：string = string.replace(/\r\n/g, "\n") 会报错Invalid regular expression: missing / (  @ 61 : 26 )  -> 		string = string.replace(/
修改后：string = string.replace(/\\r\\n/g, "\\n"); 在每个\前面在添加一个\就可以解决此类问题，又或者在字符串前面加一个r
'''

# with open('bs64.js', 'r')as f:
#     func = f.read()

func = '''
function Base64() {
	// private property
	_keyStr = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=";

	// public method for encoding
	this.encode = function(input) {
		var output = "";
		var chr1, chr2, chr3, enc1, enc2, enc3, enc4;
		var i = 0;
		input = _utf8_encode(input);
		while(i < input.length) {
			chr1 = input.charCodeAt(i++);
			chr2 = input.charCodeAt(i++);
			chr3 = input.charCodeAt(i++);
			enc1 = chr1 >> 2;
			enc2 = ((chr1 & 3) << 4) | (chr2 >> 4);
			enc3 = ((chr2 & 15) << 2) | (chr3 >> 6);
			enc4 = chr3 & 63;
			if(isNaN(chr2)) {
				enc3 = enc4 = 64;
			} else if(isNaN(chr3)) {
				enc4 = 64;
			}
			output = output +
				_keyStr.charAt(enc1) + _keyStr.charAt(enc2) +
				_keyStr.charAt(enc3) + _keyStr.charAt(enc4);
		}
		return output;
	};
	// public method for decoding
	this.decode = function(input) {
		var output = "";
		var chr1, chr2, chr3;
		var enc1, enc2, enc3, enc4;
		var i = 0;
		input = input.replace(/[^A-Za-z0-9\+\/\=]/g, "");
		while(i < input.length) {
			enc1 = _keyStr.indexOf(input.charAt(i++));
			enc2 = _keyStr.indexOf(input.charAt(i++));
			enc3 = _keyStr.indexOf(input.charAt(i++));
			enc4 = _keyStr.indexOf(input.charAt(i++));
			chr1 = (enc1 << 2) | (enc2 >> 4);
			chr2 = ((enc2 & 15) << 4) | (enc3 >> 2);
			chr3 = ((enc3 & 3) << 6) | enc4;
			output = output + String.fromCharCode(chr1);
			if(enc3 != 64) {
				output = output + String.fromCharCode(chr2);
			}
			if(enc4 != 64) {
				output = output + String.fromCharCode(chr3);
			}
		}
		output = _utf8_decode(output);
		return output;
	}

	// private method for UTF-8 encoding
	_utf8_encode = function(string) {
		string = string.replace(/\\r\\n/g, "\\n");
		var utftext = "";
		for(var n = 0; n < string.length; n++) {
			var c = string.charCodeAt(n);
			if(c < 128) {
				utftext += String.fromCharCode(c);
			} else if((c > 127) && (c < 2048)) {
				utftext += String.fromCharCode((c >> 6) | 192);
				utftext += String.fromCharCode((c & 63) | 128);
			} else {
				utftext += String.fromCharCode((c >> 12) | 224);
				utftext += String.fromCharCode(((c >> 6) & 63) | 128);
				utftext += String.fromCharCode((c & 63) | 128);
			}

		}
		return utftext;
	}

	// private method for UTF-8 decoding
	_utf8_decode = function(utftext) {
		var string = "";
		var i = 0;
		var c = c1 = c2 = 0;
		while(i < utftext.length) {
			c = utftext.charCodeAt(i);
			if(c < 128) {
				string += String.fromCharCode(c);
				i++;
			} else if((c > 191) && (c < 224)) {
				c2 = utftext.charCodeAt(i + 1);
				string += String.fromCharCode(((c & 31) << 6) | (c2 & 63));
				i += 2;
			} else {
				c2 = utftext.charCodeAt(i + 1);
				c3 = utftext.charCodeAt(i + 2);
				string += String.fromCharCode(((c & 15) << 12) | ((c2 & 63) << 6) | (c3 & 63));
				i += 3;
			}
		}
		return string;
	}
}


String.prototype.str_split = function(len) {
	var strlen = this.length;
	var str = this.toString();
	if(typeof len == "undefined" || len == 0 || len == 1) {
		return this.split("");
	}
	var count = Math.ceil(strlen / len);
	var reArray = [];
	for(var i = 0; i < count; i++) {
		reArray[i] = str.slice(i * len, i * len + len);
	}
	return reArray;
};
String.prototype.str_replace = function(findstrs, replacestrs) {
	var len = findstrs.length;
	var str = this.toString();
	for(var i = 0; i < len; i++) {
		var temp = findstrs[i];
		if(temp == "+" || temp == "=" || temp == "/")
			eval("var re = /\\\\" + temp + "/g;");
		else
			eval("var re = /" + temp + "/g;");
		str = str.replace(re, replacestrs[i]);
	}
	return str;
};
function decode(str, key) {
    // console.log(str);
    // return str;
    // console.log(typeof str); string
	var strArr = str.str_replace(["O0O0O", "o000o", "oo00o"], ["=", "+", "/"]);
	// console.log(strArr);
	// return strArr;
    // console.log(strArr);
    // console.log(typeof strArr);
	strArr = strArr.str_split(2);
	var len = strArr.length;
	var keyArr = key.str_split();
	// console.log(keyArr);
	for(var k in keyArr) {
		if(k <= len && typeof(strArr[k]) != "undefined" && strArr[k][1] == keyArr[k]) {
			strArr[k] = strArr[k][0];
		}
	}
	strArr = strArr.join("");
	// return strArr;
	// console.log(strArr);
	var Base = new Base64();
	var str = Base.decode(strArr);
	// console.log(str);
	//return str;
	// str = decodeURIComponent(str);
	return str;
	// console.log(str);
	// return str;
	// return str.str_replace(["+","x2b","x2B"],[" ","+","+"]);
}
'''

url = 'https://www.huanhuanhuishou.com//Goods/getEvaluateData?goods_id=47'
headers = {
	'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36'
}

r =  requests.get(url, headers = headers)
code = r.headers['Content-Text']
# code = '10233669;15448709'
res = "JTdCJTIyY29kZSUyMiUzQSUyMjEwMDAwJTIyJTJDJTIybXNnJTIyJTNBJTIyJUU4JUFGJUI3JUU2JUIxJTgyJUU2JTg4JTkwJUU1JThBJTlGJTIyJTJDJTIyYm9keSUyMiUzQSU1QiU3QiUyMmlkJTIyJTNBNCUyQyUyMmxvZ19pbWclMjIlM0ElMjIlMjIlMkMlMjJiYW5kX2ltZyUyMiUzQSUyMiUyMiUyQyUyMnNvcnRzJTIyJTNBOTk5OTk5JTJDJTIyd2VpeGluX2ltZyUyMiUzQSUyMmh0dHBzJTNBJTVDJTJGJTVDJTJGaW1hZ2UuaHVhbmh1YW5odWlzaG91LmNvbSU1QyUyRjQyYzQ2MWRlZThmMmUxYTRlOGVmNzU3YzQ2M2Q3ZGVlLnBuZyUyMiUyQyUyMmFwcF9pbWdzJTIyJTNBJTIyaHR0cHMlM0ElNUMlMkYlNUMlMkZpbWFnZS5odWFuaHVhbmh1aXNob3UuY29tJTVDJTJGOGJhZmM1YmY1ODVhZGZmNzVhY2U0NzYyMGJkODM3YTUucG5nJTIyJTJDJTIyc21hbGxfaW1nJTIyJTNBJTIyaHR0cHMlM0ElNUMlMkYlNUMlMkZpbWFnZS5odWFuaHVhbmh1aXNob3UuY29tJTVDJTJGMTUzNDEyY2NlNzhmZTQxNDI1ZTUyNjU5NTFlZjZkYzIucG5nJTIyJTJDJTIybmFtZSUyMiUzQSUyMiVFNiU4OSU4QiVFNiU5QyVCQSUyMiUyQyUyMmhvdCUyMiUzQSUyMjElMjIlMkMlMjJ0aWQlMjIlM0EwJTJDJTIyaW1nJTIyJTNBJTIyaHR0cHMlM0ElNUMlMkYlNUMlMkZpbWFnZS5odWFuaHVhbmh1aXNob3UuY29tJTVDJTJGNTcxNTcxNjMwOWFjNTUzOTI2YzFjYWZmMTFiZjA0YmEucG5nJTIyJTJDJTIybWltZyUyMiUzQSUyMmh0dHBzJTNBJTVDJTJGJTVDJTJGaW1hZ2UuaHVhbmh1YW5odWlzaG91LmNvbSU1QyUyRjkyNDkzMDhlNDg3NmMyMzY2YmUxYTMzNDVmZmUyOTMxLnBuZyUyMiUyQyUyMnBjaWQlMjIlM0ElMjIlMkMwJTJDJTIyJTJDJTIyaGlnaHRwcmljZSUyMiUzQSUyMjguMDAlMjIlMkMlMjJ1cmwlMjIlM0ElMjIlNUMlMkZhNC5odG1sJTIyJTdEJTJDJTdCJTIyaWQlMjIlM0E1JTJDJTIybG9nX2ltZyUyMiUzQSUyMiUyMiUyQyUyMmJhbmRfaW1nJTIyJTNBJTIyJTIyJTJDJTIyc29ydHMlMjIlM0E5OTk5ODglMkMlMjJ3ZWl4aW5faW1nJTIyJTNBJTIyaHR0cHMlM0ElNUMlMkYlNUMlMkZpbWFnZS5odWFuaHVhbmh1aXNob3UuY29tJTVDJTJGYjQ5NDllYmExNTY1ZTY3MTg2MGY2YTYwOTk2ZTZmNjQucG5nJTIyJTJDJTIyYXBwX2ltZ3MlMjIlM0ElMjJodHRwcyUzQSU1QyUyRiU1QyUyRmltYWdlLmh1YW5odWFuaHVpc2hvdS5jb20lNUMlMkY3YWNhMWZmNmE0NGViMTUyMDg4ZjVhZGY1Yzg5MmFlOC5wbmclMjIlMkMlMjJzbWFsbF9pbWclMjIlM0ElMjJodHRwcyUzQSU1QyUyRiU1QyUyRmltYWdlLmh1YW5odWFuaHVpc2hvdS5jb20lNUMlMkY2NzI2MzY4ZTVmMTczMDQxZGUxYTQ1MjQ2ZGFkMmFlNi5wbmclMjIlMkMlMjJuYW1lJTIyJTNBJTIyJUU1JTg1JUE4JUU2JTk2JUIwJUU2JTlDJUJBJTIyJTJDJTIyaG90JTIyJTNBJTIyMSUyMiUyQyUyMnRpZCUyMiUzQTAlMkMlMjJpbWclMjIlM0ElMjJodHRwcyUzQSU1QyUyRiU1QyUyRmltYWdlLmh1YW5odWFuaHVpc2hvdS5jb20lNUMlMkYxYTFmMmFlMzIwOTBlZDRkMTE0NmM3YzZlNzQ5NzIyMy5wbmclMjIlMkMlMjJtaW1nJTIyJTNBJTIyaHR0cHMlM0ElNUMlMkYlNUMlMkZpbWFnZS5odWFuaHVhbmh1aXNob3UuY29tJTVDJTJGODk2ZTQyZjgyMThjMjc5ZjMzNThiMjhmZGM5MTgxNWQucG5nJTIyJTJDJTIycGNpZCUyMiUzQSUyMiUyQzAlMkMlMjIlMkMlMjJoaWdodHByaWNlJTIyJTNBJTIyMC4wMCUyMiUyQyUyMnVybCUyMiUzQSUyMiU1QyUyRmE1Lmh0bWwlMjIlN0QlMkMlN0IlMjJpZCUyMiUzQTM4MCUyQyUyMmxvZ19pbWclMjIlM0ElMjIlMjIlMkMlMjJiYW5kX2ltZyUyMiUzQSUyMiUyMiUyQyUyMnNvcnRzJTIyJTNBOTk5OTY2JTJDJTIyd2VpeGluX2ltZyUyMiUzQSUyMiUyMiUyQyUyMmFwcF9pbWdzJTIyJTNBJTIyJTIyJTJDJTIyc21hbGxfaW1nJTIyJTNBJTIyJTIyJTJDJTIybmFtZSUyMiUzQSUyMiVFNSVBNCVBNyVFNiU4OSVCOSVFOSU4NyU4RiUyMiUyQyUyMmhvdCUyMiUzQSUyMjElMjIlMkMlMjJ0aWQlMjIlM0EwJTJDJTIyaW1nJTIyJTNBJTIyJTIyJTJDJTIybWltZyUyMiUzQSUyMiUyMiUyQyUyMnBjaWQlMjIlM0ElMjIlMkMwJTJDJTIyJTJDJTIyaGlnaHRwcmljZSUyMiUzQSUyMjAuMDAlMjIlMkMlMjJ1cmwlMjIlM0ElMjIlNUMlMkZhMzgwLmh0bWwlMjIlN0QlMkMlN0IlMjJpZCUyMiUzQTIlMkMlMjJsb2dfaW1nJTIyJTNBJTIyJTIyJTJDJTIyYmFuZF9pbWclMjIlM0FudWxsJTJDJTIyc29ydHMlMjIlM0E5OTklMkMlMjJ3ZWl4aW5faW1nJTIyJTNBJTIyaHR0cHMlM0ElNUMlMkYlNUMlMkZpbWFnZS5odWFuaHVhbmh1aXNob3UuY29tJTVDJTJGZmU5MTA1Yzg2MTZjNjVkZTcxYTllMzdlMzU2Yzg1ZjcucG5nJTIyJTJDJTIyYXBwX2ltZ3MlMjIlM0ElMjJodHRwcyUzQSU1QyUyRiU1QyUyRmltYWdlLmh1YW5odWFuaHVpc2hvdS5jb20lNUMlMkY5MTdkMWJlOTVkNzExNTIyYjdkZDU5NjNhZGZjNzFkZi5wbmclMjIlMkMlMjJzbWFsbF9pbWclMjIlM0ElMjJodHRwcyUzQSU1QyUyRiU1QyUyRmltYWdlLmh1YW5odWFuaHVpc2hvdS5jb20lNUMlMkZlN2M4Y2E3YWQwN2ZlODU1ZmNkMTNiYmZjY2VkN2MxNi5wbmclMjIlMkMlMjJuYW1lJTIyJTNBJTIyJUU1JUI5JUIzJUU2JTlEJUJGJUU3JTk0JUI1JUU4JTg0JTkxJTIyJTJDJTIyaG90JTIyJTNBJTIyMSUyMiUyQyUyMnRpZCUyMiUzQTAlMkMlMjJpbWclMjIlM0ElMjJodHRwcyUzQSU1QyUyRiU1QyUyRmltYWdlLmh1YW5odWFuaHVpc2hvdS5jb20lNUMlMkY5MzVjYmQxYTc4NWY3ZWExODQwZmMwZTAzZDZhMmI0MS5wbmclMjIlMkMlMjJtaW1nJTIyJTNBJTIyaHR0cHMlM0ElNUMlMkYlNUMlMkZpbWFnZS5odWFuaHVhbmh1aXNob3UuY29tJTVDJTJGNDQ0ZDFiMDhhYjE4ZDEyN2MxNTIxNTE4MjYyOTJkNWQucG5nJTIyJTJDJTIycGNpZCUyMiUzQSUyMiUyQzAlMkMlMjIlMkMlMjJoaWdodHByaWNlJTIyJTNBJTIyMC4wMCUyMiUyQyUyMnVybCUyMiUzQSUyMiU1QyUyRmEyLmh0bWwlMjIlN0QlMkMlN0IlMjJpZCUyMiUzQTElMkMlMjJsb2dfaW1nJTIyJTNBJTIyJTIyJTJDJTIyYmFuZF9pbWclMjIlM0ElMjIlMjIlMkMlMjJzb3J0cyUyMiUzQTExJTJDJTIyd2VpeGluX2ltZyUyMiUzQSUyMmh0dHBzJTNBJTVDJTJGJTVDJTJGaW1hZ2UuaHVhbmh1YW5odWlzaG91LmNvbSU1QyUyRjRjMDI5NThkMjFjZTg4ZTc3ODgwMTI3MmEwZjVkODMzLnBuZyUyMiUyQyUyMmFwcF9pbWdzJTIyJTNBJTIyaHR0cHMlM0ElNUMlMkYlNUMlMkZpbWFnZS5odWFuaHVhbmh1aXNob3UuY29tJTVDJTJGNDBlZDY2NGQ4YzYxNWI1NDEwNmVmNTlmM2EzNmMzNGIucG5nJTIyJTJDJTIyc21hbGxfaW1nJTIyJTNBJTIyaHR0cHMlM0ElNUMlMkYlNUMlMkZpbWFnZS5odWFuaHVhbmh1aXNob3UuY29tJTVDJTJGZGE0Y2M3MjUzYmM3MDgzNGMwZWZlNDMxNTNkZjc4ODgucG5nJTIyJTJDJTIybmFtZSUyMiUzQSUyMiVFNyVBQyU5NCVFOCVBRSVCMCVFNiU5QyVBQyUyMiUyQyUyMmhvdCUyMiUzQSUyMjElMjIlMkMlMjJ0aWQlMjIlM0EwJTJDJTIyaW1nJTIyJTNBJTIyaHR0cHMlM0ElNUMlMkYlNUMlMkZpbWFnZS5odWFuaHVhbmh1aXNob3UuY29tJTVDJTJGNjIyMGY3NWNlYWJjYmY4MmIxNDViNDYwZDdkYjJkOGMucG5nJTIyJTJDJTIybWltZyUyMiUzQSUyMmh0dHBzJTNBJTVDJTJGJTVDJTJGaW1hZ2UuaHVhbmh1YW5odWlzaG91LmNvbSU1QyUyRjU3NDE3OWVmZTk5ODY5NWE1MmNiMDJlODM1MjE3ODBiLnBuZyUyMiUyQyUyMnBjaWQlMjIlM0ElMjIlMkMwJTJDJTIyJTJDJTIyaGlnaHRwcmljZSUyMiUzQSUyMjAuMDAlMjIlMkMlMjJ1cmwlMjIlM0ElMjIlNUMlMkZhMS5odG1sJTIyJTdEJTJDJTdCJTIyaWQlMjIlM0EzJTJDJTIybG9nX2ltZyUyMiUzQSUyMiUyMiUyQyUyMmJhbmRfaW1nJTIyJTNBbnVsbCUyQyUyMnNvcnRzJTIyJTNBMCUyQyUyMndlaXhpbl9pbWclMjIlM0ElMjJodHRwcyUzQSU1QyUyRiU1QyUyRmltYWdlLmh1YW5odWFuaHVpc2hvdS5jb20lNUMlMkY3ODE1OWU5OWNmMDAwODQyNDhmZjI3ODRkMjMwMTdlYS5wbmclMjIlMkMlMjJhcHBfaW1ncyUyMiUzQSUyMmh0dHBzJTNBJTVDJTJGJTVDJTJGaW1hZ2UuaHVhbmh1YW5odWlzaG91LmNvbSU1QyUyRjI4ODcxMjkxMDk5MDFmODY1ZjRlNDM3MTg3ZmEyYTI2LnBuZyUyMiUyQyUyMnNtYWxsX2ltZyUyMiUzQSUyMmh0dHBzJTNBJTVDJTJGJTVDJTJGaW1hZ2UuaHVhbmh1YW5odWlzaG91LmNvbSU1QyUyRmVlZmY2MTBjZGZhM2ZjNDA4OTE1ZjkwOTIxY2JjNDM4LnBuZyUyMiUyQyUyMm5hbWUlMjIlM0ElMjIlRTYlOTUlQjAlRTclQTAlODElRTQlQkElQTclRTUlOTMlODElMjIlMkMlMjJob3QlMjIlM0ElMjIxJTIyJTJDJTIydGlkJTIyJTNBMCUyQyUyMmltZyUyMiUzQSUyMmh0dHBzJTNBJTVDJTJGJTVDJTJGaW1hZ2UuaHVhbmh1YW5odWlzaG91LmNvbSU1QyUyRmQyOGZlZmIwOGRhOWIyMWI3NDRjYzJlYzhmNTcyN2E2LnBuZyUyMiUyQyUyMm1pbWclMjIlM0ElMjJodHRwcyUzQSU1QyUyRiU1QyUyRmltYWdlLmh1YW5odWFuaHVpc2hvdS5jb20lNUMlMkY4ZGMwYmVlZjNjZTNhN2NjOGRmYjMzYTJiMDViYWFiMy5wbmclMjIlMkMlMjJwY2lkJTIyJTNBJTIyJTJDMCUyQyUyMiUyQyUyMmhpZ2h0cHJpY2UlMjIlM0ElMjIwLjAwJTIyJTJDJTIydXJsJTIyJTNBJTIyJTVDJTJGYTMuaHRtbCUyMiU3RCU1RCUyQyUyMmFwaXVybCUyMiUzQSUyMiU1QyUyRmluZGV4JTVDJTJGY2xhc3NpZmljYXRpb24uaHRtbCUyMiU3RA=="

ctx = execjs.compile(func)
result = ctx.call('decode', res, '49745298;69805930')
result = result.encode().decode('gbk')
print(result)
fff = '''
function hehe(strr){
    return decodeURIComponent(strr);
}
'''

ctx = execjs.compile(fff)
final_result = ctx.call('hehe', result)
print(final_result)
