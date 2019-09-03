import json, requests
import execjs,os

session = requests.session()
# 由于默认环境为pyv8 所以要先环境切换
# print(execjs.get().name) # PyV8
os.environ["EXECJS_RUNTIME"] = "Node"
# print(execjs.get().name) # Node.js (V8)

headers = {
    'User-Agent': 'Mozilla/5.0 (iPhone; CPU iPhone OS 11_0 like Mac OS X) AppleWebKit/604.1.38 (KHTML, like Gecko) Version/11.0 Mobile/15A372 Safari/604.1'
}

# 列表页url:http://bulletin.cebpubservice.com/cebinfomobile/#/
# 下面这个url是ajax加载的url 直接访问则会返回加密文本
encode_text = session.get('http://bulletin.cebpubservice.com/cutominfoapi/recommand/type/0/pagesize/20/currentpage/1/uid/0', headers = headers).text
# print(encode_text)


# 获取以下js代码有两种方法
# 方法一、对主函数进行断点调试
# 方法二、由于该类型加密方法大致相同 可以碰巧在全局搜一些关键字 例如: cryptoJS、import cryproJS、base64
a = '''
var cryptoJS = require("crypto-js");
function des_j(ciphertext){
    let key = "ctpstp@custominfo!@#qweASD";
    let keyHex = cryptoJS.enc.Utf8.parse(key);
    // direct decrypt ciphertext
    let decrypted = cryptoJS.DES.decrypt({
        ciphertext: cryptoJS.enc.Base64.parse(ciphertext)
    }, keyHex, {
        mode: cryptoJS.mode.ECB,
        padding: cryptoJS.pad.Pkcs7
    });
    let desriptedStr = decrypted.toString(cryptoJS.enc.Utf8);
    return desriptedStr;
}
'''

# with open('2.js', 'r') as f:
#     js1 = f.read()
# print(type(encode_text))
ctx1 = execjs.compile(a)
res = ctx1.call('des_j', eval(encode_text))



infos = json.loads(res)['data']['dataList']
# print(infos)
# 由于测试 只爬取前三条数据
for each in infos[:3]:
    # print(each)
    # print(each['tenderProjectName'])
    # 解密后的文章id还需要跟url拼接
    # 一下是电脑版的url
    # http://bulletin.cebpubservice.com/cebinfomobile/#/detail/9fa43ca1-7886-4913-a2da-e97f7e4eee95
    # 由于是爬去微信公众号 所以网址拼接不能从电脑上找， 有个小技巧， 需要在微信公众号分享该文章到好友手机， 然后点击复制url， 将文章id设置为{}就可以了。
    html_article = 'http://bulletin.cebpubservice.com/cebinfomobile/static/pdfjs-dist/web/viewer.html?file=http://47.95.70.97:8080/customapi/bulletinPDF/{}'
    link = 'http://bulletin.cebpubservice.com/cebinfomobile/?from=singlemessage#/sharedetail/{}'
    # print(each['bulletinID'])
    link = link.format(each['bulletinID'])
    html_article = html_article.format(each['bulletinID'])
    # print(each)
    print(html_article)
# 'http://bulletin.cebpubservice.com/cebinfomobile/#/detail/58437f9f-15a4-4350-8882-c87f9cbd5799'