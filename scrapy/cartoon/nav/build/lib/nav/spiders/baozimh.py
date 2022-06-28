import scrapy
from scrapy.utils.project import get_project_settings # 导入配置文件
from pymongo import MongoClient #mongodb数据库连接


class BaozimhSpider(scrapy.Spider):
    name = 'baozimh'
    allowed_domains = ['cn.baozimh.com']
    start_urls = ['http://cn.baozimh.com/']


    #! 初始化需要使用到数据库以达到增量爬虫的目的
    def __init__(self,*args, **kwargs):
        super(BaozimhSpider, self).__init__(*args, **kwargs)  # 这里是关键
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

    def parse(self, response):
        pass
