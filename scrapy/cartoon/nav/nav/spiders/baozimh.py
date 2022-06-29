from tkinter.messagebox import NO
from urllib.request import Request
import scrapy
from scrapy.utils.project import get_project_settings # 导入配置文件
from pymongo import MongoClient #mongodb数据库连接
from nav.items import *
from datetime import datetime, timedelta
import re

class BaozimhSpider(scrapy.Spider):
    name = 'baozimh'
    allowed_domains = ['cn.baozimh.com','cn.webmota.com']
    # input_cartoon_name = input("请输入你需要爬取的漫画：")
    input_cartoon_name = "武炼巅峰"
    start_urls = [f'https://cn.baozimh.com/search?q={input_cartoon_name}']


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
        self.mycolSC = mydb['spiderCartoons'] # 内容
        self.mycolSCI = mydb['spiderCartoonsItems'] #章节



    def parse(self, response):
        search_result = response.xpath('//div[@class="pure-g classify-items"]/div')
        for index,div in enumerate(search_result):
            text = div.xpath('./a[@class="comics-card__info"]/div/text()').extract_first()
            if text == self.input_cartoon_name.strip():
                url = div.xpath('./a[@class="comics-card__info"]/@href').extract_first()
                url = f'https://cn.baozimh.com{url}'
                yield scrapy.Request(url=url,callback=self.parse_detail)
                break;

    def parse_detail(self, response):
        item = NavCartoon()
        detail_result = response.xpath('//div[@class="pure-g de-info__box"]/div[2]')
        # 是否在连载中
        sbelong = detail_result.xpath('./div[1]/div[1]/div[@class="tag-list"]/span[1]/text()').extract_first()
        if sbelong == '连载中':
            item['sbelong'] = 1
        elif sbelong == '完结':
            item['sbelong'] = 0
        else:
            item['sbelong'] = 2
        # 模糊判断是否是最新章节,首先查询数据库看是否存在模糊查询，
        # 如果不存在，需要依次查询第二章一直到模糊查询到的章节存在为止
        latest_update = detail_result.xpath('./div[1]/div[1]/div[2]/span')
        LChapters_name = latest_update.xpath('./a/text()').extract_first()
        if len(LChapters_name) >= 4 : # 截取倒数第四位对比数据库数据
            vague_str = LChapters_name[-4:]
        else:
            vague_str = LChapters_name
        # 漫画章节url
        url = latest_update.xpath('./a/@href').extract_first() #/user/page_direct?comic_id=wuliandianfeng-pikapi&section_slot=0&chapter_slot=2366
        url_split = url.split("?")[1].split("&")
        LChapters_url = f"https://cn.webmota.com/comic/chapter/{url_split[0].split('=')[1]}/{url_split[1].split('=')[1]}_{url_split[2].split('=')[1]}.html"
        # 最新一章更新时间
        LChapters_time =  latest_update.xpath('./em/text()').extract_first().replace("(",'').replace(")",'').split(" 更新")[0].strip() #7小时前 更新
        LChapters_time = self.time_timeStemp(LChapters_time)

        # 获取前五章内容，来和数据库进行对比，找出没有更新的内容
        head_four_chapter = response.xpath('//div[@class="comics-detail"]/div[3]//div[@class="pure-g"]/div')
        head_four = []
        for div in head_four_chapter[:5]:
            chapterName = div.xpath('./a//span/text()').extract_first().strip().split(" ")[1]
            sourceHref = div.xpath('./a/@href').extract_first()
            url_split = sourceHref.split("?")[1].split("&")
            sourceHref = f"https://cn.webmota.com/comic/chapter/{url_split[0].split('=')[1]}/{url_split[1].split('=')[1]}_{url_split[2].split('=')[1]}.html"
            dict = {"sourceHref":[sourceHref],"chapterName":chapterName}
            head_four.append(dict)

        #和数据库对比确认数据库数据是否已经是最新
        db_data = list(self.mycolSC.find({"chapterName":self.input_cartoon_name}).sort("chapterOrder",-1).limit(5))
        db_vague_str = self.mycolSCI.find_one({"chapterName":{"$regex":vague_str}}) # 查询出当前章节
        # db_count_documents = self.mycolSCI.count_documents({"cartoonId":db_vague_str['cartoonId']}) # 总长度
        if db_vague_str == None: # 数据不存在需要查询出
            for index,chapter_data in enumerate(head_four): # 和数据库进行对比找出最后一章
                if len(chapter_data['chapterName']) >= 4 : # 截取倒数第四位对比数据库数据
                    vague_str = chapter_data['chapterName'][-4:]
                else:
                    vague_str = chapter_data['chapterName']
                value = self.mycolSCI.find_one({"chapterName":{"$regex":vague_str}})
                if value != None:
                    db_vague_str = value
                    head_four = head_four[:index]
                    break;
        else:
            print(f"---{self.input_cartoon_name}已是最新章节，最新章节为{db_vague_str['chapterName']}-")
            return

        
        #将数组倒叙，出入数据库
        db_cartoonId = db_vague_str['cartoonId'] #数据库最后一章的漫画id和 章节id
        db_chapterId = db_vague_str['chapterId']
        db_chapterOrder = db_vague_str['chapterOrder']
        head_four.reverse()
        for index,chapter in enumerate(head_four):
            chapter['cartoonId'] = db_cartoonId
            chapter['chapterId'] = int(db_chapterId) + index + 1
            chapter['chapterOrder'] = int(db_chapterOrder) +  index + 1
            chapter['imgUrl'] = []
            for url in chapter['sourceHref']:
                if url.find('cn.webmota.com') != -1:
                    yield scrapy.Request(url=url,callback=self.parse_chapter_detail,meta={"chapterItem":chapter})

    def parse_chapter_detail(self, response):
        chapter = response.meta['chapterItem']
        chapterItems = NavCartoonItem()
        chapter_imgUrl = response.xpath('//ul[@class="comic-contain"]/amp-img/@src').extract()
        chapterItems['imgUrl'] = chapter_imgUrl
        # chapterItems['imgUrl'] = ['http://www.baidudddd.com']
        chapterItems['cartoonId'] = chapter['cartoonId']
        chapterItems['chapterId'] = str(chapter['chapterId'])
        chapterItems['chapterName'] = chapter['chapterName']
        chapterItems['sourceHref'] = chapter['sourceHref']
        chapterItems['state'] = 1
        chapterItems['chapterOrder'] = chapter['chapterOrder']
        print(f"{chapterItems['chapterName']}--------- 准备下载图片，入库")
        yield chapterItems

    # 将时间转换为时间戳 #7小时前 更新
    def time_timeStemp(self, time_str):
        now = datetime.now() #当前时间
        date = time_str   # 最终时间
        time_str = time_str.strip()
        # 判断是否存在一二三等 re.match(r'前([\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341]*?)天','前一天').group(1) 一。 \d+ 匹配数组
        try:
            if time_str in "前天"  :
                if len(time_str).len >= 2 :
                    date = datetime.timestamp(now + timedelta(days=-2))
                else: #昨天22:12
                    hours_minutes = time_str.split("前天")[1].split(":")
                    date = datetime.timestamp(now + timedelta(days=-2,hours=int(hours_minutes[0]),minutes=int(hours_minutes[1])))
            elif time_str in "昨天":
                if len(time_str).len >= 2 :
                    date = datetime.timestamp(now + timedelta(days=-1))
                else: #昨天22:12
                    hours_minutes = time_str.split("昨天")[1].split(":")
                    date = datetime.timestamp(now + timedelta(days=-1,hours=int(hours_minutes[0]),minutes=int(hours_minutes[1])))
            elif "小时前" in time_str:# 2小时前
                hours = re.match(r'([\d+]*?)小时前',time_str).group(1)
                date = datetime.timestamp(now + timedelta(hours=int(hours)))
            elif "分钟前" in time_str: #35分钟前
                minutes = re.match(r'([\d+]*?)分钟前',time_str).group(1)
                date = datetime.timestamp(now + timedelta(minutes=int(minutes)))
            return date
        except Exception as err:
            print(err)
            return date




