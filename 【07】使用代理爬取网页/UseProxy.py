import requests
from bs4 import BeautifulSoup
import random
import time

"""
代理使用：

import requests

proxies = {
  "http": "http://10.10.1.10:3128",
  "https": "http://10.10.1.10:1080",
}

requests.get("http://example.org", proxies=proxies)
"""

# 此处代理ip下载速度极慢，建议换速度快的，或者设置为自己的本地IP
user_agent = 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5)'
headers = {'User-Agent': user_agent}
proxyList = []


def getListProxies():
    global proxyList
    session = requests.session()
    for i in range(1, 21):
        time.sleep(random.randint(1, 10))
        ip_url = r"http://www.kuaidaili.com/free/outha/" + str(i)
        page = session.get(ip_url, headers=headers)
        soup = BeautifulSoup(page.text, 'html.parser')
        taglist = soup.find('tbody').find_all('tr')
        for trtag in taglist:
            tdlist = trtag.find_all('td')
            if tdlist[6].string.find(r"2016") >= 0:
                proxy = {'http': tdlist[0].string + ':' + tdlist[1].string,
                         'https': tdlist[0].string + ':' + tdlist[1].string}
                url = "http://ip.chinaz.com/getip.aspx"  # 用来测试IP是否可用的url
                try:
                    response = session.get(url, proxies=proxy, timeout=3)
                    proxyList.append(proxy)
                    print("有效ip个数: " + len(proxyList) + "个")
                    if len(proxyList) == 10:
                        break
                except Exception as e:
                    print("第" + str(i) + "页：" + tdlist[0].string + ':' + tdlist[1].string + " 超时")
                    continue
    return proxyList


def main():
    proxyList = getListProxies()
    print(proxyList)


if __name__ == '__main__':
    main()
