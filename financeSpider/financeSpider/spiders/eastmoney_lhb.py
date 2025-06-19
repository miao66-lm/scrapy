import scrapy


class EastmoneyLhbSpider(scrapy.Spider):
    name = "eastmoney_lhb"
    allowed_domains = ["data.eastmoney.com"]
    start_urls = ["https://data.eastmoney.com/stock/tradedetail.html"]

    def parse(self, response):
        pass
