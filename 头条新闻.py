import time

import requests
import re

home_page = 'https://www.toutiao.com/api/pc/feed/?min_behot_time=0&category=__all__&utm_source=toutiao&widen=1&tadrequire=true&as=A1E5BC68B213E46&cp=5C82032EF4264E1&_signature=TdfFohAUEVcnt8tW5QWm9U3Xxb'


'''
function(t) {
                var e = (0, _.default)(), i = 0;
                this.url = this._url,
                "refresh" === t ? (i = this.list.length > 0 ? this.list[0].behot_time : 0,
                this.url += "min_behot_time=" + i) : (i = this.list.length > 0 ? this.list[this.list.length - 1].behot_time : 0,
                this.url += "max_behot_time=" + i);
                var n = (0,
                g.sign)(i + "");
                (0,
                a.default)(this.params, {
                    as: e.as,
                    cp: e.cp,
                    _signature: n
                })
            }
'''

ascp = '''
(function s() {
        var t = Math.floor((new Date).getTime() / 1e3)
          , e = t.toString(16).toUpperCase()
          , i = (0, o.default)(t).toString().toUpperCase();
        if (8 != e.length)
            return {
                as: "479BB4B7254C150",
                cp: "7E0AC8874BB0985"
            };
        for (var n = i.slice(0, 5), s = i.slice(-5), a = "", r = 0; r < 5; r++)
            a += n[r] + e[r];
        for (var l = "", u = 0; u < 5; u++)
            l += e[u + 3] + s[u];
        return {
            as: "A1" + a + e.slice(-3),
            cp: e.slice(0, 3) + l + "E1"
        }
    })
'''

import PyV8
execute = PyV8.JSContext()
execute.enter()
result = execute.eval(ascp)
print(result())

# import hashlib
# now = round(time.time())
# e = hex(int(now)).upper()[2:]
# i = hashlib.md5(str(int(now)).encode()).hexdigest().upper() #hashlib.md5().hexdigest()创建hash对象并返回16进制结果
# print(i)