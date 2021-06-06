# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class TagcountItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # 作者
    author = scrapy.Field()
    # 内容
    content = scrapy.Field()
    # 标签
    tag = scrapy.Field()
