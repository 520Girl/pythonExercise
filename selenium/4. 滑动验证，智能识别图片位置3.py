import time
import requests
import cv2
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains


class LoginDouban():
    headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.130 Safari/537.36'
    }
    def __init__(self):
        # 
        chrome_options = webdriver.ChromeOptions() 
        chrome_options.add_experimental_option('useAutomationExtension', False) # 不让浏览器显示受控组件
        chrome_options.add_experimental_option('excludeSwitches', ['enable-automation']) # 不让浏览器显示受控组件
        chrome_options.binary_location = r"D:\360jisu\360Chrome\Chrome\Application\360chrome.exe"  #浏览器路径改成自己的
        chrome_options.add_argument(r'--lang=zh-CN') # 这里添加一些启动的参数
        s = Service(r'G:\python\selenium\chromedriver.exe')
        self.driver = webdriver.Chrome(options=chrome_options, service=s) # executable_path chromedriver 的路径
    
    def login(self,url):
        driver = self.driver
        driver.get(url)
        time.sleep(2) #停顿两秒等待出现
        print("title", driver.title)

        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[1]/ul[1]/li[2]').click() # 点击密码登录页面
        driver.find_element_by_xpath('//*[@id="username"]').send_keys("15203415441")
        driver.find_element_by_xpath('//*[@id="password"]').send_keys("ruan123456")
        time.sleep(1)
        driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[2]/div/div[2]/div[1]/div[4]/a').click() # 点击登录
        time.sleep(1)
        #切换iframe, 选择刷新按钮，选中滑块
        iframe = self.driver.find_element_by_xpath('//*[@id="tcaptcha_transform"]//iframe')
        self.driver.switch_to.frame(iframe)
        reload = self.driver.find_element_by_xpath('//*[@id="reload"]') 
        slideBlock = self.driver.find_element_by_id('tcaptcha_drag_thumb')
        
        while True:
            # 下载图片
            self.get_verify_img()

            # 下载的图片比例和 网站上的图片大小不同, 此时需要还原尺寸，
            # 这样会影响图片的清晰度，可以输出网站显示 和原图的尺寸来进行移动
            # 所以才用输出比例来进行移动位置
            self.resize_img('./verify_img.jpg')

            # 滑块验证 通过opencv 计算出距离
            self.verify_slider('./verif_block.jpg','./verify_img.jpg')
            # 进行滑动登录
            ActionChains(driver).click_and_hold(slideBlock).perform() # 按下滑块
            # 模拟人工滑动
            tracks = self.get_tracks(self.moveDistance)
            for track in tracks:
                ActionChains(driver).move_by_offset(track, 0).perform() #移动
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

    def get_verify_img(self):
     
        # img_src 为带有缺口的图片，block_src 为缺口图片
        verify_img_src = self.driver.find_element_by_id('slideBg').get_attribute('src') 
        verif_block_src = self.driver.find_element_by_id('slideBlock').get_attribute('src') 


        #保存图片
        response = requests.get(verify_img_src,headers=self.headers)
        response2 = requests.get(verif_block_src,headers=self.headers)
        with open('./verify_img.jpg', 'wb') as f:

            f.write(response.content)
        with open('./verif_block.jpg', 'wb') as f:
            f.write(response2.content)
        

    def resize_img(self,img):
        # 原图大小
        img_rgb = cv2.imread(img)
        h,w = img_rgb.shape[:2]
        # 网站图的大小 356 204 | 341 195 > 750px
        ratio = 341 / w
        # img = cv2.resize(img_rgb,(0,0),fx=ratio,fy=ratio,interpolation=cv2.INTER_NEAREST)
        # cv2.imwrite('./verify_img2.jpg', img)
        # return img
        self.ratio = ratio

        
    def verify_slider(self,fadebg, fullbg):
        # 第一步.对滑块进行图片处理
        tp_img = self.fix_img(fadebg)  # 裁掉透明部分，找出滑块的大小
        tp_edge = cv2.Canny(tp_img, 100, 200)
        tp_pic = cv2.cvtColor(tp_edge, cv2.COLOR_GRAY2BGR)
        # cv_show("tp_img.png", tp_pic)
        # 第二步.对背景进行图片处理
        bg_img = cv2.imread(fullbg)
        bg_edge = cv2.Canny(bg_img, 100, 200)
        bg_pic = cv2.cvtColor(bg_edge, cv2.COLOR_GRAY2BGR)
        #cv_show("bg_pic.png", bg_pic)

        # 第三步：使用4和5等级【相关系数匹配 和 归一化相关系数匹配】
        methods = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED']
        results = {}
        move = 0
        for meth in methods:
            temp_full_img = bg_pic.copy()
            # 3.模板匹配matchTemplate
            res = cv2.matchTemplate(temp_full_img, tp_pic, eval(meth))
            loc = cv2.minMaxLoc(res)[3]  # 左上角点的位置：最大值的索引位置
            results[meth] = loc  # 方便测试
            move = loc[0]  # 移动距离
            # 绘制方框【方便查看】
            th, tw = tp_pic.shape[:2]
            bottom_right = (loc[0] + tw, loc[1] + th)  # 右下角点的坐标
            cv2.rectangle(bg_img, loc, bottom_right, (0, 0, 225), 1)  # 绘制矩形
            #cv_show(f'%s {id(meth)}' % meth, bg_img)
        print(f"匹配参数：{results}: 移动距离：{move * self.ratio}")
        self.moveDistance = int(move * self.ratio) - 46
    

    # 获取滑块的大小
    def fix_img(self,filename):
        #  1.为了更高的准确率，使用二值图像
        img = cv2.imread(filename)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)  # COLOR_BGR2GRAY:BGR和灰度图的转换
        ret, thresh = cv2.threshold(gray, 127, 255, cv2.THRESH_BINARY)
        # 2.将轮廓提取出来【对于二值化图片的物体找轮廓真的挺好用的】
        contours, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_NONE)
        # 轮廓图：用绿色线(0, 255, 0)来画出最小的矩形框架
        contour_img = cv2.drawContours(img, contours, 0, (0, 255, 0), 1)
        x, y, w, h = cv2.boundingRect(contours[0])  # 以方框标出轮廓的位置
        mixintu = contour_img[y:y + h, x:x + w]  # 截取部分区域图片
        return mixintu

    def get_tracks(self,distance, rate=0.5, t=0.2, v=0):
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

if __name__ == '__main__':
    url = 'https://accounts.douban.com/passport/login?source=movie'

    douban = LoginDouban()
    douban.login(url=url)
