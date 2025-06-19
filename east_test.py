# from playwright.sync_api import sync_playwright
from bs4 import BeautifulSoup
# import time
# import requests
#
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
    'Referer': 'https://finance.eastmoney.com/',
    'Accept-Language': 'zh-CN,zh;q=0.9',
    'Cookie': 'your_cookie_here'  # 登录后获取
}
# #
# # proxies = {
# #     'http': 'http://10.10.1.10:3128',
# #     'https': 'http://10.10.1.10:1080',
# # }
# #
# url =f'https://finance.eastmoney.com/'
# url1 =f'https://fund.eastmoney.com/a/202505183407533451.html>'
# # response = requests.get(url, headers=headers, timeout=10)
# # response.encoding = 'utf-8'
# # soup = BeautifulSoup(response.text, 'html.parser', from_encoding='utf-8')
# #
# # news_items=soup.find_all('div',class_='left')
# # print (news_items)
# # for news_item in news_items:
# #     title = news_item.a.text.strip()
# #     link = news_item.a['href']
# #     print(title+"\t"+link)
#
# response1 = requests.get(url1, headers=headers)
# soup = BeautifulSoup(response1.text, 'html.parser')
# print (soup)
# dt= soup.find("div",class_="item")
# print (dt)



# headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/128.0.0.0 Safari/537.36'}
# response = requests.get(url, headers=headers)
# soup = BeautifulSoup(response.text, 'html.parser')
# # print (soup)
# # titles = soup.find_all('div',class_='title')
# # print(titles)
# # 查找新闻条目容器
# news_items = soup.find_all('div', class_='repeatList')
# # news_items=soup.select('div.news_item')
# print(news_items)
# # # if not news_items:
# # #     print("未找到新闻条目，请检查页面结构是否变化")
# #
# # # for t in titles:
# # #     title = t.a.text.strip()
# # #     link= t.a['href']
# # #
# # #     print (title+"\t"+link)

# def get_dynamic_news(url):
#     with sync_playwright() as p:
#         # 启动浏览器（无头模式更高效）
#         browser = p.chromium.launch(headless=True)
#         page = browser.new_page()
#
#         # 设置浏览器特征（防反爬）
#         page.set_extra_http_headers({
#             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36',
#             'Referer': 'https://finance.eastmoney.com/'
#         })
#
#         # 访问页面并等待网络空闲
#         page.goto(url, wait_until="networkidle")
#
#         # 高级等待策略：直到新闻容器出现
#         page.wait_for_selector('.news-list', timeout=10000)
#
#         # 滚动加载（应对分页加载）
#         for _ in range(3):  # 滚动3次加载更多内容
#             page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
#             time.sleep(1.5)  # 滚动间隔
#
#         # 获取完整渲染后的页面内容
#         soup = BeautifulSoup(page.content(), 'html.parser')
#         browser.close()
#         results = soup.find_all('div', class_='repeatList')
#         # 解析数据（需根据实际结构调整）
#         # news_items = soup.select('.news-list li:not(.adv)')  # 排除广告
#         # results = []
#         # for item in news_items:
#         #     title = item.select_one('.title a').get_text(strip=True)
#         #     link = item.select_one('.title a')['href']
#         #     # 处理相对链接
#         #     if link.startswith('//'):
#         #         link = f'https:{link}'
#         #     elif link.startswith('/'):
#         #         link = f'https://finance.eastmoney.com{link}'
#         #     results.append({'title': title, 'link': link})
#
#         return results
#
#
# # 使用示例
# news_data = get_dynamic_news('https://finance.eastmoney.com/a/cywjh_2.html')
# for idx, item in enumerate(news_data, 1):
#     print(f"{idx}. {item['title']}\n   {item['link']}\n")
# import pymysql
# conn = pymysql.connect(
#     host='192.168.3.15',
#     user='root',
#     password='123456',
#     db='finance',
#     charset='utf8mb4'
# )
# cursor = conn.cursor()
# sql="select 2"
# print(cursor.execute(sql))

import requests
import json
import random
import time

url ='https://fund.eastmoney.com/a/202505183407533451.html'
# #  column_dic = {"345": "ccjdd","351": "cgjjj"}
# column_dic = {"345":"ccjdd"}
# #
# for k,v in column_dic.items():
#     for page in range(1,2):
#         # 动态生态jQuery
#         random_str = '1'+''.join(str(random.randint(0, 9)) for _ in range(19))
#         callback = f"jQuery{random_str}_{str(int(time.time() * 1000))}"
#         timestamp = str(int(time.time() * 1000))
#         source_url = f"https://finance.eastmoney.com/a/{v}_{page}.html"
#
#         api_url =f'https://np-listapi.eastmoney.com/comm/web/getNewsByColumns?client=web&biz=web_news_col&column={k}&order=1&needInteractData=0&page_index={page}&page_size=20&req_trace={timestamp}&fields=code,showTime,title,mediaName,summary,image,url,uniqueUrl,Np_dst&types=1,20&callback={callback}&_={timestamp}'
#         # print (api_url)
#         # print (source_url)
# # api_url = "https://np-listapi.eastmoney.com/comm/web/getNewsByColumns?client=web&biz=web_news_col&column=351&order=1&needInteractData=0"
# # params = {
# #     "page_index": 1,
# #     "callback": "jQuery18309368195047758108_1746879661947",  # 可能需要动态生成
# #     "_": "1685432101234"         # 时间戳
# # }



