import time

from selenium.webdriver.common.by import By
from selenium.webdriver.remote.webelement import WebElement
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  common.Utils import BlogDriver

#用于显式等待的until，自定义显式等待条件
def text_isnot_empty(driver):
    elem=driver.find_element(By.CSS_SELECTOR,"#title")
    text=elem.get_attribute('value')
    return text!=''


class BlogEdit:
    url = ""
    driver = ""
    def __init__(self,first_blogid=""):
        self.url=f"http://8.137.19.140:9090/blog_update.html?blogId={first_blogid}"
        self.driver=BlogDriver.driver
        self.driver.get(self.url)

    #登录状态下测试
    def IN_LoginStateTestSuccess(self):
        #页面元素检查
            #加个显式等待
        WebDriverWait(self.driver,10).until(
            text_isnot_empty
        )
        self.driver.find_element(By.CSS_SELECTOR,"#title").clear()  #标题
        self.driver.find_element(By.CSS_SELECTOR,"#submit")  #发布按钮
        self.driver.find_element(By.CSS_SELECTOR,"#editor")  #md插件区

        #标题输入可以send_keys
        strtitle="Test02"
        self.driver.find_element(By.CSS_SELECTOR,"#title").send_keys(strtitle)
            #输入区域可以点击那个插入分页符，添加内容,测试以后发现无法定位该按钮，只能用默认的输入值
            #self.driver.find_element(By.CSS_SELECTOR,"#editor > div.editormd-toolbar > div > ul > li:nth-child(33) > a > i" )
            #self.driver.find_element(By.ID, "content").clear()
            #self.driver.find_element(By.ID,"content").send_keys("Test02modifyblog")
        #经过多次测试以后发现，只能用执行JavaScript代码才能定位到md编辑器的输入区
        text = "Test02modifyblog"
        js = " var sum=document.getElementById('content'); sum.value='" + text + "';  "
        self.driver.execute_script(js)

        #发布博客
        self.driver.find_element(By.CSS_SELECTOR, "#submit").click()
        #发布后会跳到主页，所以要添加等待
        WebDriverWait(self.driver,100).until(
            EC.visibility_of_element_located( (By.CSS_SELECTOR,"body > div.container > div.right > div:nth-child(1) > div.title")   )
        )
        #测试发布后的标题是不是Test01
        elem=self.driver.find_element(By.CSS_SELECTOR,"body > div.container > div.right > div:nth-child(1) > div.title")
        actual=elem.text
        assert actual==strtitle
        #截个图
        BlogDriver.SavePicture()

    def NOTIN_LoginStateTest(self):
        #未登录状态下会跳到首页，所以要添加等待
        WebDriverWait(self.driver,100).until(
            EC.visibility_of_element_located( (By.CSS_SELECTOR,"#username") )
        )
        # 截图记录
        BlogDriver.SavePicture()
