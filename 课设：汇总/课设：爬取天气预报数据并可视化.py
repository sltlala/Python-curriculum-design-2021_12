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

def spider():
    # 输入循环
    while True:
        global city,year,citycode
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
        # 操作延迟减轻网站压力
        seconds = random.randint(3,6)
        time.sleep(seconds)

        # 获取网页并转为BeautifulSoup对象
        req = session.get(urlpage, headers=headers)
        soup = BeautifulSoup(req.text, 'html.parser')

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


'''
根据获取到的数据，进行数据可视化，绘制以下类型的图l:
XX市（每个人爬取不同的城市）: 
AQI全年走势图,AQI月均走势图,AQI季度箱形图,
PM2.5全年走势图,PM2.5月均走势图,PM2.5季度箱形图
PM2.5指数日历图,全年空气质量情况（污染程度饼图）
多个城市:
多个城市AQI全年走势图,多个城市PM2.5全年走势图
'''

import datetime
import numpy as np

import pyecharts.options as opts
from pyecharts import charts

import webbrowser
import os

# AQI全年走势图
def Aqi_year():
    # 从dataframe的'Date'获取date列表,'Aqi'获取整数aqi列表
    date = [x for x in df['Date']]
    value = [int(i) for i in df['Aqi']]

    # 绘制折线图
    line = charts.Line()
    # 添加X轴数据
    line.add_xaxis(xaxis_data=date)
    line.add_yaxis(
        "AQI指数",       # 系列数据项(数据名)
        value,           # y轴数据
        # 系统配置项
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='#0066CC'),  # 设置图形透明度  填充颜色
        label_opts=opts.LabelOpts(is_show=False),   # 标签配置项
        markpoint_opts=opts.MarkPointOpts(          # 标记点配置项
            data=[
                    opts.MarkPointItem(type_="max", name="最大值", symbol_size = 30),
                    opts.MarkPointItem(type_="min", name="最小值", symbol_size = 30),
            ]
        ),
        markline_opts=opts.MarkLineOpts(            # 标记线配置项
            data=[opts.MarkLineItem(type_="average", name="平均值")])   # 添加标记线数据
    )
    line.set_global_opts(           # 标题配置项
        title_opts=opts.TitleOpts(title=year+city+'全年AQI指数走势图')
    )
    # 文件保存
    line.render(year+'年'+city+'全年AQI指数走势图.html')
    # 默认浏览器打开,可视化展示
    webbrowser.open(year+'年'+city+'全年AQI指数走势图.html')

# AQI月均走势图
def Aqi_mouth():
    # 从'Date'列中提取每项的'month'并添加到dataframe中
    dom = df[['Date', 'Aqi']]
    list1 = []
    for j in dom['Date']:
        time = j.split('-')[1]
        list1.append(time)
    df['month'] = list1
    # 将dataframe按'mouth'分类组求得每月Aqi平均值
    month_message = df.groupby(['month'])
    month_com = month_message['Aqi'].agg(['mean'])
    # 重设索引并排序
    month_com.reset_index(inplace=True)
    month_com_last = month_com.sort_index()
    # 重新构造date列表
    date = ["{}".format(str(i) + '月') for i in range(1, 13)]
    # 将取得的Aqi平均值构造成列表
    value = np.array(month_com_last['mean'])
    value = ["{}".format(int(i)) for i in value]

    # 绘制折线图
    line = charts.Line()
    # 添加X轴数据
    line.add_xaxis(xaxis_data=date)
    line.add_yaxis(
        "AQI指数",       # 系列数据项
        value,           # y轴数据
        # 系统配置项
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='#0066CC'),  # 设置图形透明度  填充颜色
        label_opts=opts.LabelOpts(is_show=False),   # 标签配置项
        markpoint_opts=opts.MarkPointOpts(          # 标记点配置项
            data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
            ]
        )
    )
    line.set_global_opts(           # 标题配置项
        title_opts=opts.TitleOpts(title=year+city+'月均AQI指数走势图')
    )
    # 文件保存
    line.render(year+'年'+city+'月均AQI走势图.html')
    # 默认浏览器打开,可视化展示
    webbrowser.open(year+'年'+city+'月均AQI走势图.html')

