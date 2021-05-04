# -*- coding: utf-8 -*-
"""
Created on Sat Aug 22 16:45:47 2020

@author: 孔令百

Name:main.py

Desctiption:该模块实现了UI界面相关功能,哈夫曼树的绘制和前后端的对接
"""
import sys
import xlwt
from PyQt5.QtWidgets import QApplication,QMessageBox,QWidget,QTableWidgetItem,QFileDialog,QInputDialog
from PyQt5.QtGui import QPainter,QIcon,QPixmap
from PyQt5.QtCore import QPoint,Qt
from PyQt5.uic import loadUi
from huffmantree import huffman
from calculate import CalCoordinate,GenRandomText,ReadFile
"""
类:哈夫曼树窗口
功能:在控件中绘制哈夫曼树
"""
class TreeWindow(QWidget):
    """
    函数：__init__(self)
    功能：哈夫曼树窗口构造函数,初始化相关参数
    传入参数：无
    传出参数：无
    """
    def __init__(self):
        super().__init__()#父类Widget初始化
        self.coordinate={}#各个结点坐标
        self.tree={}#哈夫曼树字典
        self.root=''#根结点
        self.x=0#绘图窗口宽
        self.y=0#绘图窗口高
        
        self.d=50#结点直径
        self.isdraw=False#开始绘图标志,初始为假
    """
    函数：paintEvent(self,event)
    功能：绘图事件函数
    传入参数：event
    传出参数：无
    """ 
    def paintEvent(self,event):
        if self.isdraw:#当绘图标志为真时
            qp=QPainter(self)#绘图对象
            qp.begin(self)
            self.setMinimumSize(self.x, self.y)#设定绘图窗口大小
            self.draw(qp)#绘图
            qp.end()
    """
    函数：_drawNode(self,qp,node)
    功能：绘制各个结点
    传入参数：绘图对象qp(QPainter),当前结点node(字符串)
    传出参数：无
    """
    def _drawNode(self,qp,node):
        #绘制当前结点的圆
        qp.drawEllipse(self.coordinate[node][0],self.coordinate[node][1],self.d,self.d)
        #将当前结点的关键值标记在原旁边
        qp.drawText(self.coordinate[node][0],self.coordinate[node][1],str(self.tree[node][0]))
        #如果当前结点有儿子结点
        if len(self.tree[node][1])>0:
            #绘制当前结点与儿子结点之间的连接线
            qp.drawLine(QPoint(self.coordinate[node][0]+self.d/2,self.coordinate[node][1]+self.d), QPoint(self.coordinate[self.tree[node][1][0]][0]+self.d/2,self.coordinate[self.tree[node][1][0]][1]))
            qp.drawLine(QPoint(self.coordinate[node][0]+self.d/2,self.coordinate[node][1]+self.d), QPoint(self.coordinate[self.tree[node][1][1]][0]+self.d/2,self.coordinate[self.tree[node][1][1]][1]))
            #递归地在左右儿子上调用此函数
            self._drawNode(qp,self.tree[node][1][0])
            self._drawNode(qp,self.tree[node][1][1])
        else:#如果当前结点是叶子结点
            if len(node)>1:#当前结点名长度大于1,说明当前结点是通过关键值方式加入的,结点圆名称设定为"关键值"
                s="关键值"
            else:#否则,说明当前结点是通过文本方式加入的,结点圆名称就是结点名
                s=node
            #计算结点圆标记文本尺寸
            metrics=qp.fontMetrics()
            width=metrics.width(s)
            height=metrics.height()
            #在结点圆上写出结点圆名称
            qp.drawText(self.coordinate[node][0]+self.d/2-width/2,self.coordinate[node][1]+self.d/2+height/2,s)
    """
    函数：draw(self,qp)
    功能：绘制哈夫曼树的入口函数
    传入参数：绘图工具qp(QPainter)
    传出参数：无
    """
    def draw(self,qp):
        #从根结点开始调用递归函数
        self._drawNode(qp,self.root)
