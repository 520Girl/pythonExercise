# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import  scrapy
import os
import re
from  nav.settings import IMAGES_STORE as IMGS

class ImgsPipLine(ImagesPipeline):
    # get_media_requests在请求发出前调用，
    def get_media_requests(self, item, info):
        # 下载略缩图，并创建文件夹
        yield scrapy.Request(url=item['thum'],meta={"cartoonId":item['cartoonId']}) 
        # 下载章节漫画
        for img_list in item['content']:
            for url in img_list['imgUrl']:
                yield scrapy.Request(url=url,meta={"cartoonId":item['cartoonId'],"chapterid":img_list['id']})

    
    #file_path在请求完成将要把图片存储在本地时调用
    def file_path(self, request, response=None, info=None):
        meta = request.meta
        #判断是否为图片，当为none表示img_name不存在这些字段，否就存在为图片链接
        img_name = request.url.split("/")[-1]
        if re.search(r'\.(jpeg|jpg|png|gif|svg|webp)$',img_name) == None:
            img_name = f'{img_name}.jpg'

        #如果在表示为章节漫画， 不在表示为略缩图
        current_path = os.path.dirname(os.path.dirname(__file__))
        if "chapterid" in meta: 
            # os.makedirs(os.path.join(current_path, rf"{meta['cartoonId']}\{meta['chapterid']}"), exist_ok=True)
            # return os.path.join(current_path,rf"{meta['cartoonId']}/{meta['chapterid']}/{img_name}")
            return rf"{meta['cartoonId']}\{meta['chapterid']}\{img_name}"
        else:
            # os.makedirs(os.path.join(current_path, rf"{meta['cartoonId']}"), exist_ok=True)
            # return os.path.join(current_path,rf"{meta['cartoonId']}/{img_name}")
            return rf"{meta['cartoonId']}\{img_name}"
    # 当图片下载完成之后判断是否下载成功改变item
    def item_completed(self, results, item, info):
        for tuples in results:
            if tuples[0] == False: #表示图片下载失败
                if item['thum'] == tuples[1]['url']: #表示是略缩图1
                    item['thum'] = False
                else:
                    for img_List in item['content']:
                        for index,img in enumerate(img_List['imgUrl']): # 数组循环 是index并不是值
                            if img == tuples[1]['url']:
                                img_List['imgUrl'][index] = False
            else:
                if item['thum'] == tuples[1]['url']: #表示是略缩图
                    item['thum'] = tuples[1]['path'].split("\\")[-1]
                else:
                    for img_List in item['content']:
                        for index,img in enumerate(img_List['imgUrl']): # 数组循环 是index并不是值
                            if img == tuples[1]['url']:
                                img_List['imgUrl'][index] = tuples[1]['url'].split('/')[-1]
        print(f'----{item["title"]}爬取完成------')
        item['state'] = 1
        return item

class NavPipeline:
    def process_item(self, item, spider):
        return  

# 对数据库进行操作
class MongodbPipeline:
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
        try:
            print(f"------------------{item['title']}--------------开始写入数据库")
            mydict = item
            x = spider.mycol.insert_one(dict(mydict))
        except Exception as err:
            print(err)
        return item  
