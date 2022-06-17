# coding=gbk
# @Time : 2022/5/3 16:56
# @Author : ChenDuowen
# @File : test.py
# @Software : PyCharm
import ast
import hanlp
import PySimpleGUI as sg
HanLP = hanlp.load(hanlp.pretrained.mtl.CLOSE_TOK_POS_NER_SRL_DEP_SDP_CON_ELECTRA_SMALL_ZH) # 世界最大中文语料库
tok = hanlp.load(hanlp.pretrained.tok.COARSE_ELECTRA_SMALL_ZH)
#import test1 as x
count=0
All_TFIDF_dict={}
# Open file
fileHandler  =  open  ("all_TFIDF.index",  "r")
# Get list of all lines in file
listOfLines  =  fileHandler.readlines()
# Close file
fileHandler.close()
for line in listOfLines:
    kav = line.split(maxsplit=1)
    kavnn=kav[1].split(sep='\n')
    All_TFIDF_dict[kav[0]]=ast.literal_eval(kavnn[0])


All_RSV_dict={}
# Open file
fileHandler  =  open  ("all_RSV.index",  "r")
# Get list of all lines in file
listOfLines  =  fileHandler.readlines()
# Close file
fileHandler.close()
for line in listOfLines:
    kbv = line.split(maxsplit=1)
    kbvnn=kbv[1].split(sep='\n')
    All_RSV_dict[kbv[0]]=ast.literal_eval(kbvnn[0])
All_UN_dict={}
# Open file
fileHandler  =  open  ("all_UN.index",  "r")
# Get list of all lines in file
listOfLines  =  fileHandler.readlines()
# Close file
fileHandler.close()
for line in listOfLines:
    kcv = line.split(maxsplit=1)
    kcvnn=kcv[1].split(sep='\n')
    All_UN_dict[ast.literal_eval(kcv[0])]=ast.literal_eval(kcvnn[0])
All_BI_dict={}
# Open file
fileHandler  =  open  ("all_BI.index",  "r")
# Get list of all lines in file
listOfLines  =  fileHandler.readlines()
# Close file
fileHandler.close()
for line in listOfLines:
    kdv = line.split(maxsplit=1)
    kdvnn=kdv[1].split(sep='\n')
    All_BI_dict[ast.literal_eval(kdv[0])]=ast.literal_eval(kdvnn[0])
Ans_TFIDF_dict={}
Ans_RSV_dict={}
Ans_UN_dict={}
Ans_BI_dict={}

# 定义布局
text1=''''''
text2=''''''
text3=''''''
text4=''''''
text5='''找不到相关查询!'''
text6='''您输入的分词格式或查询格式有误，请重新尝试'''
answer1=[('30',0.01000001),('40',0.005),('50',0.004),('60',0.003),('70',0.002),('80',0.001),('90',0.0009),('100',0.0008)]
answer2=[('31',0.01000001),('41',0.005),('51',0.004),('61',0.003),('71',0.002),('81',0.001),('91',0.0009),('101',0.0008),('111',0.0007),('121',0.0006)]
answer3=[('32',0.01000001),('42',0.005),('52',0.004),('62',0.003),('72',0.002),('82',0.001),('92',0.0009),('102',0.0008),('112',0.0007),('122',0.0006)]
answer4=[('33',0.01000001),('43',0.005),('53',0.004),('63',0.003),('73',0.002),('83',0.001),('93',0.0009),('103',0.0008),('113',0.0007)]
layouta=[
    #sg.theme('Default')
    [sg.Text('',size=65),sg.Text('宋词检索',font=('宋体',30))],
    [sg.Text('',size=63),sg.Button('BM',key='B1'),sg.Button('RSV',key='R1'),sg.Button('uni-MLE',key='O1'),sg.Button('bi-MLE',key='T1')],
    [sg.Text('',size=37),sg.Text('     BM'),sg.In(key='搜索值1',size=40,font=('宋体',20)),sg.Button('百度一下',key='查询1',font=('宋体',15)),sg.Text('',size=37)],
    [sg.Text('',size=65)],
    [sg.Text('',size=1),sg.ML(default_text=text1,size=(147,32),font=('宋体'),key='LM1')],
    [sg.Text('',size=65)]
        ]
layoutb=[
    #sg.theme('Default')
    [sg.Text('',size=65),sg.Text('宋词检索',font=('宋体',30))],
    [sg.Text('',size=63),sg.Button('BM',key='B2'),sg.Button('RSV',key='R2'),sg.Button('uni-MLE',key='O2'),sg.Button('bi-MLE',key='T2')],
    [sg.Text('',size=37),sg.Text('    RSV'),sg.In(key='搜索值2',size=40,font=('宋体',20)),sg.Button('百度一下',key='查询2',font=('宋体',15)),sg.Text('',size=37)],
    [sg.Text('',size=65)],
    [sg.Text('',size=1),sg.ML(default_text=text2,size=(147,32),font=('宋体'),key='LM2')],
    [sg.Text('',size=65)]
        ]
