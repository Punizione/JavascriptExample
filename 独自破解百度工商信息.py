import json
import re
import requests
from chardet import *
import PyV8
import time
# 广州探迹科技有限公司

'''
思路
1、https://xin.baidu.com/s?q={} 从这个网页入口查找需要查找的公司名
2、通过捉包可以发现 如果需要获取到全部该公司信息的ajax地址需要三个参数 [pid,tot,_]
3、这里有个小技巧、如果你直接从主页去搜索的话、你是很难获取到pid这个值的、但如果你用第一条的那个url、你可以在搜索之后的列表页获取到pid
4、获取到pid就很关键了、因为第二个参数tot需要通过一个js函数生成、这个js函数需要两个参数分别是tk，bid 其实第一个参数tk就是pid、而第二个参数bid需要通过pid来构造url、并且通过正则获取到pid的值
5、然后就执行这个javascript函数获取到过滤后的tk
6、第三个参数为_, 是一个时间戳、python中使用time.time即可达到需求
7、然后通过这三个参数构造出url便可以获取到公司信息
'''


class Baidu_Industry:

    def __init__(self):
        self.execute = PyV8.JSContext()
        self.execute.enter()

        self.script = '''
            (function(tk, bid) {
                        var tkLen = tk.length;
                        tk = tk.split('');
                        var bdLen = bid.length;
                        bid = bid.split('');
                        for (var i = 0; i < bdLen; i++) {
                            bid[i] = parseInt(bid[i]) + parseInt(tkLen - bdLen);
                        }
                        var one = tk[bid[bdLen - 1]];
                        for (var i = bdLen - 1; i >= 0; i -= 1) {
                            tk[bid[i]] = tk[bid[i - 1]];
                            if ((i - 2) < 0) {
                                tk[bid[i - 1]] = one;
                                break;
                            }
                        }
                        return tk.join("")
                    })
        '''

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
            'Host': 'xin.baidu.com'
        }

        self.detail_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Host': 'xin.baidu.com'
        }

        self.url = 'https://xin.baidu.com/s?q={}'
        self.detail_url = 'https://xin.baidu.com/detail/compinfo?pid={}'
        self.detail_content_url = 'https://xin.baidu.com/detail/basicAjax?pid={}&{}&_={}'

        self.company_name = input("请输入需要查询的公司名 : ")


    def get_pid(self):
        r_list_page = requests.get(self.url.format(self.company_name), headers = self.headers).content
        # print(detect(r_list_page).get('encoding'))
        get_pid = re.search(r'pid=(.*?)\"', r_list_page.decode(), re.S).group(1)
        return get_pid
        # print(get_pid)

    def get_bid(self, get_pid):
        r_detail_page = requests.get(self.detail_url.format(get_pid), headers = self.headers).content
        # print(detect(r_detail_page).get('encoding'))
        get_detail_resp = r_detail_page.decode()
        baidu_code = re.search(r'id=\"baiducode\">(.*?)<', get_detail_resp, re.S).group(1)
        return baidu_code
        # print(baidu_code)

    def get_tot(self, get_pid, baidu_code):
        result = self.execute.eval(self.script)
        tot = result(get_pid, baidu_code)
        return tot
        # print(result(get_pid, baidu_code))

    def get__(self):
        t = int(time.time() * 1000)
        return t

    def get_final_result(self, get_pid, tot, t):
        detail_content = requests.get(self.detail_content_url.format(get_pid, tot, t), headers=self.detail_headers).content
        # print(detect(detail_content).get('encoding'))
        final_result = detail_content.decode('unicode_escape')
        final_result = json.loads(final_result)['data']
        return final_result

    def format_data(self, final_result):
        items = {}
        items['公司名:'] = final_result['entName']
        items['统一社会信用代码/注册号:'] = final_result['regNo']
        items['注册资本:'] = final_result['regCapital']
        items['成立日期:'] = final_result['startDate']
        items['所在地址:'] = final_result['regAddr']
        items['主要人员'] = [{i['title']: i['name']} for i in final_result['directors']]
        items['股东'] = [{i['name'].strip(): '出资额 ' + i['amount']} for i in final_result['shares']]
        print(items)

    def run(self):
        pid = self.get_pid()
        bid = self.get_bid(pid)
        tot = self.get_tot(pid, bid)
        t = self.get__()
        final_result = self.get_final_result(pid, tot, t)
        self.format_data(final_result)

if __name__ == '__main__':
    bdi = Baidu_Industry()
    bdi.run()

