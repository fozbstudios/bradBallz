# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class BradballzItem(scrapy.Item):
    url = scrapy.Field()
    fileName = scrapy.Field()
    lineDict = scrapy.Field()