"""
类:程序主类
功能:完成UI界面的设定和前后端的对接
"""        
class Main:
    """
    函数：__init__(self)
    功能：构造函数,设定UI界面对接前后端
    传入参数：无
    传出参数：无
    """
    def __init__(self):
        #加载UI文件
        self.ui=loadUi("mainUI.ui")
        #设定窗口标题
        self.ui.setWindowTitle("哈夫曼树、编码")
        #设定程序图标
        self.ui.setWindowIcon(QIcon("static/logo.ico"))
        #初始化绘图窗口
        self.treew=TreeWindow()
        #将绘图窗口放入主窗口的scrollArea_tree中
        self.ui.scrollArea_tree.setWidget(self.treew)
        #设定主窗口的comboBox_random
        self.ui.comboBox_random.addItems(["随机数字","随机字母","随机字符","随机中文"])
        
        #将窗口信号挂载到函数
        self.ui.pushButton_run.clicked.connect(self.run)
        self.ui.pushButton_random.clicked.connect(self.random)
        self.ui.pushButton_selectfile.clicked.connect(self.file)
        self.ui.pushButton_tree_save.clicked.connect(self.savetree)
        self.ui.pushButton_table_save.clicked.connect(self.savetable)
        self.ui.plainTextEdit_input.textChanged.connect(self.inputchange)
        self.ui.pushButton_add.clicked.connect(self.add)
        self.ui.pushButton_delete.clicked.connect(self.delete)
        self.ui.pushButton_change.clicked.connect(self.change)
        self.ui.pushButton_reset.clicked.connect(self.reset)
        self.ui.pushButton_run2.clicked.connect(self.run2)
        
        self.code={}#哈夫曼编码表
    """
    函数：run(self)
    功能：基于输入的文本内容运行哈夫曼算法并显示结果
    传入参数：无
    传出参数：无
    """
    def run(self):
        #执行哈夫曼算法
        huf=huffman(self.ui.plainTextEdit_input.toPlainText())
        huf.CountFrqt()
        self.treew.tree,self.treew.root,rootnum,leafnum=huf.GenerateTree()
        self.treew.coordinate,self.treew.x,self.treew.y=CalCoordinate(self.treew.tree,self.treew.root,rootnum,leafnum)
        self.code=huf.Coden()
        #绘制哈夫曼树
        if self.treew.x<=32767 and self.treew.y<=32767:
            self.treew.isdraw=True
            self.treew.update()
            self.ui.pushButton_tree_save.setEnabled(True)
        else:
            self.treew.isdraw=False
            self.ui.pushButton_tree_save.setEnabled(False)
        #显示哈夫曼编码
        self.ui.tableWidget.setRowCount(len(self.code))
        row=0
        for node in self.code:
            item=QTableWidgetItem()
            item.setText(node)
            self.ui.tableWidget.setItem(row,0,item)
            item=QTableWidgetItem()
            item.setText(self.code[node])
            self.ui.tableWidget.setItem(row,1,item)
            row+=1
    """
    函数：random(self)
    功能：生成指定类型的随机字符串到文本框
    传入参数：无
    传出参数：无
    """    
    def random(self):
        #获得指定的字符串类型与长度
        choice=self.ui.comboBox_random.currentText()
        length=self.ui.spinBox_random.value()
        text=GenRandomText(choice,length)
        #将随机字符串输入文本框
        self.ui.plainTextEdit_input.setPlainText(text)
    """
    函数：file(self)
    功能：打开TXT文本文件,读取内容到文本框
    传入参数：无
    传出参数：无
    """
    def file(self):
        filename=QFileDialog.getOpenFileName(None,'选择文件','./',".TXT(*.txt)")
        if filename[0]!="":#判断是否选定了文件
            #print(filename)
            self.ui.lineEdit_filename.setText(filename[0])#将文件路径和文件名显示到文本框
            content=ReadFile(filename[0])
            if len(content)==0:#当读取文件内容为空时输出提示信息
                msg=QMessageBox(QMessageBox.Warning,"警告","文件打开失败或文件为空文件")
                msg.exec()
            else:#否则将文本内容写入到文本框中
                self.ui.plainTextEdit_input.setPlainText(content)
    """
    函数：savetree(self)
    功能：保存绘图区的哈夫曼树为图片
    传入参数：无
    传出参数：无
    """
    def savetree(self):
        filename=QFileDialog.getSaveFileName(None,'保存哈夫曼树','./',".JPG(*.jpg);;.PNG(*.png);;.TIFF(*.tiff);;.BMP(*.bmp)")
        if filename[0]!="":#判断是否选定了文件
            #导出绘图窗口图片
            pixmap=QPixmap(self.treew.size())
            self.treew.render(pixmap)
            #根据选中的图片格式保存图片
            if filename[1]==".JPG(*.jpg)":
                pixmap.save(filename[0],"jpg",100)
            elif filename[1]==".PNG(*.png)":
                pixmap.save(filename[0],"png",100)
            elif filename[1]==".TIFF(*.tiff)":
                pixmap.save(filename[0],"tiff",100)
            elif filename[1]==".BMP(*.bmp)":
                pixmap.save(filename[0],"bmp",100)
    """
    函数：savetable(self)
    功能：保存哈夫曼编码表为表格
    传入参数：无
    传出参数：无
    """
    def savetable(self):
        filename=QFileDialog.getSaveFileName(None,'保存哈夫曼码','./',".XLS(*.xls)")
        if filename[0]!="":#判断是否选定了文件
            #将哈夫曼表写入到excel表格中
            workbook=xlwt.Workbook(encoding="utf-8")
            worksheet=workbook.add_sheet("哈夫曼编码表")
            worksheet.write(0,0,"文字")
            worksheet.write(0,1,"哈夫曼码")
            row=1
            for node in self.code:
                worksheet.write(row,0,node)
                worksheet.write(row,1,self.code[node])
                row+=1
            #保存该excel表格
            workbook.save(filename[0])
    """
    函数：inputchange(self)
    功能：判断文本框内容是否可运行
    传入参数：无
    传出参数：无
    """
    def inputchange(self):
        #当文本框内容多于两种字符时开放运行按钮
        tmp=[]
        text=self.ui.plainTextEdit_input.toPlainText()
        for c in text:
            if c not in tmp:
                tmp.append(c)
        if len(tmp)>=2:
            self.ui.pushButton_run.setEnabled(True)
        else:
            self.ui.pushButton_run.setEnabled(False)
    """
    函数：add(self)
    功能：新增关键值
    传入参数：无
    传出参数：无
    """
    def add(self):
        #通过对话框获取关键值
        num,ok=QInputDialog.getInt(self.ui,"输入框","输入关键值",1,1,65535,1,Qt.WindowCloseButtonHint)
        if ok:#获取成功时向表格新增一个单元格存放该关键值
            item=QTableWidgetItem()
            item.setText(str(num))
            row=self.ui.tableWidget_input.rowCount()+1
            self.ui.tableWidget_input.setRowCount(row)
            self.ui.tableWidget_input.setItem(row-1,0,item)
        #当表格中多余两个关键值时开放运行按钮
        if self.ui.tableWidget_input.rowCount()>=2:
            self.ui.pushButton_run2.setEnabled(True)
        else:
            self.ui.pushButton_run2.setEnabled(False)
    """
    函数：delete(self)
    功能：删除关键值
    传入参数：无
    传出参数：无
    """
    def delete(self):
        #获取当前选中单元格的位置
        row=self.ui.tableWidget_input.currentRow()
        #删除该单元格
        self.ui.tableWidget_input.removeRow(row)
        #当表格中多余两个关键值时开放运行按钮
        if self.ui.tableWidget_input.rowCount()>=2:
            self.ui.pushButton_run2.setEnabled(True)
        else:
            self.ui.pushButton_run2.setEnabled(False)
    """
    函数：change(self)
    功能：更改关键值
    传入参数：无
    传出参数：无
    """
    def change(self):
        #获取当前选中单元格的位置
        row=self.ui.tableWidget_input.currentRow()
        if row>=0:#如果当前选中单元格位置合法
            #通过对话框获取关键值
            num,ok=QInputDialog.getInt(self.ui,"输入框","输入关键值",1,1,65535,1,Qt.WindowCloseButtonHint)
            if ok:#获取成功时将关键值写入该单元格
                item=QTableWidgetItem()
                item.setText(str(num))
                self.ui.tableWidget_input.setItem(row,0,item)
    """
    函数：reset(self)
    功能：重置关键值表
    传入参数：无
    传出参数：无
    """
    def reset(self):
        #依次删除各个单元格
        row=self.ui.tableWidget_input.rowCount()
        for i in range(row):
             self.ui.tableWidget_input.removeRow(0)
        #禁用运行按钮
        self.ui.pushButton_run2.setEnabled(False)
    """
    函数：run2(self)
    功能：基于关键值表运行哈夫曼算法并显示结果
    传入参数：无
    传出参数：无
    """
    def run2(self):
        #将关键值表中的内容转化为字典数据
        frqt={}
        row=self.ui.tableWidget_input.rowCount()
        for i in range(row):
            cnum=self.ui.tableWidget_input.item(i,0).text()
            frqt['('+str(i)+"号关键值:"+cnum+')']=int(cnum)
        #运行哈夫曼算法
        huf=huffman("")
        huf.SetFrqt(frqt)
        self.treew.tree,self.treew.root,rootnum,leafnum=huf.GenerateTree()
        self.treew.coordinate,self.treew.x,self.treew.y=CalCoordinate(self.treew.tree,self.treew.root,rootnum,leafnum)
        self.code=huf.Coden()
        #绘制哈夫曼树
        if self.treew.x<=32767 and self.treew.y<=32767:
            self.treew.isdraw=True
            self.treew.update()
            self.ui.pushButton_tree_save.setEnabled(True)
        else:
            self.treew.isdraw=False
            self.ui.pushButton_tree_save.setEnabled(False)
        #显示哈夫曼编码
        self.ui.tableWidget.setRowCount(len(self.code))
        row=0
        for node in self.code:
            item=QTableWidgetItem()
            item.setText(node)
            self.ui.tableWidget.setItem(row,0,item)
            item=QTableWidgetItem()
            item.setText(self.code[node])
            self.ui.tableWidget.setItem(row,1,item)
            row+=1
if __name__=="__main__":
    app=QApplication(sys.argv)#初始化应用程序
    m=Main()#构建主对象
    m.ui.show()#显示主窗口
    app.exec_()#退出应用程序