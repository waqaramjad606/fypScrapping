import scrapy
from ..items import FypscrappingItem

class CoventrySpider(scrapy.Spider):
    name = 'coventry'
    allowed_domains = ['www.coventry.ac.uk']
    start_urls = ['https://www.coventry.ac.uk/study-at-coventry/course-finder-search-results/?startdate=1402&level=140/',
                  'https://www.coventry.ac.uk/study-at-coventry/course-finder-search-results/?startdate=1402&level=299/']
    page_no=1

    def parse(self, response):
        item = FypscrappingItem()
        apply_link='https://webapp.coventry.ac.uk/CUapply/'
        open_page='https://www.coventry.ac.uk/study-at-coventry/course-finder-search-results/?startdate=1402&level=140&page='+str(CoventrySpider.page_no)
        if CoventrySpider.page_no<11:
            CoventrySpider.page_no+=1
            yield response.follow(url=open_page,callback=self.parse)
        prg_name=response.xpath("//div[@class='col-sm-10']/h5[@class='mtm']/a/text()").extract()
        campus= response.xpath("//h5[@class='mtm']/a/span/text()").extract()
        prg_links = response.xpath("//h5[@class='mtm']/a[1]/@href").extract()
        # next_page = response.xpath("").extract()
        print(prg_links)
        item['program_name']=prg_name
        item['campus'] = campus
        item['apply_link']=apply_link
        yield item
        for href in prg_links:
            url_str="".join(map(str,href))
            int_url=url_str+"?visitor=international"
            yield response.follow(url=int_url,callback=self.program_details,dont_filter=True)

    def program_details(self,response):
        item = FypscrappingItem()
        course_duration=response.xpath("//div[@class='col-xs-7 col-sm-8 col-md-7 StudyOptions']/p/text()").extract()
        start_date=response.xpath("//div[@class='col-xs-7 col-sm-8 col-md-7 StartingDate']/p[1]/text()").extract()
        fees=response.xpath("//div[@class='col-xs-7 col-sm-8 col-md-7 Fees']/p[1]/text()").extract()
        item['start_date']=start_date
        item['fees']=fees
        item['course_duration']=course_duration
        yield item

