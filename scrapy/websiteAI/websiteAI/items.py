# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
import time



class WebsiteaiItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    belong = scrapy.Field()
    title = scrapy.Field()
    info = scrapy.Field()
    name = scrapy.Field()

class websiteItemTwo(scrapy.Item):
    belong = scrapy.Field()
    belongOne = scrapy.Field()
    title = scrapy.Field()
    icon = scrapy.Field(default='favicon.png') 
    explain = scrapy.Field(default='') 
    explainConcise = scrapy.Field(default='') 
    allNum = scrapy.Field(default=0) 
    bcColor = scrapy.Field(default='rgb(0,214,185)') 
    content = scrapy.Field(default=[]) 
    language = scrapy.Field(default='zh') 
    heartNum = scrapy.Field(default=0) 
    eyeNum = scrapy.Field(default=0) 
    onlineTime = scrapy.Field(default=int(time.time())) 