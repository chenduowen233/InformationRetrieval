# -*- coding = utf-8 -*-
# @Time : 2022/5/3 17:05
# @Author : ChenDuowen
# @File : test1.py
# @Software : PyCharm

import hanlp
import os
import re
import math
from collections import defaultdict
HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH) # 世界最大中文语料库
tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)

# 词
post_dict = dict()
# 词 分数
post_TFIDF_dict = dict()
# 词 概率模型
post_RSV_dict = dict()
# 词 一元语言模型
post_UN_dict = dict()
# 词 二元语言模型
post_BI_dict = dict()

# 题目
t_post_dict = dict()
# 题目分数
t_post_TFIDF_dict = dict()
# 题目 概率模型
t_post_RSV_dict = dict()
# 题目 一元语言模型
t_post_UN_dict = dict()
# 题目 二元语言模型
t_post_BI_dict = dict()

# 分数和
All_TFIDF_dict = defaultdict(defaultdict)
# 合并后的Ci
All_RSV_dict = defaultdict(defaultdict)
# 合并后的UN
All_UN_dict = defaultdict(defaultdict)
# 合并后的BI
All_BI_dict = defaultdict(defaultdict)
# 结果
Ans_TFIDF_dict = dict()
# 概率模型 RSV 结果
Ans_RSV_dict = dict()
# 自然语言模型 UN 结果
Ans_UN_dict = dict()
# 自然语言模型 BI 结果
Ans_BI_dict = dict()

class Node:
    def __init__(self, dataval=None):
        self.dataval = dataval
        self.nextval = None

class SLinkedList:
    def __init__(self):
        self.headval = None

    def listprint(self):
        printval = self.headval
        # result = []
        result_dict = dict()
        while printval is not None:
            # print (printval.dataval)
            # result.append(printval.dataval)
            result_dict[printval.dataval] = Ans_TFIDF_dict[printval.dataval]
            printval = printval.nextval
        # print(result)
        result_dict = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
        print(result_dict)

    def AtEnd(self, newdata):
        NewNode = Node(newdata)
        if self.headval is None:
            self.headval = NewNode
            return
        laste = self.headval
        while (laste.nextval):
            laste = laste.nextval
        laste.nextval = NewNode

# 加载停用词词典
def load_file(filename):
    with open(filename, 'r', encoding="utf-8") as f:
        contents = f.readlines()
    result = []
    for content in contents:
        result.append(content.strip())
    return result

# 去除停用词
def remove_stop_words(text,dic):
    result = []
    for k in text:
        for w in k:
            if w not in dic:
                result.append(w)
    return result

def addtwodimdict(post_dict, key_a, key_b, val):
    if key_a in post_dict:
        post_dict[key_a].update({key_b: val})
    else:
        post_dict.update({key_a:{key_b: val}})
    return post_dict

def get_post_dict(files, post_dict, path):
    for file in files: #遍历文件夹
        position = path+'\\'+ file #构造绝对路径，"\\"，其中一个'\'为转义符
    #   print (position)
    #   print(re.findall(r"\d+", file))
        txts = []
        with open(position, "r",encoding='utf-8') as f: #打开文件
            # data = f.read() #读取文件
            for num, line in enumerate(f):
                if num >= 2 :
                    #print(line)
                    if line != "/n" :
                        txts.append(line)
        temp_docID_dict = dict()
        temp_term_freq_dict = dict()
        txts = ''.join(txts)
        dic = load_file('stopwords.txt')
        result = remove_stop_words(tok([txts]), dic)
        #print(result)
        #print(tok([txts]))
        #print(txts)

        # 转换成term_freq字典
        for i in result:
            temp_term_freq_dict[i] = temp_docID_dict.get(i, txts.count(i))
            # print(txts.count(i))
        # print(temp_term_freq_dict)

        # 转换成docID字典
        for i in result:
            # print(i)
            doc_ID = int(re.findall(r"\d+", file)[0])
            temp_docID_dict[i] = temp_docID_dict.get(i, doc_ID)
        # print(temp_docID_dict)
        for i in result:
            post_dict = addtwodimdict(post_dict, i, str(temp_docID_dict[i]), str(temp_term_freq_dict[i]))
    return post_dict

def get_doc_num(post_dict, doc_num_dict):
    for i in post_dict:
        count = 0
        for j in post_dict[i]:
            count = count + 1
        doc_num_dict[i] = str(count)
            #  print(j)
            #  print(post_dict[i][j])
        # print(post_dict[i])
    return doc_num_dict

def get_coll_freq(post_dict, coll_freq_dict):
    for i in post_dict:
        count = 0
        for j in post_dict[i]:
            count = count + int(post_dict[i][j])
            # print(post_dict[i][j])
        coll_freq_dict[i] = count
    return coll_freq_dict

# 将结果写入文件
def write_file(doc_num_dict, term_post_list, coll_freq_dict, path):
    with open(path, 'w') as fp:
        count = 0
        for i in coll_freq_dict:
            fp.write(i[0] + "\t" + str(doc_num_dict[i[0]]) + "\t" + str(i[1]) + "\t" + str(term_post_list[count]))
            count = count + 1
            fp.write("\n")
        # for key in doc_num_dict:
        #     # print(key)
        #     # print(doc_num_dict[key])
        #     # print(term_post_list[count])
        #     fp.write(key + "\t" + str(doc_num_dict[key]) + "\t" + str(term_post_list[count]))
        #     count = count + 1
        #     fp.write("\n")

# 将合并结果写入文件
def write_all_file(All_TFIDF_dict, path):
    with open(path, 'w') as fp:
        for i in All_TFIDF_dict:
            fp.write(str(i) + "\t" + str(All_TFIDF_dict[i]))
            fp.write("\n")

