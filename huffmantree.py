# -*- coding: utf-8 -*-
"""
Created on Thu Aug 20 22:16:16 2020

@author: 孔令百

Name:huffmantree.py

Desctiption:该模块包含哈夫曼树类,通过哈夫曼算法求解哈夫曼树,生成哈夫曼编码
"""
from copy import deepcopy
"""
类:哈夫曼类
功能:生成哈夫曼树和哈夫曼码
"""
class huffman:
    """
    函数：__init__(self,string='')
    功能：哈夫曼类构造函数
    传入参数：执行哈夫曼算法的目标字符串string(字符串)
    传出参数：无
    """
    def __init__(self,string=''):
        self._srcString=string#原字符串
        self._countFrqt={}#各个字符关键值
        self._leafNum=0#哈夫曼树叶子节点数目
        self._rootNum=0#哈夫曼树根结点数目
        self._huffmanTree={}#哈夫曼树,格式:key=结点名称(字符串),value=[关键值(整数),[左儿子结点(字符串),右儿子结点(字符串)](列表),父亲结点(字符串),当前结点深度(整数)](列表)
        self._root=''#根结点名称
        self._code={}#哈夫曼编码表,格式:key=结点名称(字符串),value=哈夫曼编码(字符串)
    """
    函数：_CalDepth(self,node,depth)
    功能：计算结点node在哈夫曼树中的深度
    传入参数：当前结点名node(字符串),当前结点深度depth(整数)
    传出参数：无
    """
    def _CalDepth(self,node,depth):
        self._huffmanTree[node].append(depth)#将当前结点的深度记录至哈夫曼树字典中
        if len(self._huffmanTree[node][1])>0:#若当前结点有后继
            #在其后继结点上递归调用此函数
            self._CalDepth(self._huffmanTree[node][1][0],depth+1)
            self._CalDepth(self._huffmanTree[node][1][1],depth+1)
    """
    函数：CountFrqt(self)
    功能：计算原字符串中每个字符的关键值
    传入参数：无
    传出参数：无
    """
    def CountFrqt(self):
        for ch in self._srcString:
            if ch not in self._countFrqt:
                self._countFrqt[ch]=1
            else:
                self._countFrqt[ch]+=1
        self._leafNum=len(self._countFrqt)
    """
    函数：SetFrqt(self,frqt)
    功能：设定关键值表
    传入参数：关键值表frqt(字典),格式:key=字符名或关键值代号(字符串),value=关键值(整数)
    传出参数：无
    """
    def SetFrqt(self,frqt):
        self._countFrqt=frqt
    """
    函数：GenerateTree(self)
    功能：生成哈夫曼树
    传入参数：无
    传出参数：哈夫曼树self._huffmanTree(字典),哈夫曼树树根self._root(字符串),哈夫曼树非叶子结点数目self._rootNum(整数),哈夫曼树叶子结点数目self._leafNum(整数)
    """
    def GenerateTree(self):
        buf=deepcopy(self._countFrqt)#先将关键值表拷贝至buf
        #当buf中还有2个以上的结点时
        while len(buf)>1:
            #从buf中取出关键值最小的两个结点
            min1_key=min(buf,key=buf.get)
            min1_frqt=buf[min1_key]
            buf.pop(min1_key)
            min2_key=min(buf,key=buf.get)
            min2_frqt=buf[min2_key]
            buf.pop(min2_key)
            #生成这两个结点的根结点
            root_key='h'+str(self._rootNum)
            self._rootNum+=1
            root_frqt=min1_frqt+min2_frqt
            buf[root_key]=root_frqt
            #将左右儿子结点加入到哈夫曼树中,或更新儿子结点的前驱结点
            if min1_key not in self._huffmanTree:
                self._huffmanTree[min1_key]=[min1_frqt,[],root_key]
            else:
                self._huffmanTree[min1_key][2]=root_key
            if min2_key not in self._huffmanTree:
                self._huffmanTree[min2_key]=[min2_frqt,[],root_key]
            else:
                self._huffmanTree[min2_key][2]=root_key
            #将根结点加入到哈夫曼树中
            self._huffmanTree[root_key]=[root_frqt,[min1_key,min2_key],0]
        #buf中剩余的最后一个结点就是哈夫曼树的根结点    
        self._root=buf.popitem()[0]
        #从根结点开始先序遍历哈夫曼树,计算各个结点的深度
        self._CalDepth(self._root, 0)
        return self._huffmanTree,self._root,self._rootNum,self._leafNum
    """
    函数：_coden(self,node,curcode)
    功能：计算哈夫曼编码的递归函数
    传入参数：当前结点node(字符串),当前哈夫曼编码(curcode)
    传出参数：无
    """
    def _coden(self,node,curcode):
        #如果当前结点是叶子结点
        if len(self._huffmanTree[node][1])==0:
            self._code[node]=curcode#将当前哈夫曼编码存入编码表
        else:#否则递归地在当前结点的左右儿子结点上调用次函数
            self._coden(self._huffmanTree[node][1][0],curcode+'0')#进入左儿子新增编码0
            self._coden(self._huffmanTree[node][1][1],curcode+'1')#进入右儿子新增编码1
    """
    函数：Coden(self)
    功能：计算哈夫曼编码的入口函数
    传入参数：无
    传出参数：哈夫曼编码表self._code(字典)
    """
    def Coden(self):
        #从根结点开始编码,初始编码为''
        self._coden(self._root,'')
        return self._code
    """
    函数： _print(self,node)
    功能：中序遍历哈夫曼树,在控制台中打印哈夫曼树
    传入参数：当前节点node(字符串)
    传出参数：无
    """
    def _print(self,node):
        #若当前结点是叶子结点
        if len(self._huffmanTree[node][1])==0:
            print('\t\t'*self._huffmanTree[node][3]+node+':'+str(self._huffmanTree[node][2])+'deep:'+str(self._huffmanTree[node][3]))
        else:#否则在左儿子结点上递归地调用此函数,打印当前结点,在右儿子结点上递归地调用此函数
            self._print(self._huffmanTree[node][1][0])
            print('\t\t'*self._huffmanTree[node][3]+node+':'+str(self._huffmanTree[node][2])+'deep:'+str(self._huffmanTree[node][3]))
            self._print(self._huffmanTree[node][1][1])
    """
    函数：PrintTree(self)
    功能：打印哈夫曼树的入口函数
    传入参数：无
    传出参数：无
    """       
    def PrintTree(self):
        if self._root=='':
            self.GenerateTree()
        self._print(self._root)
"""
该模块的测试代码
"""       
if __name__=='__main__':
    test="132"
    huf=huffman(test)
    huf.CountFrqt()
    hufTree,root,rootnum,leafnum=huf.GenerateTree()
    huf.PrintTree()
    code=huf.Coden()
    print(code)
    print(hufTree)