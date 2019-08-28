from hashlib import md5
import execjs

# 内容数据的请求url token为js生成
url = 'https://nyloner.cn/proxy?page=1&num=15&token=d7f4969eabf63724ec549d7186cdcd67&t=1565687696'
# var token = md5(String(page) + String(num) + String(timestamp));
s = '1151565687696' # 字符串的page+num+时间戳
def getmd5(s):
    result = md5(s.encode()).hexdigest()
    return result

# 然后md5一下就获取到我们需要的token值
token = getmd5(s)
print(token)


# 然后获取到token值就可以直接请求上面的url地址
# 请求该url地址则会返回一段很明显已经加密过的字符串
# 该加密字符串是通过decode_str该函数调用
# 直接调用该函数会报错 现实base64未定义 所以要在该函数上执行base64代码上打断点
# 然后把全部代码复制下来
encode_text = "OUofBg89Mwc2BS4HKCY3AyAFJxI8LU0VISogByMtNRYnDAUJMAItGAYcPxAjBi8MPToSWSA9LAEnOiZfDzJDAjAGAAksGCcOITsFET8qHhgiOigVIy0lWSAxM1g3KAQHAyEZHgkWJBURLTBaJi0sCiMtJRohIREbNxYqGysmIxAgLC8MESlAFQstLEQnOiVaITEZWzAFGAksHDwJDjg7DD0HOAUiBCQKISpcGCEmQhY0FS4WKBgBDiIVAVU/BzNVIy0nRScUABgnDx0JMAYqXCgLWgAhKz8QPwQoXiMEIEEnEBsIJwswGBoCPgcqGy8QIzsFUD09MB8mLS9CDy5dAycPHQkwBiYZKCYFDSErCRE/OjQLIjosRCM9D1kjHzcHHz8YCQALJAkPLCdTOy0wFCAqLAcjAzkaISE3GzQGKhYsGxkeJQEsExEAKAUgByQbIS0HWiE2Ox0wLyVeBCVfFSUFAQI7BDAbIjoOBiM9CxsjMT8JNDgmWCg2DU8hBTcMFD0OCwoXLwINOiVZJyY7FjQGJhsrMVpIITxaHTwUEgUjLSQbDT5VFgomO1gwLyZbKiYFTCUGGQI7ACscDTkwGyEQLQYjDzMWNj9fGSoxXgEhFi8dPzoWXSEECggjACZWIiYwWTABAxksGAEeJQUrVz8XTRUiKjQHIxM9XiIPIxQwBRgJLBwsDw8BPww9BzgFIDoORyEqJRwnJjheGDteAiwYAR4lBScSPzoSGCIqAgYjLSEIIzE3WDQWOlgoCCcQCjwZAhcXMxwMLSxEJzolFyMxPxs0OCYWKRgnACAFKxw/BzAfJi0vBQxKJl8nDx0JMAYEWyomBRAgLC8MFikVGDU9LEQnOiUWIyE3WzU4LlopJisDJSsrHT0ENF0gBCwLJxdcHCctAQcYNC4HKhsvECE7Jxw+BCgZITogByMTIQYiJjMHGitWFwExJ08lLCdQPToSWSYHEhUnFz4fDDInBzYFLgcoGC8BIzxeEj0tSRQiFyQKIy0DFSAxHRY0PyVXKTEsTiUCAhI7BBYLJgQgCiMQWFsgNkYWNwYEGygmDRAgLC8MESlAFQstLEQnOiVaITEZWzAFGAksHDwJDjg7DD0HOAUiBCQKISpcGCEmQhY0FS4WKCYBACIrAVU9PTNVIy0nRScUABgnDx0JMAYqWigbWgMiPFpRPy1NFSE6IBsiOi0GDSJLFx0vJlgsMSdMIzsFUDsHDgsmADcCDC45BiEMMwc0Bi4WKiFeDiMsXh0/FzgUIjoKCyA9A18hNjhXNS8tWSwfAg4lBQECOwQ8WCIHUQggKlhbIDZGFjQGDAcpMS8QDyhXHBYtMFomLSxHIS0HWicMBQkwAj0eByU7ECMGLww/BDgUID1VBSE6XBcjHDMWNDgAFys2AQMjLCRcPi07WyYDCQUnEwMIJw8rGTUGKhQpGD8AIAU/VDsHDgsmACcEDRc9BiEMMwc2OARbKiEnCiUsJFUTOUgAJgQKFScTJRgjMRkaNCgIGigmIx4hOytTPzooWiIqPBsIKhsICxw4HhovJlgsMScBIysnED8ULBkgKjQHIS0pBiImMwcaK1YXATEnTyUsJ1A9OhJZJgcSFScXPh8MMicHNgUuBygYLwEjPF4SPS1JFCIXJAojLQMXIx8dXjQvJVcpMSxOJQICEjsEFgsmBCBAIwBYFiMhIxs0Bj5dKRgnSCUGGQI7ADsaDAA0GyEQLQYhMRlbNj8mHSwxJEkNOF8JOwQWCyYELAUjLQcbIyEVGjQ4IgkoJitPISsjUz8EMAUJPRIVCwAmHw0mO1gwLyYWKjYnDCEVPxA/FCgZISogGyI6LQYNIksXHS8mWCwxJ0wjOwVQOwcOCyYANwIMLjkGIQwzBzQGLhYqIV4OIyxeHT8XOBQiOgoFIwMDFyMMOFchPVJT"


