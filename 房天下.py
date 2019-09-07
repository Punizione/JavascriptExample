# -*- coding: utf-8 -*-
import execjs

'''
对房天下的登陆账号密码进行加密破解
第一步、找到密码的加密js，首先发现点击登陆时有一个post请求，URL为https://passport.fang.com/login.api，然后通过对这个url在XhR/fetch Breakpoint添加上passport.fang.com/login，然后刷新网页进行断点调试，刷新之后会看到直接就去到send这一步，密码的加密肯定在send之前，所以通过在call Stack中可以清楚的看到loginclickFn，然后点击它，果然，很清楚地看见pwd: encryptedString(key_to_encode, that.password.val())，密码就是通过这行代码进行加密的，that.password.val()就是所输入的密码，key_to_encode进行全局搜索发现是在首页的源代码中，然后在这行代码打上新的断点，然后跟进去之后就发现通过调用encryptedString函数进行一系列的加密，到此基本就找到加密函数了，将有关encryptedString的相关代码抠出来保存到js文件中，并且将之前找到的key_to_encode也放进js文件，最后通过python调用js，加密后的结果就出来了。
'''

with open('房天下.js', 'r')as f:
    js = f.read()

ctx = execjs.compile(js)
result = ctx.call('pwd', '123456')
print(result)