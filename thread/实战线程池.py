# 1. 图和提取单个页面的数据
# 2. 线程池，多个页面同时抓取

import requests
from lxml import etree
import csv
from concurrent.futures import ThreadPoolExecutor,ProcessPoolExecutor
from tqdm import tqdm

#创建存储数据文件
f = open('G:/python/thread/data.csv', mode="a", encoding="utf-8")
csvwriter = csv.writer(f)



def download_one_page(url):
    response = requests.get(url)
    response.encoding = "utf-8"

    #获取数据
    html = etree.HTML(response.text)
    container = html.xpath('/html/body//div[@class="pMain pMain_1"]/div')
    for div in container:
        title = div.xpath('./a[2]/text()')[0]
        date = div.xpath('./p/span/text()')[0]
        author = div.xpath('./p/a/text()')[0]
        imgUrl = f"https:{div.xpath('./a[1]/img/@src')[0]}".split()[0]
        # 将数据写入文件
        csvwriter.writerow([title,date,author,imgUrl])
    print('提取完毕', url)


if __name__ == "__main__":

    # for i in range(1,7): # 效率低下
    #     url = f"https://www.woyaogexing.com/tupian/z/meinv/index_{i}.html"
    #     if i == 1:
    #         url = "https://www.woyaogexing.com/tupian/z/meinv/"

    #         download_one_page(url)

    with ThreadPoolExecutor(50) as t: # 使用线程
        for i in tqdm(range(1,11)):
            url = f"https://www.woyaogexing.com/tupian/z/meinv/index_{i}.html"
            if i == 1:
                url = "https://www.woyaogexing.com/tupian/z/meinv/"
            t.submit(download_one_page,url)
    print("全部执行完毕")