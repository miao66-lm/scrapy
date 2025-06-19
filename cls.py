from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import NoSuchElementException, TimeoutException
import time

# 配置浏览器参数
chrome_options = Options()
chrome_options.add_argument("--disable-blink-features=AutomationControlled")  # 禁用自动化控制提示
chrome_options.add_argument("--headless")  # 无头模式
chrome_options.add_argument(
    "user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36")

browser = webdriver.Chrome(options=chrome_options)
browser.set_window_size(1024, 768)  # 在无头模式下最好是设置下窗口大小
# 访问目标页面
browser.get("https://www.cls.cn/depth?id=1000")
# browser.get_screenshot_as_file('preview.png')  # 输出页面截图

# 初始化浏览器
click_attempts = 0  # 点击尝试计数器
max_clicks = 10  # 最大安全点击次数（防无限循环）

while click_attempts < max_clicks:

    try:


            # 等待“加载更多”按钮出现
        wait = WebDriverWait(browser, 10)
        load_more_button = wait.until(EC.presence_of_element_located((By.XPATH, "//div[contains(@class, 'list-more-button') and contains(text(), '加载更多')]")))
        # 点击“加载更多”按钮

        if load_more_button:
            load_more_button.click()
        else:
            print ("元素不存在")
            break

        # 强制等待动态内容加载（根据网络情况调整）
        time.sleep(5)
        click_attempts += 1

    except (NoSuchElementException, TimeoutException):
        print ("已经加载到最后")
        break
        # 获取完整渲染后的页面源码

page_source = browser.page_source
print(page_source)  # 打印前1000字符验证

    # 可选：保存到文件
with open('cls_page3.html', 'w', encoding='utf-8') as f:
    f.write(page_source)


browser.quit()