# # https://finance.eastmoney.com/a/cgjjj_2.html
#         response = requests.get(api_url, headers=headers)
#         # data = json.loads(response.text)
#         # print (response.text[41:-1])
#         data = json.loads(response.text[41:-1])  # 处理JSONP响应
#         # print (data)
#         #
#         # # 解析示例（需根据实际数据结构调整）：
#         for item in data['data']['list']:
#             title = item['title']
#             link = item['uniqueUrl']
#             # update_time = item['showTime']
#             print (source_url+"\t"+link)
            # time.sleep(1)
            # response1 = requests.get(link, headers=headers)
            # # print(response.text)
            # soup = BeautifulSoup(response1.text, 'html.parser')
            # content = soup.find("div", id="ContentBody").text.strip()
            # print(link+"\t"+content)

#
# #
# #
# # def generate_params(page=1):
# #     # 生成13位时间戳
# #     timestamp = str(int(time.time() * 1000))
# #
# #     # 生成callback（两种方式任选）
# #     # 方式1：简单版本
# #     # callback = f"jQuery_{timestamp}"
# #
# #     # 方式2：真实浏览器模式
#
# #
# #     return {
# #         "page": page,
# #         "type": "cywjh",
# #         "callback": callback,
# #         "_": timestamp
# #     }
# #
# #
# # def fetch_news_api():
# #     api_url = "https://finance.eastmoney.com/news/newsajax"
# #     headers = {
# #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
# #         "Referer": "https://finance.eastmoney.com/"
# #     }
# #
# #     try:
# #         response = requests.get(
# #             api_url,
# #             params=generate_params(page=2),
# #             headers=headers
# #         )
# #
# #         # 清洗JSONP响应（示例："jQuery123_168xxx(...data...)"）
# #         json_str = response.text.split("(", 1)[1].rstrip(")")
# #         data = json.loads(json_str)
# #
# #         # 解析数据（根据实际结构调整）
# #         for item in data["result"]["data"]:
# #             print(f"标题: {item['title']}")
# #             print(f"链接: https://finance.eastmoney.com/a/{item['url']}\n")
# #
# #     except Exception as e:
# #         print(f"请求失败: {str(e)}")
# #
# #
# # if __name__ == "__main__":
# #     fetch_news_api()
import re

url='https://finance.eastmoney.com/a/202505223411665985.html'
response = requests.get(url, headers=headers)
# #             api_url,
# #             params=generate_params(page=2),
# #             headers=headers
# #         )
soup = BeautifulSoup(response.text, 'lxml')
# try:
#
#     content = soup.find("div", id="ContentBody").text.strip()
#     # finance_item["content"] = soup.select_one('div[id*="ContentBody"]').text.strip()
#     # print(content)
#
# except AttributeError:
#     print("AttributeError:获取文章文本内容解析报错")
#     content = ''

# if 'fund.eastmoney.com' in url:
# #     dt = soup.find("div", class_="time").text.strip()
# # else:

dt = soup.find("div", class_="infos").text.strip()[0:17]
source=soup.find("div", class_="infos").text.strip()[18:].replace('\n','')
print (dt)
print (source)
# else:
# dt=('none')
    # if dt:
    #     dt =dt
    # else:
# dt=re.sub(r"(\d+)年(\d+)月(\d+)日", r"\1-\2-\3", dt)
    # print(dt)
    # # 时间格式转换
    # finance_item["update_time"] = re.sub(r"(\d+)年(\d+)月(\d+)日", r"\1-\2-\3", dt)
    # # content =finance_item['content']
    # # link = finance_item['link']
    # time.sleep(0.5)


    # print(dt)
# print(content)
# print(dt)


# api_url = f'https://np-listapi.eastmoney.com/comm/web/getNewsByColumns'
# params = {
#     "client": "web",
#     "biz": "web_news_col",
#     "column": 345,
#     "order": 1,
#     "needInteractData": 0,
#     "page_index": page,
#     "page_size": 20,
#     "req_trace": timestamp,
#     "fields": "code, showTime, title, mediaName, summary, image, url, uniqueUrl, Np_dst",
#     "types": "1, 20",
#     "callback": callback,  # 可能需要动态生成
#     "_": timestamp  # 时间戳
# }


import datetime

# 获取当前日期
today = datetime.date.today()

print(today)