layoutc=[
    #sg.theme('Default')
    [sg.Text('',size=65),sg.Text('宋词检索',font=('宋体',30))],
    [sg.Text('',size=63),sg.Button('BM',key='B3'),sg.Button('RSV',key='R3'),sg.Button('uni-MLE',key='O3'),sg.Button('bi-MLE',key='T3')],
    [sg.Text('',size=37),sg.Text('uni-MLE'),sg.In(key='搜索值3',size=40,font=('宋体',20)),sg.Button('百度一下',key='查询3',font=('宋体',15)),sg.Text('',size=37)],
    [sg.Text('',size=65)],
    [sg.Text('', size=1), sg.ML(default_text=text3, size=(147, 32), font=('宋体'), key='LM3')],
    [sg.Text('',size=65)]
        ]
layoutd=[
    #sg.theme('Default')
    [sg.Text('',size=65),sg.Text('宋词检索',font=('宋体',30))],
    [sg.Text('',size=63),sg.Button('BM',key='B4'),sg.Button('RSV',key='R4'),sg.Button('uni-MLE',key='O4'),sg.Button('bi-MLE',key='T4')],
    [sg.Text('',size=37),sg.Text(' bi-MLE'),sg.In(key='搜索值4',size=40,font=('宋体',20)),sg.Button('百度一下',key='查询4',font=('宋体',15)),sg.Text('',size=37)],
    [sg.Text('',size=65)],
    [sg.Text('', size=1), sg.ML(default_text=text4, size=(147, 32), font=('宋体'), key='LM4')],
    [sg.Text('',size=65)]
        ]
layout=[
    [sg.Frame(title='',layout=layouta,key='111'),
     sg.Frame(title='',layout=layoutb,visible=False,key='222'),
     sg.Frame(title='',layout=layoutc,visible=False,key='333'),
     sg.Frame(title='',layout=layoutd,visible=False,key='444')]
]

#创建窗口
window=sg.Window('',layout,size=(1280,720))

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
        # print(result_dict)
        return result_dict[:10]

    def AtEnd(self, newdata):
        NewNode = Node(newdata)
        if self.headval is None:
            self.headval = NewNode
            return
        laste = self.headval
        while (laste.nextval):
            laste = laste.nextval
        laste.nextval = NewNode

def write_all_file(All_TFIDF_dict, path):
    with open(path, 'w') as fp:
        for i in All_TFIDF_dict:
            fp.write(str(i) + "\t" + str(All_TFIDF_dict[i]))
            fp.write("\n")

def foundlist(t1,All_TFIDF_dict):
    al = SLinkedList()
    temp = Node(0)
    temp1 = temp
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
    al.headval = temp1.nextval
    return al;

def And(la,lb):
    pl1 = la.headval
    pl2 = lb.headval
    l3 = SLinkedList()
    while pl1 is not None and pl2 is not None:
        if int(pl1.dataval) == int(pl2.dataval):
            l3.AtEnd(pl1.dataval)
            pl1 = pl1.nextval
            pl2 = pl2.nextval
        elif int(pl1.dataval) < int(pl2.dataval):
            pl1 = pl1.nextval
        elif int(pl1.dataval) > int(pl2.dataval):
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
        if int(pl1.dataval) == int(pl2.dataval):
                l3.AtEnd(pl1.dataval)
                pl1 = pl1.nextval
                pl2 = pl2.nextval
        elif int(pl1.dataval) < int(pl2.dataval):
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
        if int(pl1.dataval) == int(pl2.dataval):
                pl1 = pl1.nextval
                pl2 = pl2.nextval
        elif int(pl1.dataval) < int(pl2.dataval):
                temp = pl1.dataval
                l3.AtEnd(temp)
                pl1 = pl1.nextval
        else:
            pl2 = pl2.nextval
    return l3

def BIM(a):
    res = tok(a)
    count = 0
    print(res)
    for t in res:
        if t in All_RSV_dict:
            for i in All_RSV_dict[t]:
                if str(i) not in Ans_RSV_dict:
                    Ans_RSV_dict[str(i)] = float(All_RSV_dict[t][i])
                else:
                    Ans_RSV_dict[str(i)] = round(Ans_RSV_dict[str(i)] + float(All_RSV_dict[t][i]), 8)
                    Ans_RSV_dict[str(i)] = round(Ans_RSV_dict[str(i)], 8)
    result_dict = dict()
    for i in Ans_RSV_dict:
        count += 1
        result_dict[i] = round(Ans_RSV_dict[i] / 10, 8)
    result_dict = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    return result_dict[:10] if count > 0 else '找不到相关查询！'

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
        result_dict[i] = round(Ans_UN_dict[i] / 100, 8)
    result_dict = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    return result_dict[:10] if count > 0 else '找不到相关查询！'

