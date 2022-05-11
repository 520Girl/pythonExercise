# 1. 定位到2022必看精品
# 2. 通过必看精品中定位详情页面地址
# 3. 获取到下载地址

import requests
import re
import csv

url = "https://dytt8.net/index2.htm"
domain = "https://dytt8.net"

res = requests.get(url) #verify=False 去掉安全验证
res.encoding = 'gb2312'
page_content = res.text

# 获取精品中的信息
obj1 = re.compile(r'2022新片精品.*?<ul>(?P<ul>.*?)</ul>', re.S)
obj2 = re.compile(r"].*?<a href='(?P<a>.*?)'>", re.S)
obj3 = re.compile(r'<br /><a target="_blank" href="(?P<download>.*?)"', re.S)
result1 = obj1.finditer(page_content)

child_href_list = []
for item in result1:
    ul = item.group('ul')
    
    # print(ul)
    result2 = obj2.finditer(ul)
    for item2 in result2:
        a = item2.group('a')
        # 拼接页面访问地址
        child_href = domain + a
        child_href_list.append(child_href)

# 获取详情页面的下载地址
f = open('G:/python/regexp/movie.csv',mode='w',encoding='utf-8')
csvwrite = csv.writer(f)
for item in child_href_list:
    child_res = requests.get(item)
    child_res.encoding = 'gb2312'
    download = obj3.search(child_res.text)
    csvwrite.writerow([download.group('download')])
    break
