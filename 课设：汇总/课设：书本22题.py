import pandas as pd
import matplotlib.pyplot as plt
import os

# 任务一,数据读取及预处理
def read_data():
    while True:
        fileName = input('请输入文件名:(22.movies.csv)')
        try:
            df = pd.read_csv(fileName,encoding ='cp936')
            # 查看前三行
            print(df.head(3))
            # 查看后两行
            print(df.tail(2))
            print("任务1执行成功！")
            break
        except:
            print('文件不存在请重新输入文件名')

# 任务二,数据选择及导出
def select_data():
    while True:
        fileName = input('请输入文件名:(22.movies.csv)')
        try:
            df = pd.read_csv(fileName,encoding ='cp936')
            df = df.dropna()
            df_new = df.loc[:,['Budget','Release Year','Revenue','Title','Starring Actors Popularity']]
            df_new.to_csv('movies_revenue_starring.csv',encoding ='cp936',index =False)
            print('任务2执行成功')
            break
        except:
            print('任务2执行失败')

# 任务三,数据分类汇总
def classify_data():
    while True:
        fileName = input('请输入文件名:(movies_revenue_starring.csv)')
        try:
            df_new = pd.read_csv(fileName, encoding ='cp936')
            df_newGood = df_new[df_new['Release Year'] >1950]
            df_newGood = df_newGood[df_newGood['Release Year'] <2010]
            df_newGood.to_csv('movies_revenue_starring_1950_2010.txt',encoding ='cp936',index =False)
            print("任务3执行成功!")
            break
        except:
            print('任务2执行失败')

# 任务四,利润计算
def calculate_profit():
    while True:
        fileName = input('请输入文件名:(movies_revenue_starring_1950_2010.txt)')
        try:
            
            df_new = pd.read_csv(fileName,encoding ='cp936')
            df_new['profit'] = (df_new['Revenue'] - df_new['Budget'])
            df_new.to_csv('movies_revenue_starring_1950_2010_profit.csv',encoding ='cp936',index =False)
            print('任务4执行成功')
            break
        except:
            print('任务4执行失败')
            
# 任务五,数据统计及绘图
def plot():
    while True:
        fileName = input('请输入文件名:(movies_revenue_starring_1950_2010_profit.csv)')
        try:
            df_mean = pd.read_csv(fileName,encoding='cp936')
            df_mean = df_mean.sort_values('Title')  # 按照Title行升序排列
            df_mean = df_mean.loc[:,['Title','Starring Actors Popularity']]
            
            # 防止中文出现乱码
            plt.rcParams['font.sans-serif'] = ['SimHei']  # 黑体
            plt.rcParams['axes.unicode_minus'] = False
            # 利用matplotlib绘图
            plt.figure(figsize=(15,8))  # 创建一个画板，15英寸乘8英寸，1英寸为72像素
            plt.plot(df_mean['Title'],df_mean['Starring Actors Popularity'],label ='Starring Actors Popularity',color ='red',linewidth =0.5)#画出折线图，标签为'Starring Actors Popularity’
            plt.xlabel('Title',fontsize=20)  # 设置x轴标签与字体大小
            xlength = len(df_mean)
            xticksloc = [i for i in range(xlength) if i%200==0]  # 每隔200个取
            xtickslabels = df_mean['Title'].values[::200]  # 构建xticks显示标签，每隔200个取一个
            plt.xticks(xticksloc,xtickslabels,rotation=45)  # 设置刻度值和刻度标签倾斜45度显示
            plt.ylabel('Starring Actors Popularity',fontsize=12)  # 设置y轴标签
            plt.legend(fontsize=16)  # 显示图例并设置字号
            plt.title('Starring Actors Popularity',fontsize=16)  # 设置图标题
            plt.savefig('movies_starpopularity_1950_2010.png',dpi=400)  # 保存图片，设置像素
            plt.show()
            # 图二
            df_mean = pd.read_csv(fileName,encoding='cp936')
            df_mean = df_mean.loc[:,['Title','profit']]
            # 利用matplotlib绘图
            plt.figure(figsize=(15,8))  # 创建一个画板，15英寸乘8英寸，1英寸为72像素
            plt.plot(df_mean['Title'],df_mean['profit'],label ='profit',color ='green',linewidth =0.5)  # 画出折线图，标签为'profit’
            plt.xlabel('Title',fontsize=20)  # 设置x轴标签与字体大小
            xlength = len(df_mean)
            xticksloc = [i for i in range(xlength) if i%200==0]  # 每隔200个取
            xtickslabels = df_mean['Title'].values[::200]  # 构建xticks显示标签，每隔200个取一个
            plt.xticks(xticksloc,xtickslabels,rotation=45)  # 设置刻度值和刻度标签倾斜45度显示
            plt.ylabel('profit',fontsize= 12)  # 设置y轴标签
            plt.legend(fontsize= 16)  # 显示图例并设置字号
            plt.title('profit',fontsize=16)  # 设置图标题
            plt.savefig('movies_profit_1950_2010.png',dpi=400)  # 保存图片，设置像素
            plt.show()
            print('任务5执行成功')
            break
        except:
            print('任务5执行失败')
            
# dataVisualization()
# 系统主界面
def menu():
     print('【任务选择】\n'
        '+-------------电影数据分析及可视化系统-----------+\n'
        '|0、退出                                      |\n'
        '|1、数据读取及预处理                            |\n'
        '|2、数据选择及导出                              |\n'
        '|3、数据分类汇总                                |\n'
        '|4、数据计算及排序                              |\n'
        '|5、数据统计及绘图                              |\n'
        '|6、无                                        |\n'
        '+----------—-—-----------------------------—---+')

# 功能选择模块
def task():
    while True:
        menu()  # 打印系统主界面
        num = input("请输入任务选项:")
        if num =='1':
            read_data()
        elif num =='2':
            select_data()
        elif num =='3':
            if os.path.exists('movies_revenue_starring.csv'):
               classify_data()
            else:
                print('未能执行当前选项，请先执行前面的选项！')
        elif num =='4':
            if os.path.exists('movies_revenue_starring_1950_2010.txt'):
               calculate_profit()
            else:
                print('未能执行当前选项，请先执行前面的选项！')
        elif num =='5':
            if os.path.exists('movies_revenue_starring_1950_2010_profit.csv'):
                plot()
            else:
                print('未能执行当前选项，请先执行前面的选项！')
        elif num =='0':
            print('程序结束!')
            break
        else:
            print('输入选项有误')
        input("回车显示菜单")

# 主函数
if __name__ =='__main__':
    task()  # 调用功能选择函数
