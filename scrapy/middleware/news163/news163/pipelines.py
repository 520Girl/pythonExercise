# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient


class News163Pipeline:
    def process_item(self, item, spider):
        # print(item)
        return item

#连接数据库 
from scrapy.utils.project import get_project_settings
class MongodbPipeline:
    # 将setting中的文件赋值给self
    def open_spider(self, spider):
        setting = get_project_settings()
        self.port = setting['DB_PORT']
        self.user = setting['DB_USER']
        self.password = setting['DB_PASSWORD']
        self.host = setting['DB_HOST']

        self.connect()
    def connect(self):
        myclient = MongoClient(f"mongodb://{self.user}:{int(self.password)}@{self.host}:{int(self.port)}/navigation")
        # myclient = MongoClient(f"mongodb://nav:123456@127.0.0.1:27017/navigation")
        mydb = myclient.navigation
        self.mycol = mydb['news']

    # 将数据写入数据库
    def process_item(self, item, spider):
        mydict = {"title":f"{item['title']}","content":f"{item['content']}"}
        x = self.mycol.insert_one(mydict)
        return item

    #关闭数据库
    # def close_spider(self,spider):
    #     # self.fp.close()
    #     pass