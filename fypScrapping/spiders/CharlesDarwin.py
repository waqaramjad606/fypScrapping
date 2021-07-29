import scrapy
from ..items import FypscrappingItem

class CharlesdarwinSpider(scrapy.Spider):
    name = 'charlesDarwin'
    allowed_domains = ['https://www.cdu.edu.au/']
    start_urls = ['https://www.cdu.edu.au/']

    def parse(self, response):
        item = FypscrappingItem()
        university_name = response.xpath("//title/text()").extract()
        apply_link = response.xpath("//div[@class='hero__actions']/a/@href").extract()
        disci_links = response.xpath("//ul[@class='study-area-listing__list']/li/a/@href").extract()
        item['university_name'] = university_name
        item['apply_link'] = apply_link
        yield item
        for link in disci_links:
            url_str = ''.join(map(str, link))
            yield response.follow(url=url_str, callback=self.program_details, dont_filter=True)

    def program_details(self, response):
        item = FypscrappingItem()
        discipline = response.xpath("//h1[@class='banner__title']/text()").extract()
        program_name = response.xpath("//div[@class='course-list__course-name rich-text']/a/text()").extract()
        duration = response.xpath("//div[@class='copy--s'][1]/text()").extract()
        campus_location = response.xpath("//div[@class='fable__cell course-list__locations copy--s flex-30'][1]/div[2]").extract()
        prg_links = response.xpath("//div[@class='course-list__course-name rich-text']/a/@href").extract()
        item['discipline'] = discipline
        item['program_name'] = program_name
        item['course_duration'] = duration
        item['campus']=campus_location
        yield item
        for link in prg_links:
            url_str = ''.join(map(str, link))
            # int_url=url_str+'/international'
            yield response.follow(url=url_str, callback=self.degree_details, dont_filter=True)

    def degree_details(self,response):
        item = FypscrappingItem()
        degree = response.xpath("//h1/text()").extract()
        prg_type = response.xpath("//p[@class='section-header__section-name']/text()").extract()
        fee=response.xpath("//div[@class='field field-international-fees field-type-text-long field-label-hidden']/div/p[1]/text()").extract()
        year = response.xpath("//p[@class='section-header__page-title-suffix']/text()").extract()
        item['program_type'] = prg_type
        item['degree_title'] = degree
        item['start_date'] =year
        item['fees'] = fee
        yield item
