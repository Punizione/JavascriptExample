import requests
import re
import json

url = 'https://www.amap.com/service/poiInfo?query_type=TQUERY&pagesize=20&pagenum=1&qii=true&cluster_state=5&need_utd=true&utd_sceneid=400002&div=PC1000&addr_poi_merge=true&is_classify=true&zoom=4&city=440200&geoobj=83.023237%7C14.041081%7C125.210744%7C51.365187&keywords=%E5%94%AF%E6%84%8F'

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36',
    'Host': 'www.amap.com'
}

r = requests.get(url, headers = headers)
dirty_data = r.content.decode()
half_result = json.loads(dirty_data)['data']['poi_list']

for each in half_result:
    print(str(each))
    hehe = re.findall(r'\'value\':\s(\'[\u4e00-\u9fa5]+\')', str(each), re.S)
    print(hehe)
    break