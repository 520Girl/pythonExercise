# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
import os


class DownloadimagePipeline:
    def process_item(self, item, spider):
        return item
class BWDImagesPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        for list in item['doc']:
            print(list['name'])
            yield scrapy.Request(list['icon'],meta=list)
        
    def file_path(self, request, response=None, info=None, *, item=None):
        img_name = request.meta['name']
        print('--------------')
        print(img_name)
        return f"navWebsit{os.sep}{img_name}"
    
    def item_completed(self, results, item, info):
        for tuples in results:
            print("=======================")
            print(tuples)
        return item