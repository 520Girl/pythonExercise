# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import os

# 如果想使用管道，就需要开启管道 
class DangdangPipeline:
    #在爬虫文件开始之前执行
    def open_spider(self,spider):
        self.fp = open("./dangdang/data.json",mode="w",encoding="utf-8")

    def process_item(self, item, spider):
        self.fp.write(str(item))
        return item
    #在爬虫文件结束之前执行
    def close_spider(self,spider):
        self.fp.close()

import urllib.request
#多条管道同时进行 需要在setting中配置
#'dangdang.pipelines.DangdangDownloadimg':301
class DangdangDownloadimg():
    def process_item(self, item, spider):
            page = item.get('page')
            url = item.get("src")
            #判断文件夹是否存在
            # print(os.path.exists(f'page_{page}') )
            # if os.path.exists(f'page_{page}') == False:
            #     os.mkdir(os.getcwd()+'\\page_'+str(page))
            
            filename = f'./dangdang/images/page_{page}{item.get("name")}.jpg'

            urllib.request.urlretrieve(url=url,filename=filename)
            return item