import re

import scrapy
import scrapy.responsetypes
from scrapy.crawler import CrawlerProcess
from ..items import FypscrappingItem
import re


class UOQueensland_AUS(scrapy.Spider):
    name = "queensland"

    def start_requests(self):
        urls = [
            'https://future-students.uq.edu.au/study'
            # 'https://www.qut.edu.au/study/undergraduate-study'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # create item object
        item = FypscrappingItem()
        university_name=response.xpath("//title/text()").extract()
        disc_link = response.xpath("//section[@class='grid__col section']/div/a/@href").extract()
        item['discipline'] = response.xpath("//section[@class='spacing--top-l text--center section']/h3[@class='card__title']/text()").extract()

        yield item
        for href in disc_link:
            url_str = ''.join(map(str, href))
            yield response.follow(url=url_str, callback=self.program_parse, dont_filter=True)

        # page_link = response.xpath("//ul[@class='pager__items js-pager__items']/li/a/@href").extract()
        # for pg_no in page_link:
        #     page_url_str="".join(map(str,pg_no))
        #     yield response.follow(url=page_url_str, callback=self.program_parse, dont_filter=True)
    def program_parse(self, response):
        item =FypscrappingItem()
        degree = response.xpath("//div[@class='card__header']/h3/span/text()").extract()
        program_name = response.xpath("//h3[@class='card__title']/text()").extract()
        duration=response.xpath("//div[@class='icon-text icon--primary text--primary icon--standard--calendar-3']/span/text()").extract()
        prg_links=response.xpath("//div[@class='card card--bordered']/a/@href").extract()
        # prg_name=re.sub(r"[\t\n]*","",program_name)
        item['program_name']=program_name
        # item['course_duration']=duration
        item['degree_type']=degree
        yield item
        for href in prg_links:
            url_str = ''.join(map(str, href))
            yield response.follow(url=url_str, callback=self.program_fees, dont_filter=True)

    def program_fees(self,response):
        item = FypscrappingItem()
        location=response.xpath("//div[@class='divider--bottom divider--grey spacing--top-l spacing--bottom-xs']/dl[1]/dd[1]/text()").extract()
        fees=response.xpath("//div[@class='divider--bottom divider--grey spacing--top-l spacing--bottom-xs']/dl/dd/a/text()").extract()
        duration=response.xpath("//dd[@class='margin--bottom-reset'][1]/text()").extract()
        apply_link=response.xpath("//div[2]/a[@class='button button--primary'][1]/@href").extract()
        start_date=response.xpath("//div[@class='divider--bottom divider--grey spacing--top-l spacing--bottom-xs']/dl/dd[@class='margin--bottom-reset'][2]/text()").extract()
        item['campus']=location
        item['fees']=fees
        item['course_duration']=duration
        item['start_date']=start_date
        item['language']='English'
        yield item





