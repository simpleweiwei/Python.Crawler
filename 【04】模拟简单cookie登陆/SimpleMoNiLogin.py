import requests

# 使用cookie登陆:数据为明文且无验证码


url = r"https://ptlogin.1234567.com.cn/ptlogin.aspx?pid=37&url=&msg="
UA = "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/49.0.2623.13 Safari/537.36"

header = {"User-Agent": UA,
          "Referer": "https://ptlogin.1234567.com.cn/ptlogin.aspx?pid=37&url=http%3a%2f%2f114.141.156.68%2fdefault.aspx&msg=%e5%af%b9%e4%b8%8d%e8%b5%b7%ef%bc%8c%e8%af%b7%e5%85%88%e7%99%bb%e5%bd%95%e3%80%82"
          }

simple_session = requests.Session()
postData = {'loginname': 'wangwei',
            'password': '123456',
            'button': ''
            }

simple_session.post(url,
                  data=postData,
                  headers=header)

f = simple_session.get(r'http://114.141.156.68/TaskInfo/TaskInfoManage.aspx?navigationInfo=%E4%BB%BB%E5%8A%A1%E7%AE%A1%E7%90%86;%E4%BB%BB%E5%8A%A1%E5%88%97%E8%A1%A8', headers=header)
print(f.content.decode())
