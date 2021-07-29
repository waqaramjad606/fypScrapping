import scrapy
from ..items import FypscrappingItem

class SouthernqueenslandSpider(scrapy.Spider):
    name = 'southernQueensland'
    allowed_domains = ['https://www.usq.edu.au/']
    start_urls = ['https://www.usq.edu.au/']

    def parse(self, response):
        item = FypscrappingItem()
        university_name=response.xpath("//a[contains(@class,'c-header__logo c-header__logo--full')]/img/@alt").extract()
        apply_link=response.xpath("//div[@class='c-dual-inline-cta__button-two-wrapper']/a/@href").extract()
        disci_links=response.xpath("//div[@class='col-sm-6 col-md-4 c-link-grid__item c-link-grid__item--no-margin']/a/@href").extract()
        # item['university_name']=university_name
        # item['apply_link']=apply_link
        # yield item
        for link in disci_links:
            url_str = ''.join(map(str, link))
            yield response.follow(url=url_str, callback=self.program_details, dont_filter=True)

    def program_details(self,response):
        item = FypscrappingItem()
        discipline=response.xpath("//h1[@class='c-study-image-banner__name mb-0']/text()").extract()
        # item['discipline'] = discipline
        # yield item
        program_name=response.xpath("//div[@class='js-program-table-wrapper mb-5']/h4[@class='mb-4']/text()").extract()
        prg_type=response.xpath(".//tr/td[@class='u-background--white py-4 font-weight-bold']/text()").extract()
        degree=response.xpath("//span[@class='d-flex justify-content-between align-items-center p-3']/text()").extract()
        prg_links=response.xpath("//a[@class='c-program-table__program-link o-flourish-link o-flourish-link--transparent position-relative']/@href").extract()
        item['discipline']=discipline
        item['program_name']=program_name
        item['program_type']=prg_type
        item['degree_title'] = degree
        yield item
        for link in prg_links:
            url_str = ''.join(map(str, link))
            int_url=url_str+'/international'
            yield response.follow(url=int_url, callback=self.degree_details, dont_filter=True)
    def degree_details(self,response):
        item = FypscrappingItem()
        duration=response.xpath("//ul[@class='pl-4']/li[@class='c-program-summary__list-item']/text()").extract()
        term=response.xpath("//ul[@class='pl-4']/li[@class='c-program-summary__list-item pb-1']/text()").extract()
        item['course_duration']=duration
        item['start_term']=term
        item['fees']=response.xpath("//table[@class='o-details-table']/tbody/tr[1]/td/text()").extract()
        yield item




