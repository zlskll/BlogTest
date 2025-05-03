import datetime
import time
from autotestblog import BlogEdit,BlogEditNewBlog
from common.Utils import BlogDriver
from autotestblog import BlogList
from autotestblog import BlogLogin
from autotestblog import BlogDetail

if __name__=='__main__':
    print(datetime.datetime.now())

    #非登录状态下测试页面
    BlogLogin.BlogLogin().LoginFailTest()
    time.sleep(3)
    BlogList.BlogList().NOTIN_LoginStateTest()
    time.sleep(3)
    BlogDetail.BlogDetail().NOTIN_LoginStateTest()
    time.sleep(3)
    BlogEdit.BlogEdit().NOTIN_LoginStateTest()
    time.sleep(3)
    BlogEditNewBlog.BlogEditNewBlog().NOTIN_LoginStateTest()
    time.sleep(10)

    #登录状态下测试页面
    BlogLogin.BlogLogin().LoginSuccessTest()
    time.sleep(3)
    BlogList.BlogList().IN_LoginStateTest()
    time.sleep(3)
    BlogDetail.BlogDetail( BlogList.BlogList().GetFblogid() ).IN_LoginStateTest()
    time.sleep(3)
    BlogEdit.BlogEdit( BlogList.BlogList().GetFblogid()   ).IN_LoginStateTestSuccess()
    time.sleep(3)
    #BlogEdit.BlogEdit()
    time.sleep(3)
    BlogEditNewBlog.BlogEditNewBlog().IN_LoginStateTestSuccess()
    time.sleep(3)
    BlogEditNewBlog.BlogEditNewBlog().IN_LoginStateTestFail()


    #关闭浏览器
    BlogDriver.driver.quit()