def get_t_post_dict(files, t_post_dict, path):
    for file in files: #遍历文件夹
        position = path+'\\'+ file #构造绝对路径，"\\"，其中一个'\'为转义符
        txts = []
        with open(position, "r",encoding='utf-8') as f: #打开文件
            # data = f.read() #读取文件
            for num, line in enumerate(f):
                if num == 0 :
                    if line != "/n" :
                        data = line.split('·')
                        for s in data:
                            txts.append(s)
        temp_t_docID_dict = dict()
        temp_t_term_freq_dict = dict()
        txts = ''.join(txts)
        dic = load_file('stopwords.txt')
        result = remove_stop_words(tok([txts]), dic)
        #print(result)
        #print(tok([txts]))
        #print(txts)

        # 转换成term_freq字典
        for i in result:
            temp_t_term_freq_dict[i] = temp_t_docID_dict.get(i, txts.count(i))
            # print(txts.count(i))
        # print(temp_t_term_freq_dict)

        # 转换成docID字典
        for i in result:
            # print(i)
            t_doc_ID = int(re.findall(r"\d+", file)[0])
            temp_t_docID_dict[i] = temp_t_docID_dict.get(i, t_doc_ID)
            # print(temp_t_docID_dict)
        for i in result:
            t_post_dict = addtwodimdict(t_post_dict, i, str(temp_t_docID_dict[i]), str(temp_t_term_freq_dict[i]))

    return t_post_dict

def get_t_TF_IDF_dict(t_doc_num_dict, t_IDF_dict, files, t_post_TFIDF_dict, path):
    for i in t_doc_num_dict:
        t_IDF_dict[i] = float(math.log10(200 / int(t_doc_num_dict[i]) + 1))
        # print(t_IDF_dict[i])

    for file in files: #遍历文件夹
        position = path+'\\'+ file #构造绝对路径，"\\"，其中一个'\'为转义符
        txts = []
        # 字数
        title_len = 0
        with open(position, "r",encoding='utf-8') as f: #打开文件
            for num, line in enumerate(f):
                if num == 0 :
                    #print(line)
                    title_len = len(line) - 2
                    if line != "/n" :
                        data = line.split('·')
                        for s in data:
                            txts.append(s)
        temp_t_docID_dict = dict()
        temp_t_term_freq_dict = dict()
        temp_t_TF_dict = dict()
        txts = ''.join(txts)
        dic = load_file('stopwords.txt')
        result = remove_stop_words(tok([txts]), dic)

        # 转换成term_freq字典
        for i in result:
            temp_t_term_freq_dict[i] = temp_t_docID_dict.get(i, txts.count(i))

        # 转换成docID字典
        for i in result:
            # print(i)
            t_doc_ID = int(re.findall(r"\d+", file)[0])
            temp_t_docID_dict[i] = temp_t_docID_dict.get(i, t_doc_ID)

        # 转换成TF分数字典
        for i in result:
            temp_t_TF_dict[i] = float(temp_t_term_freq_dict[i]/title_len)

        for i in result:
            tfidf = round(float(temp_t_TF_dict[i]) * float(t_IDF_dict[i]), 6)
            t_post_TFIDF_dict = addtwodimdict(t_post_TFIDF_dict, i, str(temp_t_docID_dict[i]), str(tfidf))
    # print(t_post_TFIDF_dict)
    return t_post_TFIDF_dict

def get_TF_IDF_dict(doc_num_dict, IDF_dict, files, post_TFIDF_dict, path):
    for i in doc_num_dict:
        IDF_dict[i] = float(math.log10(200 / int(doc_num_dict[i]) + 1))
        # print(t_IDF_dict[i])

    for file in files: #遍历文件夹
        position = path+'\\'+ file #构造绝对路径，"\\"，其中一个'\'为转义符
        txts = []
        # 字数
        ci_len = 0
        with open(position, "r",encoding='utf-8') as f: #打开文件
            for num, line in enumerate(f):
                if num >= 2 :
                    #print(line)
                    if line != "/n" :
                        txts.append(line)
                        ci_len = ci_len + len(line) - 2
        temp_docID_dict = dict()
        temp_term_freq_dict = dict()
        temp_TF_dict = dict()
        txts = ''.join(txts)
        dic = load_file('stopwords.txt')
        result = remove_stop_words(tok([txts]), dic)

        # 转换成term_freq字典
        for i in result:
            temp_term_freq_dict[i] = temp_docID_dict.get(i, txts.count(i))

        # 转换成docID字典
        for i in result:
            # print(i)
            doc_ID = int(re.findall(r"\d+", file)[0])
            temp_docID_dict[i] = temp_docID_dict.get(i, doc_ID)

        # 转换成TF分数字典
        for i in result:
            temp_TF_dict[i] = float(temp_term_freq_dict[i]/ci_len)

        for i in result:
            tfidf = round(float(temp_TF_dict[i]) * float(IDF_dict[i]), 6)
            post_TFIDF_dict = addtwodimdict(post_TFIDF_dict, i, str(temp_docID_dict[i]), str(tfidf))
    # print(t_post_TFIDF_dict)
    return post_TFIDF_dict

def get_t_RSV_dict(t_doc_num_dict, t_IDF_dict, files, t_post_RSV_dict, path, t_post_Num):
    t_P_dict = dict()
    t_C_dict = dict()
    for i in t_doc_num_dict:
        t_P_dict[i] = float((1/3)+(2/3)*(int(t_doc_num_dict[i])/200))

    for i in t_doc_num_dict:
        t_C_dict[i] = float(math.log10(t_P_dict[i] / (1 - t_P_dict[i])) + t_IDF_dict[i])

    for file in files: #遍历文件夹
        position = path+'\\'+ file #构造绝对路径，"\\"，其中一个'\'为转义符
        txts = []
        # 字数
        title_len = 0
        with open(position, "r",encoding='utf-8') as f: #打开文件
            for num, line in enumerate(f):
                if num == 0 :
                    #print(line)
                    title_len = len(line) - 2
                    if line != "/n" :
                        data = line.split('·')
                        for s in data:
                            txts.append(s)
        temp_t_docID_dict = dict()
        temp_t_term_freq_dict = dict()
        temp_t_TF_dict = dict()
        txts = ''.join(txts)
        dic = load_file('stopwords.txt')
        result = remove_stop_words(tok([txts]), dic)

        # 转换成term_freq字典
        for i in result:
            temp_t_term_freq_dict[i] = temp_t_docID_dict.get(i, txts.count(i))
            t_post_Num += 1

        # 转换成docID字典
        for i in result:
            # print(i)
            t_doc_ID = int(re.findall(r"\d+", file)[0])
            temp_t_docID_dict[i] = temp_t_docID_dict.get(i, t_doc_ID)

        # 转换成TF分数字典
        for i in result:
            temp_t_TF_dict[i] = float(temp_t_term_freq_dict[i]/title_len)

        for i in result:
            c = round(1.5 * float(t_C_dict[i]), 6)
            t_post_RSV_dict = addtwodimdict(t_post_RSV_dict, i, str(temp_t_docID_dict[i]), str(c))
    # print(t_post_RSV_dict)
    # print(t_post_Num)
    return t_post_RSV_dict, t_post_Num

