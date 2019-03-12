import requests
import re


def get_iphone(url):
    """

    :param url: ex: https://www.51sole.com/company/detail_8290863.html
    :return: list ex:  ['023-52532105', '18996586800']
    """
    headers = {
        'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 '
                      '(KHTML, like Gecko) Chrome/72.0.3626.121 Mobile Safari/537.36'
    }
    res = requests.get(url, headers=headers)
    iphones = re.findall(r'/company/getimg/\?phone=(.+?)"', res.text, re.S)
    data = list()
    for iphone in iphones:
        data.append(iphone)
    print(data)
    return data


get_iphone('http://m.51sole.com/company/detail_4457551.html')




