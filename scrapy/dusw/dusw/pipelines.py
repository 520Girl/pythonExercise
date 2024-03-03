# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface

#导入mongdb
from pymongo import MongoClient

class DuswPipeline:
    def open_spider(self, spider):
        self.fp = open("data.json","w",encoding="utf-8")

    def process_item(self, item, spider):
        self.fp.write(str(item))
        return item # 传递给下一个即将执行的管道类

    def close_spider(self,spider):
        self.fp.close()


#导入setting中的配置        
from scrapy.utils.project import get_project_settings
#建立存储到数据库的管道
class mongoDBPipeline:
    #链接数据库
    def open_spider(self, spider):
        setting = get_project_settings()
        # DB_PORT = "27017"
        # DB_USER = "nav"
        # DB_PASSWORD = "123456"
        # DB_HOST = "127.0.0.1"
        # DB_DATABASE = "articledb"
        self.port = setting['DB_PORT']
        self.user = setting['DB_USER']
        self.password = setting['DB_PASSWORD']
        self.host = setting['DB_HOST']
        self.database = setting['DB_DATABASE']

        self.connect()
    def connect(self):
        #mongodb://nav:123456@127.0.0.1:27017/navigation

        myclient = MongoClient("mongodb://nav:123456@127.0.0.1:27017/navigation")
        # myclient.close()
        mydb = myclient.navigation
        self.mycol = mydb['books']
        
        # myclient = MongoClient(host="127.0.0.1",port=27017, username="root",password="123456"，authSource=“navigation”)
        # mydb = myclient['articledb']
        # self.mycol = mydb['books']

    def process_item(self, item, spider):
        #创建数据 存入数据
        print(item)
        mydict  = {"name":f"{item['name']}","src":f"{item['src']}"}
        # x = self.mycol.insert_one(mydict)
        # print(x)
        return item

    #关闭数据库
    def close_spider(self,spider):
        # self.fp.close()
        pass