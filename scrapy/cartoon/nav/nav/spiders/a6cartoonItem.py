#! 该爬虫只负责更新数据
from tkinter.messagebox import NO
from urllib.request import Request
import scrapy
from scrapy.utils.project import get_project_settings # 导入配置文件
from pymongo import MongoClient #mongodb数据库连接
from nav.items import *
from datetime import datetime, timedelta
import re

class A6cartoonitemSpider(scrapy.Spider):
    name = 'a6cartoonItem'
    allowed_domains = ['www.sixmh7.com']
    input_cartoon_name = "武炼巅峰"
    start_urls = [f'http://www.sixmh7.com/search.php?keyword={input_cartoon_name}']

    #! 初始化需要使用到数据库以达到增量爬虫的目的
    def __init__(self,*args, **kwargs):
        super(A6cartoonitemSpider, self).__init__(*args, **kwargs)  # 这里是关键
        #lamb 2. 连接数据库
        #? 2.1 配置文件读取 数据库配置信息
        setting = get_project_settings()
        self.port = setting['DB_PORT']
        self.user = setting['DB_USER']
        self.password = setting['DB_PASSWORD']
        self.host = setting['DB_HOST']

        #? 2.2 连接数据库
        myclient = MongoClient(f"mongodb://{self.user}:{int(self.password)}@{self.host}:{int(self.port)}/navigation")
        mydb = myclient.navigation
        self.mycolSC = mydb['spiderCartoons'] # 内容
        self.mycolSCI = mydb['spiderCartoonsItems'] #章节

    def parse(self, response):
        # 先确认 数据库是否存在这个漫画 并且还需要有章节数据
        db_title = self.mycolSC.find_one({"title":self.input_cartoon_name.strip()})
        if db_title == None:
            print(f"--------{self.input_cartoon_name.strip()} 漫画数据库不存在")
            return
        else:
            db_title_chapter_item = self.mycolS.find_one({"cartoonId":str(db_title['cartoonId'])})
            if db_title_chapter_item == None:
                print(f"--------{self.input_cartoon_name.strip()} 漫画没有章节数据")
                return
                
        search_result = response.xpath('//div[@class="position"]/span[2]/text()').extract_first().strip().replace("“",'').replace("”",'')
        if int(search_result) != 0:
            search_result_title =  response.xpath('//div[@class="cy_content"]/div[2]//li[2]//text()').extract_first()
            if search_result_title == self.input_cartoon_name:
                url = response.xpath('//div[@class="cy_content"]/div[2]//li[1]/a/@href').extract_first()
                yield scrapy.Request(url=url,callback=self.parse_chapter_detail)

    def parse_chapter_detail(self, response):
        pass