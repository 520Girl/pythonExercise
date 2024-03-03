import scrapy

from scrapy.utils.project import get_project_settings # 导入配置文件
from pymongo import MongoClient #mongodb数据库连接
from downloadImage.items import  DownloadimageItem
import requests
import os

class ImagedownloadSpider(scrapy.Spider):
    name = 'imageDownload'
    allowed_domains = ['www.baidu.com']
    start_urls = ['http://www.baidu.com/']

    def __init__(self,*args, **kwargs):
        #lamb 2. 连接数据库
        #? 2.1 配置文件读取 数据库配置信息
        setting = get_project_settings()
        self.port = setting['DB_PORT']
        self.user = setting['DB_USER']
        self.password = setting['DB_PASSWORD']
        self.host = setting['DB_HOST']
        self.setting = setting

        #? 2.2 连接数据库
        myclient = MongoClient(f"mongodb://{self.user}:{int(self.password)}@{self.host}:{int(self.port)}/navigation")
        mydb = myclient.navigation
        self.mycol = mydb['websiteLists']
        # filter_find = {"content":{'$elemMatch':{"id":"1358025","imgUrl":{"$exists":True}}}}


    def parse(self, response):
        filter_find = {"belongOne":5841945}
        self.websiteList = self.mycol.find(filter_find)
        print(self.websiteList[0]['title'])
        item = DownloadimageItem()
        item['files'] = 'files'
        item['doc'] = []
        for icon in self.websiteList:
            obj = {"icon":f'https://media.porndudecdn.com/includes/images/categories/{icon["icon"]}',"name":icon["icon"]}

            svg_response = requests.get(obj['icon']).text

            with open(f'{self.setting["IMAGES_STORE"]}{os.sep}navWebsit{os.sep}{obj["name"]}', 'w', encoding='utf-8') as f:
                f.write(svg_response)
            item['doc'].append(obj)
            item['image_urls'] = []
        yield item