# AQI季度箱形图
def Aqi_season():
    # 从dataframe中提取'Date'和'Aqi'
    dom = df[['Date', 'Aqi']]
    # 将数据分为四个季度并添加到data列表中
    data = [[], [], [], []]
    dom1, dom2, dom3, dom4 = data
    for i, j in zip(dom['Date'], dom['Aqi']):
        time = i.split('-')[1]
        if time in ['01', '02', '03']:
            dom1.append(int(j))
        elif time in ['04', '05', '06']:
            dom2.append(int(j))
        elif time in ['07', '08', '09']:
            dom3.append(int(j))
        else:
            dom4.append(int(j))

    # 绘制箱线图
    c = charts.Boxplot()
    # 添加X轴数据
    c.add_xaxis(['第一季度', '第二季度', '第三季度', '第四季度'])
    # 添加Y轴数据
    c.add_yaxis('AQI指数', c.prepare_data(data))
    # 标题配置项
    c.set_global_opts(title_opts =opts.TitleOpts(title =year+'年'+city+'季度AQI箱形图'))
    # 文件保存
    c.render(year+'年'+city+'季度AQI箱形图.html')
    # 默认浏览器打开,可视化展示
    webbrowser.open(year+'年'+city+'季度AQI箱形图.html')

# PM2.5全年走势图
def Pm_year():
    # 从dataframe的'Date'获取date列表,'Pm2.5'获取整数PM2.5列表
    date = [x for x in df['Date']]
    value = [int(i) for i in df['Pm2.5']]

    # 绘制折线图
    line = charts.Line()
    # 添加X轴数据
    line.add_xaxis(xaxis_data=date)
    line.add_yaxis(
        "PM2.5",       # 系列数据项(数据名)
        value,           # y轴数据
        # 系统配置项
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='#0066CC'),  # 设置图形透明度  填充颜色
        label_opts=opts.LabelOpts(is_show=False),   # 标签配置项
        markpoint_opts=opts.MarkPointOpts(          # 标记点配置项
            data=[
                    opts.MarkPointItem(type_="max", name="最大值", symbol_size = 30),
                    opts.MarkPointItem(type_="min", name="最小值", symbol_size = 30),
            ]
        ),
        markline_opts=opts.MarkLineOpts(            # 标记线配置项
            data=[opts.MarkLineItem(type_="average", name="平均值")])   # 添加标记线数据
    )
    line.set_global_opts(           # 标题配置项
        title_opts=opts.TitleOpts(title=year+city+'全年PM2.5走势图')
    )
    # 文件保存
    line.render(year+'年'+city+'全年PM2.5走势图.html')
    # 默认浏览器打开,可视化展示
    webbrowser.open(year+'年'+city+'全年PM2.5走势图.html')

