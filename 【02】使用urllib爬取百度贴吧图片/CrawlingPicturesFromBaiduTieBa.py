import re
import urllib.request

x = 0  # 标号


def getHtml(url):
    page = urllib.request.urlopen(url)  # 打开:在python3.3后urllib2已经不能再用，只能用urllib.request来代替
    html = page.read()  # 读取
    return html


def getimg(html, reg):
    html = html.decode('utf-8')  # 原因为Python3 findall数据类型用bytes类型，因此在正则表达式前应添加html = html.decode('utf-8')
    imgre = re.compile(reg, re.S)  # 开始正则的匹配。
    imglist = re.findall(imgre, html)  # 获取图片链表
    global x
    for img_url in imglist:  # 遍历这个列表
        urllib.request.urlretrieve(img_url, r'D:\webImage\%s.jpg' % x)  # 把列表中的每一个都保存下来，取名为 x.jpg
        print(img_url)
        x += 1


def demo1():
    for i in range(20):
        url = 'http://tieba.baidu.com/p/4830294363?pn=' + str(i)
        reg = r'class="BDE_Image" src="(.*?)" size'  # 此正则比较好用
        html = getHtml(url)
        getimg(html, reg)


def demo2():
    zhihuUrl = "https://www.zhihu.com/question/34243513"
    reg = r' data-original="(.*?)"'  # 此正则比较好用
    html = getHtml(zhihuUrl)
    getimg(html, reg)


def main():
    # demo1()
    demo2()


if __name__ == '__main__':
    main()
