# -*- coding = utf-8 -*-
# @Time : 2022/5/3 19:08
# @Author : ChenDuowen
# @File : test3.py
# @Software : PyCharm

import os

path = r"C:\Users\90643\Desktop\InformationRetrieval\dataset(1)"
files= os.listdir(path) #得到文件夹下的所有文件名称

for file in files: #遍历文件夹
    position = path+'\\'+ file #构造绝对路径，"\\"，其中一个'\'为转义符
#   print (position)
    txts = []
    with open(position, "r",encoding='utf-8') as f: #打开文件
        # data = f.read() #读取文件
        for num, line in enumerate(f):
            if num >= 2 :
                #print(line)
                if line != "/n" :
                    txts.append(line)
    txts = ''.join(txts)
    print(txts)
# txts = ''.join(txts)#转化为非数组类型
# print (txts)
