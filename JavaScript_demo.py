import PyV8

execute = PyV8.JSContext()
execute.enter()


func01 = '''
(function jandan_load_img() {
    var e = "Ly93eDQuc2luYWltZy5jbi9tdzYwMC83YTY5ODA0OWd5MWcwMWZhbHpxaGFqMjE2MDFrMDRxcC5qcGc="
    var c = jdbbMJ9sf1okhAg9WNRZ3tJlnKEXWT7edj(e, "NhTiXBVB0rv6Oo2e1IWvBusR1R68aRBY");
})
'''

func02 = '''
var jdbbMJ9sf1okhAg9WNRZ3tJlnKEXWT7edj = (function(o, y, g) {
    var d = o;
    var l = "DECODE";
    var y = y ? y : "";
    var g = g ? g : 0;
    var h = 4;
    y = md5(y);
    var x = md5(y.substr(0, 16));
    var v = md5(y.substr(16, 16));
    if (h) {
        if (l == "DECODE") {
            var b = md5(microtime());
            var e = b.length - h;
            var u = b.substr(e, h)
        }
    } else {
        var u = ""
    }
    var t = x + md5(x + u);
    var n;
    if (l == "DECODE") {
        g = g ? g + time() : 0;
        tmpstr = g.toString();
        if (tmpstr.length >= 10) {
            o = tmpstr.substr(0, 10) + md5(o + v).substr(0, 16) + o
        } else {
            var f = 10 - tmpstr.length;
            for (var q = 0; q < f; q++) {
                tmpstr = "0" + tmpstr
            }
            o = tmpstr + md5(o + v).substr(0, 16) + o
        }
        n = o
    }
    var k = new Array(256);
    for (var q = 0; q < 256; q++) {
        k[q] = q
    }
    var r = new Array();
    for (var q = 0; q < 256; q++) {
        r[q] = t.charCodeAt(q % t.length)
    }
    for (var p = q = 0; q < 256; q++) {
        p = (p + k[q] + r[q]) % 256;
        tmp = k[q];
        k[q] = k[p];
        k[p] = tmp
    }
    var m = "";
    n = n.split("");
    for (var w = p = q = 0; q < n.length; q++) {
        w = (w + 1) % 256;
        p = (p + k[w]) % 256;
        tmp = k[w];
        k[w] = k[p];
        k[p] = tmp;
        m += chr(ord(n[q]) ^ (k[(k[w] + k[p]) % 256]))
    }
    if (l == "DECODE") {
        m = base64_encode(m);
        var c = "";
        // m = m.replace(c, "");
        m = u + m;
        m = base64_decode(d)
    }
    return m
})
'''
with open('md5.js')as f:
    a = f.read()
result01 = execute.eval(a + func01 + func02)
# result02 = execute.eval(func02)
print(result01())