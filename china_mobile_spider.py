import requests, time, pymysql, re, redis, threading
from lxml import etree
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from city_data import get_city_dict
from Regular_Expression import regularExpression


class China_mobile_spider:

    def __init__(self):
        self.base_url = 'https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html'
        self.headers = {
            'Host' : 'b2b.10086.cn',
            'Referer': 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            # 'Cookie': 'saplb_*=(J2EE204289720)204289750; JSESSIONID=9lSNLXETgElfDjJ06OHVRxwU2Y3ObAHWNi0M_SAPFdqkRBM4y2JyDKsnuddVXXzh'
        }
        self._qt = ''
        # 请求首页获取第一个cookie
        self.url = 'https://b2b.10086.cn/b2b/main/preIndex.html'
        # 获取JSEESIONID
        self.url02 = 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2'
        # 获取post参数qt
        self.get_qt_url = 'https://b2b.10086.cn/b2b/main/listVendorNotice.html?noticeType=2'
        # 采购公告 资格预审
        self.bidding = '2?_qt={}&page.currentPage={}'
        self.qulificate = '3?_qt={}&page.currentPage={}'
        self.candidate = '7?_qt={}&page.currentPage={}'
        self.result = '16?_qt={}&page.currentPage={}'
        self.singleSource = '1?_qt={}&page.currentPage={}'
        self.last_part = '&page.perPageSize=20&noticeBean.sourceCH=&noticeBean.source=&noticeBean.title=&noticeBean.startDate=&noticeBean.endDate='
        self.duplicate_part = 'https://b2b.10086.cn/b2b/main/listVendorNoticeResult.html?noticeBean.noticeType='
        self.article_url = 'https://b2b.10086.cn/b2b/main/viewNoticeContent.html?noticeBean.id='
        self.city_dict = get_city_dict()
        self.lock = threading.Lock()
        self.conn = pymysql.connect(host='47.106.13.62',
                                    user='root',
                                    password='jack888mydb',
                                    database='zb_data',
                                    # database='test_demo',
                                    port=3306,
                                    charset='utf8')
        self.cur = self.conn.cursor()

        pool = redis.ConnectionPool(host='120.77.159.174', port=6379, db=15)
        self.r = redis.Redis(connection_pool=pool)
        # 转换成localtime
        now_time = '%.0f' % time.time()
        time_local = time.localtime(int(now_time))
        # 转换成新的时间格式(2016-05-05 20:28:54)
        # dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
        self.dt = time.strftime("%Y-%m-%d", time_local)
        self.session = requests.session()


    def upload_items(self, items):

        dirty_article = requests.get(items['url'], headers = self.headers).content.decode()
        try:
            dirty_article = re.search(r'(<div id="mobanDiv">.*?)<div class=" footer" style="">', str(dirty_article), re.S).group(1)
        except:
            dirty_article = re.search(r'(<table class="zb_table".*?)<div class=" footer"', str(dirty_article), re.S).group(1)
        dirty_article = re.sub(r'href="', 'href="https://b2b.10086.cn', dirty_article, flags = re.S)
        # 将文章的垃圾数据进行清洗
        clean_article = re.sub(regularExpression, ' ', dirty_article)
        items["intro"] = clean_article
        items['source_name'] = '中国移动采购与招标网'

        if items['addr_id'] == '':
            items['addr_id'] = '100'

        # print(items)
        try:
            if items['addr_id'] != '' and items['title'] != '' and items['url'] != '' and items['intro'] != '' and \
                    items['web_time'] != '':
                items['web_time'] = int(time.mktime(time.strptime(items['web_time'], "%Y-%m-%d")))
                # 正式上传到服务器
                sql = "INSERT INTO ztb_py_data (catid,title,style,addtime,adddate,areaid,linkurl,content) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (items['type_id'], items['title'], items['source_name'], items['time'], items['web_time'], items['addr_id'], items['url'], pymysql.escape_string(items['intro']))
                time.sleep(0.1)
                self.lock.acquire()
                self.cur.execute(sql)
                self.conn.commit()
                self.lock.release()
                self.r.hincrby(self.dt, items['source_name'])
                print('ok')

                # 单机测试
                # print(items)
                # sql = "INSERT INTO winkboy (catid,title,style,addtime,adddate,areaid,linkurl,content) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % ( items['type_id'], items['title'], items['source_name'], int(items['time']), items['web_time'], items['addr_id'], items['url'], pymysql.escape_string(items['intro']))
                # self.lock.acquire()
                # self.cur.execute(sql)
                # self.conn.commit()
                # self.lock.release()
                # print('1')

            else:
                try:
                    items['web_time'] = int(time.mktime(time.strptime(items['web_time'], "%Y-%m-%d")))
                except:
                    pass

                sql = "INSERT INTO ztb_error_infos (catid,title,style,addtime,adddate,areaid,status,linkurl,content) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
                    items['type_id'], items['title'], items['source_name'], items['time'], items['web_time'],
                    items['addr_id'], 3, items['url'], pymysql.escape_string(items['intro']))
                self.lock.acquire()
                self.cur.execute(sql)
                self.conn.commit()
                self.lock.release()



        except Exception as e:
            print("数据上传失败")
            print(items['title'])
            print(items['url'])
            print(e)


    def parse(self, url):
        # for url in urls:
        # print(url)
        z = self.duplicate_part + url + self.last_part
        # print(z)
        post_url = z.rsplit('?', 1)[0]
        a = z.rsplit('?', 1)[-1]
        # print(a)
        data = {}
        b = a.split('&')
        # print(b)
        for i in b:
            c = i.split('=')
            d = c[0]
            e = c[1]
            data[d] = e
        resp = requests.post(post_url, headers = self.headers, data = data).content.decode()
        resp = etree.HTML(resp)
        list_url = resp.xpath('//table[@class="zb_result_table"]//tr')[2:]
        if len(list_url) == 0:
            pass
        for each_tr in list_url[:]:
            items = {}
            items['intro'] = ''
            items['addr_id'] = '100'
            items['title'] = ''
            items['url'] = ''
            items['web_time'] = ''
            items["time"] = '%.0f' % time.time()

            try:
                items['title'] = each_tr.xpath('./td[3]/a/text()')[0]
            except:
                pass

            try:
                items['web_time'] = each_tr.xpath('./td[4]/text()')[0]
                if len(items['web_time']) < 10:
                    hehe = int(time.mktime(time.strptime(items['web_time'], "%Y-%m-%d")))
                    time_local = time.localtime(hehe)
                    items['web_time'] = time.strftime("%Y-%m-%d", time_local)
            except:
                pass

            try:
                dirty_url = each_tr.xpath('./@onclick')[0]
                article_id = re.search(r'\(\'(.*?)\'\)', dirty_url, re.S).group(1)
                items['url'] = self.article_url + article_id
            except:
                pass

            if items['addr_id'] == '100':
                for each_city in self.city_dict:
                    if each_city in items['title']:
                        items['addr_id'] = self.city_dict[each_city]
                        break

            # 如果标题出现失败、基本可以证明是失败公示、所以将其纳入38257
            if '中标' in items['title'] or '成交' in items['title'] or '结果' in items['title'] or '失败' in \
                    items['title'] or '流标' in items['title'] or '候选人' in items['title'] or '中选人' in \
                    items['title'] or '作废' in items['title'] or '终止' in items['title']:
                items['type_id'] = '38257'
            elif '更正' in items['title'] or '变更' in items['title'] or '答疑' in items['title'] or '澄清' in \
                    items['title'] or '补充' in items['title'] or '延期' in items['title']:
                items['type_id'] = '38256'
            else:
                items['type_id'] = '38255'

            self.upload_items(items)
            # print(items)


    def getCookies(self):
        # 获取到第一个cookies saplb_*
        r = self.session.get(self.url, headers = self.headers)
        cookies01 = requests.utils.dict_from_cookiejar(r.cookies)
        # print(cookies01)
        for i in cookies01.items():
            # print(i[1] == '(J2EE204289720)204289752')
            cookies01 = i[0] + '=' + i[1]
            self.headers['Cookie'] = i[0] + '=' + i[1] + ';'

        # 获取第二个cookies JSESSIONID
        resp = self.session.get(self.url02, headers = self.headers)
        cookies02 = resp.cookies['JSESSIONID']
        cookies02 = 'JSESSIONID' + '=' + cookies02 + '; '
        self.headers['Cookie'] = cookies02 + cookies01


    def get_qt(self):
        qt = self.session.get(self.get_qt_url, headers = self.headers).content.decode()
        # print(qt)

        qtPart01 = re.search(r'\'(\w{14})\'', qt, re.S).group(1)
        qtPart02 = re.search(r'\'(\w{29})\'', qt, re.S).group(1)
        self._qt = qtPart01 + qtPart02
        print(self._qt)


    def run(self):
        self.getCookies()
        self.get_qt()
        start = time.time()
        all_list_pages = []
        # # 采购公告@6 资格预审公告@1 候选人公告@4 中选人结果@4 单一来源采购信息@4
        all_list_pages.extend([self.bidding.format(self._qt, i) for i in range(1, 7)])
        all_list_pages.extend([self.qulificate.format(self._qt, i) for i in range(1, 2)])
        all_list_pages.extend([self.candidate.format(self._qt, i) for i in range(1, 5)])
        all_list_pages.extend([self.result.format(self._qt, i) for i in range(1, 5)])
        all_list_pages.extend([self.singleSource.format(self._qt, i) for i in range(1, 5)])
        # print(all_list_pages)

        try:
            with ThreadPoolExecutor(max_workers=3) as pool:
                pool.map(self.parse, all_list_pages)
        except Exception as e:
            print(e)


        # self.parse(all_list_pages)
        end = time.time()
        print(end - start)


if __name__ == '__main__':
    cms = China_mobile_spider()
    cms.run()