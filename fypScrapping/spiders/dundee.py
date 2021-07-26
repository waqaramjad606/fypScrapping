import scrapy
from ..items import FypscrappingItem

class DundeeSpider(scrapy.Spider):
    name = 'dundee'
    allowed_domains = ['dundee.ac.uk']
    other = "https://www.dundee.ac.uk/postgraduate/courses"
    start_urls = ['https://www.dundee.ac.uk/undergraduate/courses','https://www.dundee.ac.uk/postgraduate/courses']

    def parse(self, response):
        item=FypscrappingItem()
        programs = response.xpath("//nav[@class='link-list  ']/ul/li/a/text()").extract()
        program_links = response.xpath("//nav[@class='link-list  ']/ul/li/a/@href").extract()
        university_name = 'University of Dundee'
        city = 'Dundee'
        state = 'scotland'
        country = 'united kingdom'
        apply_link = 'https://evision.dundee.ac.uk/urd/sits.urd/run/siw_ipp_lgn.login?process=siw_ipp_app_crs'
        # yield {
        #     "university name":university_name,
        #     "city": city,
        #     "state": state,
        #     "country": country,
        #     "apply_link": apply_link
        # }
        # if programs=='Undergraduate':
        # yield {
        #     "programs": programs,
        #
        # }
        for link in program_links:
            url_str = ''.join(map(str, link))
            yield response.follow(url=url_str, callback=self.course_details, dont_filter=True)

    def course_details(self, response):
        item = FypscrappingItem()
        course_info = response.xpath("//div[@class='program__overview-item']/p/strong/text()").extract()
        program_name = response.xpath("//h1[@class='hero__title']/text()").extract()
        prg_fees_link = response.xpath("//li[@class='subnav__item '][3]/a/@href").extract()
        school_name = response.xpath("//p[@class='hero__group_name']/a/text()").extract()
        prg_fees = response.xpath("//p[@id='international-fees']/text()").extract()
        item['program_name'] = program_name
        item['program_type']=response.xpath("//ul[@class='hero__breadcrumb']/li[2]/a/text()").extract()
        item['language']='English'
        item['start_term']=course_info
        yield item
        # yield {
        #
        #     "Program_type": response.xpath("//ul[@class='hero__breadcrumb']/li[2]/a/text()").extract(),
        #     "school": school_name,
        #     'language':'english',
        #     "program details": course_info
        # }
        # extract fees details
        for fees_links in prg_fees_link:
            url_str2 = ''.join(map(str, fees_links))
            yield response.follow(url=url_str2, callback=self.program_fees, dont_filter=True)

    def program_fees(self, response):
        item = FypscrappingItem()
        prg_fees = response.xpath("//p[@id='international-fees']/text()").extract()
        item['fees']=prg_fees
        yield item
        # yield {
        #     "program_fess": prg_fees,
        #     "country":'uk'
        # }
