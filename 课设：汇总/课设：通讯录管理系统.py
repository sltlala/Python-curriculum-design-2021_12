"""
完成通讯录管理系统，具有以下功能：
（1）增加联系人。
（2）删除联系人。
（3）可按联系人姓名、单位、电话，查找对应的联系人，
如果查询结果有多个，输出所有结果。
（4）提供联系人信息的保存、读取功能
"""

# 定义全局变量
import os

info_list = []  # 用来存放所有职工数据，每个职工的数据都是一个列表
filename = "info.txt"

def load_info():  # 每次打开程序都有对文件夹里的信息进行读取，所以要有登陆界面
    global info_list
    f = open(filename, "r", encoding="utf-8")
    str1 = f.read()
    info_list = eval(str1)
    f.close()

def save_info():  # 添加信息后，退出程序时，需要将信息保存到文件夹
    f = open(filename, "w", encoding="utf-8")
    f.write(str(info_list))
    f.close()
    
def add_info_name():  # 输入姓名
    name = str(input("请输入姓名:"))
    return name

def add_info_gender():  # 输入性别
    while True:
        gender = str(input("请输入性别:"))
        if gender in "男女":
            return gender
        else:
            print("性别输入有误，请输入男或女！")

def add_info_company():  # 输入单位
    while True:
        company = str(input("请输入单位:"))
        return company

def add_info_phoneNumber():  # 输入电话
    while True:
        phoneNumber = str(input("请输入电话:"))
        if len(list(phoneNumber)) == 11 and phoneNumber.isdigit() is True:
            return phoneNumber
        else:
            print("电话输入有误，请输入11位纯数字！")

def search_name():  # 按姓名查找
    name = add_info_name()
    name_list = []
    for i in info_list:
        name_list.append(i['name'])
        if name in i.values():
            print('姓名:',i['name'],',性别:',i['gender'],',电话:',i['phoneNumber'],',单位:',i['company'])
    if name not in name_list:
        print("查无此人，请重新输入！")

def search_company():  # 按单位查找
    name = add_info_company()
    company_list = []
    for i in info_list:
        company_list.append(i['company'])
        if name in i.values():
            print('姓名:',i['name'],',性别:',i['gender'],',电话:',i['phoneNumber'],',单位:',i['company'])
    if name not in company_list:
        print("查无此人，请重新输入！")

def search_phoneNumber():  # 按电话查找
    phoneNumber = str(input("请输入电话:"))
    phoneNumber_list = []
    for i in info_list:
        phoneNumber_list.append(i['phoneNumber'])
        if phoneNumber in i.values():
            print('姓名:',i['name'],',性别:',i['gender'],',电话:',i['phoneNumber'],',单位:',i['company'])
    if phoneNumber not in phoneNumber_list:
        print("查无此人，请重新输入！")

def remove():  # 删除函数
    name = add_info_name()
    name_list = []
    for i in info_list:
        name_list.append(i['name'])
        if name in i['name']:
            info_list.remove(i)
            print("删除成功！")
    if name not in name_list:
        print("查无此人，请重新输入！")

def main():
    if os.path.exists(filename):  # 判断这个文件是否存在，存在才加载
        load_info()
    else:  # 不存在就创建，创建后也要记得加载数据
        f = open(filename, "w")
        f.write("[]")
        f.close()
        load_info()
    while True:
        print("******************** 名片管理器 ************************")
        print("-------------------- 1.增加联系人 ----------------------")
        print("-------------------- 2.删除联系人 ----------------------")
        print("-------------------- 3.查询联系人 ------------------------")
        print("-------------------- 4.退出保存 ------------------------")
        print("******************** 名片管理器 ************************")
        command = str(input("请输入对应数字进行操作:"))  # 采用字符串形式，避免用户输入时报错
        print("-" * 30)  # 分隔线
        if command == "1":  # 采用字符串形式，避免用户输入时报错
            dic = {"name": add_info_name(), "gender": add_info_gender(), 
            "phoneNumber": add_info_phoneNumber(),"company": add_info_company(),}
            info_list.append(dic)
            print("添加成功！")
        elif command == "2":
            remove()   
        elif command == "3":
            search_name()
            search_company()
            search_phoneNumber()

        elif command == "4":
            sign = input("确定要退出吗？是(y)或否(n):")
            if sign == "y":
                save_info()  # 退出时一定要记得保存信息
                print("谢谢使用，您已成功退出系统！")
                exit()
            else:
                continue
        else:
            print("输入有误，请重新输入相应数字进行操作！")

if __name__ == '__main__':
    main() #调用功能选择函数

