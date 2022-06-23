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
        image_urls = []
        for list in item['doc']:
            image_urls.append(list['sourceHref'])
            yield scrapy.Request(list['sourceHref'],meta={'item':"1234"})
            for img in list['content']:
                yield scrapy.Request(img['img'],meta={'item':"123"})
        
    def file_path(self, request, response=None, info=None, *, item=None):
        img_name = request.url.split('/')[-1]
        
        return request.meta['item']+img_name