# -*- coding: utf-8 -*-
from hashlib import md5
import execjs, os
os.environ["EXECJS_RUNTIME"] = "Node"



'''
url:https://www.jidaihome.com/officer/#/login
老规矩直接输入错误密码进行捉包、发现是一个payload的data，无法直接搜索关键字，所以只有使用xhr进行断点调试，断点停在一个地方（由于此时加密数据已经加密好），所以通过堆栈对加密数据怎行回溯
断点停留的函数y传入一个参数t，t中包含我们需要的提交数据
然后在n.login这个栈中发现加密参数是通过调用d.a.aseParam获取的然后对该行代码打上断点，追进去发现
aesParam = function(e) {
                var r = randomKey(16)
                  , i = aesEncrypt(JSON.stringify(e), r);
                return {
                    header: {
                        key: "Authorization",
                        value: base64Encrypt(r)
                    },
                    param: i
                }
            }
参数是通过这个函数返回出来的，只需要将相关函数和参数抠出来就能正常返回加密参数

通过断点可以得知 e参数是一个保存账号密码的字典，密码是经过MD5处理过的(可以直接使用python代码进行预处理)
'''


def getmd5(s):
    result = md5(s.encode()).hexdigest()
    return result


password = getmd5('123456')


js = '''
            var cryptoJS = require("crypto-js");
            
            aesEncrypt = function(t, e) {
                var r = cryptoJS.enc.Utf8.parse(e)
                  , n = cryptoJS.enc.Utf8.parse(t);
                return cryptoJS.AES.encrypt(n, r, {
                    iv: cryptoJS.enc.Utf8.parse("0102030405060708"),
                    mode: cryptoJS.mode.CBC,
                    padding: cryptoJS.pad.Pkcs7
                }).toString()
            }
            ,

            base64Encrypt = function(t) {
                return cryptoJS.enc.Base64.stringify(cryptoJS.enc.Utf8.parse(t))
            }
            ,
            base64Decrypt = function(t) {
                return cryptoJS.enc.Base64.parse(t).toString(cryptoJS.enc.Utf8)
            }
            ,
            aesParam = function(e) {
                var r = randomKey(16)
                  , i = aesEncrypt(JSON.stringify(e), r);
                return {
                    header: {
                        key: "Authorization",
                        value: base64Encrypt(r)
                    },
                    param: i
                }
            }
            ,
            randomKey = function(t) {
                for (var e = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/=", r = 0, i = ""; r < t; ) {
                    var n = Math.floor(Math.random() * e.length);
                    i += e.charAt(n),
                    r++
                }
                return i
            }
            
            
            call_js = function(user){
                result = aesParam(user);
                return result;
            }
'''

user = {'mobile': "13316214395", 'password': password}

ctx = execjs.compile(js)
final_result = ctx.call('call_js', user)
print(final_result)
