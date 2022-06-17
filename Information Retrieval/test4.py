#-*- coding = utf-8 -*-
#@Time : 2022/5/6 13:24
#@Author : ChenDuowen
#@File : test4.py
#@Software : PyCharm

class Node:
    def __init__(self, dataval=None):
        self.dataval = dataval
        self.nextval = None

class SLinkedList:
    def __init__(self):
        self.headval = None

    def listprint(self):
        printval = self.headval
        while printval is not None:
            print (printval.dataval)
            printval = printval.nextval

    def AtEnd(self, newdata):
        NewNode = Node(newdata)
        if self.headval is None:
            self.headval = NewNode
            return
        laste = self.headval
        while (laste.nextval):
            laste = laste.nextval
        laste.nextval = NewNode
l1 = SLinkedList()
l1.headval = Node(1)
e2=Node(2)
e3=Node(3)
l1.headval.nextval = e2
e2.nextval=e3
l2 = SLinkedList()
l2.headval = Node(2)
e3=Node(3)
e4=Node(4)
l2.headval.nextval = e3
e3.nextval = e4

l1.listprint()
l2.listprint()

l3 = SLinkedList()

def intersect(la,lb):
    pl1 = la.headval
    pl2 = lb.headval
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

def combine(la,lb):
    pl1 = l1.headval
    pl2 = l2.headval
    while pl1 is not None or pl2 is not None:
        if pl1 is None:
            while pl2 is not None:
                l3.AtEnd(pl2.dataval)
                pl2 = pl2.nextval
            break
        elif pl2 is None:
            while pl2 is not None:
                l3.Atend(pl1.dataval)
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
def andNot(la,lb):
    pl1 = l1.headval
    pl2 = l2.headval
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
combine(l1,l2)
l3.listprint()