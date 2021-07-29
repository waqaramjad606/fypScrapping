# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class FypscrappingItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    program_name = scrapy.Field()
    program_type = scrapy.Field()
    fees = scrapy.Field()
    degree_title = scrapy.Field()
    degree_type = scrapy.Field()
    course_duration = scrapy.Field()
    apply_link = scrapy.Field()
    start_term = scrapy.Field()
    start_date = scrapy.Field()
    deadline = scrapy.Field()
    discipline=scrapy.Field()
    campus = scrapy.Field()
    language = scrapy.Field()
