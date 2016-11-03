import requests
from requests.adapters import HTTPAdapter
import re
import time
import os.path
import json
import random
try:
    from PIL import Image
except:
    pass
from bs4 import BeautifulSoup

# 知乎用户名密码是明文

logn_url = r"https://www.zhihu.com/#signin"
session = requests.session()
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36'
}

content = session.get(logn_url, headers=headers, verify=False).content
soup = BeautifulSoup(content, 'html.parser')


def getxsrf():
    return soup.find('input', attrs={'name': "_xsrf"})['value']


# 获取验证码
def get_captcha():
    t = str(int(time.time() * 1000))
    captcha_url = 'https://www.zhihu.com/captcha.gif?r=' + t + "&type=login"
    r = session.get(captcha_url, headers=headers, verify=False)
    with open('captcha.jpg', 'wb') as f:
        f.write(r.content)
        f.close()
    # 用pillow 的 Image 显示验证码
    # 如果没有安装 pillow 到源代码所在的目录去找到验证码然后手动输入
    try:
        im = Image.open('captcha.jpg')
        im.show()
        im.close()
    except:
        print(u'请到 %s 目录找到captcha.jpg 手动输入' % os.path.abspath('captcha.jpg'))
    captcha = input("please input the captcha\n>")
    return captcha


def isLogin():
    # 通过查看用户个人信息来判断是否已经登录
    url = "https://www.zhihu.com/settings/profile"
    login_code = session.get(url, allow_redirects=False, verify=False).status_code
    if int(x=login_code) == 200:
        return True
    else:
        return False


def login(secret, account):
    # 通过输入的用户名判断是否是手机号
    if re.match(r"^1\d{10}$", account):
        print("手机号登录 \n")
        post_url = 'https://www.zhihu.com/login/phone_num'
        postdata = {
            '_xsrf': getxsrf(),
            'password': secret,
            'remember_me': 'true',
            'phone_num': account
        }
    else:
        print("邮箱登录 \n")
        post_url = 'https://www.zhihu.com/login/email'
        postdata = {
            '_xsrf': getxsrf(),
            'password': secret,
            'remember_me': 'true',
            'email': account
        }
    try:
        # 不需要验证码直接登录成功
        login_page = session.post(post_url, data=postdata, headers=headers, verify=False)
        login_code = login_page.text
        print(login_page.status)
        print(login_code)
    except:
        # 需要输入验证码后才能登录成功
        postdata["captcha"] = get_captcha()
        login_page = session.post(post_url, data=postdata, headers=headers, verify=False)
        login_code = eval(login_page.text)
        print(login_code['msg'])


def getImageUrl(offsetLimit):
    allImageUrl = []
    url = r"https://www.zhihu.com/node/QuestionAnswerListV2"
    offset = 10
    while offset <= offsetLimit:
        time.sleep(random.randint(30, 60))  # 随机睡觉
        print("----offset----" + str(offset))
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/52.0.2743.82 Safari/537.36',
            'Referer': 'https://www.zhihu.com/question/34243513',
            'Origin': 'https://www.zhihu.com',
            'Accept-Encoding': 'gzip, deflate, br'
        }
        data = {
            'method': 'next',
            'params': '{"url_token":' + str(34243513) + ',"pagesize": "10",' + '"offset":' + str(offset) + "}",
            '_xsrf': getxsrf()
        }
        offset += 10
        question = session.post(url, headers=header, data=data, verify=False)
        dic = json.loads(question.content.decode('ISO-8859-1'))
        listMsg = dic['msg']
        if not listMsg:
            print("获取question第【" + str((offset - 10) / 10) + "】页回答的图片URL列表完毕")
            return set(allImageUrl)
        pattern = re.compile(r'data-actualsrc="(.*?)">', re.S)
        for pageUrl in listMsg:
            items = re.findall(pattern, pageUrl)
            for item in items:
                allImageUrl.append(item)
    else:
        print("获取question第【" + str((offset - 10) / 10) + "】页回答的图片URL列表完毕")
        return set(allImageUrl)


def saveImagesFromUrl(imagesUrl):
    print("图片总数：" + str(len(imagesUrl)))
    if not imagesUrl:
        print("图片URL集合为空")
        return
    nameNumber = 0
    for image in imagesUrl:
        time.sleep(random.randint(15, 40))  # 随机睡觉
        print("downloading----" + image)
        suffixNum = image.rfind('.')
        suffix = image[suffixNum:]
        fileName = r"D:\webFile\{0}{1}".format(str(nameNumber), suffix)
        nameNumber += 1
        try:
            # 设置超时重试次数及超时时间单位秒
            session.mount(image, HTTPAdapter(max_retries=3))
            response = session.get(image, timeout=20, verify=False)
            contents = response.content
            with open(fileName, "wb") as pic:
                pic.write(contents)
        except IOError:
            print("io error")
        except requests.exceptions.ConnectionError:
            print("连接超时,URL:" + image)
    print("图片下载完毕")


if __name__ == '__main__':

    if isLogin():
        print('您已经登录')
    else:
        account = input('请输入你的用户名\n>  ')
        secret = input("请输入你的密码\n>  ")
        login(secret, account)
    imagesUrl = getImageUrl(10)  # 下载链接
    saveImagesFromUrl(imagesUrl)  # 保存图片
