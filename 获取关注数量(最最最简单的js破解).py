import requests
import json

'''
'http://www.eshow365.com/zhanhui/html/127989_0.html#' 链接
第一步 通过查看网页源代码 发现关注人数无法显示出来
第二步 在这段html标签中 该span标签虽然关注人数无法显示出来、但是你会发现通过这个span标签的id'txtClicks'，然后全站搜索
你会发现下面这段javascript代码、该代码意思很明确 通过post下面这个url，带上下面两个参数便可以获取到关注量。
下面是代码实现
'''

'''
<script type="text/javascript">
    $(function () {
        $.post("/ZhanHui/ajax/UpdateClickByEshowNo.ashx", { id: 127989, isupdate: 1 }, function(data) {
                    $("#txtClicks").html(data.Click);
                }, "json");
                          
                        })
</script>

'''

url = 'http://www.eshow365.com/zhanhui/html/127989_0.html'
base_url = 'http://www.eshow365.com'
concern_nums = '/ZhanHui/ajax/UpdateClickByEshowNo.ashx'

article_id = url.split('/')[-1].split('_')[0]

data = {
	'id' : article_id,
	'isupdate' : '1'
}

headers = {
	'Host' : 'www.eshow365.com',
	'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.96 Safari/537.36'
}

r = requests.post(url = base_url + concern_nums, headers = headers, data = data)
print(json.loads(r.content.decode())['Click'])