decode_js = '''

/*
 * $Id: base64.js,v 2.15 2014/04/05 12:58:57 dankogai Exp dankogai $
 *
 *  Licensed under the BSD 3-Clause License.
 *    http://opensource.org/licenses/BSD-3-Clause
 *
 *  References:
 *    http://en.wikipedia.org/wiki/Base64
 */

(function (global) {
    // existing version for noConflict()
    var _Base64 = global.Base64;
    var version = "2.1.9";
    // if node.js, we use Buffer
    var buffer;
    if (typeof module !== 'undefined' && module.exports) {
        try {
            buffer = require('buffer').Buffer;
        } catch (err) {
        }
    }
    // constants
    var b64chars
        = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/';
    var b64tab = function (bin) {
        var t = {};
        for (var i = 0, l = bin.length; i < l; i++) t[bin.charAt(i)] = i;
        return t;
    }(b64chars);
    var fromCharCode = String.fromCharCode;
    // encoder stuff
    var cb_utob = function (c) {
        if (c.length < 2) {
            var cc = c.charCodeAt(0);
            return cc < 0x80 ? c
                : cc < 0x800 ? (fromCharCode(0xc0 | (cc >>> 6))
                + fromCharCode(0x80 | (cc & 0x3f)))
                    : (fromCharCode(0xe0 | ((cc >>> 12) & 0x0f))
                    + fromCharCode(0x80 | ((cc >>> 6) & 0x3f))
                    + fromCharCode(0x80 | ( cc & 0x3f)));
        } else {
            var cc = 0x10000
                + (c.charCodeAt(0) - 0xD800) * 0x400
                + (c.charCodeAt(1) - 0xDC00);
            return (fromCharCode(0xf0 | ((cc >>> 18) & 0x07))
            + fromCharCode(0x80 | ((cc >>> 12) & 0x3f))
            + fromCharCode(0x80 | ((cc >>> 6) & 0x3f))
            + fromCharCode(0x80 | ( cc & 0x3f)));
        }
    };
    var re_utob = /[\uD800-\uDBFF][\uDC00-\uDFFFF]|[^\x00-\x7F]/g;
    var utob = function (u) {
        return u.replace(re_utob, cb_utob);
    };
    var cb_encode = function (ccc) {
        var padlen = [0, 2, 1][ccc.length % 3],
            ord = ccc.charCodeAt(0) << 16
                | ((ccc.length > 1 ? ccc.charCodeAt(1) : 0) << 8)
                | ((ccc.length > 2 ? ccc.charCodeAt(2) : 0)),
            chars = [
                b64chars.charAt(ord >>> 18),
                b64chars.charAt((ord >>> 12) & 63),
                padlen >= 2 ? '=' : b64chars.charAt((ord >>> 6) & 63),
                padlen >= 1 ? '=' : b64chars.charAt(ord & 63)
            ];
        return chars.join('');
    };
    var btoa = global.btoa ? function (b) {
        return global.btoa(b);
    } : function (b) {
        return b.replace(/[\s\S]{1,3}/g, cb_encode);
    };
    var _encode = buffer ? function (u) {
            return (u.constructor === buffer.constructor ? u : new buffer(u))
                .toString('base64')
        }
            : function (u) {
                return btoa(utob(u))
            }
    ;
    var encode = function (u, urisafe) {
        return !urisafe
            ? _encode(String(u))
            : _encode(String(u)).replace(/[+\/]/g, function (m0) {
                return m0 == '+' ? '-' : '_';
            }).replace(/=/g, '');
    };
    var encodeURI = function (u) {
        return encode(u, true)
    };
    // decoder stuff
    var re_btou = new RegExp([
        '[\xC0-\xDF][\x80-\xBF]',
        '[\xE0-\xEF][\x80-\xBF]{2}',
        '[\xF0-\xF7][\x80-\xBF]{3}'
    ].join('|'), 'g');
    var cb_btou = function (cccc) {
        switch (cccc.length) {
            case 4:
                var cp = ((0x07 & cccc.charCodeAt(0)) << 18)
                        | ((0x3f & cccc.charCodeAt(1)) << 12)
                        | ((0x3f & cccc.charCodeAt(2)) << 6)
                        | (0x3f & cccc.charCodeAt(3)),
                    offset = cp - 0x10000;
                return (fromCharCode((offset >>> 10) + 0xD800)
                + fromCharCode((offset & 0x3FF) + 0xDC00));
            case 3:
                return fromCharCode(
                    ((0x0f & cccc.charCodeAt(0)) << 12)
                    | ((0x3f & cccc.charCodeAt(1)) << 6)
                    | (0x3f & cccc.charCodeAt(2))
                );
            default:
                return fromCharCode(
                    ((0x1f & cccc.charCodeAt(0)) << 6)
                    | (0x3f & cccc.charCodeAt(1))
                );
        }
    };
    var btou = function (b) {
        return b.replace(re_btou, cb_btou);
    };
    var cb_decode = function (cccc) {
        var len = cccc.length,
            padlen = len % 4,
            n = (len > 0 ? b64tab[cccc.charAt(0)] << 18 : 0)
                | (len > 1 ? b64tab[cccc.charAt(1)] << 12 : 0)
                | (len > 2 ? b64tab[cccc.charAt(2)] << 6 : 0)
                | (len > 3 ? b64tab[cccc.charAt(3)] : 0),
            chars = [
                fromCharCode(n >>> 16),
                fromCharCode((n >>> 8) & 0xff),
                fromCharCode(n & 0xff)
            ];
        chars.length -= [0, 0, 2, 1][padlen];
        return chars.join('');
    };
    var atob = global.atob ? function (a) {
        return global.atob(a);
    } : function (a) {
        return a.replace(/[\s\S]{1,4}/g, cb_decode);
    };
    var _decode = buffer ? function (a) {
        return (a.constructor === buffer.constructor
            ? a : new buffer(a, 'base64')).toString();
    }
        : function (a) {
            return btou(atob(a))
        };
    var decode = function (a) {
        return _decode(
            String(a).replace(/[-_]/g, function (m0) {
                return m0 == '-' ? '+' : '/'
            })
                .replace(/[^A-Za-z0-9\+\/]/g, '')
        );
    };
    var noConflict = function () {
        var Base64 = global.Base64;
        global.Base64 = _Base64;
        return Base64;
    };
    // export Base64
    global.Base64 = {
        VERSION: version,
        atob: atob,
        btoa: btoa,
        fromBase64: decode,
        toBase64: encode,
        utob: utob,
        encode: encode,
        encodeURI: encodeURI,
        btou: btou,
        decode: decode,
        noConflict: noConflict
    };
    // if ES5 is available, make Base64.extendString() available
    if (typeof Object.defineProperty === 'function') {
        var noEnum = function (v) {
            return {value: v, enumerable: false, writable: true, configurable: true};
        };
        global.Base64.extendString = function () {
            Object.defineProperty(
                String.prototype, 'fromBase64', noEnum(function () {
                    return decode(this)
                }));
            Object.defineProperty(
                String.prototype, 'toBase64', noEnum(function (urisafe) {
                    return encode(this, urisafe)
                }));
            Object.defineProperty(
                String.prototype, 'toBase64URI', noEnum(function () {
                    return encode(this, true)
                }));
        };
    }
    // that's it!
    if (global['Meteor']) {
        Base64 = global.Base64; // for normal export in Meteor.js
    }
    if (typeof module !== 'undefined' && module.exports) {
        module.exports.Base64 = global.Base64;
    }
    if (typeof define === 'function' && define.amd) {
        // AMD. Register as an anonymous module.
        define([], function () {
            return global.Base64
        });
    }
})(typeof self !== 'undefined' ? self
    : typeof window !== 'undefined' ? window
        : typeof global !== 'undefined' ? global
            : this
);

function decode_str(scHZjLUh1) {
    scHZjLUh1 = Base64["\x64\x65\x63\x6f\x64\x65"](scHZjLUh1);
    key = '\x6e\x79\x6c\x6f\x6e\x65\x72';
    len = key["\x6c\x65\x6e\x67\x74\x68"];
    code = '';
    for (i = 0; i < scHZjLUh1["\x6c\x65\x6e\x67\x74\x68"]; i++) {
        var coeFYlqUm2 = i % len;
        // ["\x53\x74\x72\x69\x6e\x67"]["\x66\x72\x6f\x6d\x43\x68\x61\x72\x43\x6f\x64\x65"]
        // 上面的代码解码之后就是String.fromCharCode
        // code += ["\x53\x74\x72\x69\x6e\x67"]["\x66\x72\x6f\x6d\x43\x68\x61\x72\x43\x6f\x64\x65"](scHZjLUh1["\x63\x68\x61\x72\x43\x6f\x64\x65\x41\x74"](i) ^ key["\x63\x68\x61\x72\x43\x6f\x64\x65\x41\x74"](coeFYlqUm2))
        code += String.fromCharCode(scHZjLUh1["\x63\x68\x61\x72\x43\x6f\x64\x65\x41\x74"](i) ^ key["\x63\x68\x61\x72\x43\x6f\x64\x65\x41\x74"](coeFYlqUm2))
    }
    return Base64["\x64\x65\x63\x6f\x64\x65"](code)
}
'''

# 通过execjs执行js代码获取到解密后的文本
ctx = execjs.compile(decode_js)
result = ctx.call('decode_str', encode_text)
print(result)