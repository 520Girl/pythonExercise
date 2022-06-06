# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class Wangyi163Item(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    content = scrapy.Field()
    commentNum = scrapy.Field()
    time = scrapy.Field()
    createTime = scrapy.Field()
    rbelong = scrapy.Field()
    cbelong = scrapy.Field()
    rimg = scrapy.Field()
    type = scrapy.Field()
    sbelong  = scrapy.Field()
    newsHref = scrapy.Field()
    topList = scrapy.Field()
    keyword = scrapy.Field()
    weight = scrapy.Field()
    puTime = scrapy.Field()
    heartNum = scrapy.Field()
    eyeNum = scrapy.Field()
    cauthor = scrapy.Field()
    address = scrapy.Field()
    state = scrapy.Field()
