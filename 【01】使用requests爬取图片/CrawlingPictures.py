import re
import requests
import time

# 适当修改即可爬取任意图片，不借助第三方框架

i = 0
# reg = r'href="(.*?\.jpg)" '
# jpgre = re.compile(reg)
for item in range(2100, 2160):
    # targetUrl = "http://www.meh.ro/page/" + str(item)
    targetUrl = "http://jandan.net/ooxx/page-" + str(item) + "#comments"
    html = requests.get(targetUrl).text
    # time.sleep(5)
    pic_url = re.findall('<img src="(.*?)"',html,re.S)
    # pic_url = re.findall(jpgre, html)
    print(str(item))

    for each in pic_url:
        # url = 'http://www.qdaily.com' + each
        url = each
        print('now downloading:' + url)
        try:
            pic = requests.get(url)
        except Exception:
            continue
        if url.find(".jpg") > 0:
            fp = open('pic//' + str(i) + '.jpg','wb')
        elif url.find(".png") > 0:
            fp = open('pic//' + str(i) + '.png','wb')
        else:
            continue
        # fp = open('pic//' + str(i) + '.jpg','wb')
        fp.write(pic.content)
        fp.close()
        i += 1