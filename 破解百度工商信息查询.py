import re
import time
import execjs
import requests
from chardet import *
from scrapy import Selector


class BaiDuQiYeXinYong:
    def __init__(self):
        self.key_world = input('请输入想要查询的公司名：')

    def index(self):
        """
        首页信息获取。
        :return: 详情界面的 url
        """
        index_url = 'https://xin.baidu.com/s'
        index_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
            'Referer': 'https://xin.baidu.com/',
        }
        params = {
            'q': self.key_world,
            't': '0'
        }
        response = requests.get(url=index_url, headers=index_headers, params=params).content
        type_code = detect(response).get('encoding')  # 获取编码格式。
        print(type_code)
        response = response.decode(type_code)  # 转化为字符串。
        selector_response = Selector(text=response)
        details_href = selector_response.xpath('//a[@class="zx-list-item-url"]/@href').extract_first()
        pid = re.findall(r'pid=(.*)', details_href)[0]  # 获取pid的值。
        details_href = 'https://xin.baidu.com' + details_href
        return pid, details_href

    def details(self, pid, details_href):
        """
        获取查找公司的 基本信息。
        :param pid: 参数 pid 的值
        :param details_href: 详情界面的 url
        :return:
        """
        details_headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/64.0.3282.119 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        }
        details_response = requests.get(url=details_href, headers=details_headers)
        selector_details_response = Selector(text=details_response.text)
        bid = selector_details_response.xpath('//span[@id="baiducode"]//text()').extract_first()
        by_id, attribute = \
            re.findall(r"tk = document.getElementById\('(.*?)'\)\.getAttribute\('(.*?)'\)", details_response.text)[0]
        tk = re.findall(attribute + r'="(.*?)"\>', details_response.text)[0]  # 通过属性来查找tk值
        mix_func = re.findall(r'(function mix.*)\(function', details_response.text)[0]
        mix_func = """
        %s
        """ % mix_func
        js_function = execjs.compile(mix_func)
        tot = js_function.call('mix', tk, bid)  # 得到tot
        search_time = int(time.time() * 1000)
        info_url = "https://xin.baidu.com/detail/basicAjax?"
        params = {
            'pid': pid,
            'tot': tot,
            '_': search_time,
        }
        response = requests.get(info_url, headers=details_headers, params=params)
        return response.content

    def run(self):
        """
        开始运行，返回最终的信息
        :return:
        """
        pid, details_href = self.index()
        content_info = self.details(pid, details_href)
        print(content_info.decode('utf8'))


if __name__ == '__main__':
    bai_xin_yong = BaiDuQiYeXinYong()
    bai_xin_yong.run()