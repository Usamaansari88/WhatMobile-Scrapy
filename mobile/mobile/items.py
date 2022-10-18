# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MobileItem(scrapy.Item):
    # define the fields for your item here like:
    Model_name = scrapy.Field()
    Price = scrapy.Field()
    RAM = scrapy.Field()
    ROM = scrapy.Field()
    OS = scrapy.Field()

    
