# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class DownloadimageItem(scrapy.Item):
    # define the fields for your item here like:
    doc = scrapy.Field()
    image_urls = scrapy.Field()
    files = scrapy.Field()


