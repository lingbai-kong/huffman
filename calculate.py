# -*- coding: utf-8 -*-
"""
Created on Fri Aug 21 10:40:48 2020

@author: 孔令百

Name:caculate.py

Desctiption:该模块包含计算哈夫曼树结点坐标、生成随机文本、读文件的方法
"""
import random
from huffmantree import huffman
"""
函数：CalCoordinate(tree,root,rootNum,leafNum)
功能：计算哈夫曼树结点坐标
传入参数：哈夫曼树tree(字典)、哈夫曼树树根root(字符串)、哈夫曼树非叶子结点数rootNum(整数)、哈夫曼树叶子结点数leafNum(整数)
传出参数：哈夫曼树结点坐标coordinate(字典)、哈夫曼树绘制区域大小:宽X(整数),高Y(整数)
"""
def CalCoordinate(tree,root,rootNum,leafNum):
    xBondary=100#绘图区左右边框宽度
    yBondary=100#绘图区上下边框宽度
    xUnit=100#每个叶子结点横坐标距离
    yUnit=150#每层结点纵坐标距离
    xMax=32767#绘图区最大宽度
    yMax=32767#绘图区最大高度
    coordinate={}#哈夫曼树结点坐标,格式:key=哈夫曼树结点关键字(字符串),value=(横坐标x(整数),纵坐标y(整数))(元组)
    curNode=root#当前结点,初始化为根结点
    maxDepth=tree[max(tree,key=lambda x: tree[x][3])][3]#哈夫曼树的高度
    X=xUnit*leafNum+2*xBondary#计算绘图区宽度
    Y=yUnit*maxDepth+2*yBondary#计算绘图区高度
    xCount=0#已生成坐标的叶子结点数目
    
    if X>xMax:#当绘图区宽度超限制时,重新计算参数
        xUnit=(xMax-2*xBondary)/leafNum
        X=xMax
    if Y>yMax:#当绘图区高度超限制时,重新计算参数
        yUnit=(yMax-2*yBondary)/maxDepth
        Y=yMax
    
    while True:#主循环
        down=False#进入下一层标志,初始为假
        for nextNode in tree[curNode][1]:#遍历当前结点的子结点
            if nextNode not in coordinate:#找到一个未生成坐标的子结点
                if len(tree[nextNode][1])>0:#这个子结点还有后继
                    down=True#进入下一层标志为正
                    break#跳出该循环
                else:#这个子结点没有后继,就是叶子结点
                    #计算这个结点的坐标
                    coordinate[nextNode]=((xBondary+xCount*xUnit),(yBondary+tree[nextNode][3]*yUnit))
                    xCount+=1#已生成坐标的叶子结点数目增1
        if down:#如果进入下一层标志为真
            curNode=nextNode#以这个未生成坐标的子结点为当前结点进入下一次主循环
        else:#进入下一层标志为假,说明当前结点的子结点均有坐标
            childrenSumX=0#子结点横坐标和
            childrenNum=len(tree[curNode][1])#子结点数目
            # if childrenNum==0:
            #     childrenNum=1
            for child in tree[curNode][1]:#计算子结点横坐标之和
                childrenSumX+=coordinate[child][0]
            #计算当前结点的坐标
            coordinate[curNode]=((childrenSumX/childrenNum),(yBondary+tree[curNode][3]*yUnit))
            if(curNode==root):#如果当前结点是根结点,说明所有结点坐标均已计算完成
                break#退出主循环
            curNode=tree[curNode][2]#否则回溯到当前结点的前驱进入下一次主循环
    return coordinate,X,Y
"""
函数：GenRandomText(choice,length)
功能：生成随机字符串
传入参数：随机字符串类型choice(字符串)、随机字符串长度length(整数)
传出参数：随机字符串text(字符串)
"""
def GenRandomText(choice,length):
    text=""
    if choice=="随机数字":
        for i in range(length):
            text+=random.choice('0123456789')
    elif choice=="随机字母":
        for i in range(length):
            text+=random.choice('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz')
    elif choice=="随机字符":
        for i in range(length):
            text+=random.choice('0123456789ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz`~!@#$%^&*()_+=-[]{}|\\;:\'",./<>?')
    elif choice=="随机中文":
        for i in range(length):
            head=random.randint(0xb0, 0xf7)
            body=random.randint(0xa1, 0xf9)  # 在head区号为55的那一块最后5个汉字是乱码,为了方便缩减下范围
            text+= bytes.fromhex(f'{head:x}{body:x}').decode('gb2312')
    return text
"""
函数：ReadFile(filename)
功能：读取文件内容
传入参数：文件路径及文件名filename(字符串)
传出参数：文本文件内容content(字符串)
"""
def ReadFile(filename):
    try:
        f=open(filename,'r',encoding='utf8')
        content=f.read()
        f.close()
    except IOError as e:
        print("error:",e)
        content=""    
    return content
"""
该模块的测试代码
"""
if __name__=='__main__':
    test=GenRandomText("随机中文", 100)
    print(test)
    huf=huffman("11114324324111")
    huf.CountFrqt()
    hufTree,root,rootNum,leafNum=huf.GenerateTree()
    coordinate,X,Y=CalCoordinate(hufTree, root, rootNum, leafNum)
    print(coordinate,X,Y)    
    content=ReadFile(r"C:\Users\HP\Desktop\test.txt")
    print(content)
    
    