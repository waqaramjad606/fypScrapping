import scrapy
from ..items import FypscrappingItem

class GreenwichSpider(scrapy.Spider):
    name = 'greenwich'
    allowed_domains = ['www.gre.ac.uk']
    start_urls = ['https://www.gre.ac.uk/undergraduate-courses/a-z/','https://www.gre.ac.uk/postgraduate-courses/a-z']

    def parse(self, response):
        # program_name=response.xpath("//div[@class='cell gre-three-columns']/ul/li/a/text()").extract()
        links=response.xpath("//div[@class='cell gre-three-columns']/ul/li/a/@href").extract()
        for href in links:
            url_str="".join(map(str,href))
            yield response.follow(url=url_str,callback=self.program_details,dont_filter=True)

    def program_details(self, response):
        item = FypscrappingItem()
        prg_name=response.xpath("//h1/text()").extract()
        course_duration=response.xpath("//div[@id='prog-mode']/ul/li[1]/text()").extract()
        start_date=response.xpath("//div[@id='prog-mode']/p/text()").extract()
        start_term=response.xpath("//div[@class='gre-fee-mode-group']/h4[@class='h5']/text()").extract()
        fees=response.xpath("//span[@class='gre-fees-intl']/text()").extract()
        item['program_name']=prg_name
        item['course_duration']=course_duration
        item['start_term']=start_term
        item['start_date']=start_date
        item['fees']=fees
        item['language']='English'
        yield item


