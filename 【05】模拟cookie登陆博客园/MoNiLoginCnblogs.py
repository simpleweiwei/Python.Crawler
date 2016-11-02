import requests

# 模拟登录博客园
# 1.首先使用Fiddler抓取提交的数据：POST的数据是input1,input2和remember
# 2.由于RSA加过密后的内容可以不一样，但是解密后的数据是一样的，所以上述抓取数据可以直接用做POST data
# 3.注意Cookie用的是登录后主页的cookie，不是登录页的cookie
# 4.注意https的问题


def login(url):
    session = requests.Session()
    headers = {
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        'Referer': 'https://passport.cnblogs.com/user/signin',
        'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
        'Cookie': '__gads=ID=a2833ae9f0b587fc:T=1442900505:S=ALNI_MYH5a0lbh_WzRtiOyab3WmNCeZGqA; _ga=GA1.2.520164261.1473159541; .CNBlogsCookie=4B0558BEFBD679ED9FC5E4BD4352B03E4FE3B78DE665546993CF44DFDD508A0C34DC81BCD3DF4043C2CBF1E9F93E311C64C696811E9E41BB94138AE5523161D7E4EA09CF852936A18564BAED477E2ACBF2615194'}
    login_data = {
        'input1': r'oJ6Kse65lwKXnm6G+gMmConvPjk+2T4PtI7Qk9DUVf32dNd1nTFKGlWUhsw7t8TiPlbIYnxxNSX6s1CcAvJtw1fwdmWehTrlUwv5n5PY7vZFaTGyI5I66LLs1DpXsAOgJrTFjE1rMgSl5AhqAsZT6oV3pz7aVQGR/sWq/ZffF3Y=',
        'input2': r'pHlftirvwn8iorZEMLSNnZmVAqSRezf1cckD3IbIbijDw9vtbTl2umiAFoTfCLQ/ftlM2CCjwgpFWXyHXvEf29y2KY+xVahAd+InIQz0HwAu0A2UMIx5VkmMXpPGdK4QLk4U22hPnUInN5Pa/G1posWDR0cvnox0lCTABRcVLvo=',
        'remember': 'false'
        }
    req = session.post(url, data=login_data, headers=headers, verify=False)  # 加verify是为了解决https证书错误
    print(req.status_code)  # 200
    print(req.content.decode())  # {"success":false,"message":"您已处于登录状态"}

    f = session.get('https://home.cnblogs.com/followers', headers=headers, verify=False)
    print(f.status_code)
    print(f.text)


def main():
    url = 'https://passport.cnblogs.com/user/signin'
    login(url)


if __name__ == '__main__':
    main()
