import sys
import time

from selenium.webdriver.common import alert
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from common.Utils import BlogDriver

class BlogLogin:
    url=""
    driver=""
    def __init__(self):
        self.url="http://8.137.19.140:9090/blog_login.html"
        self.driver=BlogDriver.driver
        self.driver.get(self.url)

    #输入账号密码的子函数
    def _InputInforAndClick(self,username,password):
        #输入之前先清理输入框内容
        self.driver.find_element(By.CSS_SELECTOR, "#username").clear()
        self.driver.find_element(By.CSS_SELECTOR, "#password").clear()
        #输入
        self.driver.find_element(By.CSS_SELECTOR,"#username").send_keys(username)
        self.driver.find_element(By.CSS_SELECTOR,"#password").send_keys(password)
        self.driver.find_element(By.CSS_SELECTOR,"#submit").click()

    #正常登录
    def LoginSuccessTest(self):
        #输入正确的账号和正确的密码
        #self.driver.find_element(By.CSS_SELECTOR,"#username").send_keys("zhangsan")
        #self.driver.find_element(By.CSS_SELECTOR,"#password").send_keys("123456")
        #self.driver.find_element(By.CSS_SELECTOR,"#submit").click()
        self._InputInforAndClick("zhangsan","123456")

        #判断是否登录成功，因为涉及跳转，所以需要添加等待
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located( (By.CSS_SELECTOR, "body > div.container > div.left > div > h3") )
        )
        #停止网页渲染，用于调试的
        #self.driver.execute_script('window.stop();')
        #elem=self.driver.find_element(By.CSS_SELECTOR,"body > div.container > div.left > div > h3")
        assert elem.text=="zhangsan"

        #保存截图
        BlogDriver.SavePicture()
        #测试完返回登录页面
        self.driver.back()

    def LoginFailTest(self):
        #"zhangsan","12345"，输入正确的账号和错误的密码
        handle=self.driver.current_window_handle
        self._InputInforAndClick("zhangsan","12345")
        #唤起弹窗，添加显式等待，等待弹窗出现
        AlertWindow01=WebDriverWait(self.driver,10).until(
            EC.alert_is_present()
        )
        #断言弹窗文字是否符合预期
        assert AlertWindow01.text=="密码错误"
        #处理弹窗
        AlertWindow01.accept()
        #截个图
        BlogDriver.SavePicture()

        #"wangwu" "123456"， 输入错误的账号和正确的密码
        self._InputInforAndClick("wangwu","123456")
        AlertWindow02 = WebDriverWait(self.driver, 10).until(
            EC.alert_is_present()
        )
        # 断言弹窗文字是否符合预期
        assert AlertWindow02.text == "用户不存在"
        # 处理弹窗
        AlertWindow02.accept()
        # 截个图
        BlogDriver.SavePicture()

        # "wangwu" "1234"， 输入错误的账号和正确的密码
        self._InputInforAndClick("wangwu", "1234")
        AlertWindow03 = WebDriverWait(self.driver, 10).until(
            EC.alert_is_present()
        )
        # 断言弹窗文字是否符合预期
        assert AlertWindow03.text == "用户不存在"
        # 处理弹窗
        AlertWindow03.accept()
        # 截个图
        BlogDriver.SavePicture()