def get_RSV_dict(doc_num_dict, IDF_dict, files, post_RSV_dict, path, post_Num):
    P_dict = dict()
    C_dict = dict()
    for i in doc_num_dict:
        P_dict[i] = float((1 / 3) + (2 / 3) * (int(doc_num_dict[i]) / 200))

    for i in doc_num_dict:
        C_dict[i] = float(math.log10(P_dict[i] / (1 - P_dict[i])) + IDF_dict[i])

    for file in files: #遍历文件夹
        position = path+'\\'+ file #构造绝对路径，"\\"，其中一个'\'为转义符
        txts = []
        # 字数
        ci_len = 0
        with open(position, "r",encoding='utf-8') as f: #打开文件
            for num, line in enumerate(f):
                if num >= 2 :
                    #print(line)
                    if line != "/n" :
                        txts.append(line)
                        ci_len = ci_len + len(line) - 2
        temp_docID_dict = dict()
        temp_term_freq_dict = dict()
        temp_TF_dict = dict()
        txts = ''.join(txts)
        dic = load_file('stopwords.txt')
        result = remove_stop_words(tok([txts]), dic)

        # 转换成term_freq字典
        for i in result:
            temp_term_freq_dict[i] = temp_docID_dict.get(i, txts.count(i))
            post_Num += 1

        # 转换成docID字典
        for i in result:
            # print(i)
            doc_ID = int(re.findall(r"\d+", file)[0])
            temp_docID_dict[i] = temp_docID_dict.get(i, doc_ID)

        # 转换成TF分数字典
        for i in result:
            temp_TF_dict[i] = float(temp_term_freq_dict[i]/ci_len)

        for i in result:
            c = round(float(C_dict[i]), 6)
            post_RSV_dict = addtwodimdict(post_RSV_dict, i, str(temp_docID_dict[i]), str(c))

    # print(post_RSV_dict)
    # print(post_Num)
    return post_RSV_dict, post_Num

def get_t_UN_dict(t_doc_num_dict, t_coll_freq_dict, files, t_post_UN_dict, path, t_post_Num):
    t_Mc_dict = dict()
    t_Md_dict = dict()
    doc = 0
    lmd = 0.5
    # print(t_doc_num_dict)
    for i in t_doc_num_dict:
        t_Mc_dict[i] = float(float(t_coll_freq_dict[i])/float(t_post_Num))
        t_Md_dict[i] = 0
    # print(t_Mc_dict)

    for file in files: #遍历文件夹
        position = path+'\\'+ file #构造绝对路径，"\\"，其中一个'\'为转义符
        txts = []
        # 字数
        title_len = 0
        doc += 1
        with open(position, "r",encoding='utf-8') as f: #打开文件
            for num, line in enumerate(f):
                if num == 0 :
                    #print(line)
                    title_len = len(line) - 2
                    if line != "/n" :
                        data = line.split('·')
                        for s in data:
                            txts.append(s)
        temp_t_docID_dict = dict()
        temp_t_term_freq_dict = dict()
        temp_t_TF_dict = dict()
        temp_t_Num = 0
        txts = ''.join(txts)
        dic = load_file('stopwords.txt')
        result = remove_stop_words(tok([txts]), dic)

        # print(result)
        # 转换成term_freq字典
        for i in result:
            temp_t_Num += 1
            temp_t_term_freq_dict[i] = temp_t_docID_dict.get(i, txts.count(i))

        # print(temp_t_Num)
        # 转换成docID字典
        # for i in result:
        #     # print(i)
        #     t_doc_ID = int(re.findall(r"\d+", file)[0])
        #     temp_t_docID_dict[i] = temp_t_docID_dict.get(i, t_doc_ID)
        #

        for i in t_doc_num_dict:
            t_Md_dict[i] = 0

        # 转换成TF分数字典
        for i in result:
            temp_t_TF_dict[i] = float(temp_t_term_freq_dict[i]/temp_t_Num)
            t_Md_dict[i] = temp_t_TF_dict[i]

        for term in t_doc_num_dict:
            p = round(float((1-lmd)*t_Mc_dict[term] + lmd*t_Md_dict[term]), 8)
            t_post_UN_dict = addtwodimdict(t_post_UN_dict, doc, term, str(p))
    # print(t_post_UN_dict)
    return t_post_UN_dict

