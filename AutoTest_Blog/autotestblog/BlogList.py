from selenium.webdriver.common.by import By
from selenium.webdriver.ie.webdriver import WebDriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from common.Utils import BlogDriver

import re  #正则表达式模块

# 匹配 http://8.137.19.140:9090/blog_detail.html?blogId=83588
def extract_blogid(url):
    pattern=r'blog_detail\.html\?blogId=(\d+)'
    match=re.search(pattern,url)
    if match:
        return match.group(1)
    return None

class BlogList:
    url=""
    driver=""
    first_blogid=""
    def __init__(self):
        self.url="http://8.137.19.140:9090/blog_list.html"
        self.driver=BlogDriver.driver
        self.driver.get(self.url)



    def GetFblogid(self):
        # 提取出第一个博客的blogid
        elem = WebDriverWait(self.driver, 10).until(
            EC.visibility_of_element_located(
                (By.CSS_SELECTOR, "body > div.container > div.right > div:nth-child(1) > a"))
        )
        self.first_blogid = extract_blogid(elem.get_attribute("href"))
        return self.first_blogid

    def IN_LoginStateTest(self):
        #页面元素检查
        #个人信息部分
        self.driver.find_element(By.CSS_SELECTOR,"body > div.container > div.left > div > img")
        self.driver.find_element(By.CSS_SELECTOR,"body > div.container > div.left > div > h3")
        self.driver.find_element(By.CSS_SELECTOR,"body > div.container > div.left > div > div:nth-child(4) > span:nth-child(1)")
        self.driver.find_element(By.CSS_SELECTOR,"body > div.container > div.left > div > div:nth-child(4) > span:nth-child(2)")
        self.driver.find_element(By.CSS_SELECTOR,"body > div.container > div.left > div > div:nth-child(5) > span:nth-child(1)")
        self.driver.find_element(By.CSS_SELECTOR,"body > div.container > div.left > div > div:nth-child(5) > span:nth-child(2)")
        #博客部分加载慢，需要添加等待
        WebDriverWait(self.driver,100).until(
            EC.visibility_of_element_located( (By.CSS_SELECTOR,"body > div.container > div.right > div:nth-child(1) > div.title") )
        )
        self.driver.find_element(By.CSS_SELECTOR,"body > div.container > div.right > div:nth-child(1) > div.title")
        self.driver.find_element(By.CSS_SELECTOR,"body > div.container > div.right > div:nth-child(1) > div.date")
        self.driver.find_element(By.CSS_SELECTOR,"body > div.container > div.right > div:nth-child(1) > div.desc")
        self.driver.find_element(By.CSS_SELECTOR,"body > div.container > div.right > div:nth-child(1) > a")

        #截图记录
        BlogDriver.SavePicture()


    def NOTIN_LoginStateTest(self):
        #会跳转到登录页面,有跳转所以添加等待
        WebDriverWait(self.driver,10).until(
            EC.visibility_of_element_located( (By.CSS_SELECTOR,"body > div.container-login > div > h3") )
        )

        # 截图记录
        BlogDriver.SavePicture()