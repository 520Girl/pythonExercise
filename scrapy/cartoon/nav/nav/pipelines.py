# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy.pipelines.images import ImagesPipeline
import  scrapy
import os
from  nav.settings import IMAGES_STORE as IMGS

class ImgsPipLine(ImagesPipeline):
    # get_media_requests在请求发出前调用，
    def get_media_requests(self, item, info):
        yield scrapy.Request(url = item['img_src'],meta={'item':item})

    
    #file_path在请求完成将要把图片存储在本地时调用
    def file_path(self, request, response=None, info=None):
        item = request.meta['item']
        print('########',item)
        filePath = item['img_name']
        return filePath
 
    def item_completed(self, results, item, info):
        return item

class NavPipeline:
    def process_item(self, item, spider):
        return          
