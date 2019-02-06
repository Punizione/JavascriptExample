import re
import PyV8
import requests

'''
1、由于使用chrome浏览器一直找不到url的加密JavaScript、这里有一个小技巧、使用火狐浏览器、右击检查、可以看到a标签旁边有一个event按钮、点击之后便会出现url加密的函数
2、通过分析该函数获取所需的参数
var hh = $(this).attr("href"); 很明显是：http://ggzy.gzlps.gov.cn:80/xxgkdt/20640.jhtml 待加密的url
var ee = $(this).attr('target'); 很明显是：_blank 这个可有可无
var k = CryptoJS.enc.Utf8.parse(s); 这个s参数在这个函数里从来没有出现过、所以假设这个参数藏在某个js当中、通过'var s'为搜索关键字逐个js搜索（笨方法）然后发现JS.jquery.min.js中 有一个赋值 var s = 'qnbyzzwmdgghmcnm';
3、这三个参数获取到之后、那就直接使用pyv8包了
4、直接运行这个函数的话 会报错、显示说类似没有加载到cryptojs包的错误
5、http://ggzy.gzlps.gov.cn/r/cms/com.ggzyjy.www/com.ggzyjy.www/js/jquery.lyh-1.1.0.js然后找到这个cryptojs是从这个网页的js加载的、暴力的方法就是复制整个js到一个js文件中、然后使用with open、read（）的方法 然后将刚刚的解释url函数进行拼接、
6、最后运行的时候还会报错、显示说$这个没有定义、还是蠢方法、在刚刚新建的js文件中将所有$替换为''空
'''


class Encode_num:
    def __init__(self):
        self.execute = PyV8.JSContext()
        self.execute.enter()
        with open('ase_encryption.js')as f:
            self.a = f.read()


    def parse_javaScript(self, url):

        func = '''
            (function() {
          var hh = ''' + '"{}"'.format(url) + ''';
          if (typeof(hh) == 'undefined' || hh == '#') {
            return
          }
          var aa = hh.split("/");
          var aaa = aa.length;
          var bbb = aa[aaa - 1].split('.');
          var ccc = bbb[0];
          var cccc = bbb[1];
          var r = /^\+?[1-9][0-9]*/;
          var ee = '_blank';
          if (r.test(ccc) && cccc.indexOf('jhtml') != -1) {
            var srcs = CryptoJS.enc.Utf8.parse(ccc);
            var k = CryptoJS.enc.Utf8.parse('qnbyzzwmdgghmcnm');
            var en = CryptoJS.AES.encrypt(srcs, k, {
              mode: CryptoJS.mode.ECB,
              padding: CryptoJS.pad.Pkcs7
            });
            var ddd = en.toString();
            ddd = ddd.replace(/\//g, "^");
            ddd = ddd.substring(0, ddd.length - 2);
            var bbbb = ddd + '.' + bbb[1];
            aa[aaa - 1] = bbbb;
            var uuu = '';
            for (i = 0; i < aaa; i++) {
              uuu += aa[i] + '/'
            }
            uuu = uuu.substring(0, uuu.length - 1);
            if (typeof(ee) == 'undefined') {
              location = uuu
            } 
          }
          return uuu
        })
            '''

        result = self.execute.eval(self.a + func)
        print(result())

if __name__ == '__main__':
    url = 'http://ggzy.gzlps.gov.cn:80/jyxxgcgg/20849.jhtml'
    en = Encode_num()
    en.parse_javaScript(url)