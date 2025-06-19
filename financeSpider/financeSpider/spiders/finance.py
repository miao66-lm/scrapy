import scrapy
from bs4 import BeautifulSoup
from datetime import datetime
from financeSpider.items import FinancespiderItem
import time
import re

# 爬取东方财富网首页财经导读
class FinanceSpider(scrapy.Spider):
    name = "finance"
    allowed_domains = ["finance.eastmoney.com"]
    start_urls = ["https://finance.eastmoney.com/"]


    # def start_requests(self):
    #     # url声明为全局变量，以便后续都能用到
    #     global url
    #     url= "https://finance.eastmoney.com/"
    #     yield scrapy.Request(url,callback=self.parse,headers={
    #         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'})


    def parse(self, response):
        # response.encoding = 'utf-8'
        soup = BeautifulSoup(response.text, 'lxml')
        news_items = soup.find_all('div', class_='left')

        print(news_items)
        for t in news_items:
            item = FinancespiderItem()
            item['source'] = '东方财富网'
            item['source_url'] = 'https://finance.eastmoney.com/'
            item['title'] = t.a.text.strip()
            item['link'] = t.a['href']
            title =item['title']
            link = item['link']
            # print (title,link)
            time.sleep(0.5)
            yield scrapy.Request(url=item['link'], meta={"item":item},callback=self.parse2,headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'})



    def parse2(self, response):
        item = response.meta['item']
        soup = BeautifulSoup(response.text, 'lxml')
        print ("正在抓取内容")
        item["content"] = soup.find("div",id="ContentBody").text.strip()
        dt= soup.find("div",class_="item").text.strip()
        # 时间格式转换
        item["update_time"] = re.sub(r"(\d+)年(\d+)月(\d+)日",r"\1-\2-\3",dt)
        # content =item['content']
        # update_time = item['update_time']

        # print  (update_time)
        yield item

