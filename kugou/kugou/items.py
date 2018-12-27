# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field
class KugouItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    singer = Field()
    song = Field()
    song_down_url = Field()
    time = Field()
