# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DocscraperItem(scrapy.Item):
    # define the fields for your item here like:
    domain = scrapy.Field()
    url = scrapy.Field()
    relative_path = scrapy.Field()
    checksum = scrapy.Field()
    status = scrapy.Field()
    url_date = scrapy.Field()
    filetype = scrapy.Field()
    original_filename = scrapy.Field()
    file_urls = scrapy.Field()
    files = scrapy.Field()