def get_UN_dict(doc_num_dict, coll_freq_dict, files, post_UN_dict, path, post_Num):
    Mc_dict = dict()
    Md_dict = dict()
    doc = 0
    lmd = 0.5
    for i in doc_num_dict:
        Mc_dict[i] = float(coll_freq_dict[i] / post_Num)

    for file in files: #遍历文件夹
        position = path+'\\'+ file #构造绝对路径，"\\"，其中一个'\'为转义符
        txts = []
        # 字数
        ci_len = 0
        doc += 1
        with open(position, "r",encoding='utf-8') as f: #打开文件
            for num, line in enumerate(f):
                if num >= 2 :
                    #print(line)
                    if line != "/n" :
                        txts.append(line)
                        ci_len = ci_len + len(line) - 2
        temp_docID_dict = dict()
        temp_term_freq_dict = dict()
        temp_TF_dict = dict()
        temp_Num = 0
        txts = ''.join(txts)
        dic = load_file('stopwords.txt')
        result = remove_stop_words(tok([txts]), dic)

        # 转换成term_freq字典
        for i in result:
            temp_term_freq_dict[i] = temp_docID_dict.get(i, txts.count(i))
            temp_Num += 1

        # # 转换成docID字典
        # for i in result:
        #     # print(i)
        #     doc_ID = int(re.findall(r"\d+", file)[0])
        #     temp_docID_dict[i] = temp_docID_dict.get(i, doc_ID)
        for i in doc_num_dict:
            Md_dict[i] = 0

        # 转换成TF分数字典
        for i in result:
            temp_TF_dict[i] = float(temp_term_freq_dict[i]/temp_Num)
            Md_dict[i] = temp_TF_dict[i]

        for term in doc_num_dict:
            p = round(float((1 - lmd) * Mc_dict[term] + lmd * Md_dict[term]), 8)
            post_UN_dict = addtwodimdict(post_UN_dict, doc, term, str(p))

    # print(post_UN_dict)
    return post_UN_dict

def get_t_BI_dict(t_doc_num_dict, t_coll_freq_dict, files, t_post_BI_dict, path, t_post_Num):
    t_Mc_dict = dict()
    t_Md_dict = dict()
    t_BiMc_dict = dict()
    t_BiMd_dict = dict()
    doc = 0
    lmd = 0.4
    temp = []
    # print(t_doc_num_dict)
    for i in t_doc_num_dict:
        temp.append(i)
        t_Mc_dict[i] = float(float(t_coll_freq_dict[i])/float(t_post_Num))
        t_Md_dict[i] = 0
    # print(t_Mc_dict)

    # print(temp)
    for i in range(0, len(temp)-1):
        temp_t_str = str(temp[i]) + str(temp[i + 1])
        # t_BiMc_dict[temp_t_str] = float(float(t_coll_freq_dict[temp[i]]) / float(t_post_Num))
        t_BiMc_dict[temp_t_str] = float(1.0 / float(t_post_Num))
        t_BiMd_dict[temp_t_str] = 0

    for file in files: #遍历文件夹
        position = path+'\\'+ file #构造绝对路径，"\\"，其中一个'\'为转义符
        txts = []
        # 字数
        title_len = 0
        doc += 1
        with open(position, "r",encoding='utf-8') as f: #打开文件
            for num, line in enumerate(f):
                if num == 0 :
                    #print(line)
                    title_len = len(line) - 2
                    if line != "/n" :
                        data = line.split('·')
                        for s in data:
                            txts.append(s)
        temp_t_docID_dict = dict()
        temp_t_term_freq_dict = dict()
        temp_t_Biterm_freq_dict = dict()
        temp_t_TF_dict = dict()
        temp_t_Num = 0
        txts = ''.join(txts)
        dic = load_file('stopwords.txt')
        result = remove_stop_words(tok([txts]), dic)

        # print(result)
        # 转换成term_freq字典
        for i in result:
            temp_t_Num += 1
            temp_t_term_freq_dict[i] = temp_t_docID_dict.get(i, txts.count(i))

        for i in range(0, len(temp)-1):
            temp_t_str = str(temp[i]) + str(temp[i + 1])
            temp_t_Biterm_freq_dict[temp_t_str] = temp_t_docID_dict.get(temp_t_str, txts.count(temp_t_str))

        # print(temp_t_Num)
        # 转换成docID字典
        # for i in result:
        #     # print(i)
        #     t_doc_ID = int(re.findall(r"\d+", file)[0])
        #     temp_t_docID_dict[i] = temp_t_docID_dict.get(i, t_doc_ID)
        #

        for i in t_doc_num_dict:
            t_Md_dict[i] = 0

        for i in range(0, len(temp)-1):
            temp_t_str = str(temp[i]) + str(temp[i + 1])
            t_BiMd_dict[temp_t_str] = 0

        # 转换成TF分数字典
        for i in result:
            temp_t_TF_dict[i] = float(temp_t_term_freq_dict[i]/temp_t_Num)
            t_Md_dict[i] = temp_t_TF_dict[i]

        for i in range(0, len(temp)-1):
            temp_t_str = str(temp[i]) + str(temp[i + 1])
            t_BiMd_dict[temp_t_str] = float(temp_t_Biterm_freq_dict[temp_t_str] / temp_t_Num)

        for i in range(0, len(temp)-1):
            temp_t_str = str(temp[i]) + str(temp[i + 1])
            p = round(float(float((1-lmd)*t_BiMc_dict[temp_t_str]) + lmd*t_BiMd_dict[temp_t_str]) /
                      float((1-lmd)*t_Mc_dict[str(temp[i])] + lmd*t_Md_dict[str(temp[i])]), 8)
            t_post_BI_dict = addtwodimdict(t_post_BI_dict, doc, temp_t_str, str(p))
    # print(t_post_BI_dict)
    return t_post_BI_dict