def BI_MLE(a):
    res = tok(a)
    count = 0
    print(res)
    for doc in range(1, 201):
        if len(res) > 1:
            for i in range(0, len(res) - 1):
                if str(doc) not in Ans_BI_dict:
                    if res[i] in All_UN_dict[doc]:
                        Ans_BI_dict[str(doc)] = float(All_UN_dict[doc][str(res[i])])*100
                else:
                    temp_str = str(res[i - 1]) + str(res[i])
                    if temp_str in All_BI_dict[doc]:
                        Ans_BI_dict[str(doc)] = round(Ans_BI_dict[str(doc)] * float(All_BI_dict[doc][str(temp_str)]), 8)*100
                        Ans_BI_dict[str(doc)] = round(Ans_BI_dict[str(doc)], 8)
        else:
            if str(doc) not in Ans_BI_dict:
                if res[0] in All_UN_dict[doc]:
                    Ans_BI_dict[str(doc)] = float(All_UN_dict[doc][str(res[0])])*100
    result_dict = dict()
    for i in Ans_BI_dict:
        count += 1
        result_dict[i] = round(Ans_BI_dict[i] / 100, 8)
    result_dict = sorted(result_dict.items(), key=lambda x: x[1], reverse=True)
    return result_dict[:10] if count > 0 else '找不到相关查询！'

