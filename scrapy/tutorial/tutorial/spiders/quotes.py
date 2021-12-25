import scrapy


# scrapy uses spiders to scrape information from a websites
# they must define the initial requests to make
class QuotesSpider(scrapy.Spider):
    # identifies the spider and must be unique within a project
    name = 'quotes'

    # start_requests method should return an iterable of Request objects which
    # the spider will begin to crawl from
    # scrapy will schedule these Request objects and for each of their
    # Response objects the callback method will be called given the object
    def start_requests_(self):
        urls = [
            'http://quotes.toscrape.com/page/1/',
            'http://quotes.toscrape.com/page/2/',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # start_requests method also has a default implementation which uses
    # start_urls class attribute to generate the initial iterable of Request
    # objects the class attribute could be a list of urls
    # the default callback method for the generated Request objects will be
    # parse
    start_urls = [
        'http://quotes.toscrape.com/page/1/',
        'http://quotes.toscrape.com/page/2/',
    ]

    # the method which is called to handle the response of each request made
    # always passed a TextResponse object
    def parse(self, response):
        page = response.url.split('/')[-2]
        filename = f'quotes-{page}.html'
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log(f'Saved file {filename}.')