def get_BI_dict(doc_num_dict, coll_freq_dict, files, post_BI_dict, path, post_Num):
    Mc_dict = dict()
    Md_dict = dict()
    BiMc_dict = dict()
    BiMd_dict = dict()
    doc = 0
    lmd = 0.4
    temp = []
    for i in doc_num_dict:
        temp.append(i)
        Mc_dict[i] = float(float(coll_freq_dict[i]) / float(post_Num))
        Md_dict[i] = 0
    # print(t_Mc_dict)

    # print(temp)
    for i in range(0, len(temp) - 1):
        temp_str = str(temp[i]) + str(temp[i + 1])
        # BiMc_dict[temp_str] = float(float(coll_freq_dict[temp[i]]) / float(post_Num))
        BiMc_dict[temp_str] = float(1.0 / float(post_Num))
        BiMd_dict[temp_str] = 0

    for file in files: #遍历文件夹
        position = path+'\\'+ file #构造绝对路径，"\\"，其中一个'\'为转义符
        txts = []
        # 字数
        ci_len = 0
        doc += 1
        with open(position, "r",encoding='utf-8') as f: #打开文件
            for num, line in enumerate(f):
                if num >= 2 :
                    #print(line)
                    if line != "/n" :
                        txts.append(line)
                        ci_len = ci_len + len(line) - 2
        temp_docID_dict = dict()
        temp_term_freq_dict = dict()
        temp_Biterm_freq_dict = dict()
        temp_TF_dict = dict()
        temp_Num = 0
        txts = ''.join(txts)
        dic = load_file('stopwords.txt')
        result = remove_stop_words(tok([txts]), dic)

        # 转换成term_freq字典
        for i in result:
            temp_Num += 1
            temp_term_freq_dict[i] = temp_docID_dict.get(i, txts.count(i))

        for i in range(0, len(temp) - 1):
            temp_str = str(temp[i]) + str(temp[i + 1])
            temp_Biterm_freq_dict[temp_str] = temp_docID_dict.get(temp_str, txts.count(temp_str))

        for i in doc_num_dict:
            Md_dict[i] = 0

        for i in range(0, len(temp) - 1):
            temp_str = str(temp[i]) + str(temp[i + 1])
            BiMd_dict[temp_str] = 0

        # 转换成TF分数字典
        for i in result:
            temp_TF_dict[i] = float(temp_term_freq_dict[i] / temp_Num)
            Md_dict[i] = temp_TF_dict[i]

        for i in range(0, len(temp) - 1):
            temp_str = str(temp[i]) + str(temp[i + 1])
            BiMd_dict[temp_str] = float(temp_Biterm_freq_dict[temp_str] / temp_Num)

        for i in range(0, len(temp) - 1):
            temp_str = str(temp[i]) + str(temp[i + 1])
            p = round(float(float((1 - lmd) * BiMc_dict[temp_str]) + lmd * BiMd_dict[temp_str]) /
                      float(float((1 - lmd) * Mc_dict[str(temp[i])] + lmd * Md_dict[str(temp[i])])), 8)
            post_BI_dict = addtwodimdict(post_BI_dict, doc, temp_str, str(p))

    # print(post_UN_dict)
    return post_BI_dict

def sum_value(obj):
    for key in obj:
        if type(obj[key]).__name__ == 'dict':
            if key not in All_TFIDF_dict:
                All_TFIDF_dict[key] = {}
            for subkey in obj[key]:
                if subkey not in All_TFIDF_dict[key]:
                    All_TFIDF_dict[key][subkey] = 0
                All_TFIDF_dict[key][subkey] += round(float(obj[key][subkey]), 6)
                All_TFIDF_dict[key][subkey] = round(All_TFIDF_dict[key][subkey], 6)
        else:
            if key not in All_TFIDF_dict:
                All_TFIDF_dict[key] = 0
            All_TFIDF_dict[key] += obj[key]
    return All_TFIDF_dict

def sum_RSV(obj):
    for key in obj:
        if type(obj[key]).__name__ == 'dict':
            if key not in All_RSV_dict:
                All_RSV_dict[key] = {}
            for subkey in obj[key]:
                if subkey not in All_RSV_dict[key]:
                    All_RSV_dict[key][subkey] = 0
                All_RSV_dict[key][subkey] += round(float(obj[key][subkey]), 6)
                All_RSV_dict[key][subkey] = round(All_RSV_dict[key][subkey], 6)
        else:
            if key not in All_RSV_dict:
                All_RSV_dict[key] = 0
            All_RSV_dict[key] += obj[key]
    return All_RSV_dict

def sum_UN(obj):
    for key in obj:
        if type(obj[key]).__name__ == 'dict':
            if key not in All_UN_dict:
                All_UN_dict[key] = {}
            for subkey in obj[key]:
                if subkey not in All_UN_dict[key]:
                    All_UN_dict[key][subkey] = 0
                All_UN_dict[key][subkey] += round(float(obj[key][subkey]), 8)
                All_UN_dict[key][subkey] = round(All_UN_dict[key][subkey], 8)
        else:
            if key not in All_UN_dict:
                All_UN_dict[key] = 0
            All_UN_dict[key] += obj[key]
    return All_UN_dict

def sum_BI(obj):
    for key in obj:
        if type(obj[key]).__name__ == 'dict':
            if key not in All_BI_dict:
                All_BI_dict[key] = {}
            for subkey in obj[key]:
                if subkey not in All_BI_dict[key]:
                    All_BI_dict[key][subkey] = 1.0
                All_BI_dict[key][subkey] *= round(float(obj[key][subkey]), 8)
                All_BI_dict[key][subkey] = round(All_BI_dict[key][subkey], 8)
        else:
            if key not in All_BI_dict:
                All_BI_dict[key] = 0
            All_BI_dict[key] += obj[key]
    return All_BI_dict

