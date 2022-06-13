import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


chrome_options = webdriver.ChromeOptions() 
chrome_options.add_experimental_option('useAutomationExtension', False) # 不让浏览器显示受控组件
chrome_options.add_experimental_option('excludeSwitches', ['enable-automation']) # 不让浏览器显示受控组件
chrome_options.binary_location = r"D:\360jisu\360Chrome\Chrome\Application\360chrome.exe"  #浏览器路径改成自己的
chrome_options.add_argument(r'--lang=zh-CN') # 这里添加一些启动的参数
s = Service(r'G:\python\selenium\chromedriver.exe')
driver = webdriver.Chrome(options=chrome_options, service=s) # executable_path chromedriver 的路径
driver.get('https://accounts.douban.com/passport/login?source=movie')
# 设置网页最长等待时间，查看元素是否出现，出现则停止计时，非出现则停止到最长时间
wait = WebDriverWait(driver,20)

driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[1]/ul[1]/li[2]').click() # 点击密码登录页面
driver.find_element_by_xpath('//*[@id="username"]').send_keys("15203415441")
driver.find_element_by_xpath('//*[@id="password"]').send_keys("ruan123456")
driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a').click() # 点击登录


#执行js
js = '''
document.getElementsByClassName("tab-start")[0].children[1].classList.add("on");
document.getElementsByClassName("tab-start")[0].children[0].setAttribute("class","account-tab-account");
'''
driver.execute_script(js)

#切换iframe, 选择刷新按钮，选中滑块
time.sleep(1)
iframe = driver.find_element_by_xpath('//*[@id="tcaptcha_transform"]//iframe')
driver.switch_to.frame(iframe)
# time.sleep(2)
#! 浏览器窗口截屏 https://blog.csdn.net/yeshang_lady/article/details/122824626
driver.save_screenshot('fff.png')

#显式等待元素出现
# presence_of_element_located： 当我们不关心元素是否可见，只关心元素是否存在在页面中。
# visibility_of_element_located： 当我们需要找到元素，并且该元素也可见。
#! 元素截图
ele = wait.until(EC.presence_of_element_located((By.ID, 'slideBg')))
ele.screenshot('fff2.png')