# PM2.5月均走势图
def Pm_mouth():
    # 从'Date'列中提取每项的'month'并添加到dataframe中
    dom = df[['Date', 'Pm2.5']]
    list1 = []
    for j in dom['Date']:
        time = j.split('-')[1]
        list1.append(time)
    df['month'] = list1
    # 将dataframe按'mouth'分类组求得每月PM2.5平均值
    month_message = df.groupby(['month'])
    month_com = month_message['Pm2.5'].agg(['mean'])
    # 重设索引并排序
    month_com.reset_index(inplace=True)
    month_com_last = month_com.sort_index()
    # 重新构造date列表
    date = ["{}".format(str(i) + '月') for i in range(1, 13)]
    # 将取得的PM2.5平均值构造成列表
    value = np.array(month_com_last['mean'])
    value = ["{}".format(int(i)) for i in value]

    # 绘制折线图
    line = charts.Line()
    # 添加X轴数据
    line.add_xaxis(xaxis_data=date)
    line.add_yaxis(
        "PM2.5",       # 系列数据项
        value,           # y轴数据
        # 系统配置项
        areastyle_opts=opts.AreaStyleOpts(opacity=0.5, color='#0066CC'),  # 设置图形透明度  填充颜色
        label_opts=opts.LabelOpts(is_show=False),   # 标签配置项
        markpoint_opts=opts.MarkPointOpts(          # 标记点配置项
            data=[
                    opts.MarkPointItem(type_="max", name="最大值"),
                    opts.MarkPointItem(type_="min", name="最小值"),
            ]
        )
    )
    line.set_global_opts(           # 标题配置项
        title_opts=opts.TitleOpts(title=year+city+'月均PM2.5走势图')
    )
    # 文件保存
    line.render(year+'年'+city+'月均PM2.5走势图.html')
    # 默认浏览器打开,可视化展示
    webbrowser.open(year+'年'+city+'月均PM2.5走势图.html')

# PM2.5季度箱形图
def Pm_season():
    # 从dataframe中提取'Date'和'Pm2.5'
    dom = df[['Date', 'Pm2.5']]
    # 将数据分为四个季度并添加到data列表中
    data = [[], [], [], []]
    dom1, dom2, dom3, dom4 = data
    for i, j in zip(dom['Date'], dom['Pm2.5']):
        time = i.split('-')[1]
        if time in ['01', '02', '03']:
            dom1.append(int(j))
        elif time in ['04', '05', '06']:
            dom2.append(int(j))
        elif time in ['07', '08', '09']:
            dom3.append(int(j))
        else:
            dom4.append(int(j))

    # 绘制箱线图
    c = charts.Boxplot()
    # 添加X轴数据
    c.add_xaxis(['第一季度', '第二季度', '第三季度', '第四季度'])
    # 添加Y轴数据
    c.add_yaxis('PM2.5', c.prepare_data(data))
    # 标题配置项
    c.set_global_opts(title_opts =opts.TitleOpts(title =year+'年'+city+'季度PM2.5箱形图'))
    # 文件保存
    c.render(year+'年'+city+'季度PM2.5箱形图.html')
    # 默认浏览器打开,可视化展示
    webbrowser.open(year+'年'+city+'季度PM2.5箱形图.html')

