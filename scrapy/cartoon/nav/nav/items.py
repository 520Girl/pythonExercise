# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class NavCartoon(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    createTime = scrapy.Field()
    time = scrapy.Field()
    author = scrapy.Field()
    desc = scrapy.Field()
    thum = scrapy.Field()
    classify = scrapy.Field()
    keywords = scrapy.Field()
    sbelong = scrapy.Field()
    state = scrapy.Field()
    # content = scrapy.Field()
    weight = scrapy.Field()
    puTime = scrapy.Field()
    commentNum = scrapy.Field()
    cheart = scrapy.Field()
    ceye = scrapy.Field()
    LChapters = scrapy.Field()
    sourceHref = scrapy.Field()
    cartoonId = scrapy.Field()
    crawlLength = scrapy.Field()


class NavCartoonItem(scrapy.Item):
    cartoonId = scrapy.Field()
    chapterId = scrapy.Field()
    chapterName = scrapy.Field()
    imgUrl = scrapy.Field()
    sourceHref = scrapy.Field()
    state = scrapy.Field()
    chapterOrder = scrapy.Field()
    LChapters = scrapy.Field()
    
    
