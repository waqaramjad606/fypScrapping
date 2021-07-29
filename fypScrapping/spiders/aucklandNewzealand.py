import scrapy
from ..items import FypscrappingItem

class AucklandnewzealandSpider(scrapy.Spider):
    name = 'aucklandNewzealand'
    allowed_domains = ['https://www.auckland.ac.nz']
    start_urls = ['https://www.auckland.ac.nz/en/study/study-options/find-a-study-option.html?programmeType=bachelors,bachelors-honours,certificate,doctorates,masters,postgraduate-diploma-and-certificates,undergraduate-diploma&_charset_=UTF-8#list/']

    def parse(self, response):
        item = FypscrappingItem()
        university_name=response.xpath("//title/text()").extract()
        apply_link='https://iam.auckland.ac.nz/profile/SAML2/Redirect/SSO?execution=e1s1'
        discipline = response.xpath("//dd[@class='faculty']/text()").extract()
        program_name=response.xpath("//p[@class='listing-item__heading']/@data-programme-name").extract()
        prg_links=response.xpath("//ul[@class='page-listing__list']/li/a/@href").extract()
        # item['university_name']=university_name
        item['discipline']=discipline
        item['program_name']=program_name
        item['apply_link']=apply_link
        yield item
        for link in prg_links:
            url_str = ''.join(map(str, link))
            yield response.follow(url=url_str, callback=self.cousre_details, dont_filter=True)
    def cousre_details(self,response):
        item = FypscrappingItem()
        fees=response.xpath("//dl[@class='fees-box__list international']/dd/text()").extract()
        prg_type=response.xpath("//div[@class='quick-facts']/dl[5]/dd/text()").extract()
        start_date=response.xpath("//div[@class='quick-facts']/dl[2]/dd[1]/text()").extract()
        duration=response.xpath("//div[@class='quick-facts']/dl[1]/dd[1]/text()").extract()
        deadline=response.xpath("//div[@class='closing-dates__container']/dl/dd/text()").extract()
        item['fees']=fees
        item['program_type']=prg_type
        item['start_date']=start_date
        item['course_duration']=duration
        item['deadline']=deadline
        yield item