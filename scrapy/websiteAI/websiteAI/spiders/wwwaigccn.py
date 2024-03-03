import scrapy
from scrapy.utils.project import get_project_settings # 导入配置文件
from pymongo import MongoClient #mongodb数据库连接
from websiteAI.items import WebsiteaiItem,websiteItemTwo # 导入数据结构
import random
class WwwaigccnSpider(scrapy.Spider):
    name = 'wwwaigccn'
    allowed_domains = ['www.aigc.cn']
    start_urls = ['http://www.aigc.cn/']

    def __init__(self,*args, **kwargs):
        super(WwwaigccnSpider, self).__init__(*args, **kwargs)  # 这里是关键
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
    #通过左边的rank 中href的#term-1908内数字
    #1908 的数字项，得到全部分类的连接
    def parse(self, response):
        ai_list_rank = response.xpath('//div[@class="sidebar-menu-inner"]/ul/li')
        class_id_arr = []
        ai_url_arr = [] 
        one_level_tag = []
        two_level_tag = []
        # {
        #     "belong":'',
        #     "title":"",
        #     "info":{"class":"AI","address":"aigc.cn"}
        # }

        # 一级标签
        for item in ai_list_rank[1:]:
            href_class_id_ori = item.xpath('./a/@href').extract_first('')
            href_class_id = href_class_id_ori.split("-")[1]
            one_level = WebsiteaiItem()
            one_level = {}
            one_level['belong'] = int(href_class_id)
            one_level['title'] = item.xpath('./a/span/text()').extract_first('')
            one_level['info'] = {"class":"AI","address":"aigc.cn"}
            one_level['heartNum'] = 0
            one_level['eyeNum'] = 0

            yield one_level
            one_level_tag.append(one_level)
            class_id_arr.append(href_class_id) #13
        
        #获取页面跳转连接 #二级标签
        ai_urls = response.xpath('//div[@class="d-flex flex-fill flex-tab align-items-center"]//ul/li')  
        for item in ai_urls[1:]:
            #https://www.aigc.cn/favorites/image-generation
            ai_url = item.xpath('./a/@data-link').extract_first('')
            two_level = {}
            two_level['title'] = item.xpath('./a/text()').extract_first('')
            two_level['belong'] = int(item.xpath('./a/@id').extract_first('').split("-")[2])
            two_level['belongOne'] = int(item.xpath('./a/@id').extract_first('').split("-")[1])

            if ai_url == '':
                id = item.xpath('./a/@id').extract_first('').split("-")[2]
                taxonomy = 'favorites'
                action = 'load_home_tab'
                post_id = 0
                sidebar = 0
                # 表示需要get请求直接得到数据
                ai_url = {"status":2,"url":f'https://www.aigc.cn/wp-admin/admin-ajax.php?id={id}&taxonomy=favorites&action=load_home_tab&post_id=0&sidebar=0'}
            else:
                # 表示跳转页面的
                ai_url = {"status":1,"url":ai_url}
                ai_url_arr.append(ai_url)
            two_level['content'] = []
            two_level['ai_url'] = ai_url
            two_level_tag.append(two_level)
        
        #循环三级标签获取内容
        for item in two_level_tag:
            yield scrapy.Request(
                url=item['ai_url']['url'],
                callback=self.item_source,
                meta={"item":item,}
                )

    def item_source(self, response):
        # 表示 跳转页面的数据
        item = response.meta['item']
        item_content = item['content']
        item_all_heartNum = 0
        item_all_eyeNum = 0
        if item['ai_url']['status'] == 1:
            response_data = response.xpath('//div[@class="content-layout"]//div[normalize-space(@class)="url-body default"]')
            for div_list in response_data:
                item_obj = {}
                item_obj['explain'] = div_list.xpath('./a[1]//div[@class="url-info flex-fill"]/p/text()').extract_first('')
                item_obj['favicon'] = div_list.xpath('./a[1]//img/@data-src').extract_first('')
                item_obj['belong'] = div_list.xpath('./a[1]/@data-id').extract_first('')
                item_obj['title'] = div_list.xpath('./a[1]//img/@alt').extract_first('')
                item_obj['hrefUrl'] = div_list.xpath('./a[1]/@data-url').extract_first('')
                item_obj['heartNum'] = random.randint(1, 10)
                item_obj['eyeNum'] = random.randint(item_obj['heartNum'], 15)
                item_obj['YesReason'] = []
                item_obj['NoReason'] = []
                item_obj['score'] = random.randint(4, 5)
                item_obj['puTime'] = random.randint(1, 12)
                item_obj['weight'] = 1
                item_obj['state'] = 1
                item_all_heartNum += item_obj['heartNum']
                item_all_eyeNum += item_obj['eyeNum']
                
                item_content.append(item_obj)
        else:
            response_data =response.xpath('//div[normalize-space(@class)="url-body default"]')
            for div_list in response_data:
                item_obj = {}
                item_obj['explain'] = div_list.xpath('./a[1]//div[@class="url-info flex-fill"]/p/text()').extract_first('')
                item_obj['favicon'] = div_list.xpath('./a[1]//img/@data-src').extract_first('')
                item_obj['belong'] = div_list.xpath('./a[1]/@data-id').extract_first('')
                item_obj['title'] = div_list.xpath('./a[1]//img/@alt').extract_first('')
                item_obj['hrefUrl'] = div_list.xpath('./a[1]/@data-url').extract_first('')
                item_obj['heartNum'] = random.randint(1, 10)
                item_obj['eyeNum'] = random.randint(item_obj['heartNum'], 15)
                item_obj['YesReason'] = []
                item_obj['NoReason'] = []
                item_obj['score'] = random.randint(4, 5)
                item_obj['puTime'] = random.randint(1, 12)
                item_obj['weight'] = 1
                item_obj['state'] = 1
                item_all_heartNum += item_obj['heartNum']
                item_all_eyeNum += item_obj['eyeNum']

                item_content.append(item_obj)
        item['content'] = item_content
        item['allNum'] = len(item_content)
        item['heartNum'] = int(item_all_heartNum)
        item['explain'] = item['title']
        item['explainConcise'] = item['title']
        item['eyeNum'] = int(item_all_eyeNum)
        del item['ai_url']
        item_over = websiteItemTwo()
        yield {**item,**item_over}