def reverse_index(path):
    # 按照顺序得到文件夹下的所有文件名称
    files = sorted(os.listdir(path), key=lambda x: len(x))
    # 词
    doc_num_dict = dict()
    coll_freq_dict = dict()
    IDF_dict = dict()
    # 词 总 term 数
    post_Num = 0
    get_post_dict(files, post_dict, path)
    get_doc_num(post_dict, doc_num_dict)
    get_coll_freq(post_dict, coll_freq_dict)
    get_TF_IDF_dict(doc_num_dict, IDF_dict, files, post_TFIDF_dict, path)
    get_RSV_dict(doc_num_dict, IDF_dict, files, post_RSV_dict, path, post_Num)
    post_Num = get_RSV_dict(doc_num_dict, IDF_dict, files, post_RSV_dict, path, post_Num)[1]
    get_UN_dict(doc_num_dict, coll_freq_dict, files, post_UN_dict, path, post_Num)
    get_BI_dict(doc_num_dict, coll_freq_dict, files, post_BI_dict, path, post_Num)
    # 按value值（term） 排序
    coll_freq_dict = sorted(coll_freq_dict.items(), key=lambda x: x[1])
    # print(coll_freq_dict)
    # for i in coll_freq_dict:
    #     print(i[0])
    # print(get_post_dict(files, post_dict, path))
    # print(get_doc_num(post_dict, doc_num_dict))
    # term_post_list = post_dict.values()
    term_post_list = []
    term_TFIDF_list = []
    for i in coll_freq_dict:
        term_post_list.append(post_dict[i[0]])
        term_TFIDF_list.append(post_TFIDF_dict[i[0]])
    # print(term_post_list)
    write_file(doc_num_dict, term_post_list, coll_freq_dict, "dict.index")
    write_file(doc_num_dict, term_TFIDF_list, coll_freq_dict, "TFIDF.index")
    # 题目
    t_doc_num_dict = dict()
    t_coll_freq_dict = dict()
    t_IDF_dict = dict()
    # 题目 总 term 数
    t_post_Num = 0
    get_t_post_dict(files, t_post_dict, path)
    get_doc_num(t_post_dict, t_doc_num_dict)
    get_coll_freq(t_post_dict, t_coll_freq_dict)
    get_t_TF_IDF_dict(t_doc_num_dict, t_IDF_dict, files, t_post_TFIDF_dict, path)
    get_t_RSV_dict(t_doc_num_dict, t_IDF_dict, files, t_post_RSV_dict, path, t_post_Num)
    t_post_Num = get_t_RSV_dict(t_doc_num_dict, t_IDF_dict, files, t_post_RSV_dict, path, t_post_Num)[1]
    get_t_UN_dict(t_doc_num_dict, t_coll_freq_dict, files, t_post_UN_dict, path, t_post_Num)
    get_t_BI_dict(t_doc_num_dict, t_coll_freq_dict, files, t_post_BI_dict, path, t_post_Num)
    t_coll_freq_dict = sorted(t_coll_freq_dict.items(), key=lambda x: x[1])
    t_term_post_list = []
    for i in t_coll_freq_dict:
        t_term_post_list.append(t_post_dict[i[0]])
    t_term_TFIDF_list = []
    for i in t_coll_freq_dict:
        t_term_TFIDF_list.append(t_post_TFIDF_dict[i[0]])
    write_file(t_doc_num_dict, t_term_post_list, t_coll_freq_dict, "t_dict.index")
    write_file(t_doc_num_dict, t_term_TFIDF_list, t_coll_freq_dict, "t_TFIDF.index")
    # 合并
    sum_value(post_TFIDF_dict)
    sum_value(t_post_TFIDF_dict)
    # Ci合并
    sum_RSV(post_RSV_dict)
    sum_RSV(t_post_RSV_dict)
    # UN合并
    sum_UN(post_UN_dict)
    sum_UN(t_post_UN_dict)
    # BI合并
    sum_BI(post_BI_dict)
    sum_BI(t_post_BI_dict)
    # print(All_TFIDF_dict)
    # print(All_UN_dict)
    # print(All_UN_dict[1]['丙'])
    write_all_file(All_TFIDF_dict, "all_TFIDF.index")
    write_all_file(All_RSV_dict, "all_RSV.index")
    write_all_file(All_UN_dict, "all_UN.index")
    write_all_file(All_BI_dict, "all_BI.index")

def foundList(t1,All_TFIDF_dict):
    al = SLinkedList()
    temp = Node(0)
    temp1 = temp
    if t1 in All_TFIDF_dict:
        for i in All_TFIDF_dict[t1]:
            # Ans_TFIDF_dict[i] = All_TFIDF_dict[t1][i]
            # print(Ans_TFIDF_dict)
            temp.nextval = Node(i)
            temp = temp.nextval
            # print(All_TFIDF_dict[t1][i])
            if str(i) not in Ans_TFIDF_dict:
                Ans_TFIDF_dict[str(i)] = float(All_TFIDF_dict[t1][i])
            else:
                Ans_TFIDF_dict[str(i)] = round(Ans_TFIDF_dict[str(i)] + float(All_TFIDF_dict[t1][i]), 6)
        # print(Ans_TFIDF_dict)
        al.headval = temp1.nextval
    return al;

def AND(l):
    la = foundList(l[0], All_TFIDF_dict)
    lb = foundList(l[1], All_TFIDF_dict)
    # return And(la, lb).listprint()
    return And(la, lb)

def OR(l):
    la = foundList(l[0], All_TFIDF_dict)
    lb = foundList(l[1], All_TFIDF_dict)
    # return Or(la, lb).listprint()
    return Or(la, lb)

def ANDNOT(l):
    la = foundList(l[0], All_TFIDF_dict)
    lb = foundList(l[1], All_TFIDF_dict)
    return AndNOT(la, lb).listprint()

def And(la,lb):
    pl1 = la.headval
    pl2 = lb.headval
    l3 = SLinkedList()
    while pl1 is not None and pl2 is not None:
        if pl1.dataval == pl2.dataval:
            l3.AtEnd(pl1.dataval)
            pl1 = pl1.nextval
            pl2 = pl2.nextval
        elif pl1.dataval < pl2.dataval:
            pl1 = pl1.nextval
        else:
            pl2 = pl2.nextval
    return l3

def Or(la,lb):
    pl1 = la.headval
    pl2 = lb.headval
    l3 = SLinkedList()
    while pl1 is not None or pl2 is not None:
        if pl1 is None:
            while pl2 is not None:
                l3.AtEnd(pl2.dataval)
                pl2 = pl2.nextval
            break
        elif pl2 is None:
            while pl1 is not None:
                l3.AtEnd(pl1.dataval)
                pl1 = pl1.nextval
            break
        if pl1.dataval == pl2.dataval:
                l3.AtEnd(pl1.dataval)
                pl1 = pl1.nextval
                pl2 = pl2.nextval
        elif pl1.dataval < pl2.dataval:
                l3.AtEnd(pl1.dataval)
                pl1 = pl1.nextval
        else:
            l3.AtEnd(pl2.dataval)
            pl2 = pl2.nextval
    return l3