# PM2.5指数日历图
def Pm_calender():
    # 从dataframe中提取'Date'和'Pm2.5'
    dom = df[['Date', 'Pm2.5']]
    # 设置日历图开始和结束时间
    begin = datetime.date(int(year), 1, 1)
    end = datetime.date(int(year), 12, 31)
    # 将每天的'Date'和'Pm2.5'组成列表添加进data列表
    data = []
    for i in range((end - begin).days + 1):
        day = [dom['Date'][i], dom['Pm2.5'][i].tolist()]
        data.append(day)

    # 绘制日历图
    c = charts.Calendar()

    c.add("",data,
        # 系统配置项
        calendar_opts=opts.CalendarOpts(
            # 日历图时间
            range_=year,
            # 设置标签文字种类
            daylabel_opts=opts.CalendarDayLabelOpts(name_map="cn"),
            monthlabel_opts=opts.CalendarMonthLabelOpts(name_map="cn"),
        ),
    )
    c.set_global_opts(           # 标题配置项
        title_opts=opts.TitleOpts(title=year+'年'+city+'PM2.5指数日历图'),
        # 图例配置项
        visualmap_opts=opts.VisualMapOpts(
            # 范围
            max_=(max(df['Pm2.5'])//5+1)*5,min_=0,
            # 颜色主题
            orient="horizontal",is_piecewise=True,
            # 位置
            pos_top="230px",pos_left="100px",
        ),
    )
    # 文件保存
    c.render(year+'年'+city+'PM2.5指数日历图.html')
    # 默认浏览器打开,可视化展示
    webbrowser.open(year+'年'+city+'PM2.5指数日历图.html')

# 全年空气质量饼图
def Quality_grade_pie():
    # 从dataframe中提取'Date'和'Quality'
    dom = df[['Date', 'Quality']]
    # 统计'Quality'中各个空气质量等级的数量,与等级组成列表加入data列表
    data = []
    data.append(['优',dom['Quality'].value_counts()['优'].tolist()])
    data.append(['良',dom['Quality'].value_counts()['良'].tolist()])
    data.append(['轻度污染',dom['Quality'].value_counts()['轻度污染'].tolist()])
    data.append(['中度污染',dom['Quality'].value_counts()['中度污染'].tolist()])
    data.append(['重度污染',dom['Quality'].value_counts()['重度污染'].tolist()])

    # 绘制饼图
    c = charts.Pie()
    # 添加数据
    c.add("",data,center=["30%", "55%"])
    # 标题配置项
    c.set_global_opts(
        title_opts=opts.TitleOpts(title=year+city+'空气质量'),
        legend_opts=opts.LegendOpts(pos_left="20%"),)
    # 标签配置项
    c.set_series_opts(label_opts=opts.LabelOpts(formatter="{b}: {c}"))
    # 文件保存
    c.render(year+'年'+city+'空气质量饼图.html')
    # 默认浏览器打开,可视化展示
    webbrowser.open(year+'年'+city+'空气质量饼图.html')

def menu():

    while True:
        # 打印操作列表
        print("****************** 空气数据可视化 **********************")
        print("------------------ 1.AQI全年走势图 ---------------------")
        print("------------------ 2.AQI月均走势图 ---------------------")
        print("------------------ 3.AQI季度箱线图 ---------------------")
        print("------------------ 4.PM2.5全年走势图 -------------------")
        print("------------------ 5.PM2.5月均走势图 -------------------")
        print("------------------ 6.PM2.5季度箱线图 -------------------")
        print("------------------ 7.PM2.5全年日历图 -------------------")
        print("------------------ 8.空气质量全年饼图 -------------------")
        print("------------------ 9.退出 -----------------------------")
        print("****************** 空气数据可视化 ***********************")
        
        command = str(input("请输入对应数字进行操作:"))  # 采用字符串形式，避免用户输入时报错
        print("-" * 30)  # 分隔线
        if command == "1":  # 采用字符串形式，避免用户输入时报错
            Aqi_year()
        elif command == "2":
            Aqi_mouth()
        elif command == "3":
            Aqi_season()
        elif command == "4":
            Pm_year()
        elif command == "5":
            Pm_mouth()
        elif command == "6":
            Pm_season()
        elif command == "7":
            Pm_calender()
        elif command == "8":
            Quality_grade_pie()
        elif command == "9":
            print("您已成功退出!")
            exit()
        else:
            print("输入有误，请重新输入相应数字进行操作!")


while True:
    # 打印操作列表
    print("------------------ 1.爬取历史天气数据 -------------------")
    print("------------------ 2.历史空气数据可视化 -----------------")
    print("------------------ 3.退出 -------------------------------")
    command = str(input("请输入对应数字进行操作:"))  # 采用字符串形式，避免用户输入时报错
    print("-" * 30)  # 分隔线
    if command == "1":  # 采用字符串形式，避免用户输入时报错
        spider()
    elif command == "2":
        city = str(input('输入需要操作的城市:'))
        year = str(input("输入数据的年份:"))
        # 实例拼音转换对象
        p = Pinyin()
        citycode = p.get_pinyin(city,'')
        filename = citycode+'('+year+').xlsx'
        if os.path.exists(filename):    # 检查数据文件是否存在
            # 从excel读取为dataframe
            df = pd.read_excel(filename)
            # 主函数
            menu()
        else:
            print('文件不存在')
    elif command == "3":
        print("您已成功退出!")
        exit()
    else:
        print("输入有误，请重新输入相应数字进行操作!")
