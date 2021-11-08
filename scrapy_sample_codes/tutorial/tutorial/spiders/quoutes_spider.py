import scrapy


# scrapy uses spiders to scrape information from a websites
# they must define the initial requests to make
class QuotesSpider(scrapy.Spider):
    # identifies the spider and must be unique within a project
    name = 'quotes'

    # should return an iterable of Request objects which the spider will begin
    # to crawl from
    def start_requests(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # the method which is called to handle the response of each request made
    # always passed a TextResponse object
    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}.')