def AndNOT(la,lb):
    pl1 = la.headval
    pl2 = lb.headval
    l3 = SLinkedList()
    while pl1 is not None:
        if pl2 is None:
            while pl1 is not None:
                temp = pl1.dataval
                l3.AtEnd(temp)
                pl1 = pl1.nextval
            break
        if pl1.dataval == pl2.dataval:
                pl1 = pl1.nextval
                pl2 = pl2.nextval
        elif pl1.dataval < pl2.dataval:
                temp = pl1.dataval
                l3.AtEnd(temp)
                pl1 = pl1.nextval
        else:
            pl2 = pl2.nextval
    return l3

def PLUS_AND(li):
    # 构建二维链表 链表值存储term_post链表的头节点
    term_list = SLinkedList()
    for i in li:
        term_list.AtEnd(foundList(i, All_TFIDF_dict))
    # print(term_list)
    # term_list.listprint()
    return PLUS_And(term_list)

def PLUS_OR(li):
    # 构建二维链表 链表值存储term_post链表的头节点
    term_list = SLinkedList()
    for i in li:
        term_list.AtEnd(foundList(i, All_TFIDF_dict))
    # print(term_list)
    # term_list.listprint()
    return PLUS_Or(term_list)

def PLUS_And(li):
    # temp1 = foundList(li[0],post_dict)
    # temp2 = foundList(li[1],post_dict)
    # ptr 为指针
    ptr = li.headval
    temp1 = ptr.dataval
    ptr = ptr.nextval
    temp2 = ptr.dataval
    temp = And(temp1, temp2)
    # count = 2
    while ptr is not None:
        temp = And(temp, ptr.dataval)
        ptr = ptr.nextval
    # while count is not len(li):
    #     temp = And(temp, li)
    #     count = count + 1
    return temp

def PLUS_Or(li):
    ptr = li.headval
    temp1 = ptr.dataval
    ptr = ptr.nextval
    temp2 = ptr.dataval
    temp = Or(temp1, temp2)
    while ptr is not None:
        temp = Or(temp, ptr.dataval)
        ptr = ptr.nextval
    return temp

def PLUS_or(a):
    temp1 = a[0]
    temp2 = a[1]
    temp = Or(temp1, temp2)
    i = 2
    while i is not len(a):
        temp = Or(temp, a[i])
        i = i + 1
    return temp

def PLUS_and(a):
    temp1 = a[0]
    temp2 = a[1]
    temp = And(temp1, temp2)
    i = 2
    while i is not len(a):
        temp = And(temp, a[i])
        i = i + 1
    return temp

def BIM(a):
    res = tok(a)
    count = 0
    print(res)
    for t in res:
        for i in All_RSV_dict[t]:
            if str(i) not in Ans_RSV_dict:
                Ans_RSV_dict[str(i)] = float(All_RSV_dict[t][i])
            else:
                Ans_RSV_dict[str(i)] = round(Ans_RSV_dict[str(i)] + float(All_RSV_dict[t][i]), 6)
    result_dict = dict()
    for i in Ans_RSV_dict:
        count += 1
        result_dict[i] = Ans_RSV_dict[i]
    result_dict = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    return result_dict if count > 0 else '找不到相关查询！'

def UN_MLE(a):
    res = tok(a)
    count = 0
    print(res)
    for doc in range(1, 201):
        for t in res:
            if str(doc) not in Ans_UN_dict:
                if t in All_UN_dict[doc]:
                    Ans_UN_dict[str(doc)] = float(All_UN_dict[doc][str(t)])*100
            else:
                if t in All_UN_dict[doc]:
                    Ans_UN_dict[str(doc)] = round(Ans_UN_dict[str(doc)] * float(All_UN_dict[doc][str(t)]), 8)*100
                    Ans_UN_dict[str(doc)] = round(Ans_UN_dict[str(doc)], 8)
    result_dict = dict()
    for i in Ans_UN_dict:
        count += 1
        result_dict[i] = Ans_UN_dict[i]
    result_dict = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    return result_dict[:10] if count > 0 else '找不到相关查询！'

def BI_MLE(a):
    res = tok(a)
    count = 0
    print(res)
    for doc in range(1, 201):
        for i in range(0, len(res)-1):
            if len(res) > 1:
                if str(doc) not in Ans_BI_dict:
                    if res[i]in All_UN_dict[doc]:
                        Ans_BI_dict[str(doc)] = float(All_UN_dict[doc][str(res[i])])*100
                else:
                    temp_str = str(res[i - 1]) + str(res[i])
                    if temp_str in All_BI_dict[doc]:
                        Ans_BI_dict[str(doc)] = round(Ans_BI_dict[str(doc)] * float(All_BI_dict[doc][str(temp_str)]), 8)*100
                        Ans_BI_dict[str(doc)] = round(Ans_BI_dict[str(doc)], 8)
            else:
                if str(doc) not in Ans_BI_dict:
                    if res[i] in All_UN_dict[doc]:
                        Ans_BI_dict[str(doc)] = float(All_UN_dict[doc][str(res[i])])*100
    result_dict = dict()
    for i in Ans_BI_dict:
        count += 1
        result_dict[i] = Ans_BI_dict[i]
    result_dict = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    return result_dict[:10] if count > 0 else '找不到相关查询！'

