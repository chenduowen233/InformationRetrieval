# -*- coding = utf-8 -*-
# @Time : 2022/5/3 18:43
# @Author : ChenDuowen
# @File : test2.py
# @Software : PyCharm

# encoding=utf-8
import jieba

seg_list = jieba.cut("明月几时有？把酒问青天。不知天上宫阙，今夕是何年。我欲乘风归去，又恐琼楼玉宇，高处不胜寒。起舞弄清影，何似在人间？转朱阁，低绮户，照无眠。不应有恨，何事长向别时圆？人有悲欢离合，月有阴晴圆缺，此事古难全。但愿人长久，千里共婵娟。")  # 默认是精确模式
print(", ".join(seg_list))

seg_list = jieba.cut("寻寻觅觅，冷冷清清，凄凄惨惨戚戚。乍暖还寒时候，最难将息。三杯两盏淡酒，怎敌他、晚来风急？雁过也，正伤心，却是旧时相识。满地黄花堆积。憔悴损，如今有谁堪摘？守著窗儿，独自怎生得黑？梧桐更兼细雨，到黄昏、点点滴滴。这次第，怎一个愁字了得！")  # 默认是精确模式
print(", ".join(seg_list))

def topk(li, k):
    # 1. 建堆
    heap = li[0:k]  # 先把列表索引0到k的数取出来(取列表前k个数)，进行建堆
    for i in range((k-2)//2, -1, -1):
        sift(heap, i, k-1)
    # 2. 遍历
    for i in range(k, len(li)-1):   # 从k开始
        if li[i] > heap[0]:  # 比较li[i]和堆顶的元素的大小，如果大于堆顶，则替换堆顶，并做一次调整，如果小于堆顶，则舍弃这个li[i]
            heap[0] = li[i]
            sift(heap, 0, k-1)
    # 3. 出数
    for i in range(k - 1, -1, -1):
        # i指向当前堆的最后一个元素
        heap[0], heap[i] = heap[i], heap[0]
        sift(heap, 0, i - 1)  # i-1是新的high
    return heap