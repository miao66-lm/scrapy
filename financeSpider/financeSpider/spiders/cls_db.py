import scrapy
from scrapy import Spider, Request
import time
from bs4 import BeautifulSoup
from financeSpider.items import FinanceCLSItem
import json
from datetime import datetime, timedelta
import csv
import random


#scrapy crawl cls_db

class ClsDbSpider(Spider):
    name = 'cls_db'
    allowed_domains = ["cls.cn"]
    start_urls = ["https://www.cls.cn/"]

    # 设置爬取数据的天数，以及开始日期（自己调整）
    daytime=120
    start_date = "2024-11-03"
    # 当前日期转换为datetime对象
    current_dt = datetime.strptime(start_date, "%Y-%m-%d")
    # 初始化lastTime  2025-06-05 23:59:59
    last_time = int(current_dt.timestamp()) + 86399  # 示例初始值，根据实际情况替换
    base_params = {"keyword": "",
                 "category": "",
                 "os": "web",
                 "sv": "8.4.6",
                 "app": "CailianpressWeb"}

    def start_requests(self):
        url = "https://www.cls.cn/api/csw?app=CailianpressWeb&os=web&sv=8.4.6&sign=9f8797a1f4de66c2370f7a03990d2737"
        # post_data = {"lastTime":self.last_time,
        #              "keyword":"",
        #              "category":"",
        #              "os":"web",
        #              "sv":"8.4.6",
        #              "app":"CailianpressWeb"}
        post_data = self.base_params.copy()
        post_data["lastTime"] = self.last_time
        yield Request(url, method='POST',body=json.dumps(post_data),callback=self.parse)


    def parse(self, response):
        soup = BeautifulSoup(response.text, 'lxml')
        data=json.loads(response.text)
        print (data)
        # 下载数据查看json逻辑
        # with open("d.json","w",encoding="utf-8") as f:
        #     json.dump(data, f,ensure_ascii=False)

        for d in data['list']:
            item = FinanceCLSItem()
            item['title'] = d['title']
            item['content'] = d['content']
            ctime = d['ctime']
            item['update_time'] = datetime.fromtimestamp(ctime).strftime('%Y-%m-%d %H:%M')
            # #########yield item  必须注释掉，不然就跑pipline去了
            # 管道不支持递归，所以直接存入本地文件csv
            with open(f'cls_history_db_{self.start_date}.csv', 'a+', encoding='utf-8') as f:
                writer = csv.writer(f)
                row = item["title"], item["content"], item["update_time"]
                writer.writerow(row)
            # print (item)

        #开始翻页循环逻辑
        # 截至日期，为了反爬，爬一次尽量别怕太多天，暂定爬1天
        last_record_time = ctime
        record_datetime = datetime.fromtimestamp(last_record_time)
        deadline = self.current_dt - timedelta(days=self.daytime)
        # 因为时间是从当前日期向前爬的，所以日期大于截至日期时继续请求
        if record_datetime.date() > deadline.date():
        # 更新lastTime并继续请求
            self.last_time = last_record_time
            # 防止反爬设置爬虫频率
            # 随机小数间隔（1.0~3.5秒）
            wait_time = random.uniform(1.0, 3.5)
            time.sleep(wait_time)
            return self.start_requests()  # 递归调用继续请求