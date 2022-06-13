import time
import requests
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver import ActionChains
from selenium.common.exceptions import UnexpectedAlertPresentException



chrome_options = webdriver.ChromeOptions() 
chrome_options.add_experimental_option('useAutomationExtension', False) # 不让浏览器显示受控组件
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation']) # 不让浏览器显示受控组件
chrome_options.binary_location = r"D:\360jisu\360Chrome\Chrome\Application\360chrome.exe"  #浏览器路径改成自己的
chrome_options.add_argument(r'--lang=zh-CN') # 这里添加一些启动的参数
s = Service(r'G:\python\selenium\chromedriver.exe')
driver = webdriver.Chrome(options=chrome_options, service=s) # executable_path chromedriver 的路径
driver.get('https://www.baidu.com/s?ie=utf-8&f=8&rsv_bp=1&rsv_idx=1&tn=baidu&wd=selenium%20%E6%88%AA%E5%9B%BE%E6%95%B4%E4%B8%AA%E7%BD%91%E9%A1%B5get_screenshot_as_file&fenlei=256&oq=selenium%2520%25E6%2588%25AA%25E5%259B%25BE%25E6%2595%25B4%25E4%25B8%25AA%25E7%25BD%2591%25E9%25A1%25B5&rsv_pq=a516f1fc00001f7f&rsv_t=26bffp0HHcomZdq8fZWnSz1C4xRNxyXc6Tp%2BGv1YKjwAmVK%2FgsUQPtXFH9U&rqlang=cn&rsv_dl=tb&rsv_enter=1&rsv_btype=t&inputT=835&rsv_sug3=87&rsv_sug1=79&rsv_sug7=100&rsv_n=2&rsv_sug2=0&rsv_sug4=938')


# js滚动页面
def jsroll(driver, top):
    js = "var action=document.documentElement.scrollTop=" + str(top)
    driver.execute_script(js)

#! 1. 定位滚动 这里必须滚动条元素存在
# slider = driver.find_elements_by_class_name("slide-to-unlock-handle")
# action = ActionChains(driver)
# action.click_and_hold(slider).perform() #单击并按下鼠标左键


# for index in range(200):
#     try:
#         action.move_by_offset(5, 0).perform() #移动鼠标，第一个参数为x坐标距离，第二个参数为y坐标距离；
#     except UnexpectedAlertPresentException: #重置action.
#         break
#     action.reset_actions()
#     time.sleep(0.1)      # 等待停顿时间

# 打印警告框提示
# success_text = driver.switch_to.alert.text


#! 2. 通过js 滚动
# jsroll(driver,1000)
# width = driver.execute_script("return document.documentElement.scrollWidth")
# height = driver.execute_script("return document.documentElement.scrollHeight")
# driver.set_window_size(width,height) #修改浏览器窗口大小
# print("整个网页尺寸:height={},width={}".format(height,width))
# driver.get_screenshot_as_file('webpage.png')

#! 3 使用js防抖滚动
execute_script = """
            (function () {
              var y = 0;
              var step = 100;
              window.scroll(0, 0);

              function f() {
                if (y < document.body.scrollHeight) {
                  y += step;
                  window.scroll(0, y);
                  setTimeout(f, 50);
                } else {
                  window.scroll(0, 0);
                  document.title += "scroll-done";
                }
              }

              setTimeout(f, 1000);
            })();
"""

# 滚轴问题解决
driver.execute_script(execute_script)


driver.close()