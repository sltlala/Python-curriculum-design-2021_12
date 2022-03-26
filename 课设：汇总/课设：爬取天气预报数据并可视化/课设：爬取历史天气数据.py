'''使用爬虫,从天气预报网页上爬取指定城市的空气质量指数AQI_PM2.5历史数据（任意指定年份）,
分析网页,分析数据组织方式,将爬取的数据保存到本地,存为excel文件。
'''

import pandas as pd
import time
import random

from bs4 import BeautifulSoup
import requests

from xpinyin import Pinyin

# 设置请求方式和请求头
session = requests.Session()
headers = {
'Accept':'*/*',
'Accept-Encoding':'gzip, deflate',
'Accept-Language':'zh-CN,zh;q=0.9',
'Connection':'keep-alive',
'User-Agent':'User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 \
    (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36 Edg/91.0.864.41'
}

urlpages = []
# 定义添加链接的函数
def link(citycode):
    urlpages.clear()
    for month in range(1,13):
        if month<10:
            urlpages.append(str('http://www.tianqihoubao.com/aqi/'\
                +citycode+'-%s0%s.html') %(year,month))
        else:
            urlpages.append(str('http://www.tianqihoubao.com/aqi/'\
                +citycode+'-%s%s.html') %(year,month))
    urlpages

# 定义确认输入城市的函数
def indentify(req):
    # 判断输入是否正确
    status = req.status_code
    if status==200:
        return True
    else:
        print('不存在该城市的数据')
        return False

# 输入循环
while True:
    city = str(input('请输入需要获取数据的城市:'))
    year = input("你想获取的年份(2014年以后):")

    # quit程序
    if city == 'quit' or city =='退出':
        print('已退出')
        break
    
    # 实例拼音转换对象
    p = Pinyin()
    citycode = p.get_pinyin(city,'')

    # 测试是否存在该城市的数据
    url =  'http://www.tianqihoubao.com/aqi/'+citycode+'-202111.html'
    req = session.get(url, headers=headers)

    if indentify(req):
        # 转换为城市代码,生成链接列表
        link(citycode)
        # 抓取提醒
        print('正在抓取数据。。。')
        break

# 存储数据列表
info = []

for urlpage in urlpages:

    # 获取网页并转为BeautifulSoup对象
    req = session.get(urlpage, headers=headers)
    soup = BeautifulSoup(req.text, 'html.parser')

    # 操作延迟减轻网站压力
    seconds = random.randint(3,6)
    time.sleep(seconds)

    # 在Table中寻找数据
    table = soup.find('table')
    # 将Table分成行
    results = table.find_all('tr')
    # 每个网页的数据行数
    # print('Number of results:', len(results))
    
    # 循环该月的每一天
    for result in results:

        # 排除掉网页表格的表头
        if result != results[0]:

            # 从结果中找出每一行
            data = result.find_all('td')
            
            # 匹配找到的数据同时去除多余的字符
            Date = data[0].getText().strip()
            Quality = data[1].getText().strip()
            Aqi = data[2].getText().strip()
            AQI_Ranking = data[3].getText().strip()
            Pm2_5 = data[4].getText().strip()
            Pm10 = data[5].getText().strip()
            So2 = data[6].getText().strip()
            No2 = data[7].getText().strip()
            Co = data[8].getText().strip()
            o3 = data[9].getText().strip()

            # 创建DataFrame
            info.append(pd.DataFrame({'Date':Date, 'Quality':Quality, 'Aqi':Aqi, 
            'AQI Ranking':AQI_Ranking, 'Pm2.5':Pm2_5, 'Pm10':Pm10,
            'So2':So2, 'No2':No2, 'Co':Co, 'O3':o3},index=[0]))

# 生成数据表
weather = pd.concat(info)
# 数据导出
weather.to_excel(citycode+'('+year+').xlsx',index = False)
