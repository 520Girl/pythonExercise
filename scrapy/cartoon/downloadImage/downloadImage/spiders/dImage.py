from asyncio.windows_events import NULL
import scrapy
from downloadImage.items import  DownloadimageItem
from scrapy.utils.project import get_project_settings # 导入配置文件
from pymongo import MongoClient #mongodb数据库连接


class DimageSpider(scrapy.Spider):
    name = 'dImage'
    allowed_domains = ['www.jianshu.com']
    start_urls = ['https://www.jianshu.com/']


    def __init__(self,*args, **kwargs):
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
        self.mycol = mydb['spiderCartoons']
        filter_find = {"content":{'$elemMatch':{"id":"1358025","imgUrl":{"$exists":True}}}}
        value = self.mycol.find(filter_find)
        print(list(value)[0]['state'])
        print(list(self.mycol.find(filter_find)))

    def parse(self, response):
        dow =[
            {
        "sourceHref":"https://p3.byteimg.com/origin/ffbc0002b033d6f76f81",
        "content":[{
            "img":"https://p3.byteimg.com/tos-cn-i-8gu37r9deh/71545a8a88e340439344cf0a22a0f518~noop.jpg",
            "name":"父陈子1"
        },{
            "img":"https://p3.byteimg.com/tos-cn-i-8gu37r9deh/c0ff5c278a1a4c9d9a100960e5ac2053~noop.jpg",
            "name":"父陈子2"
        },{
            "img":"https://p3.byteimg.com/tos-cn-i-8gu37r9deh/724837141f634adb9bdda6d7af3792c0~noop.jpg",
            "name":"父陈子3"
        }]
        },{
        "sourceHref":"https://p3.byteimg.com/tos-cn-i-8gu37r9deh/a352a24b28194c29ac3a9ed2929afc98~noop.jpg",
        "content":[{
            "img":"https://p3.byteimg.com/tos-cn-i-8gu37r9deh/35fcc182d6be479192121506c8fea038~noop.jpg",
            "name":"末世1"
        },{
            "img":"https://p3.byteimg.com/tos-cn-i-8gu37r9deh/cd95feb5a51d4348b4e57d38b3918646~noop.jpg",
            "name":"末世2"
        },{
            "img":"https://p3.byteimg.com/tos-cn-i-8gu37r9deh/1bc0ad593f2b4ce78a54a801481a3ee7~noop.jpg",
            "name":"末世3"
        }]
        }
        ]
        item = DownloadimageItem()
        item['files'] = 'files'
        item['doc'] = dow
        item['image_urls'] = [
            'https://p3.byteimg.com/tos-cn-i-8gu37r9deh/a179768b71e645b187421ae0abc3b740~noop.jpg',
            'https://p3.byteimg.com/tos-cn-i-8gu37r9deh/ede2db674fc9446f98253c161b76a530~noop.jpg',
            'https://p3.byteimg.com/tos-cn-i-8gu37r9deh/5c21474b115b456fbb266dc75223855e~noop.jpg'
            ]
        yield item
    

