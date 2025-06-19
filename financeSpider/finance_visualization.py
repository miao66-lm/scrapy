import pandas as pd
import re
import datetime
from datetime import timedelta
import jieba
import jieba.posseg as psg
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from PIL import Image
import numpy as np
from wordcloud import WordCloud

today = datetime.date.today()
# dropna删除缺失值
# 数据集自己准备 ***文件路径自己改一下哈  注意下路径是 //
df =pd.read_csv(f'finance_news_{today}.csv').dropna()
# drop_duplicates去除重复行
df= df.drop_duplicates()
# 字段名称列表
headers = ['url','title','source','source_url','content', 'news_source','update_time']
# 为数据添加字段名称
df.columns = headers
# 提取需要的字段 url,title,content,source,update_time
df = df[['url', 'title','content','source', 'update_time']]  # 双括号创建列名的列表
# 为数据添加字段名称
df.info()

# 对网站做个筛选    '财联社|同花顺|华尔街见闻|新浪财经|东方财富网'
# df=df[df['source'].str.contains('财联社', na=False)]
# 把none值的数据删除
df=df[df['content']!='none'].copy() # 使用copy避免SettingWithCopyWarning
# 只提取24小时内的财经新闻
now = datetime.datetime.now()
hour24 = now - timedelta(days=1)
df=df[df['update_time']>hour24.strftime('%Y-%m-%d %H:%M')]  # 格式化为年-月-日 时:分
# 去除特殊符号
pattern=re.compile('[^\u4e00-\u9fa5a-zA-Z0-9]')
df['text']=df['content'].apply(lambda x:re.sub(pattern," ",x))
df.info()
df.head()

# 分词
# 添加分词词典
jieba.load_userdict('add_word.txt')
# 临时添加（最好把词添加在add_word.txt）
# 这个数据来自财联社的电报新闻，jieba分词没有把财联社正确分词，所以把财联社添加进词典
jieba.add_word("财联社")
# 读取停用词
with open('stopwords.txt','r',encoding="utf-8") as f:
    stopwords =set(f.read().split())
# 优化 用set（）把数据转换成无序的集合 能提高数据的运行速度
# 手动添加停用词#临时添加
stopwords=stopwords.union({'财联社','风险','预期','收益率','','公司','中国','市场','企业','投资','发展','产品','行业','数据','全球','业务','交易','来源','时间','文章','公告','股份','管理','经济','产业','日讯','合作','影响','新闻','项目','预计','有限公司','国家','领域','平台','责任编辑','全国','资本','资本','编辑'})
# 词频
count={}
flag=('n', 'vn', 'nt','nz')
for idx,line in df.iterrows():
    word_psg=psg.cut(line['text'])
    for word_flag in word_psg:
        word=re.sub(pattern,'',word_flag.word)
        if word_flag.flag in flag and len(word)>1 and word not in stopwords:
            count[word]=count.get(word,0)+1
# 使用元组排序：值降序(-x[1])，键升序(x[0])
sorted_items = sorted(
        count.items(),
        key=lambda x: (-x[1], x[0])
    )
# 词频排序显示
print (sorted_items[0:500])

# 词频可视化
# 词频统计通过单词计数获取
# top15
ylist =sorted(count,key=count.get,reverse=True)[:20]
xlist =[count.get(word) for word in ylist]
# 设置全局字体为支持中文的字体，这里以微软雅黑为例
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 或者你系统中的其他中文字体
plt.rcParams['axes.unicode_minus'] = False  # 正确显示负号
plt.barh(ylist,xlist)
plt.gca().invert_yaxis()  # 反转 y轴

# 词云
# 用Counter方法统计词频，结果是个词典
# 3. 加载中国地图遮罩
# mask = np.array(Image.open(r'china_mask.png'))  # 替换为你的图片路径
# 创建WordCloud对象
# font_path 设置字体路径

wordcloud = WordCloud(
    font_path='C:\Windows\Fonts\simhei.ttf',  # 这个是词云字体路径，字体格式一般是在电脑的这个路径下面
    background_color='white',
    # mask=mask,
    width=1200,
    height=1200,
    max_words=100
    # contour_width=0.0001,
    # contour_color="brown"

).generate_from_frequencies(count)

# # 显示词云
plt.figure(figsize=(8, 8), facecolor=None)
plt.imshow(wordcloud)
plt.axis("off")
plt.tight_layout(pad=0)
plt.show()
# 下载词云图片
wordcloud.to_file(f"finance_{today}.png")

# 情感分析 用snownlp
# snownlp非标准库需要下载 可以使用国内国内镜像下载快些 pip install -i https://pypi.mirrors.ustc.edu.cn/simple/ snownlp
from snownlp import SnowNLP
df['sentiments']=df['title'].apply(lambda x:SnowNLP(x).sentiments)
# 评分越高越积极区间为【0，1】
# 情感标签 消极 积极 中性
df['sentiment_label'] = df['sentiments'].apply(lambda x: '积极' if x > 0.6 else '消极' if x < 0.4 else '中性')

# 情感分布饼图
sentiment_counts = df['sentiment_label'].value_counts()
plt.figure(figsize=(8, 6))
plt.pie(sentiment_counts, labels=sentiment_counts.index, autopct='%1.1f%%')
plt.title('财经新闻情感分布')
plt.show()