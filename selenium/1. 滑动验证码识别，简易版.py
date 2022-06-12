#1.  手动滑动验证码豆瓣 https://accounts.douban.com/passport/login?source=movie
#2. 模拟用户先加速再手动滑动滑块
#3. 模拟用户输入密码，用户名，完成登录

import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains



def get_tracks(distance, rate=0.5, t=0.2, v=0):
    """ 
        将 distance 分割为小段距离，
        ditance 为总距离，
        rate 为加速和减速的临界值
        a1 加速度
        a2 减速度
        t  单位时间
        return 小段距离集合
    """
    tracks = []
    # 加速度临界值
    mid = rate * distance
    # 当前移动的距离
    s = 0
    # 循环 出距离集合
    while s < distance:
        #初速度
        v0 = v
        if s < mid:
            a = 20
        else:
            a = -3
        # 计算当前t 时间段走过的距离
        s0 = v0 * t + 0.5 * a * t * t
        # 计算当前速度
        v = v0 + a * t
        # 四舍五入距离，因为像素没有小数
        tracks.append(round(s0))
        # 计算当前距离
        s += s0
    return tracks

#登录豆瓣
def login_douban(driver,url):

    # 请求页面
    driver.get(url)
    time.sleep(2) #停顿两秒等待出现
    print("title", driver.title)

    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[1]/ul[1]/li[2]').click() # 点击密码登录页面
    driver.find_element_by_xpath('//*[@id="username"]').send_keys("15203415441")
    driver.find_element_by_xpath('//*[@id="password"]').send_keys("ruan123456")
    driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a').click() # 点击登录

    time.sleep(2) #停顿两秒等待出现

    #todo切换iframe 此时滑动验证是在iframe上显示的
    driver.switch_to.frame(1)
    block = driver.find_element_by_xpath('//*[@id="tcaptcha_drag_button"]') #选择滑块
    reload = driver.find_element_by_xpath('//*[@id="reload"]') # 选择刷新按钮

    while True:
        ActionChains(driver).click_and_hold(block).perform() # 按下滑块
        ActionChains(driver).move_by_offset(180, 0).perform() #移动
        #获取位移
        tracks = get_tracks(30)
        #循环
        for track in tracks:
            #移动
            ActionChains(driver).move_by_offset(track, 0).perform()
        # 释放
        ActionChains(driver).release().perform()
        #判断
        if driver.title == "登录豆瓣":
            print("失败...再来一次...")
            #单击刷新按钮刷新
            reload.click()
            # 停一下
            time.sleep(2)
        else:
            break

#通过qq号登录百度网盘
def login_qq(driver,url):
    # 请求页面
    driver.get(url)
    time.sleep(2) #停顿两秒等待出现
    print("title", driver.title)

    #点击登录按钮
    login = driver.find_element_by_xpath('/html/body/div[1]/div[1]/div[4]/a')
    login.click()
    time.sleep(2)

    #点击请求登录方式qq登录
    driver.find_element_by_xpath('/html/body/div[5]/div[2]/div[2]/div/div/div/div/div/div[2]/div/div/div/div[1]/div/ul/li[1]/a').click()
    #todo此时他会打开新的已窗口,选择新窗口
    windows = driver.window_handles
    driver.switch_to.window(windows[1])
    #todo 新窗口中也是个iframe 嵌入的qq登录， 并且最大化当前正在使用的窗口
    driver.find_element_by_id('ptlogin_iframe').click()
    driver.maximize_window()
    #todo 切换至账户密码框 iframe框架标签
    driver.switch_to.frame('ptlogin_iframe')
    # 选择账号密码登陆
    driver.find_element_by_id('switcher_plogin').click()
    #qq用户
    driver.find_element_by_id('u').send_keys('815842080')
    # 
    driver.find_element_by_id('p').send_keys('rmb52045@gmail')
     # 登陆
    driver.find_element_by_id('login_button').click()




def main():
    chrome_options = webdriver.ChromeOptions() 
    chrome_options.add_experimental_option('useAutomationExtension', False) # 不让浏览器显示受控组件
    chrome_options.add_experimental_option('excludeSwitches', ['enable-automation']) # 不让浏览器显示受控组件
    chrome_options.binary_location = r"D:\360jisu\360Chrome\Chrome\Application\360chrome.exe"  #浏览器路径改成自己的
    chrome_options.add_argument(r'--lang=zh-CN') # 这里添加一些启动的参数
    s = Service(r'G:\python\selenium\chromedriver.exe')
    driver = webdriver.Chrome(options=chrome_options, service=s) # executable_path chromedriver 的路径
    
    login_douban(driver,url="https://accounts.douban.com/passport/login?source=movie") #! 执行登录验证
    login_qq(driver,url="https://www.baidu.com/") #! 通过qq的方式登录百度网盘

if __name__ == "__main__":
    # url = "https://accounts.douban.com/passport/login?source=movie"
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.192 Safari/537.36"
    }
    main()