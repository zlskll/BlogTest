from operator import truediv

from selenium.webdriver.common.by import By

from common.Utils import BlogDriver
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import  re

#提取blogid
def extract_blogid(url):
    pattern=r'blog_detail\.html\?blogId=(\d+)'
    match=re.search(pattern,url)
    if match:
        return match.group(1)
    return None


class BlogDetail:
    url=""
    driver=""
    def __init__(self,first_blogid=""):
        self.url=f"http://8.137.19.140:9090/blog_detail.html?blogId={first_blogid}"
        self.driver=BlogDriver.driver
        self.driver.get(self.url)


    def IN_LoginStateTest(self):
        #页面元素检查,添加等待
        WebDriverWait(self.driver,100).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"#detail"))
        )
        self.driver.find_element(By.CSS_SELECTOR,"body > div.container > div.right > div > div.title")
        self.driver.find_element(By.CSS_SELECTOR,"body > div.container > div.right > div > div.date")
        self.driver.find_element(By.CSS_SELECTOR,"#detail")
        #截图记录
        BlogDriver.SavePicture()

    def NOTIN_LoginStateTest(self):
        # 会跳转到登录页面,有跳转所以添加等待
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR, "body > div.container-login > div > h3"))
        )

        # 截图记录
        BlogDriver.SavePicture()


    #删除按钮的测试
    def IN_LoginDeleteTest(self,deleteid):
        self.driver.get(f"http://8.137.19.140:9090/blog_detail.html?blogId={deleteid}")
        #跳转，添加等待
        WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located((By.CSS_SELECTOR,"body > div.container > div.right > div > div.operating > button:nth-child(2)"))
        )
        self.driver.find_element(By.CSS_SELECTOR,"body > div.container > div.right > div > div.operating > button:nth-child(2)").click()
        #等待确认弹窗出现
        AlertAccDelete=WebDriverWait(self.driver, 10).until(
            EC.alert_is_present()
        )
        #确认
        AlertAccDelete.accept()
        #确认后回到主页,查看是不是删除成功了
        isfind_id=self.__findid(deleteid)
        assert isfind_id is None


    #根据blogid查找，找到就返回这个元素
    def __findid(self,blogid):
        elemlist=self.driver.find_elements(By.CSS_SELECTOR,'[class="blog"]')
        for index in range(len(elemlist)):
            elem_detail=elemlist[index].find_element(By.CSS_SELECTOR,'[class="detail"]')
            elem_href=elem_detail.get_attribute('href')
            if blogid==extract_blogid(elem_href):
                return elemlist[index]
        return None