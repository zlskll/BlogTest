import datetime
import os
import sys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager


class Driver:
    #类成员
    driver=""
    #构造函数
    def __init__(self):
        options = webdriver.ChromeOptions()
        #options.page_load_strategy='eager'
        self.driver=webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
        # 设置隐式等待，不推荐使用，因为隐式等待并不是等待页面元素渲染完成后就停止的，建议用显式等待。
        #self.driver.implicitly_wait(3000000000)
    def SavePicture(self):
        #截图按日期分类，一个文件夹存放一天的截图
            #检查是否存在这样的文件夹，如果不存在就创建一个
        dirtime=datetime.datetime.now().strftime('%Y-%m-%d')
        if not os.path.exists("../images/"+dirtime):
            os.mkdir("../images/"+dirtime)
        #创建文件名字
            #使用sys提供的一个能自动识别当前调用函数名字的函数
        callername=sys._getframe().f_back.f_code.co_name
        filename=datetime.datetime.now().strftime('%Y-%m-%d-%H%M%S')+".png"
        self.driver.save_screenshot("../images/"+dirtime+"/"+callername+"-"+filename)


#保存唯一实例的Driver对象，调用该模块的时候，只需要调用BolgDriver.driver即可
BlogDriver=Driver()