if __name__ == "__main__" :
    reverse_index(r"C:\Users\90643\Desktop\InformationRetrieval\dataset")

    print(BIM("丙辰中秋"))
    Ans_RSV_dict.clear()
    print(UN_MLE("丙辰中秋"))
    Ans_UN_dict.clear()
    print(BI_MLE("丙辰中秋"))
    Ans_BI_dict.clear()
    print(BIM("春花秋月"))
    Ans_RSV_dict.clear()
    print(UN_MLE("春花秋月"))
    Ans_UN_dict.clear()
    print(BI_MLE("春花秋月"))
    Ans_BI_dict.clear()
    print(BIM("临江危楼"))
    Ans_RSV_dict.clear()
    print(UN_MLE("临江危楼"))
    Ans_UN_dict.clear()
    print(BI_MLE("临江危楼"))
    Ans_BI_dict.clear()
    print(BIM("乱石桃花"))
    Ans_RSV_dict.clear()
    print(UN_MLE("乱石桃花"))
    Ans_UN_dict.clear()
    print(BI_MLE("乱石桃花"))
    Ans_BI_dict.clear()
    print(BIM("细细危楼"))
    Ans_RSV_dict.clear()
    print(UN_MLE("细细危楼"))
    Ans_UN_dict.clear()
    print(BI_MLE("细细危楼"))
    Ans_BI_dict.clear()
    print(BIM("一曲新词"))
    Ans_RSV_dict.clear()
    print(UN_MLE("一曲新词"))
    Ans_UN_dict.clear()
    print(BI_MLE("一曲新词"))
    Ans_BI_dict.clear()
    print(BIM("啦啦啦"))
    Ans_RSV_dict.clear()
    print(UN_MLE("啦啦啦"))
    Ans_UN_dict.clear()

    AND(['一', '曲']).listprint()
    Ans_TFIDF_dict.clear()
    AND(['丙辰', '中秋']).listprint()
    Ans_TFIDF_dict.clear()

    # AND('丙辰', '中秋', post_dict)
    # AND(['丙辰', '中秋']).listprint()
    # Ans_TFIDF_dict.clear()
    # AND(['陈同甫', '卢飞快']).listprint()
    # Ans_TFIDF_dict.clear()
    # OR(['欢', '作']).listprint()
    # Ans_TFIDF_dict.clear()
    # And(AND(['丙辰', '中秋']), OR(['欢', '作'])).listprint()
    # Ans_TFIDF_dict.clear()
    # ANDNOT(['有', '此'])
    # Ans_TFIDF_dict.clear()
    # PLUS_AND(['作', '醉', '此']).listprint()
    # Ans_TFIDF_dict.clear()
    # PLUS_and([PLUS_AND(['作', '醉', '此']), PLUS_AND(['欢', '作', '此']), PLUS_AND(['丙辰', '中秋', '此'])]).listprint()
    # Ans_TFIDF_dict.clear()
    # PLUS_OR(['作', '醉', '此']).listprint()
    # Ans_TFIDF_dict.clear()
    # PLUS_or([PLUS_OR(['作', '醉', '此']), PLUS_OR(['欢', '达', '旦', '陈同甫']), PLUS_OR(['丙辰', '中秋', '断肠'])]).listprint()
    # Ans_TFIDF_dict.clear()
    #
    # And(PLUS_OR(['杳杳', '神京', '仙子']), AND(['登山', '每'])).listprint()
    # Ans_TFIDF_dict.clear()
    # Or(Or(PLUS_AND(['都', '赋', '柔']), foundList('练',All_TFIDF_dict)),foundList('游人',All_TFIDF_dict)).listprint()
    # Ans_TFIDF_dict.clear()
    # AndNOT(Or(PLUS_AND(['门外', '相续', '嗟']),foundList('索',All_TFIDF_dict)),foundList('昨',All_TFIDF_dict)).listprint()
    # Ans_TFIDF_dict.clear()
    # AndNOT(And(PLUS_OR(['心事', '断肠', '句']),foundList('渡',All_TFIDF_dict)),foundList('尺',All_TFIDF_dict)).listprint()
    # Ans_TFIDF_dict.clear()
    # AndNOT(Or(AND(['华灯','碍']),foundList('池',All_TFIDF_dict)),PLUS_AND(['丽日', '明', '屋'])).listprint()
    # Ans_TFIDF_dict.clear()
    # Or(Or(PLUS_AND(['伫倚', '危楼', '迟']),foundList('尘',All_TFIDF_dict)),foundList('随',All_TFIDF_dict)).listprint()
    # Ans_TFIDF_dict.clear()
    # And(PLUS_OR(['临江', '奴娇', '歌子']),PLUS_OR(['仙', '念', '南'])).listprint()
    # Ans_TFIDF_dict.clear()
    # And(And(PLUS_OR(['乱石', '桃花', '兵']), foundList('风',All_TFIDF_dict)),foundList('低',All_TFIDF_dict)).listprint()
    # Ans_TFIDF_dict.clear()
    # AndNOT(And(PLUS_OR(['休', '泛', '相']), foundList('有', All_TFIDF_dict)), foundList('此', All_TFIDF_dict)).listprint()
    # Ans_TFIDF_dict.clear()
    # Or(Or(PLUS_OR(['此', '有', '随']), foundList('尘', All_TFIDF_dict)), foundList('随', All_TFIDF_dict)).listprint()


# text = '我自横刀向天笑，去留肝胆两昆仑'
# print(HanLP(['明月几时有？把酒问青天。不知天上宫阙，今夕是何年。我欲乘风归去，又恐琼楼玉宇⑺，高处不胜寒。起舞弄清影，何似在人间？转朱阁，低绮户，照无眠。不应有恨，何事长向别时圆？人有悲欢离合，月有阴晴圆缺，此事古难全。但愿人长久，千里共婵娟。']))
#
# print(HanLP([text]))
#
# print(HanLP(['寻寻觅觅，冷冷清清，凄凄惨惨戚戚。乍暖还寒时候，最难将息。三杯两盏淡酒，怎敌他、晚来风急？雁过也，正伤心，却是旧时相识。满地黄花堆积。憔悴损，如今有谁堪摘？守著窗儿，独自怎生得黑？梧桐更兼细雨，到黄昏、点点滴滴。这次第，怎一个愁字了得！']))