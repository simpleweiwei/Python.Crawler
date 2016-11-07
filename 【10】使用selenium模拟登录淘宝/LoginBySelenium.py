from selenium import webdriver
import os
from bs4 import BeautifulSoup
import time


class ChromeWebDriver:
    """
    模拟浏览器
    """
    # 此处要设定chrome driver路径
    chromedriver = "C:\Program Files (x86)\Google\Chrome\Application\chromedriver.exe"
    os.environ["webdriver.chrome.driver"] = chromedriver
    driver = webdriver.Chrome(chromedriver)

    def auto_send(self, my_username, my_password):
        self.driver.get("https://login.taobao.com/member/login.jhtml")
        self.driver.implicitly_wait(15)
        self.driver.find_element_by_id("TPL_username_1").clear()
        self.driver.find_element_by_id("TPL_password_1").clear()
        self.driver.find_element_by_id("TPL_username_1").send_keys(my_username)
        self.driver.find_element_by_id("TPL_password_1").send_keys(my_password)
        self.driver.find_element_by_id("J_SubmitStatic").click()
        time.sleep(5)
        cookie = [item["name"] + "=" + item["value"] for item in self.driver.get_cookies()]
        cookiestr = ';'.join(item for item in cookie)
        print(cookie)
        print(cookiestr)
        print("登陆后：" + self.driver.current_url)
        self.driver.get("https://cart.taobao.com/cart.htm")
        print("购物车页面：" + self.driver.current_url)
        html_text = self.driver.page_source
        self.driver.close()
        return html_text


def parse_html(html):
    # 解析购物车
    soup = BeautifulSoup(html, 'html.parser')
    result = soup.find_all("div", attrs={"class": "shop-info"})
    for item in result:
        print(item.a.get_text())  # 获取店铺名


if __name__ == "__main__":
    browser = ChromeWebDriver()
    html_text = browser.auto_send("XXX", "123456")  # 账号密码
    parse_html(html_text)
