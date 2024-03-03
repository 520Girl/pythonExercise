import scrapy
import random
from scrapy.utils.project import get_project_settings # 导入配置文件
from pymongo import MongoClient #mongodb数据库连接
import time
from websiteAI.items import WebsiteaiItem,websiteItemTwo

class HaouisdccomSpider(scrapy.Spider):
    name = 'haoUisdcCom'
    allowed_domains = ['hao.uisdc.com']
    start_urls = ['http://hao.uisdc.com/']

    def __init__(self,*args, **kwargs):
        super(HaouisdccomSpider, self).__init__(*args, **kwargs)  # 这里是关键
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
        self.mysqlwebsitOne = mydb['oneLevelWebsiteLists'] # 一级标签内容
        self.mysqlwebsitTwo = mydb['websiteLists'] #二级三级标签内容

    def parse(self, response):
        zonghe_list = response.xpath('//div[@class="part-cats-loop"]/div[@class="part-cat-block part-cat-block-website"]')
        one_level_tag = []
        two_level_tag = []

        
        #一级标签
        for item in zonghe_list[1:]:
            zhonghe_class_id = int(str(time.time()).split('.')[1])
            # 第一种可能 没有更多，第二种可能有更多
            one_level = WebsiteaiItem()
            one_level = {}
            two_level = {}
            three_level = {}
            
            zhonghe_class = item.xpath('./h2[@class="c-title"]/div[@class="r"]/a/text()').extract_first()
            zhonghe_info_class = item.xpath('./h2[@class="c-title"]/@id').extract_first()
            one_level['info'] = {"class":zhonghe_info_class,"address":"uisdc.com"}
    
            if zhonghe_class == None: #没有更多
                zhonghe_class_title = item.xpath('./h2[@class="c-title"]/div[@class="l"]/strong/text()').extract_first()
                # one_level['info']['status'] = 1

            else:
                zhonghe_class_title = item.xpath('./h2[@class="c-title"]/div[@class="l"]/strong/a/text()').extract_first()
                #更多的连接
                # one_level['info']['status'] = 2
            one_level['info']['address'] = item.xpath('./h2[@class="c-title"]/div[@class="l"]/strong/a/@href').extract_first()
            one_level['title'] = str(zhonghe_class_title) + '平台'
            one_level['belong'] = zhonghe_class_id
            yield one_level
            one_level_tag.append(one_level)
        

            # 创建二级数据
            two_level = websiteItemTwo()
            two_level['title'] = str(zhonghe_class_title)
            two_level['belongOne'] = zhonghe_class_id
            two_level['belong'] = item.xpath('./h2[@class="c-title"]/@id').extract_first()
            two_level['allNum'] = 0
            two_level['heartNum'] = 0
            two_level['eyeNum'] = 0
            two_level['explain'] = two_level['title']
            two_level['explainConcise'] = two_level['title']
            two_level['icon'] = 'favicon.png'
            two_level['bcColor'] = f'rgb({random.randint(0, 255)},{random.randint(0, 255)},{random.randint(0, 255)})'
            two_level['language'] = 'zh'

            two_level['content'] = []

            #加入三级数据
            if zhonghe_class == None: #没有更多
                zhonghe_three = item.xpath('./div[normalize-space(@class)="c-content"]/div[@class="c-loop c-loop-website flex"]/div[@class="part-item-website f-item p-item"]')
                item_all_heartNum = 0
                item_all_eyeNum = 0
                for item2 in zhonghe_three:
                    three_level = {}
                    zhonghe_three_status = 'uisdc.com' in item2.xpath('./a/@href').extract_first() #表示站内块，不要
                    if zhonghe_three_status == True:
                        continue
                    three_level['explain'] = item2.xpath('./a/div[@class="item-desc"]/text()').extract_first()
                    three_level['favicon'] = item2.xpath('./a/h3/i/i/img/@src').extract_first()
                    three_level['belong'] = int(str(time.time()).split('.')[1])
                    three_level['title'] = item2.xpath('./a/h3/strong/text()').extract_first()
                    three_level['hrefUrl'] = item2.xpath('./a/@href').extract_first()
                    three_level['heartNum'] = random.randint(1, 10)
                    three_level['eyeNum'] = random.randint(three_level['heartNum'], 15)
                    three_level['YesReason'] = []
                    three_level['NoReason'] = []
                    three_level['score'] = random.randint(4, 5)
                    three_level['weight'] = 1
                    three_level['state'] = 1
                    three_level['puTime'] = random.randint(1, 12)
                    item_all_heartNum += three_level['heartNum']
                    item_all_eyeNum += three_level['eyeNum']

                    two_level['content'].append(three_level)
                two_level['allNum'] = len(two_level['content'])
                two_level['heartNum'] = int(item_all_heartNum)
                two_level['eyeNum'] = int(item_all_eyeNum)
                
                yield {**two_level}
            else:
                yield scrapy.Request(
                url=one_level['info']['address'],
                callback=self.item_source,
                meta={"three_level":three_level,"two_level":two_level,'zhonghe_class_id':zhonghe_class_id}
                ) 
                
        
    def item_source(self, response):
        three_level = response.meta['three_level']
        two_level = websiteItemTwo()

        zonghe_list = response.xpath('//div[@class="part-cats-loop"]/div[@class="part-cat-block part-cat-block-website"]')   
        
        #二级标签
        for item in zonghe_list[1:]:
            two_level['title'] = item.xpath('./h2[@class="c-title"]/div[@class="l"]/strong/text()').extract_first()
            two_level['belongOne'] = response.meta['zhonghe_class_id']
            two_level['belong'] = item.xpath('./h2[@class="c-title"]/@id').extract_first()
            two_level['allNum'] = 0
            two_level['heartNum'] = 0
            two_level['eyeNum'] = 0
            two_level['icon'] = 'favicon.png'
            two_level['bcColor'] = f'rgb({random.randint(0, 255)},{random.randint(0, 255)},{random.randint(0, 255)})'
            two_level['language'] = 'zh'
            two_level['explain'] = two_level['title']
            two_level['explainConcise'] = two_level['title']
            two_level['content'] = []

            #三级标签
            zhonghe_three = item.xpath('./div[normalize-space(@class)="c-content"]/div[@class="c-loop c-loop-website flex"]/div[@class="part-item-website f-item p-item"]')
            item_all_heartNum = 0
            item_all_eyeNum = 0
            for item2 in zhonghe_three:
                zhonghe_three_status = 'uisdc.com' in item2.xpath('./a/@href').extract_first() #表示站内块，不要
                three_level = {}
                if zhonghe_three_status == True:
                    continue
                three_level['explain'] = item2.xpath('./a/div[@class="item-desc"]/text()').extract_first()
                three_level['favicon'] = item2.xpath('./a/h3/i/i/img/@src').extract_first()
                three_level['belong'] = int(str(time.time()).split('.')[1])
                three_level['title'] = item2.xpath('./a/h3/strong/text()').extract_first()
                three_level['hrefUrl'] = item2.xpath('./a/@href').extract_first()
                three_level['heartNum'] = random.randint(1, 10)
                three_level['eyeNum'] = random.randint(three_level['heartNum'], 15)
                three_level['YesReason'] = []
                three_level['NoReason'] = []
                three_level['score'] = random.randint(4, 5)
                three_level['weight'] = 1
                three_level['state'] = 1
                three_level['puTime'] = random.randint(1, 12)
                two_level['content'].append(three_level)
            two_level['allNum'] = len(two_level['content'])
            two_level['heartNum'] = int(item_all_heartNum)
            two_level['eyeNum'] = int(item_all_eyeNum)
            yield {**two_level}