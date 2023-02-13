# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MysqlVarsItem(scrapy.Item):
    name=scrapy.Field()
    href=scrapy.Field()
    format=scrapy.Field()
    version=scrapy.Field()
    scope=scrapy.Field()
    dynamic=scrapy.Field()
    hint=scrapy.Field()
    type=scrapy.Field()
    default=scrapy.Field()
    min=scrapy.Field()
    max=scrapy.Field()
    unit=scrapy.Field()
    validation=scrapy.Field()
    description=scrapy.Field()