#事件循环
while True:

    event,values=window.read()

    if event==None:
        break
    if event=='R1':
        window['111'].update(visible=False)
        window['222'].update(visible=True)
    if event == 'O1':
        window['111'].update(visible=False)
        window['333'].update(visible=True)
    if event == 'T1':
        window['111'].update(visible=False)
        window['444'].update(visible=True)
    if event=='B2':
        window['222'].update(visible=False)
        window['111'].update(visible=True)
    if event == 'O2':
        window['222'].update(visible=False)
        window['333'].update(visible=True)
    if event == 'T2':
        window['222'].update(visible=False)
        window['444'].update(visible=True)
    if event=='B3':
        window['333'].update(visible=False)
        window['111'].update(visible=True)
    if event == 'R3':
        window['333'].update(visible=False)
        window['222'].update(visible=True)
    if event == 'T3':
        window['333'].update(visible=False)
        window['444'].update(visible=True)
    if event=='B4':
        window['444'].update(visible=False)
        window['111'].update(visible=True)
    if event == 'R4':
        window['444'].update(visible=False)
        window['222'].update(visible=True)
    if event == 'O4':
        window['444'].update(visible=False)
        window['333'].update(visible=True)
    if event == '查询1':

        print(values['搜索值1'])
        strs=values['搜索值1']
        text1=''''''
        #print(temp)
        temp = 0

        window['LM1'].update(value=text1)
        jieguo = strs.split()
        print(jieguo)
        try:
            if jieguo[1] == 'and':
                print(count)
                temp=And(foundlist(jieguo[0], All_TFIDF_dict), foundlist(jieguo[2], All_TFIDF_dict))
                print(temp)
            elif jieguo[1] == 'or':
                #temp=Or(foundList(0), foundList(2))

                temp=Or(foundlist(jieguo[0], All_TFIDF_dict), foundlist(jieguo[2], All_TFIDF_dict))
                print(temp)
            elif jieguo[1] == 'andnot':
                #temp=AndNot(foundList(0), foundList(2))
                temp=AndNOT(foundlist(jieguo[0], All_TFIDF_dict), foundlist(jieguo[2], All_TFIDF_dict))
                print(temp)
            i=3
            while i<len(jieguo):
                if jieguo[i] == 'and':
                    temp = And(temp, foundlist(jieguo[i+1], All_TFIDF_dict))
                    print(temp)
                elif jieguo[i] == 'or':
                    #temp=Or(temp,foundList(i+1))
                    temp = Or(temp, foundlist(jieguo[i + 1], All_TFIDF_dict))
                    print(temp)
                else:
                    #temp=AndNOT(temp,foundList(i+1))
                    temp = AndNOT(temp, foundlist(jieguo[i + 1], All_TFIDF_dict))
                    print(temp)
                i = i+2
        except:
            print(233333)
            window['LM1'].update(value=text6)
        else:
            print(temp.headval)
            Ans = temp.listprint()
            print(temp.headval)
            if len(Ans)==0:
                window['LM1'].update(value=text5)
            else:
                print(Ans)
                j=0
                while j <= len(Ans)-1:
                    with open("C:\\Users\\90643\\Desktop\\InformationRetrieval\\dataset\\" + Ans[j][0] + ".txt", "r", encoding='utf-8') as f:
                        data=''''''
                        line = f.readline().strip()
                        data = line + '\n'
                        while line:
                            line = f.readline()
                            if line != '\n':
                                data = data + line
                        strl=str(j+1)
                        text1 = text1 +'\n'+strl.zfill(2)+'                                              '+'诗词编号：'+ Ans[j][0].zfill(3) + '                                    ' + '匹配分数: '+ str(Ans[j][1])+'\n'+ data +'\n'+'-----------------------------------------------------------------------------------------------------------------------'

                    j = j + 1
                Ans_TFIDF_dict.clear()
                window['LM1'].update(value=text1)

    if event == '查询2':

        print(values['搜索值2'])
        strs = values['搜索值2']
        text2=''''''
        window['LM2'].update(value=text2)
        answer2=BIM(values['搜索值2'])

        '''abc='100'
            with open("C:\\Users\\dell\\Desktop\\dataset\\"+abc+".txt","r",encoding='utf-8') as f:
                data = f.read()
                print(data)
                text1=data + '1'
                print(text1)
            window['LM1'].update(value=text1)
            '''
        j = 0
        if answer2 == '找不到相关查询！':
            window['LM2'].update(text5)
        else:
            while j <= len(answer2)-1:
                 with open("C:\\Users\\90643\\Desktop\\InformationRetrieval\\dataset\\" + answer2[j][0] + ".txt", "r", encoding='utf-8') as f:
                    data = ''''''
                    line = f.readline().strip()
                    data = line + '\n'
                    while line:
                        line = f.readline()
                        if line != '\n':
                            data = data + line
                    strl = str(j + 1)
                    text2 = text2 + '\n' + strl.zfill(2) + '                                              ' + '诗词编号：' + answer2[j][0].zfill(3) + '                                    ' + '匹配分数: ' + str(answer2[j][1]) + '\n' + data + '\n' + '-----------------------------------------------------------------------------------------------------------------------'
                 j = j + 1
            window['LM2'].update(value=text2)
        Ans_RSV_dict.clear()

    if event == '查询3':

        print(values['搜索值3'])
        strs = values['搜索值3']
        text3=''''''
        window['LM3'].update(value=text3)
        answer3 = UN_MLE(values['搜索值3'])

        '''abc='100'
            with open("C:\\Users\\dell\\Desktop\\dataset\\"+abc+".txt","r",encoding='utf-8') as f:
                data = f.read()
                print(data)
                text1=data + '1'
                print(text1)
            window['LM1'].update(value=text1)
            '''
        j = 0
        if answer3=='找不到相关查询！':
            window['LM3'].update(text5)
        else:
            while j <= len(answer3)-1:
                 with open("C:\\Users\\90643\\Desktop\\InformationRetrieval\\dataset\\" + answer3[j][0] + ".txt", "r", encoding='utf-8') as f:
                    data = ''''''
                    line = f.readline().strip()
                    data = line + '\n'
                    while line:
                        line = f.readline()
                        if line != '\n':
                            data = data + line
                    strl = str(j + 1)
                    text3 = text3 + '\n' + strl.zfill(2) + '                                              ' + '诗词编号：' + answer3[j][0].zfill(3) + '                                    ' + '匹配分数: ' + str(answer3[j][1]) + '\n' + data + '\n' + '-----------------------------------------------------------------------------------------------------------------------'
                 j = j + 1
            window['LM3'].update(value=text3)
        Ans_UN_dict.clear()

    if event == '查询4':

        print(values['搜索值4'])
        strs = values['搜索值4']
        text4=''''''
        window['LM4'].update(value=text4)
        answer4 = BI_MLE(values['搜索值4'])

        '''abc='100'
            with open("C:\\Users\\dell\\Desktop\\dataset\\"+abc+".txt","r",encoding='utf-8') as f:
                data = f.read()
                print(data)
                text1=data + '1'
                print(text1)
            window['LM1'].update(value=text1)
            '''
        j = 0
        if answer4=='找不到相关查询！':
            window['LM4'].update(text5)
        else:
            while j <= len(answer4)-1:
                 with open("C:\\Users\\90643\\Desktop\\InformationRetrieval\\dataset\\" + answer4[j][0] + ".txt", "r", encoding='utf-8') as f:
                    data = ''''''
                    line = f.readline().strip()
                    data = line + '\n'
                    while line:
                        line = f.readline()
                        if line != '\n':
                            data = data + line
                    strl = str(j + 1)
                    text4 = text4 + '\n' + strl.zfill(2) + '                                              ' + '诗词编号：' + answer4[j][0].zfill(3) + '                                    ' + '匹配分数: ' + str(answer4[j][1]) + '\n' + data + '\n' + '-----------------------------------------------------------------------------------------------------------------------'
                 j = j + 1
            window['LM4'].update(value=text4)
        Ans_BI_dict.clear()

#关闭窗口
window.close()