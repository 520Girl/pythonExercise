#! 该爬虫只负责更新数据
import scrapy
from scrapy.utils.project import get_project_settings # 导入配置文件
from pymongo import MongoClient #mongodb数据库连接
from nav.items import *
from datetime import datetime, timedelta
import re
import random

class BaozimhSpider(scrapy.Spider):
    name = 'baozimhItem'
    allowed_domains = ['cn.baozimh.com','cn.webmota.com']
    # input_cartoon_name = input("请输入你需要爬取的漫画：")
    input_cartoon_name = "武炼巅峰"
    start_urls = [f'https://cn.baozimh.com/search?q={input_cartoon_name}']
    
    # 修改初始url 重写start_requests
    def start_requests(self):
        if hasattr(self,'arg1'):
            self.input_cartoon_name = self.arg1
            return [scrapy.Request(url=f"https://cn.baozimh.com/search?q={self.arg1}")]
        return [scrapy.Request(url=f"https://cn.baozimh.com/search?q={self.input_cartoon_name}")]
        

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
        # 先确认 数据库是否存在这个漫画 并且还需要有章节数据
        db_title = self.mycolSC.find_one({"title":self.input_cartoon_name.strip()})
        if db_title == None:
            print(f"--------{self.input_cartoon_name.strip()} 漫画数据库不存在")
            return
        else:
            db_title_chapter_item = self.mycolSCI.find_one({"cartoonId":str(db_title['cartoonId'])})
            if db_title_chapter_item == None:
                print(f"--------{self.input_cartoon_name.strip()} 漫画没有章节数据")
                return

        search_result = response.xpath('//div[@class="pure-g classify-items"]/div')
        for index,div in enumerate(search_result):
            text = div.xpath('./a[@class="comics-card__info"]/div/text()').extract_first()
            if text == self.input_cartoon_name.strip():
                url = div.xpath('./a[@class="comics-card__info"]/@href').extract_first()
                url = f'https://cn.baozimh.com{url}'
                yield scrapy.Request(url=url,callback=self.parse_detail,meta={"cartoonId":db_title['cartoonId']})
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
        LChapters_name = latest_update.xpath('./a/text()').extract_first().strip().split(" ")[1]
        # 漫画章节url
        url = latest_update.xpath('./a/@href').extract_first() #/user/page_direct?comic_id=wuliandianfeng-pikapi&section_slot=0&chapter_slot=2366
        url_split = url.split("?")[1].split("&")
        LChapters_url = f"https://cn.webmota.com/comic/chapter/{url_split[0].split('=')[1]}/{url_split[1].split('=')[1]}_{url_split[2].split('=')[1]}.html"
        # 最新一章更新时间
        LChapters_time =  latest_update.xpath('./em/text()').extract_first().replace("(",'').replace(")",'').split(" 更新")[0].strip() #7小时前 更新
        LChapters_time = self.time_timeStemp(LChapters_time)

        #先查询数据库最新章节数据和 当前爬取的章节做对比得到需要爬取的章节之后进行爬取
        # 这个是点击查看全部章节的漫画，需要组合上面已经显示的章节
        head_four_chapter = response.xpath('//div[@class="comics-detail"]/div[@class="l-content"]/div/div[@id="chapters_other_list"]/div')
        show_four_chapter = response.xpath('//div[@class="comics-detail"]/div[@class="l-content"]/div/div[@id="chapter-items"]/div')
        head_four_chapter = show_four_chapter + head_four_chapter # 进行数组合并
        head_four_chapter.reverse() # 倒叙循环减少循环的次数

        state = False
        index = 4
        while state == False:
            find_new_chapter_value =self.find_new_chapter(response.meta['cartoonId'],head_four_chapter,index)
            head_four = find_new_chapter_value[0]
            db_vague_str = find_new_chapter_value[1]
            state = find_new_chapter_value[2]
            if len(head_four) >= 1: # 二次查询确认是否是不存在的
                chapterName = head_four[-1]['chapterName']
                if self.mycolSCI.find_one({"chapterName":{"$regex":chapterName}}) == None:
                    state = True
                else:
                    index+=1
            else:
                print(f"---{self.input_cartoon_name}已是最新章节，最新章节为{LChapters_name}-")
                state = True
                return


        
        #将数组倒叙，出入数据库
            db_cartoonId = db_vague_str['cartoonId'] #数据库最后一章的漫画id和 章节id
        db_chapterId = db_vague_str['chapterId']
        db_chapterOrder = db_vague_str['chapterOrder']
        head_four.reverse()

        for index,chapter in enumerate(head_four):
            chapter['cartoonId'] = db_cartoonId
            # chapter['chapterId'] = int(db_chapterId) + index + random.randint(1,4)
            chapter['chapterId'] = int(db_chapterId) + index + 1
            chapter['chapterOrder'] = int(db_chapterOrder) + index + 1
            chapter['imgUrl'] = []
            for url in chapter['sourceHref']:
                if url.find('cn.webmota.com') != -1:
                    if chapter['chapterName'] == LChapters_name:
                        chapter['LChapters'] = {"updateTime":LChapters_time,"name":LChapters_name,"chapterId":chapter['chapterId'],"url":LChapters_url}
                yield scrapy.Request(url=url,callback=self.parse_chapter_detail,meta={"chapterItem":chapter})

    def parse_chapter_detail(self, response):
        chapter = response.meta['chapterItem']
        chapterItems = NavCartoonItem()
        chapter_imgUrl = response.xpath('//ul[@class="comic-contain"]//amp-img/@src').extract()
        chapterItems['imgUrl'] = chapter_imgUrl
        # chapterItems['imgUrl'] = ['http://www.baidudddd.com']
        chapterItems['cartoonId'] = chapter['cartoonId']
        chapterItems['chapterId'] = str(chapter['chapterId'])
        chapterItems['chapterName'] = chapter['chapterName']
        chapterItems['sourceHref'] = chapter['sourceHref']
        if 'LChapters' in chapter:
            chapterItems['LChapters'] = chapter['LChapters']
        chapterItems['state'] = 1
        chapterItems['chapterOrder'] = chapter['chapterOrder']
        print(f"{chapterItems['chapterName']}--------- 准备下载图片，入库")
        yield chapterItems

    # 将时间转换为时间戳 #7小时前 更新
    def time_timeStemp(self, time_str):
        now = datetime.now() #当前时间
        date = time_str   # 最终时间
        time_str = time_str.strip().replace(" ", "")
        # 判断是否存在一二三等 re.match(r'前([\u4e00\u4e8c\u4e09\u56db\u4e94\u516d\u4e03\u516b\u4e5d\u5341]*?)天','前一天').group(1) 一。 \d+ 匹配数组
        try:
            if time_str in "前天"  :
                if len(time_str) == 2 :
                    date = datetime.timestamp(now + timedelta(days=-2))
                else: #昨天22:12
                    hours_minutes = time_str.split("前天")[1].split(":")
                    date = datetime.timestamp(now + timedelta(days=-2,hours=int(hours_minutes[0]),minutes=int(hours_minutes[1])))
            elif time_str in "昨天":
                if len(time_str) == 2 :
                    date = datetime.timestamp(now + timedelta(days=-1))
                else: #昨天22:12
                    hours_minutes = time_str.split("昨天")[1].split(":")
                    date = datetime.timestamp(now + timedelta(days=-1,hours=int(hours_minutes[0]),minutes=int(hours_minutes[1])))
            elif time_str in '今天': #(今天 00:33 更新)
                if len(time_str) > 2:
                    hours_minutes = time_str.split("今天")[1].split(":")
                    date = datetime.timestamp(now + timedelta(days=-1,hours=int(hours_minutes[0]),minutes=int(hours_minutes[1])))
            elif "小时前" in time_str:# 2小时前
                hours = re.match(r'([\d+]*?)小时前',time_str).group(1)
                date = datetime.timestamp(now + timedelta(hours=int(hours)))
            elif "分钟前" in time_str: #35分钟前
                minutes = re.match(r'([\d+]*?)分钟前',time_str).group(1)
                date = datetime.timestamp(now + timedelta(minutes=int(minutes)))
            return date * 1000
        except Exception as err:
            print(err)
            return date

    # 遍历获取未爬取到的章节,通过数据库排序获取到最新章节，和爬取的页面数据进行对比
    def find_new_chapter(self,cartoonId,head_four_chapter,index):
        up_new_data = list(self.mycolSCI.find({"cartoonId":str(cartoonId)}).sort("chapterOrder",-1).limit(1))[0]
        state = False
        # 截取倒数第八位对比数据库数据
        if len(up_new_data['chapterName']) >= index :
            vague_str = up_new_data['chapterName'][-index:]
        else:
            vague_str = up_new_data['chapterName'] #当截取判断的标题等于标题时结束while
            state = True
        head_four = []
        for div in head_four_chapter:
            chapterName = "".join(div.xpath('./a//span/text()').extract_first().strip().split(" ")[1:])
            if re.match(rf"(.*{vague_str})$",chapterName) == None: # 表示章节不存在
                sourceHref = div.xpath('./a/@href').extract_first()
                url_split = sourceHref.split("?")[1].split("&")
                sourceHref = f"https://cn.webmota.com/comic/chapter/{url_split[0].split('=')[1]}/{url_split[1].split('=')[1]}_{url_split[2].split('=')[1]}.html"
                dict = {"sourceHref":[sourceHref],"chapterName":chapterName}
                head_four.append(dict)
            else:
                break;
        return (head_four,up_new_data,state)





