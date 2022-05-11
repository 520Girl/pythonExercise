from telnetlib import RSP
import bs4
import requests
from bs4 import BeautifulSoup

url ="https://sc.chinaz.com/tupian/"

rsep = requests.get(url)
rsep.encoding = 'utf-8'

#解析数据
# 1. 把页面源代码交给beautifulSoup进行处理，生成bs对象
page = BeautifulSoup(rsep.text,'html.parser')

pageLi = page.select('.pic_wrap')[0].find_all('div',attrs={
    "class":"box"
})

for item in pageLi:
    itema = f"https:{item.find('div').a['href']}"
    # 请求图片详细页面
    itemDownload = requests.get(itema)
    itemDownload.encoding = 'utf-8'
    childPage = BeautifulSoup(itemDownload.text,'html.parser')
    childPageDown = f'http:{childPage.select(".imga")[0].a.get("href")}'
    print(childPageDown)
    
    #下载图片
    img_res = requests.get(childPageDown)
    img_name = childPageDown.split('/')[-1] #拿到src 最后一个/ 后的内容
    with open(f"G:/python/beautifulSoup/image/{img_name}","wb") as f:
        f.write(img_res.content)
    break
    