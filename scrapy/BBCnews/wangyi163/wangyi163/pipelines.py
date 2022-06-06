from pymongo import MongoClient


class Wangyi163Pipeline:
    def process_item(self, item, spider):
        return item


#! 创建管道对数据库进行创建管道
from scrapy.utils.project import get_project_settings
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
        mydict = item
        x = spider.mycol.insert_one(mydict)
        return item 