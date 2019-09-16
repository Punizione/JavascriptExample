import os, time, re, redis, pymysql,time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from lxml import etree
from city_data import get_city_dict
from Regular_Expression import regularExpression

# os.system('cd /Users/杰/AppData/Local/Google/Chrome/Application')
# os.system('chrome.exe --remote-debugging-port=9222 -user-data-dir="c:/selenium/automationprofile"')

class China_unicom(object):
	def __init__(self):
		self.city_dict = get_city_dict()
		self.pattern01 = r'服务区域：(.*?)<'
		self.pattern02 = r'服务地点：(.*?)<'
		self.pattern03 = r'服务地址：(.*?)<'
		self.pattern04 = r'采.*?购.*?人(.*?)<'
		self.pattern05 = r'比.*?选.*?人：(.*?)<'
		self.pattern08 = r'地址：(.*?)<'
		self.pattern06 = r'联系地址：(.*?)<'
		self.pattern07 = r'详细地址：(.*?)<'
		# 正则表达式的规则列表
		self.pattern_list = [self.pattern01, self.pattern02, self.pattern03, self.pattern04, self.pattern08, self.pattern05, self.pattern06, self.pattern07]
		# self._arguments = []
		self.base_url = 'http://www.chinaunicombidding.cn'
		self.chrome_options = Options()
		# chrome_options.add_experimental_option("debuggerAddress","127.0.0.1:9222")
		self.chrome_options.add_argument('disable-infobars')
		self.chrome_options.add_experimental_option('excludeSwitches', ['enable-automation'])
		# self.option = webdriver.ChromeOptions()
		self.going_to_crawl_bid = '{}&type=1'
		self.going_to_crawl_result = '{}&type=2'
		self.going_to_crawl_single = '{}&type=3'
		self.duplicate_part = 'http://www.chinaunicombidding.cn/jsp/cnceb/web/info1/infoList.jsp?page='

		self.conn = pymysql.connect(host='0.0.0.0',
									user='root',
									password='jiayou875',
									database='zb_data',
									# database='test_demo',
									port=3306,
									charset='utf8')
		self.cur = self.conn.cursor()

		pool = redis.ConnectionPool(host='0.0.0.0', port=6379, db=15)
		self.r = redis.Redis(connection_pool=pool)
		# 转换成localtime
		now_time = '%.0f' % time.time()
		time_local = time.localtime(int(now_time))
		# 转换成新的时间格式(2016-05-05 20:28:54)
		# dt = time.strftime("%Y-%m-%d %H:%M:%S",time_local)
		self.dt = time.strftime("%Y-%m-%d", time_local)


	def upload_items(self, items):
		if items['addr_id'] == '':
			items['addr_id'] = '100'
		try:
			if items['addr_id'] != '' and items['title'] != '' and items['url'] != '' and items['intro'] != '' and items[
				'web_time'] != '':
				items['web_time'] = int(time.mktime(time.strptime(items['web_time'], "%Y-%m-%d")))
				# 正式上传到服务器
				sql = "INSERT INTO ztb_py_data (catid,title,style,addtime,adddate,areaid,linkurl,content) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
					items['type_id'], items['title'], items['source_name'], items['time'], items['web_time'],
					items['addr_id'],
					items['url'], pymysql.escape_string(items['intro']))
				time.sleep(0.1)
				self.cur.execute(sql)
				self.conn.commit()
				self.r.hincrby(self.dt, items['source_name'])

				# 单机测试
				# sql = "INSERT INTO winkboy (catid,title,style,addtime,adddate,areaid,linkurl,content) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % ( items['type_id'], items['title'], items['source_name'], items['time'], items['web_time'], items['addr_id'], items['url'], pymysql.escape_string(items['intro']))
				# self.cur.execute(sql)
				# self.conn.commit()

			else:
				try:
					items['web_time'] = int(time.mktime(time.strptime(items['web_time'], "%Y-%m-%d")))
				except:
					pass

				sql = "INSERT INTO ztb_error_infos (catid,title,style,addtime,adddate,areaid,status,linkurl,content) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s');" % (
					items['type_id'], items['title'], items['source_name'], items['time'], items['web_time'],
					items['addr_id'], 3, items['url'], pymysql.escape_string(items['intro']))
				self.cur.execute(sql)
				self.conn.commit()


		except Exception as e:
			print("数据上传失败")
			print(items['title'])
			print(items['url'])
			print(e)


	def get_response(self, resource, driver):
		list_content = etree.HTML(resource)
		list_url = list_content.xpath('//div[@id="div1"]//tr[@height="35px"]')
		print(len(list_url))
		if len(list_url) == 0:
			pass
		for each_tr in list_url[:]:
			items = {}
			items['intro'] = ''
			items['addr_id'] = ''
			items['title'] = ''
			items['url'] = ''
			items['web_time'] = ''
			items["time"] = '%.0f' % time.time()

			items['title'] = each_tr.xpath('.//span/@title')[0].strip()

			# 获取文章id、然后使用网页前缀拼接文章id获取到文章的真实id
			article_url = each_tr.xpath('.//span/@onclick')[0]
			items['url'] = self.base_url + re.search(r'window.open\("(.*?)","",', article_url, re.S).group(1)
			print(items['url'])
			js = "window.open({})".format('"' + items['url'] + '"')  # 可以看到是打开新的标签页 不是窗口
			# print(js)
			time.sleep(0.01)
			Sucess = True
			# while Sucess:
			# 	try:
			# 		driver.execute_script(js)
			# 		driver.implicitly_wait(30)
			# 		Sucess = False
			# 	except:
			# 		driver.switch_to_window(3)
			# 		driver.refresh()
			# time.sleep(2.5)
			try:
				driver.execute_script(js)
				driver.implicitly_wait(30)
			except:
				driver.switch_to_window(3)
				driver.refresh()
			now_handle = driver.current_window_handle
			# print(driver.window_handles, now_handle)
			driver.switch_to_window(driver.window_handles[driver.window_handles.index(now_handle) + 1])
			# 获取日期
			items['web_time'] = each_tr.xpath('.//td/following-sibling::td/text()')[0].strip()
			# 获取到地址然后通过城市表获取城市id
			try:
				items['address'] = each_tr.xpath('.//td[3]/text()')[0].strip()
			except:
				pass
			dirty_article = driver.page_source
			# print(dirty_article)
			try:
				# print(1111111)
				time.sleep(0.01)
				dirty_article = re.search(r'<body.*?>(.*?)</body></html>',str(dirty_article), re.S).group(1)
				dirty_article = re.sub(r'href="', 'href="http://www.chinaunicombidding.cn', dirty_article, flags = re.S)
				dirty_article = re.sub(r'<iframe.*?>.*?</iframe>', '', dirty_article, flags = re.S)
				# print(2222222)
				# 将文章的垃圾数据进行清洗
				clean_article = re.sub(regularExpression, ' ', dirty_article)
				items["intro"] = clean_article
				# print(items["intro"])
			except Exception as e:
				print(e)
				pass

			# 如果标题出现失败、基本可以证明是失败公示、所以将其纳入38257
			if '中标' in items['title'] or '成交' in items['title'] or '结果' in items['title'] or '失败' in items['title'] or '流标' in items['title'] or '候选人' in items['title'] or '中选人' in items['title'] or '作废' in items['title'] or '终止' in items['title']:
				items['type_id'] = '38257'
			elif '更正' in items['title'] or '变更' in items['title'] or '答疑' in items['title'] or '澄清' in items['title'] or '补充' in items['title'] or '延期' in items['title']:
				items['type_id'] = '38256'
			else:
				items['type_id'] = '38255'

			try:
				for each_city in self.city_dict:
					if each_city in items['address']:
						items['addr_id'] = self.city_dict[each_city]
						break
			except:
				pass

			# 如果从地址栏找不到地址 则从标题获取
			if items['addr_id'] == '':
				for each_city in self.city_dict:
					if each_city in items['title']:
						items['addr_id'] = self.city_dict[each_city]
						break

			if items['addr_id'] == '':
				for each_pattern in self.pattern_list:
					try:
						search_text = re.search(each_pattern, dirty_article, re.S).group(1)
						for city_name in self.city_dict:
							if city_name in search_text:
								items['addr_id'] = self.city_dict[city_name]
								break
					except:
						continue

					if items['addr_id'] != '':
						break
			items["source_name"] = '中国联通采购与招标网'
			self.upload_items(items)
			# print(items['title'])
			driver.close()
			time.sleep(0.01)
			driver.switch_to_window(driver.window_handles[driver.window_handles.index(now_handle)])
			# break

	def crawl_first_page(self, driver):
		driver.get('http://www.chinaunicombidding.cn/jsp/cnceb/web/info1/infoList.jsp?page=1&type=1')
		driver.implicitly_wait(25)
		self.get_response(driver.page_source, driver)

	def run(self):
		all_list_pages = []
		all_list_pages.extend([self.going_to_crawl_bid.format(i) for i in range(1, 20)])
		all_list_pages.extend([self.going_to_crawl_result.format(i) for i in range(1, 7)])
		all_list_pages.extend([self.going_to_crawl_single.format(i) for i in range(1, 3)])
		print(len(all_list_pages))
		while all_list_pages:
			print(all_list_pages)
			driver = webdriver.Chrome(executable_path='C:/Program Files (x86)/Google/Chrome/Application/chromedriver.exe',options=self.chrome_options)

			time.sleep(1)
			current_page = all_list_pages[0]
			js = "window.open({})".format('"' + self.duplicate_part + current_page + '"')  # 可以看到是打开新的标签页 不是窗口
			# print(js)
			time.sleep(1)
			driver.execute_script(js)
			time.sleep(2)
			all_list_pages.pop(all_list_pages.index(all_list_pages[0]))
			driver.implicitly_wait(20)
			time.sleep(1)
			driver.switch_to_window(driver.window_handles[1])
			current_times = time.localtime(time.time())
			print(current_times)
			# print(driver.page_source[:500])
			if '<input' in driver.page_source[:500]:
				print(current_page)
				all_list_pages.append(current_page)
			else:
				print('success')
				self.get_response(driver.page_source, driver)

			driver.quit()



if __name__ == '__main__':
	while True:
		try:
			current_time = time.localtime(time.time())
			if current_time.tm_hour == 11 and current_time.tm_min == 35 and current_time.tm_sec == 0:
				c = China_unicom()
				c.run()
			elif current_time.tm_hour == 20 and current_time.tm_min == 37 and current_time.tm_sec == 0:
				c = China_unicom()
				c.run()
		except:
			pass
	#
	# c = China_unicom()
	# c.run()
