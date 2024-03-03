# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import scrapy
import time
import random
import re
import os

class ImgsPipLine(ImagesPipeline):
    # get_media_requests在请求发出前调用，
    def get_media_requests(self, item, info):
        # 下载略缩图，并创建文件夹
        if 'belongOne' in item:
            for url in item['content']:
                yield scrapy.Request(url=url['favicon'],meta={"item":url})

    #file_path在请求完成将要把图片存储在本地时调用
    def file_path(self, request, response=None, info=None):
        meta = request.meta['item']
        #判断是否为图片，当为none表示img_name不存在这些字段，否就存在为图片链接
        img_name = request.url.split("/")[-1]
        if re.search(r'\.(jpeg|jpg|png|gif|svg|webp)$',img_name) == None:
            img_name = f'{img_name}.jpg'

        #如果在表示为章节漫画， 不在表示为略缩图 #/Users/Desktop/chapter9Exercises
        current_path = os.path.dirname(os.path.dirname(__file__))
        img_Name = str(meta['belong'])+'.'+ str(img_name.split(".",-1)[-2])+'.'+ str(img_name.split(".",-1)[-1])
        request.meta['item']['favicon'] = img_Name
        return f"{img_Name}"
    # 当图片下载完成之后判断是否下载成功改变item
    def item_completed(self, results, item, info):
    
        return item

class WebsiteaiPipeline:
    #lamb 1. 将setting中的文件赋值给self
    def open_spider(self, spider):
        # setting = get_project_settings()
        # self.port = setting['DB_PORT']
        # self.user = setting['DB_USER']
        # self.password = setting['DB_PASSWORD']
        # self.host = setting['DB_HOST']

        # self.connect()
        pass
    def connect(self):
        # myclient = MongoClient(f"mongodb://{self.user}:{int(self.password)}@{self.host}:{int(self.port)}/navigation")
        # # myclient = MongoClient(f"mongodb://nav:123456@127.0.0.1:27017/navigation")
        # mydb = myclient.navigation
        # self.mycol = mydb['news']
        pass

    #lamb 2. 将数据写入数据库
    def process_item(self, item, spider):
        
        if 'allNum' in item:
            item.setdefault('icon', 'favicon.png')
            item.setdefault('bcColor', f'rgb({random.randint(0, 255)},{random.randint(0, 255)},{random.randint(0, 255)})')
            item.setdefault('language', 'zh')
            timestamp_sec = int(time.time())

            # 获取当前毫秒数
            milliseconds = int(time.time() * 1000) % 1000

            # 生成15位时间戳
            timestamp_15 = timestamp_sec * 1000 + milliseconds
            item.setdefault('onlineTime', timestamp_15)
            mydict = item
            x = spider.mysqlwebsitTwo.insert_one(mydict)
        else:
            mydict = item
            print(item)
            x = spider.mysqlwebsitOne.insert_one(mydict)
        print(item['title'])
        return item 
