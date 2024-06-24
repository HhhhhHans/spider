# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    name = scrapy.Field()
    comment_url = scrapy.Field()

class UserItem(scrapy.Item):
    name = scrapy.Field()
    comment = scrapy.Field()
    like = scrapy.Field()


