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
        if 'chapterId' in item: 
            for url in item['imgUrl']:
                yield scrapy.Request(url=url,meta={"cartoonId":item['cartoonId'],"chapterId":item['chapterId']})
        else:# 下载章节漫画
            yield scrapy.Request(url=item['thum'],meta={"cartoonId":item['cartoonId']}) 

    
    #file_path在请求完成将要把图片存储在本地时调用
    def file_path(self, request, response=None, info=None):
        meta = request.meta
        #判断是否为图片，当为none表示img_name不存在这些字段，否就存在为图片链接
        img_name = request.url.split("/")[-1]
        if re.search(r'\.(jpeg|jpg|png|gif|svg|webp)$',img_name) == None:
            img_name = f'{img_name}.jpg'

        #如果在表示为章节漫画， 不在表示为略缩图
        current_path = os.path.dirname(os.path.dirname(__file__))
        if "chapterId" in meta: 
            # os.makedirs(os.path.join(current_path, rf"{meta['cartoonId']}\{meta['chapterid']}"), exist_ok=True)
            # return os.path.join(current_path,rf"{meta['cartoonId']}/{meta['chapterid']}/{img_name}")
            return rf"{meta['cartoonId']}\{meta['chapterId']}\{img_name}"
        else:
            # os.makedirs(os.path.join(current_path, rf"{meta['cartoonId']}"), exist_ok=True)
            # return os.path.join(current_path,rf"{meta['cartoonId']}/{img_name}")
            return rf"{meta['cartoonId']}\{img_name}"
    # 当图片下载完成之后判断是否下载成功改变item
    def item_completed(self, results, item, info):
        for tuples in results:
            if tuples[0] != False: #表示图片下载失败
                if  'chapterId' not in item: #表示是略缩图
                    if item['thum'] == tuples[1]['url']:
                        item['thum'] = tuples[1]['path'].split("\\")[-1]
                else:
                    for index,img in enumerate(item['imgUrl']):
                        if img == tuples[1]['url']:
                            item['imgUrl'][index] = tuples[1]['path'].split('\\')[-1]
                            if not(re.search(r'^(http://|https://)',item['imgUrl'][index]) == None):
                                item['state'] = 0 # 修改状态
            else:
                item['state'] = 0 # 修改状态
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
            if 'chapterId' in item: #表示为章节数据
                if 'LChapters' in item: #更新最新章节
                    spider.mycolSC.update_one({"cartoonId":item['cartoonId']},{'$set':{"LChapters":item['LChapters']}})
                    item.pop('LChapters')
                    spider.mycolSCI.insert_one(dict(item))
                else:
                    spider.mycolSCI.insert_one(dict(item))
            else: # 表示为内容数据
                spider.mycolSC.insert_one(dict(item))
        except Exception as err:
            print(err)
        return item  
        pass
    
    def close_spider(self, spider):
        #关闭数据库管道时循环状态更新 内容表中的状态
        all_cartoon = list(spider.mycolSC.find())
        for cartoon in all_cartoon:
            if cartoon['state'] == 0:
                cartoon_id = cartoon['cartoonId']
                all_chapters = list(spider.mycolSCI.find({"cartoonId":cartoon_id}).sort("chapterOrder",-1))
                chapter_state = True
                for chapter in all_chapters:
                    if chapter['state'] == 0:
                        chapter_state = False
                        spider.mycolSC.update_one({"cartoonId":cartoon_id},{'$set':{"state":0}})
                        break;
                    spider.mycolSC.update_one({"cartoonId":cartoon_id},{'$set':{"crawlLength":len(all_chapters)}})
                if chapter_state:
                    spider.mycolSC.update_one({"cartoonId":cartoon_id},{'$set':{"state":1}})


