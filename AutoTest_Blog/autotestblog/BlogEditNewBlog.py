import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from  common.Utils import BlogDriver
from autotestblog import BlogEdit
import re  #正则表达式模块

# 匹配 http://8.137.19.140:9090/blog_detail.html?blogId=83588
def extract_blogid(url):
    pattern=r'blog_detail\.html\?blogId=(\d+)'
    match=re.search(pattern,url)
    if match:
        return match.group(1)
    return None

class BlogEditNewBlog:
    url = ""
    driver = ""
    newblog_id=""
    def __init__(self):
        self.url="http://8.137.19.140:9090/blog_edit.html"
        self.driver=BlogDriver.driver
        self.driver.get(self.url)
    #登录状态下测试
    def IN_LoginStateTestSuccess(self):
        #页面元素检查
        self.driver.find_element(By.CSS_SELECTOR,"#title")
        self.driver.find_element(By.CSS_SELECTOR,"#submit")
        self.driver.find_element(By.CSS_SELECTOR,"#editor")
        #标题输入框可以send_keys
        strtime=datetime.datetime.now()
        strtitle="Test"+strtime.strftime("%Y%m%d-%H%M%S")
        self.driver.find_element(By.CSS_SELECTOR,"#title").clear()
        self.driver.find_element(By.CSS_SELECTOR,"#title").send_keys(strtitle)
        #md编辑器输入区
        text = strtitle+":添加一个新博客"
        js = " var sum=document.getElementById('content'); sum.value='" + text + "';  "
        self.driver.execute_script(js)

        #发布博客
        self.driver.find_element(By.CSS_SELECTOR, "#submit").click()
        #发布后会跳到主页，所以要添加等待
        WebDriverWait(self.driver,100).until(
            EC.visibility_of_element_located( (By.CSS_SELECTOR,"body > div.container > div.right > div:nth-child(1) > div.title")   )
        )
        #测试发布后的标题是不是strtile
        #首先找到标题strtitle所在的整个大元素
        is_strtitle_elem= self.__findtitle(strtitle)
        #断言，如果没找到就断言失败
        assert is_strtitle_elem is not None
        #发布成功，获取detatil元素的href值
        href_to_url=is_strtitle_elem.find_element(By.CSS_SELECTOR,'[class="detail"]').get_attribute('href')
        #通过href获取blogid
        self.newblog_id=extract_blogid(href_to_url)

    def IN_LoginStateTestFail(self):
        #没有输入标题
        self.__TestNoInputTitle()
        #没有输入博客内容
            #首先填上标题"TmpTitle"
        #self.__TestNoInputContent()

        TmpTitle=f"TmpTitle+{datetime.datetime.now().strftime('%Y%m%d-%H%M%S')} "
        self.driver.find_element(By.CSS_SELECTOR, "#title").send_keys(TmpTitle)
        # 经过多次测试以后发现，只能用执行JavaScript代码才能定位到md编辑器的输入区
        js = " var sum=document.getElementById('content'); sum.value='""';  "
        self.driver.execute_script(js)
        self.driver.find_element(By.CSS_SELECTOR, "#submit").click()
        alertWin_nocontent = WebDriverWait(self.driver, 10).until(
            EC.alert_is_present()
        )
        assert alertWin_nocontent.text == ""
        alertWin_nocontent.accept()

        #没有点击发布按钮，直接回到主页，会发现博客内容没有发布
            #填入md编辑区内容

        strtime = datetime.datetime.now()
        strcontent = "Test" + strtime.strftime("%Y%m%d-%H%M%S")
        js_2 = " var sum=document.getElementById('content'); sum.value=' "+strcontent+" ';  "
        self.driver.execute_script(js_2)
        #手动跳到主页http://8.137.19.140:9090/blog_list.html
        self.driver.get("http://8.137.19.140:9090/blog_list.html")
        isfind=self.__findtitle(TmpTitle)
        assert isfind is None
        #截个图
        BlogDriver.SavePicture()

    def NOTIN_LoginStateTest(self):
        #未登录状态下点击发布博客会跳到首页，所以要添加等待
        self.driver.find_element(By.CSS_SELECTOR,"#submit").click()
        WebDriverWait(self.driver,100).until(
            EC.visibility_of_element_located( (By.CSS_SELECTOR,"#username") )
        )
        # 截图记录
        BlogDriver.SavePicture()



    #IN_LoginStateTestFail:没有输入标题
    def __TestNoInputTitle(self):
        self.driver.find_element(By.CSS_SELECTOR, "#title").clear()
        self.driver.find_element(By.CSS_SELECTOR, "#submit").click()
        alertWin_notitle = WebDriverWait(self.driver, 10).until(
            EC.alert_is_present()
        )
        assert alertWin_notitle.text == ""
        alertWin_notitle.accept()

    #在BlogList博客列表里寻找标题为strtitle的博客元素，返回标题为strtitle的WebElement类型的元素
    def __findtitle(self,strtitle):
        elemlist=self.driver.find_elements(By.CSS_SELECTOR,'[class="blog"]')
        lenlist=len(elemlist)
        for index in range(lenlist):
            elem=elemlist[index].find_element(By.CSS_SELECTOR,'[class="title"]')
            if strtitle==elem.text:
                return elemlist[index]
        return None #没找到


