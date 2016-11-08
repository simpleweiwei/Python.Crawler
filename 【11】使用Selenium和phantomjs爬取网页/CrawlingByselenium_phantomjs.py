from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time


# PhantomJS说白了就是一个没有界面的浏览器
driver = webdriver.PhantomJS(executable_path=r'D:\phantomjs-2.1.1-windows\bin\phantomjs.exe')
driver.set_window_size(1920, 1080)  # 控制屏幕截图的大小，实际上相当于浏览器的大小
driver.get("https://www.zhihu.com/#signin")
time.sleep(10)
driver.get_screenshot_as_file(r'D:\show.png')  # 打印登录页面，这样就可以查看验证码了
print("可以查看是否有验证码了")
time.sleep(30)
my_username = "xx"
my_password = "****"
driver.find_element_by_name("account").clear()
driver.find_element_by_name("password").clear()
driver.find_element_by_name("account").send_keys(my_username)
driver.find_element_by_name("password").send_keys(my_password)
time.sleep(2)
driver.get_screenshot_as_file(r'D:\showw.png')  # 打印登录页面，这样就可以查看验证码了
print("再次查看是否有验证码")
time.sleep(20)
code = input("请输入验证码：")  # 如没有则随意输入一个字符
if len(code) >= 4:
    my_code = code
else:
    my_code = ""
if my_code:
    driver.find_element_by_id("captcha").clear()
    driver.find_element_by_id("captcha").send_keys(my_code)
driver.find_element_by_tag_name("form").submit()
time.sleep(20)
driver.get_screenshot_as_file(r'D:\show2.png')
print("登录成功:" + driver.current_url)
user = driver.find_element_by_xpath(r'//a[@class="zu-top-nav-userinfo "]')
ActionChains(driver).move_to_element(user).perform()
time.sleep(10)
ActionChains(driver).click(user).perform()
print("跳转用户页面成功:" + driver.current_url)
time.sleep(20)
driver.get_screenshot_as_file(r'D:\show3.png')
# print(driver.page_source)
driver.quit()
