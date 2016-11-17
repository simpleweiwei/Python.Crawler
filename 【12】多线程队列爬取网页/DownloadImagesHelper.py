import re
import requests
import time


class ImagesHelper:
    def __init__(self, queue, start_page=2100, end_page=2105):
        self.start_page = start_page
        self.end_page = end_page
        self.url_queue = queue

    def get_urls(self):
        for item in range(self.start_page, self.end_page):
            time.sleep(1)
            targetUrl = "http://jandan.net/ooxx/page-" + str(item) + "#comments"
            html = requests.get(targetUrl).text
            pic_url = re.findall('<img src="(.*?)"', html, re.S)
            for url in pic_url:
                self.url_queue.put(url)

    @staticmethod
    def down_url(url, image_no):
        print('now downloading:' + url)
        try:
            pic = requests.get(url)
        except Exception:
            return
        if url.find(".jpg") > 0:
            fp = open("D:\\webCrawling\\" + str(image_no) + '.jpg', 'wb')
        elif url.find(".png") > 0:
            fp = open("D:\\webCrawling\\" + str(image_no) + '.png', 'wb')
        else:
            return
        fp.write(pic.content)
        fp.close()
