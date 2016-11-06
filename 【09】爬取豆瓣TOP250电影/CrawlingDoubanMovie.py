"""
爬取豆瓣电影TOP250
"""

import codecs
import time
import random
import requests
from bs4 import BeautifulSoup

DOWNLOAD_URL = 'https://movie.douban.com/top250'
movie_no = 1


def download_page(url):
    return requests.get(url, headers={
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_2) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/47.0.2526.80 Safari/537.36'
    }, verify=False).content


def parse_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    movie_list_soup = soup.find('ol', attrs={'class': 'grid_view'})
    movie_name_list = []
    for movie_li in movie_list_soup.find_all('li'):
        detail = movie_li.find('div', attrs={'class': 'hd'})
        movie_name = detail.find('span', attrs={'class': 'title'}).getText()
        movie_name_list.append(movie_name)
    # 下面的语句比较巧妙：用程序查找下一页链接然后拼接返回，不需要知道有多少页
    next_page = soup.find('span', attrs={'class': 'next'}).find('a')
    if next_page:
        return movie_name_list, DOWNLOAD_URL + next_page['href']
    return movie_name_list, None


def main():
    url = DOWNLOAD_URL
    global movie_no
    with open(r'D:\Movies.txt', 'a') as f:
        while url:  # 这样不管有多少页都能爬完
            time.sleep(random.randint(5, 10))
            html = download_page(url)
            movies, url = parse_html(html)
            for movie in movies:
                f.write(str(movie_no) + r': ' + str(movie) + '\n')
                movie_no += 1


if __name__ == '__main__':
    main()
