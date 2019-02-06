import re
import PyV8
import requests




class Encode_num:
    def __init__(self):
        self.execute = PyV8.JSContext()
        self.execute.enter()

url = 'http://www.baidu.com'
func = '''
    (function() {
  var hh = ''' + '{}'.format(url) + ''';
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

print(func)

# with open('ase_encryption.js')as f:
#     a = f.read()
#
# result = execute.eval(a + func)
#
# print(result())