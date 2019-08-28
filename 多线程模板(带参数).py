import requests,pymysql, re, time, threading
from concurrent.futures import ThreadPoolExecutor
from functools import partial
from lxml import etree

class Crawl_company_name:
    def __init__(self):
        self.headers = {
            'Host': 'www.qianlima.com',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.100 Safari/537.36',
            }

        self.lock = threading.Lock()
        self.conn = pymysql.connect(
                            host='47.106.13.62',
                            user='root',
                            password='jiayou875',
                            database='test_demo',
                            # database='zb_data',
                            port=3306,
                            charset='utf8')
        self.cur = self.conn.cursor()


    def crawl_detail(self, page, f):
        try:
            resp = requests.get(f'http://www.qianlima.com/caizhao_{page}/', headers = self.headers).content.decode('gbk')
            full_name = etree.HTML(resp).xpath('//title/text()')[0]
            sample_name = re.sub(r'有限.*|分公司|公司', '', full_name, flags = re.S)
            if not sample_name == full_name:
                f.write(sample_name + '\n')
                f.write(full_name + '\n')
                print(f'正在写入id:{page}')
            else:
                f.write(full_name + '\n')

            
        except Exception as e:
            print(e)
            print(f'{page} 该网页id出现编码问题')
            pass

        try:
            self.upload_company_name(full_name, sample_name)
        except Exception as e:
            print(e)
            pass

    def upload_company_name(self, full, abbr):   
        try:
            sql = "INSERT INTO company_name (simple_name, full_name) VALUES ('%s', '%s');" % (abbr, full)
            time.sleep(0.3)
            self.lock.acquire()
            self.cur.execute(sql)
            self.conn.commit()
            self.lock.release()
        except:
            pass


    def run(self):
        with open('companyname8.txt', 'a')as f:
            urls = (i for i in range(1600000,  1800000))
            print('项目开启')
            try:
                with ThreadPoolExecutor(max_workers=3) as pool:
                    pool.map(partial(self.crawl_detail, f = f), urls)
            except Exception as e:
                print(e)
        self.conn.close()

if __name__ == '__main__':
    ccn = Crawl_company_name()
    ccn.run()


