# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import scrapy
from scrapy import signals
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter
from selenium.webdriver.common.action_chains import ActionChains
import random

class FinancespiderSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class FinancespiderDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info("Spider opened: %s" % spider.name)


class SeleniumMiddleware:
    #
    # def __init__(self):
    #     print ("开始使用selenium")
    #     # 配置浏览器参数
    #     chrome_options = Options()
    #     # chrome_options.add_argument("--ignore-certificate-errors")  # 忽略 SSL 证书错误
    #     # chrome_options.add_argument('--ignore-ssl-errors')
    #     chrome_options.add_argument('--headless')  # 无头模式
    #     self.driver = webdriver.Chrome(options=chrome_options)


    def process_request(self, request, spider):

        # 检查是否需要使用Selenium，默认关闭
        if not request.meta.get('use_selenium', False):
            return None  # 继续正常处理

        # 配置浏览器参数
        chrome_options = Options()
        # chrome_options.add_argument("--ignore-certificate-errors")  # 忽略 SSL 证书错误
        # chrome_options.add_argument('--ignore-ssl-errors')
        chrome_options.add_argument('--headless')  # 无头模式
        driver = webdriver.Chrome(options=chrome_options)

        try:
             driver.get(request.url)

             # 只有财联社需要
             if "cls.cn" in request.url:
                 # max_clicks = 10  # 最大点击次数（防死循环）
                 while True:
                 ## for i in range(max_clicks):
                    try:
                        # 等待“加载更多”按钮出现
                        wait = WebDriverWait(driver, 10)
                        load_more_button = wait.until(EC.presence_of_element_located(
                            (By.XPATH, "//div[contains(@class, 'more-button') and contains(text(), '加载更多')]")))

                        # 点击“加载更多”按钮
                        # 做个有点击按钮的判断，没有不进行循环
                        if load_more_button:
                            load_more_button.click()
                        else:
                            print ("没有加载按钮")
                            break

                        # 强制等待动态内容加载（根据网络情况调整）
                        time.sleep(3)

                    except (NoSuchElementException, TimeoutException):
                        print("已经加载到最后")
                        break

            # page_source = self.driver.page_source
            # # 可选：保存到文件
            # with open('cls_page3.html', 'w', encoding='utf-8') as f:
            #     f.write(page_source)

             # 华尔街见闻鼠标滚动（不用了）
             # if "wallstreetcn.com" in request.url:
             #     # actions = ActionChains(driver)
             #     for _ in range(10):  # 滚动10次
             #     # 随机生成 200-500 之间的滚动量 更真实的模拟人类操作
             #     #     delta = random.randint(400, 700)
             #     #     actions.scroll_by_amount(0, delta).perform()
             #        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")
             #        time.sleep(2)
                 # 记录滚动开始时间
                 # start_time = time.time()
                 # # 持续滚动 3 秒
                 # while (time.time() - start_time) < 3:
                 #     # 使用 JavaScript 模拟滚动到页面底部
                 #     driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                 #
                 #     # 短暂停顿以模拟人类操作并允许内容加载
                 #     time.sleep(0.1)

                     # 可选：动态调整滚动位置（例如向上滚动一半）
                     # driver.execute_script("window.scrollBy(0, window.innerHeight / 2);")



            # 获取完整渲染后的页面源码
             body = driver.page_source
             return HtmlResponse(url=driver.current_url, body=body, encoding='utf-8')
        finally:
            driver.quit()  #把关闭浏览器放在这后SSL证书错误这种报错消失了


    # def closed(self):
    #     self.driver.quit()  # 关闭浏览器












