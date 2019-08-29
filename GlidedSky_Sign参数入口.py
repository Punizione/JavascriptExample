import hashlib, requests
sha1 = hashlib.sha1()

'''
从每个页面中爬取一些数字，然后计算总和，一共 1000页。

我们开始抓包分析吧。

请求第一个页面，很快发现数据都在这里：http://glidedsky.com/api/level/web/crawler-javascript-obfuscation-1/items?page=1&t=1566019443&sign=a7dacf4977254f92683ba0ec15d49ebfdfdce083

其中请求参数包含page页数、t为时间轴、sign（全局搜索过后并没有发现可疑的代码）现在用换换回收手机网的搜索方法， 在这个url的xhr选项卡上的Initiator依次跟进去 便会发现第四行有个 VM220:4

然后sign的生成代码就出来了

还有第二种方法找到sign参数 类似于jsfuck

network中下面这个url的返回值就时一段jsfuck的代码 解密后其实就是下面的(func)js代码
http://glidedsky.com/js/crawler-javascript-obfuscation-1.js

处理这种混淆js代码 有一个思路

首先点击该混淆js的最后一个右括号、然后找到相对应的左括号、并且将左括号前的所有代码复制一遍、在控制台中用console.log()输出出来、 如果结果是eval、 则证明括号内的则是函数或调用语句
、 然后此时把刚刚从混淆的js代码中最后的右括号和相应的左括号中间的代码抠出来 并用console.log打印, 得到的结果便是跟下面func的代码相同
'''

url = 'http://glidedsky.com/level/web/crawler-javascript-obfuscation-1'

func = '''
        var p = 1;
        var t = Math.floor((155139679629 - 99) / 99);
        var sign = sha1('Xr0Z-javascript-obfuscation-1' + t);
        return sign;
'''

# 用python代码模拟js代码得出结果
t = int((155139679629 - 99) / 99)
string = 'Xr0Z-javascript-obfuscation-1' + str(t)
sha1.update(string.encode('utf-8'))
sign = sha1.hexdigest()
print(sign)