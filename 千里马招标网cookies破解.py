import requests, re, time, execjs, jsbeautifier, csv, random, PyV8, redis
from lxml import etree


class Qianlima_Spider:
    def __init__(self):
        # 建立redis连接池 11为剑鱼 12为千里马
        pool = redis.ConnectionPool(host='0.0.0.0', port=6379, db=12)
        self.r = redis.Redis(connection_pool=pool)

        self.casual_headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'Host': 'search.qianlima.com',
            'Cookie' : '',
            'Referer': 'http://search.qianlima.com/search.jsp?p_xs=1&p_area=5&p_state=-1&p_tflt=-1&q_mod=0&q_kat=0&p_type=0&q=%B9%E3%B8%E6',
        }
        self.base_url = 'http://www.qianlima.com/'
        self.url = 'http://search.qianlima.com/search.jsp?q=%B9%E3%B8%E6&p_xs=1&p_area=5&q_kat=0&q_mod=0&p={}'
        # appendix_url = 'http://www.qianlima.com/zb/detail/20190412_124831386.html'
        # 列表页的headers
        self.list_headers = {
            'Host': 'search.qianlima.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Referer': 'http://search.qianlima.com/search.jsp?p_xs=1&p_area=5&p_state=-1&p_tflt=-1&q_mod=0&q_kat=0&p_type=0&q=%B9%E3%B8%E6',
            'Accept-Language': 'en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Upgrade-Insecure-Requests': '1',
            # 'Cookie': 'gr_user_id=8827172c-6bfc-4420-ae5b-42a88f02f857; UM_distinctid=169dd1d8916820-01db9f186b0cfd-12306d51-13c680-169dd1d89178d4; __jsluid=94d56eb05b782867937d0f4e746255af; seo_refUrl="http://www.directlyaccess.com"; seo_curUrl="http://www.qianlima.com/common/detail.jsp"; seo_intime="2019-04-13 16:11:32"; Hm_lvt_0a38bdb0467f2ce847386f381ff6c0e8=1555061550,1555067399,1555127924,1555308179; Hm_lvt_5dc1b78c0ab996bd6536c3a37f9ceda7=1555061550,1555067399,1555127924,1555308179; cookie_insert_log=0; qlm_username=18925125930; qlm_password=UKCmpg7RBUKpmRu8pj38gfgCRo7pREug; rem_login=1; qlmll_his=",125090114,125007560,125007750,124998826,124916207,124916495,124916572,124918943,124919846,124923150,"; JSESSIONID=9FC6CEDBF39318701676E0CEF64BF8A1.tomcat1; CNZZDATA1848524=cnzz_eid%3D1475461932-1554191115-http%253A%252F%252Fsearch.qianlima.com%252F%26ntime%3D1555311261; fromWhereUrl="http://www.qianlima.com/zb/detail/20190415_125090114.html"; gr_session_id_83e3b26ab9124002bae03256fc549065=82a1acf4-e993-4338-99c0-96aa46733518; Hm_lpvt_0a38bdb0467f2ce847386f381ff6c0e8=1555322553; Hm_lpvt_5dc1b78c0ab996bd6536c3a37f9ceda7=1555322553; gr_session_id_83e3b26ab9124002bae03256fc549065_82a1acf4-e993-4338-99c0-96aa46733518=true; __jsl_clearance=1555322578.732|0|EBsLmKZi2nTW0orS7psIBIlsHMI%3D'
        }
        # 详情页的headers
        self.detail_headers = {
            'Host': 'www.qianlima.com',
            'Accept-Encoding': 'gzip, deflate',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.103 Safari/537.36',
            'Connection': 'keep-alive',
            'Cache-Control': 'max-age=0',
            'Referer': 'http://search.qianlima.com/search.jsp',
            'Accept-Language': 'en-GB,en;q=0.9,zh-CN;q=0.8,zh;q=0.7',
            'Upgrade-Insecure-Requests': '1',
            # 'Cookie' : '__jsluid=3916982eeeab2b3a9956cb85e06da152; gr_user_id=8827172c-6bfc-4420-ae5b-42a88f02f857; UM_distinctid=169dd1d8916820-01db9f186b0cfd-12306d51-13c680-169dd1d89178d4; seo_refUrl="http://www.directlyaccess.com"; seo_curUrl="http://www.qianlima.com/common/detail.jsp"; seo_intime="2019-04-13 16:11:32"; Hm_lvt_0a38bdb0467f2ce847386f381ff6c0e8=1555061550,1555067399,1555127924,1555308179; Hm_lvt_5dc1b78c0ab996bd6536c3a37f9ceda7=1555061550,1555067399,1555127924,1555308179; cookie_insert_log=0; qlm_username=18925125930; qlm_password=UKCmpg7RBUKpmRu8pj38gfgCRo7pREug; rem_login=1; qlmll_his=",125090114,125007560,125007750,124998826,124916207,124916495,124916572,124918943,124919846,124923150,"; CNZZDATA1848524=cnzz_eid%3D917825304-1554191115-null%26ntime%3D1555311261; Hm_lpvt_0a38bdb0467f2ce847386f381ff6c0e8=1555315195; Hm_lpvt_5dc1b78c0ab996bd6536c3a37f9ceda7=1555315195'
        }
        # 保存txt的文件名
        self.path_name = 'qianlima.txt'

    def crawl_list(self, page_num):
        print('正在捉取第{}页'.format(page_num))
        list_url = self.url.format(page_num)

        r = requests.get(list_url, headers=self.casual_headers)
        cookies = r.cookies
        cookies_id = '; '.join(['='.join(item) for item in cookies.items()])
        print(cookies_id)
        decoding = r.encoding
        # 判断是否有编码格式、如果是则有内容、如果没有则是js代码
        if decoding:
        # print(r)
            r = r.content.decode(decoding)
            resp = etree.HTML(r)
            infos = resp.xpath('//div[@class="mianL3"]/table//tr')[1:]

            for each_info in infos:
                sleep_num = random.randint(50, 101) / 100
                time.sleep(sleep_num)
                surffix = ''
                link = each_info.xpath('./td[2]/a/@href')[0]
                try:
                    detail_resp = requests.get(link, headers = self.detail_headers)
                    decoding = detail_resp.encoding
                    # print(decoding, type(decodjing))
                    detail_resp = detail_resp.content.decode(decoding)
                except:
                    print('报错url：', link)
                    continue

                try:
                    surffix = re.search(r'<div>报名地址：(.*?)</div>', detail_resp, re.S).group(1).strip()
                except:
                    pass

                if surffix == '':
                    try:
                        surffix = re.search(r'</div>来源：(.*?)</div>"', detail_resp, re.S).group(1).strip()
                    except:
                        pass

                if surffix == '':
                    try:
                        surffix = re.search(r'</div>竞价.*?地址：(.*?)</div>"', detail_resp, re.S).group(1).strip()
                    except:
                        pass

                if surffix == '':
                    try:
                        surffix = re.search(r'<div>相关附件：.*?href=\"(.*?)</div>', detail_resp, re.S).group(1)
                    except:
                        pass

                if surffix == '':
                    try:
                        surffix = re.search(r'</div>信息来源：(.*?)</div>', detail_resp, re.S).group(1)
                    except:
                        pass

                if surffix == '':
                    try:
                        surffix = re.search(r'<div>附件.*?：.*?href=\"(.*?)</div>', detail_resp, re.S).group(1)
                    except:
                        pass

                if surffix == '':
                    try:
                        # 当详情页当中存在附件、则通过该正则获取到附件链接、当点击该链接首先会跳转到千里马的确定窗口、可以从改窗口获取到该附件的原网页链接
                        appendix_url = re.search(r'href="(http://www.qianlima.com/downloads/.*?)"', detail_resp, re.S).group(1)
                        appendix_resp = etree.HTML(requests.get(appendix_url, headers = self.casual_headers).content.decode())
                        surffix = str(appendix_resp.xpath('//a[@class="l8"]/@href')[0])
                        try:
                            if '://' in surffix:
                                original_link_prefix = surffix.split('://')[0]
                                original_link_url = surffix.split('://')[1].split('/', 1)[0]
                            else:
                                pass

                            # 判断是http还是https
                            if original_link_prefix == 'http':
                                surffix = 'http://' + original_link_url
                            elif original_link_prefix == 'https':
                                surffix = 'https://' + original_link_url
                            else:
                                pass
                        except:
                            pass
                    except:
                        pass

                if surffix != '':
                    try:
                        self.r.sadd('source_link', surffix)
                    except:
                        pass

        else:
            # cookies = r.cookies
            # cookies = '; '.join(['='.join(item) for item in cookies.items()])
            # print(1111)
            # print(cookies)
            resp = r.content.decode()
            resp = re.search(r'<script>(.*?)</script', resp, re.S).group(1)
            beautify_script = jsbeautifier.beautify(resp)
            # print(beautify_script)
            x = re.search(r'var x = \"(.*?)\"', beautify_script, re.S).group(1)
            y = re.search(r'y = \"(.*?)\"', beautify_script, re.S).group(1)

            lists_page_js = '''
            var aaa;
            var x = ''' + "'{}'".format(x) + '''.replace(/@*$/, "").split("@"),
                y = ''' + '"{}"'.format(y) + ''',
                f = function(x, y) {
                    var a = 0,
                        b = 0,
                        c = 0;
                    x = x.split("");
                    y = y || 99;
                    while ((a = x.shift()) && (b = a.charCodeAt(0) - 77.5)) c = (Math.abs(b) < 13 ? (b + 48.5) : parseInt(a, 36)) + y * c;
                    return c
                },
                z = f(y.match(/\w/g).sort(function(x, y) {
                    return f(x) - f(y)
                }).pop());
            while (z++) try {
                aaa = y.replace(/\\b\w+\\b/g, function(y) {
                    return x[f(y, z) - 1] || ("_" + y)
                });
                break
            } catch (_) {}
            function fff(){
                  return aaa;  
                }
            fff();
            '''
            # 格式化后的第一段js代码
            # print(lists_page_js)
            execute = PyV8.JSContext()
            execute.enter()
            result = execute.eval(lists_page_js)
            # 解完第一段js后得到第二段js的代码
            second_beautify_script = jsbeautifier.beautify(result)
            # print(second_beautify_script)

            # 通过正则表达式将第二段返回的js代码进行清洗 方便接下来用execjs进行调用
            second_script = re.sub(r'(setTimeout.*?;)', '', second_beautify_script, flags = re.S)
            second_script = re.sub(r'({\s*?document\.a.*})', '', second_script, flags = re.S)
            second_script = re.sub(r'(if\s*?\(\(function.*\))', '', second_script, flags = re.S)
            second_script = re.sub(r'(document\.)', '', second_script, flags = re.S)
            second_script = re.sub(r'(GMT;Path=/;\')', 'GMT;Path=/;\' \n return cookie;', second_script, flags = re.S)
            function_name = re.search(r'var\s(.*?)\s', second_script, re.S).group(1) + '();'
            second_script = second_script + '\n' + function_name
            second_script = re.sub(r'!!window.headless', '', second_script, flags = re.S)
            second_script = re.sub(r'window', '', second_script, flags = re.S)
            # print(second_script)
            # 破解第二段js之后便获取到cookie 然后拼接
            cookie_js = execute.eval(second_script)
            print(cookie_js)
            # 拼接cookies
            self.casual_headers['Cookie'] = cookies_id + cookie_js
            # 然后递归调用该函数
            self.crawl_list(page_num)
            # print(self.casual_headers)

    def save_link(self):
        with open(self.path, 'a+', encoding='utf8')as f:
            for each_link in self.r.smembers('source_link'):
                try:
                    # 获取该招标公告或结果的网页来源源代码、为了获取它的标题
                    original_link_text = requests.get(each_link.decode(), headers=self.casual_headers).content.decode()
                    original_resp = etree.HTML(original_link_text)
                    title = str(original_resp.xpath('//title/text()')[0][:15])
                    # 写入链接以及地址
                    f.write(each_link.decode() + '\t' + title + '\n')
                except Exception as e:
                    print(e, 444444444)
                    f.write(each_link.decode() + '\n')
                    continue

    def run(self):
        # for page in range(3, 5):
        self.crawl_list(1)


if __name__ == '__main__':
    qs = Qianlima_Spider()
    qs.run()
