import random
import requests
from bs4 import BeautifulSoup
import time

# 使用BeautifulSoup4匹配内容
# 伪装成浏览器爬取博客园文章 [博客园做了反爬]
# 有些网站会检查你是不是真的浏览器访问，还是机器自动访问的。这种情况，加上User-Agent，表明你是浏览器访问即可。有时还会检查是否带Referer信息还会检查你的Referer是否合法，一般再加上Referer。
x = 0  # 标号


def get_header():
    headers = [
        "Mozilla/5.0 (Windows NT 10.0; WOW64; Trident/7.0; rv:11.0) like Gecko",
        "Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.116 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:48.0) Gecko/20100101 Firefox/48.0",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/51.0.2704.79 Safari/537.36 Edge/14.14393"]
    referer = r"http://www.cnblogs.com/"
    return {'User-Agent': headers[random.randint(0, 3)], 'Referer': referer}


def get_html(url):
    response = requests.get(url=url, headers=get_header())
    return response.text


def html_match(html):
    soup = BeautifulSoup(html, 'html.parser')
    return soup.find_all("a", attrs={"class": "titlelnk"})  # css选择器


def handle_content(content_list):
    global x
    for content in content_list:  # 遍历这个列表
        title = content.contents
        with open(r'D:\webFile\file.txt', 'a') as f:
            f.write(str(x) + r":" + ''.join(title) + '\n')
        x += 1


def main():
    url = 'http://www.cnblogs.com/#p' + str(36)
    html = get_html(url)
    results = html_match(html)
    print(url)
    print(results)
    handle_content(results)


if __name__ == '__main__':
    main()
