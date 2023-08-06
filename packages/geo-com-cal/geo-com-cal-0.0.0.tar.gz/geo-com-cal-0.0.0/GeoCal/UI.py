# This Python file uses the following encoding: gbk
import os
import math

from PySide2 import QtWidgets
from PySide2.QtCore import QFile,QRegExp,QObject,Qt
from PySide2.QtWidgets import *
from PySide2.QtUiTools import QUiLoader
from PySide2.QtGui import QDoubleValidator, QRegExpValidator,QIcon
from decimal import Decimal
from . import images
from .RollLabel import RollLabel
from .Geo import Geo


#singleton-class
class UI(QWidget):
    #单例标识
    __instance_UI_1 = None
    def __new__(cls, *args, **kwargs):
        if cls.__instance_UI_1 is None:
            cls.__instance_UI_1 = QWidget.__new__(cls)
            pass
        return  cls.__instance_UI_1

    def __init__(self):
        super(UI, self).__init__()
        ico=QIcon(":/geo.ico")
        self.setWindowIcon(ico)
        self.setWindowFlags(self.windowFlags()&~Qt.WindowMaximizeButtonHint)
        #计算时采用的椭球相关信息列表记录
        self.eList=[None,None,None,None,None,None]
        #计算类成员
        self.geo=None
        #ui
        self.ui=None
        #样式
        self.qss=None
        self.load_ui()
        #居中显示
        deskRect=QApplication.desktop().availableGeometry()
        self.move((deskRect.width()-self.ui.width())/2, (deskRect.height()-self.ui.height())/2)
        self.setFixedSize(self.ui.width(),self.ui.height())
        #加控件
        temp="""      警告：高斯投影正反算需用到子午线弧长X及垂足纬度Bf，对于三个已知椭球，计算X及Bf时使用的是带值公式，如此高斯投影的计算结果精度达到0.001m，对于未记录的椭球"""
        temp+=""",参数X及Bf是根据传统的展开至10次幂的子午线弧长公式来计算，这使得高斯投影误差在恶劣情况下可至个位数"""
        rl=RollLabel(temp,self.ui)
        rl.move(140,175)
        rl.resize(520,20)
        rl.setObjectName("warning")
        rl.setToolTip(temp)
        # 加载QSS
        self.load_qss()
        #设置表头标签
        self.ui.tableWidget1.setColumnCount(3)
        labels=["L","B","H"]
        self.ui.tableWidget1.setHorizontalHeaderLabels(labels)
        self.ui.tableWidget1.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.ui.tableWidget2.setColumnCount(3)
        labels=["X","Y","Z"]
        self.ui.tableWidget2.setHorizontalHeaderLabels(labels)
        self.ui.tableWidget2.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.ui.tableWidget3.setColumnCount(3)
        labels=["X","Y","Z"]
        self.ui.tableWidget3.setHorizontalHeaderLabels(labels)
        self.ui.tableWidget3.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.ui.tableWidget4.setColumnCount(3)
        labels=["L","B","H"]
        self.ui.tableWidget4.setHorizontalHeaderLabels(labels)
        self.ui.tableWidget4.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.ui.tableWidget5.setColumnCount(2)
        labels=["L","B"]
        self.ui.tableWidget5.setHorizontalHeaderLabels(labels)
        self.ui.tableWidget5.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.ui.tableWidget6.setColumnCount(3)
        labels=["x","y","y假定"]
        self.ui.tableWidget6.setHorizontalHeaderLabels(labels)
        self.ui.tableWidget6.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.ui.tableWidget7.setColumnCount(3)
        labels=["x","y","y假定"]
        self.ui.tableWidget7.setHorizontalHeaderLabels(labels)
        self.ui.tableWidget7.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.ui.tableWidget8.setColumnCount(2)
        labels=["L","B"]
        self.ui.tableWidget8.setHorizontalHeaderLabels(labels)
        self.ui.tableWidget8.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.ui.tableWidget9.setColumnCount(4)
        labels=["L1","B1","S","A1"]
        self.ui.tableWidget9.setHorizontalHeaderLabels(labels)
        self.ui.tableWidget9.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.ui.tableWidget10.setColumnCount(3)
        labels=["L2","B2","A2"]
        self.ui.tableWidget10.setHorizontalHeaderLabels(labels)
        self.ui.tableWidget10.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.ui.tableWidget11.setColumnCount(4)
        labels=["L1","B1","L2","B2"]
        self.ui.tableWidget11.setHorizontalHeaderLabels(labels)
        self.ui.tableWidget11.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.ui.tableWidget12.setColumnCount(3)
        labels=["S","A1","A2"]
        self.ui.tableWidget12.setHorizontalHeaderLabels(labels)
        self.ui.tableWidget12.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        #进度条初始化不可视
        self.ui.progressBar.setVisible(False)
        self.ui.progressLabel.setText("")

        self.ui.d6Label.setVisible(False)
        self.ui.radioButton2.setVisible(False)

        #限制输入
        #浮点数
        rx = QRegExp("^(6378)\d{3,3}(\.\d+)$?")
        lValidator = QRegExpValidator(rx, self.ui)
        self.ui.longLEdit.setValidator(lValidator)
        rx = QRegExp("^(0\.003352)\d{0,8}$")
        oValidator = QRegExpValidator(rx, self.ui)
        self.ui.oblatenessLEdit.setValidator(oValidator)

        #x y z
        #3小数点浮点数
        dValidator=QDoubleValidator()
        dValidator.setDecimals(3)
        self.ui.x2LEdit.setValidator(dValidator)
        self.ui.y2LEdit.setValidator(dValidator)
        self.ui.z2LEdit.setValidator(dValidator)

        #已知
        #L
        rx = QRegExp("(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))°(\d|[0-5]\d)′(\d|[0-5]\d)(\.[0-9]{1,3})?″")
        lValidator = QRegExpValidator(rx, self.ui)
        self.ui.l1LEdit.setValidator(lValidator)
        self.ui.l3LEdit.setValidator(lValidator)
        self.ui.gl1LEdit1.setValidator(lValidator)
        self.ui.gl1LEdit2.setValidator(lValidator)
        self.ui.gl2LEdit2.setValidator(lValidator)
        #方位角
        self.ui.ga1LEdit1.setValidator(lValidator)
        #B
        rx = QRegExp("(-)?(\d|[1-9]\d|(1[0-7]\d|180))°(\d|[0-5]\d)′(\d|[0-5]\d)(\.[0-9]{1,3})?″")
        bValidator = QRegExpValidator(rx, self.ui)
        self.ui.b3LEdit.setValidator(bValidator)
        self.ui.b1LEdit.setValidator(bValidator)
        self.ui.gb1LEdit1.setValidator(bValidator)
        self.ui.gb1LEdit2.setValidator(bValidator)
        self.ui.gb2LEdit2.setValidator(bValidator)
        #h
        self.ui.h1LEdit.setValidator(dValidator)
        #x y y假定
        #y可以为负数
        self.ui.y4LEdit.setValidator(dValidator)

        dpValidator=QDoubleValidator()
        dpValidator.setRange(0,math.pow(2,31),3)
        self.ui.x4LEdit.setValidator(dpValidator)
        self.ui.yf4LEdit.setValidator(dpValidator)
        self.ui.gsLEdit1.setValidator(dpValidator)


        #实例化计算类
        self.geo=Geo()
        #初始化数据
        self.updateEllipsoidParameter()
        #连接信号
        self.ui.ellipsoidCBox.activated[str].connect(self.selectEllipsoid)
        self.ui.longLEdit.editingFinished.connect(self.customCalculation)
        self.ui.oblatenessLEdit.editingFinished.connect(self.customCalculation)

        self.ui.calCBox.activated[int].connect(self.calTypeChanged)
        self.ui.radioButton.toggled.connect(self.batHandleChanged)
        self.ui.l1LEdit.textEdited.connect(self.lbhCompletiuon)
        self.ui.b1LEdit.textEdited.connect(self.lbhCompletiuon)
        self.ui.l3LEdit.textEdited.connect(self.lbhCompletiuon)
        self.ui.b3LEdit.textEdited.connect(self.lbhCompletiuon)
        self.ui.gb1LEdit1.textEdited.connect(self.lbhCompletiuon)
        self.ui.gl1LEdit1.textEdited.connect(self.lbhCompletiuon)
        self.ui.ga1LEdit1.textEdited.connect(self.lbhCompletiuon)
        self.ui.gl1LEdit2.textEdited.connect(self.lbhCompletiuon)
        self.ui.gb1LEdit2.textEdited.connect(self.lbhCompletiuon)
        self.ui.gl2LEdit2.textEdited.connect(self.lbhCompletiuon)
        self.ui.gb2LEdit2.textEdited.connect(self.lbhCompletiuon)

        self.ui.calBtn.clicked.connect(self.calBtnClicked)

        self.ui.radioButton.toggled.emit(self.ui.radioButton.isChecked())

        self.ui.importBtn1.clicked.connect(self.importData)
        self.ui.saveBtn1.clicked.connect(self.exportData)
        self.ui.importBtn2.clicked.connect(self.importData)
        self.ui.saveBtn2.clicked.connect(self.exportData)
        self.ui.importBtn3.clicked.connect(self.importData)
        self.ui.saveBtn3.clicked.connect(self.exportData)
        self.ui.importBtn4.clicked.connect(self.importData)
        self.ui.saveBtn4.clicked.connect(self.exportData)
        self.ui.importBtn5.clicked.connect(self.importData)
        self.ui.saveBtn5.clicked.connect(self.exportData)
        self.ui.importBtn6.clicked.connect(self.importData)
        self.ui.saveBtn6.clicked.connect(self.exportData)

        pass

    def load_ui(self):
        self.setWindowTitle("大地测量综合计算")
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui=loader.load(ui_file, self)
        ui_file.close()
        pass

    def load_qss(self):
        # 加载QSS
        path= os.path.join(os.path.dirname(__file__), "QSS/task_ui.qss")
        with open(path, "r",encoding='gbk') as qs:
            self.qss=qs.read()
            self.setStyleSheet(self.qss)
            pass
        pass

    #更新参数
    def updateEllipsoidParameter(self):
        self.ui.longLEdit.setText(str(self.geo.a))
        self.ui.shortLEdit.setText(str(self.geo.b))
        self.ui.curLEdit.setText(str(self.geo.c))
        self.ui.oblatenessLEdit.setText(str(self.geo.f))
        self.ui.fEccentricityLEdit.setText(str(self.geo.e1))
        self.ui.sEccentricityLEdit.setText(str(self.geo.e2))
        if(self.ui.longLEdit.isEnabled()==False):
            self.ui.longLEdit.setCursorPosition(0)
            self.ui.shortLEdit.setCursorPosition(0)
            pass
        self.ui.curLEdit.setCursorPosition(0)
        self.ui.oblatenessLEdit.setCursorPosition(0)
        self.ui.fEccentricityLEdit.setCursorPosition(0)
        self.ui.sEccentricityLEdit.setCursorPosition(0)
        pass


    #大地坐标与大地空间坐标正算
    #参数：°′″格式的L B 以及H
    #返回 X Y Z
    def geoToGeoSpatial(self,L,B,H):
        #l度数转弧度
        list=L.split("°")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("′")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("″")
                m=list[0]
                pass

            pass

        #度数转弧度
        L=self.geo.degToRad(d,f,m)
        #b度数转弧度
        list=B.split("°")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("′")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("″")
                m=list[0]
                pass

            pass
        #度数转弧度
        B=self.geo.degToRad(d,f,m)
        return self.geo.geoAndGeoSpatialCal(L,B,H)


    #单例大地坐标与大地空间坐标正算
    def singleGeoToGeoSpatialCal(self):
        L=self.ui.l1LEdit.text()
        B=self.ui.b1LEdit.text()
        H=self.ui.h1LEdit.text()
        rx=QRegExp(".+(°|′|″)$")
        i=rx.indexIn(L)
        if not L.strip() or not B.strip() or not H.strip():
            tip="信息：数据没有输入\n\r"
            QMessageBox.information(self.ui,
            self.tr("提示"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        if i==-1:
            tip="提示：大地经度可能是错误的!\n\r值："+L
            QMessageBox.critical(self.ui,
            self.tr("错误"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(B)
        if i==-1:
            tip="提示：大地纬度可能是错误的!\n\r值："+B
            QMessageBox.critical(self.ui,
            self.tr("错误"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        (X,Y,Z)=self.geoToGeoSpatial(L,B,H)
        self.ui.x1LEdit.setText(str(X.quantize(Decimal("1.0000"))))
        self.ui.y1LEdit.setText(str(Y.quantize(Decimal("1.0000"))))
        self.ui.z1LEdit.setText(str(Z.quantize(Decimal("1.0000"))))
        pass

    #批量大地坐标与大地空间坐标正算
    def batGeoToGeoSpatialCal(self):
        sum=self.ui.tableWidget1.rowCount()
        if sum<1:
            return
        i=0
        self.ui.progressBar.setVisible(True)
        self.ui.progressLabel.setText("进度：")
        self.ui.progressBar.setValue(i)
        self.ui.tableWidget2.setRowCount(sum)
        self.eList[0]=self.ui.ellipsoidCBox.currentText()+"    椭球参数(a="+str(self.geo.a)+"m,"+"f="+str(self.geo.f)+")"
        while i<sum:
            L=self.ui.tableWidget1.item(i,0).text()
            B=self.ui.tableWidget1.item(i,1).text()
            H=self.ui.tableWidget1.item(i,2).text()
            (X,Y,Z)=self.geoToGeoSpatial(L,B,H)
            item=QTableWidgetItem(str(X.quantize(Decimal("1.0000"))))
            flags=item.flags()
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget2.setItem(i,0,item)
            item=QTableWidgetItem(str(Y.quantize(Decimal("1.0000"))))
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget2.setItem(i,1,item)
            item=QTableWidgetItem(str(Z.quantize(Decimal("1.0000"))))
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget2.setItem(i,2,item)
            i+=1
            self.ui.progressBar.setValue(i/sum*100)
            pass
        self.ui.progressBar.setVisible(False)
        self.ui.progressLabel.setText("")
        pass

    #大地坐标与大地空间坐标反算
    #参数：X Y Z
    #返回 L B（浮点数度数） H decimal类型
    def invertedGeoToGeoSpatial(self,X,Y,Z):
        return self.geo.geoAndGeoSpatialInvertedCal(X,Y,Z)

    #单例大地与空间直角反算
    def singleInvertedGeoToGeoSpatialCal(self):
        X=self.ui.x2LEdit.text()
        Y=self.ui.y2LEdit.text()
        Z=self.ui.z2LEdit.text()
        if not X.strip() or not Y.strip() or not Z.strip():
            tip="信息：数据没有输入\n\r"
            QMessageBox.information(self.ui,
            self.tr("提示"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        (L,B,H)=self.invertedGeoToGeoSpatial(X,Y,Z)
        (d,m,s)=self.geo.deg_60(L)
        s=s.quantize(Decimal("1.0000"))
        if m<10:
            m="0"+str(m)
            pass
        if s<10:
            s="0"+str(s)
            pass
        L=str(d)+"°"+str(m)+"′"+str(s)+"″"
        (d,m,s)=self.geo.deg_60(B)
        s=s.quantize(Decimal("1.0000"))
        if m<10:
            m="0"+str(m)
            pass
        if s<10:
            s="0"+str(s)
            pass
        B=str(d)+"°"+str(m)+"′"+str(s)+"″"
        self.ui.l2LEdit.setText(L)
        self.ui.b2LEdit.setText(B)
        self.ui.h2LEdit.setText(str(H.quantize(Decimal("1.0000"))))
        pass

    #批量大地与空间直角反算
    def batInvertedGeoToGeoSpatialCal(self):
        sum=self.ui.tableWidget3.rowCount()
        if sum<1:
            return
        i=0
        self.ui.progressBar.setValue(i)
        self.ui.progressBar.setVisible(True)
        self.ui.progressLabel.setText("进度：")
        self.ui.tableWidget4.setRowCount(sum)
        self.eList[1]=self.ui.ellipsoidCBox.currentText()+"    椭球参数(a="+str(self.geo.a)+"m,"+"f="+str(self.geo.f)+")"
        while i<sum:
            X=self.ui.tableWidget3.item(i,0).text()
            Y=self.ui.tableWidget3.item(i,1).text()
            Z=self.ui.tableWidget3.item(i,2).text()
            (L,B,H)=self.invertedGeoToGeoSpatial(X,Y,Z)
            (d,m,s)=self.geo.deg_60(L)
            s=s.quantize(Decimal("1.0000"))
            if m<10:
                m="0"+str(m)
                pass
            if s<10:
                s="0"+str(s)
                pass
            L=str(d)+"°"+str(m)+"′"+str(s)+"″"
            (d,m,s)=self.geo.deg_60(B)
            s=s.quantize(Decimal("1.0000"))
            if m<10:
                m="0"+str(m)
                pass
            if s<10:
                s="0"+str(s)
                pass
            B=str(d)+"°"+str(m)+"′"+str(s)+"″"
            item=QTableWidgetItem(L)
            flags=item.flags()
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget4.setItem(i,0,item)
            item=QTableWidgetItem(B)
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget4.setItem(i,1,item)
            item=QTableWidgetItem(str(H.quantize(Decimal("1.0000"))))
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget4.setItem(i,2,item)
            i+=1
            self.ui.progressBar.setValue(i/sum*100)
            pass

        self.ui.progressBar.setVisible(False)
        self.ui.progressLabel.setText("")
        pass

    #高斯投影正算
    #参数 L B（度分秒） d3（bool型 true为3度带） X 数值型 用来指定公式计算子午线弧长(0代表自定义椭球，用展开10次幂的多项式公式 其精度低，1 2 3分别代表求弧长使用了对应椭球列表的数值公式，精度可靠)
    #返回 x y yf（y假定）
    def geoToGuass(self,L,B,d3,X):
        #l度数转弧度
        list=L.split("°")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("′")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("″")
                m=list[0]
                pass

            pass

        #度数转弧度
        L=self.geo.degToRad(d,f,m)
        #b度数转弧度
        list=B.split("°")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("′")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("″")
                m=list[0]
                pass

            pass
        #度数转弧度
        B=self.geo.degToRad(d,f,m)
        if X:
            X=self.geo.getX3(B,X-1)
            pass
        else:
            X=self.geo.getX(B)
            pass
        return self.geo.geoAndGuassCal(L,B,d3,X)

    #单例高斯投影正算
    #参数：X 数值型 用来指定公式计算子午线弧长(0代表自定义椭球，用展开10次幂的多项式公式，1 2 3分别代表求弧长使用了对应椭球列表的数值公式，精度可靠)
    def singleGeoToGuassCal(self,X):
        L=self.ui.l3LEdit.text()
        B=self.ui.b3LEdit.text()
        rx=QRegExp(".+(°|′|″)$")
        i=rx.indexIn(L)
        if not L.strip() or not B.strip():
            tip="信息：数据没有输入\n\r"
            QMessageBox.information(self.ui,
            self.tr("提示"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        if i==-1:
            tip="提示：大地经度可能是错误的!\n\r值："+L
            QMessageBox.critical(self.ui,
            self.tr("错误"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(B)
        if i==-1:
            tip="提示：大地纬度可能是错误的!\n\r值："+B
            QMessageBox.critical(self.ui,
            self.tr("错误"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        (x,y,yf)=self.geoToGuass(L,B,not self.ui.radioButton2.isChecked(),X)
        self.ui.x3LEdit.setText(str(x.quantize(Decimal("1.000"))))
        self.ui.y3LEdit.setText(str(y.quantize(Decimal("1.000"))))
        self.ui.y3fLEdit.setText(str(yf.quantize(Decimal("1.000"))))
        pass

    #批量高斯投影正算
    #参数X 数值型 用来指定公式计算子午线弧长(0代表自定义椭球，用展开10次幂的多项式公式，1 2 3分别代表求弧长使用了对应椭球列表的数值公式，精度可靠)
    def batGeoToGuassCal(self,X):
        sum=self.ui.tableWidget5.rowCount()
        if sum<1:
            return
        i=0
        d3=not self.ui.radioButton2.isChecked()
        self.ui.progressBar.setValue(i)
        self.ui.progressLabel.setText("进度：")
        self.ui.progressBar.setVisible(True)
        self.ui.tableWidget6.setRowCount(sum)
        temp=self.ui.ellipsoidCBox.currentText()+"    椭球参数(a="+str(self.geo.a)+"m,"+"f="+str(self.geo.f)+")"
        if self.ui.radioButton2.isChecked():
            temp+=",投影分带：6°带"
            pass
        else:
            temp+=",投影分带：3°带"
            pass
        self.eList[2]=temp

        while i<sum:
            L=self.ui.tableWidget5.item(i,0).text()
            B=self.ui.tableWidget5.item(i,1).text()
            (x,y,yf)=self.geoToGuass(L,B,d3,X)
            item=QTableWidgetItem(str(x.quantize(Decimal("1.000"))))
            flags=item.flags()
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget6.setItem(i,0,item)
            item=QTableWidgetItem(str(y.quantize(Decimal("1.000"))))
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget6.setItem(i,1,item)
            item=QTableWidgetItem(str(yf.quantize(Decimal("1.000"))))
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget6.setItem(i,2,item)
            i+=1
            self.ui.progressBar.setValue(i/sum*100)
            pass
        self.ui.progressBar.setVisible(False)
        self.ui.progressLabel.setText("")
        pass

    #高斯投影反算
    #参数 x y yf（y假定） d3（bool型 true为3度带） Bf 数值型 用来指定公式计算垂足纬度(0代表自定义椭球，用展开10次幂的多项式公式反算Bf ，1 2 3分别代表求弧长使用了对应椭球列表的数值公式，精度可靠)
    #返回L B 单位:度
    def geoToGuassInverted(self,x,y,yf,d3,Bf):
        if Bf:
            Bf=self.geo.getBf3(x,Bf-1)
            pass
        else:
            Bf=self.geo.getBf(x)
            pass
        return self.geo.geoAndGuassInvertedCal(x,y,yf,d3,Bf)

    #单例高斯投影反算
    #参数：Bf 数值型 用来指定公式计算垂足纬度(0代表自定义椭球，用展开10次幂的多项式公式反算Bf ，1 2 3分别代表求弧长使用了对应椭球列表的数值公式，精度可靠)
    def singleGeoToGuassInvertedCal(self,Bf):
        x=self.ui.x4LEdit.text()
        y=self.ui.y4LEdit.text()
        yf=self.ui.yf4LEdit.text()
        if not x.strip() or not y.strip() or  not yf.strip():
            tip="信息：数据没有输入\n\r"
            QMessageBox.information(self.ui,
            self.tr("提示"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        (L,B)=self.geoToGuassInverted(x,y,yf,not self.ui.radioButton2.isChecked(),Bf)
        (d,m,s)=self.geo.deg_60(L)
        s=s.quantize(Decimal("1.000"))
        if m<10:
            m="0"+str(m)
            pass
        if s<10:
            s="0"+str(s)
            pass
        L=str(d)+"°"+str(m)+"′"+str(s)+"″"
        (d,m,s)=self.geo.deg_60(B)
        s=s.quantize(Decimal("1.000"))
        if m<10:
            m="0"+str(m)
            pass
        if s<10:
            s="0"+str(s)
            pass
        B=str(d)+"°"+str(m)+"′"+str(s)+"″"
        self.ui.l4LEdit.setText(L)
        self.ui.b4LEdit.setText(B)
        pass
    #批量高斯投影正算
    #参数Bf 数值型 用来指定公式计算垂足纬度(0代表自定义椭球，用展开10次幂的多项式公式反算 ，1 2 3分别代表求弧长使用了对应椭球列表的数值公式，精度可靠)
    def batGeoToGuassInvertedCal(self,Bf):
        sum=self.ui.tableWidget7.rowCount()
        if sum<1:
            return
        i=0
        d3=not self.ui.radioButton2.isChecked()
        self.ui.progressBar.setValue(i)
        self.ui.progressLabel.setText("进度：")
        self.ui.progressBar.setVisible(True)
        self.ui.tableWidget8.setRowCount(sum)
        temp=self.ui.ellipsoidCBox.currentText()+"    椭球参数(a="+str(self.geo.a)+"m,"+"f="+str(self.geo.f)+")"
        if self.ui.radioButton2.isChecked():
            temp+=",投影分带：6°带"
            pass
        else:
            temp+=",投影分带：3°带"
            pass
        self.eList[3]=temp

        while i<sum:
            x=self.ui.tableWidget7.item(i,0).text()
            y=self.ui.tableWidget7.item(i,1).text()
            yf=self.ui.tableWidget7.item(i,2).text()
            (L,B)=self.geoToGuassInverted(x,y,yf,d3,Bf)
            (d,m,s)=self.geo.deg_60(L)
            s=s.quantize(Decimal("1.000"))
            if m<10:
                m="0"+str(m)
                pass
            if s<10:
                s="0"+str(s)
                pass
            L=str(d)+"°"+str(m)+"′"+str(s)+"″"
            (d,m,s)=self.geo.deg_60(B)
            s=s.quantize(Decimal("1.000"))
            if m<10:
                m="0"+str(m)
                pass
            if s<10:
                s="0"+str(s)
                pass
            B=str(d)+"°"+str(m)+"′"+str(s)+"″"
            item=QTableWidgetItem(L)
            flags=item.flags()
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget8.setItem(i,0,item)
            item=QTableWidgetItem(B)
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget8.setItem(i,1,item)
            i+=1
            self.ui.progressBar.setValue(i/sum*100)
            pass
        self.ui.progressBar.setVisible(False)
        self.ui.progressLabel.setText("")
        pass
    #大地问题正解
    #参数 p1点的大地坐标L1 B1 p1p2之间的大地线长S,及大地方位角A1
    #返回 p2点的大地坐标L2 B2 以及大地线在p2点的大地反方位角 A2
    def geoProblemPSolutionCal(self,L1,B1,S,A1):
        #l度数
        list=L1.split("°")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("′")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("″")
                m=list[0]
                pass
            pass

        #l度数
        L1=self.geo.degToRad(d,f,m)
        L1=math.degrees(L1)
        #b度数
        list=B1.split("°")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("′")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("″")
                m=list[0]
                pass

            pass
        #度数转弧度
        B1=self.geo.degToRad(d,f,m)
        B1=math.degrees(B1)
        #a1度数转弧度
        list=A1.split("°")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("′")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("″")
                m=list[0]
                pass

            pass
        #度数转弧度
        A1=self.geo.degToRad(d,f,m)
        A1=math.degrees(A1)
        return  self.geo.geoProblemPSolutionCal(L1,B1,S,A1)

    #单例大地问题正解
    def singleGeoProblemPSolutionCal(self):
        L1=self.ui.gl1LEdit1.text()
        B1=self.ui.gb1LEdit1.text()
        S=self.ui.gsLEdit1.text()
        A1=self.ui.ga1LEdit1.text()
        rx=QRegExp(".+(°|′|″)$")
        if not L1.strip() or not B1.strip() or not S.strip() or not A1.strip():
            tip="信息：数据没有输入\n\r"
            QMessageBox.information(self.ui,
            self.tr("提示"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(L1)
        if i==-1:
            tip="提示：大地经度可能是错误的!\n\r值："+L1
            QMessageBox.critical(self.ui,
            self.tr("错误"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(B1)
        if i==-1:
            tip="提示：大地纬度可能是错误的!\n\r值："+B1
            QMessageBox.critical(self.ui,
            self.tr("错误"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(A1)
        if i==-1:
            tip="提示：大地方位角可能是错误的!\n\r值："+A1
            QMessageBox.critical(self.ui,
            self.tr("错误"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        (L2,B2,A2)=self.geoProblemPSolutionCal(L1,B1,S,A1)
        (d,m,s)=self.geo.deg_60(L2)
        s=s.quantize(Decimal("1.000"))
        if m<10:
            m="0"+str(m)
            pass
        if s<10:
            s="0"+str(s)
            pass
        L2=str(d)+"°"+str(m)+"′"+str(s)+"″"
        (d,m,s)=self.geo.deg_60(B2)
        s=s.quantize(Decimal("1.000"))
        if m<10:
            m="0"+str(m)
            pass
        if s<10:
            s="0"+str(s)
            pass
        B2=str(d)+"°"+str(m)+"′"+str(s)+"″"
        (d,m,s)=self.geo.deg_60(A2)
        s=s.quantize(Decimal("1.000"))
        if m<10:
            m="0"+str(m)
            pass
        if s<10:
            s="0"+str(s)
            pass
        A2=str(d)+"°"+str(m)+"′"+str(s)+"″"
        self.ui.gl2LEdit1.setText(L2)
        self.ui.gb2LEdit1.setText(B2)
        self.ui.ga2LEdit1.setText(A2)
        pass
    #批量大地问题正解
    def batGeoProblemPSolutionCal(self):
        sum=self.ui.tableWidget9.rowCount()
        if sum<1:
            return
        i=0
        self.ui.progressBar.setVisible(True)
        self.ui.progressLabel.setText("进度：")
        self.ui.progressBar.setValue(i)
        self.ui.tableWidget10.setRowCount(sum)
        self.eList[4]=self.ui.ellipsoidCBox.currentText()+"    椭球参数(a="+str(self.geo.a)+"m,"+"f="+str(self.geo.f)+")"
        while i<sum:
            L1=self.ui.tableWidget9.item(i,0).text()
            B1=self.ui.tableWidget9.item(i,1).text()
            S=self.ui.tableWidget9.item(i,2).text()
            A1=self.ui.tableWidget9.item(i,3).text()
            (L2,B2,A2)=self.geoProblemPSolutionCal(L1,B1,S,A1)
            (d,m,s)=self.geo.deg_60(L2)
            s=s.quantize(Decimal("1.000"))
            if m<10:
                m="0"+str(m)
                pass
            if s<10:
                s="0"+str(s)
                pass
            L2=str(d)+"°"+str(m)+"′"+str(s)+"″"
            (d,m,s)=self.geo.deg_60(B2)
            s=s.quantize(Decimal("1.000"))
            if m<10:
                m="0"+str(m)
                pass
            if s<10:
                s="0"+str(s)
                pass
            B2=str(d)+"°"+str(m)+"′"+str(s)+"″"
            (d,m,s)=self.geo.deg_60(A2)
            s=s.quantize(Decimal("1.000"))
            if m<10:
                m="0"+str(m)
                pass
            if s<10:
                s="0"+str(s)
                pass
            A2=str(d)+"°"+str(m)+"′"+str(s)+"″"
            item=QTableWidgetItem(L2)
            flags=item.flags()
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget10.setItem(i,0,item)
            item=QTableWidgetItem(B2)
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget10.setItem(i,1,item)
            item=QTableWidgetItem(A2)
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget10.setItem(i,2,item)
            i+=1
            self.ui.progressBar.setValue(i/sum*100)
            pass
        self.ui.progressBar.setVisible(False)
        self.ui.progressLabel.setText("")
        pass
    #大地问题反解
    #参数 2点的大地坐标
    #返回 p1的方位角A1 p2的大地反方位角A2 大地线长S
    def geoProblemISolutionCal(self,L1,B1,L2,B2):
        #l度数
        list=L1.split("°")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("′")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("″")
                m=list[0]
                pass
            pass

        #l1度数
        L1=self.geo.degToRad(d,f,m)
        L1=math.degrees(L1)
        #b1度数
        list=B1.split("°")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("′")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("″")
                m=list[0]
                pass

            pass
        #b1度数转弧度
        B1=self.geo.degToRad(d,f,m)
        B1=math.degrees(B1)
        #l2度数
        list=L2.split("°")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("′")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("″")
                m=list[0]
                pass
            pass

        #l2度数
        L2=self.geo.degToRad(d,f,m)
        L2=math.degrees(L2)
        #b2度数
        list=B2.split("°")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("′")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("″")
                m=list[0]
                pass

            pass
        #度数转弧度
        B2=self.geo.degToRad(d,f,m)
        B2=math.degrees(B2)

        return self.geo.geoProblemISolutionCal(L1,B1,L2,B2)

    #单例大地问题反解
    def singleGeoProblemISolutionCal(self):
        L1=self.ui.gl1LEdit2.text()
        B1=self.ui.gb1LEdit2.text()
        L2=self.ui.gl2LEdit2.text()
        B2=self.ui.gb2LEdit2.text()

        if not L1.strip() or not B1.strip() or not L2.strip() or not B2.strip():
            tip="信息：数据没有输入\n\r"
            QMessageBox.information(self.ui,
            self.tr("提示"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        rx=QRegExp(".+(°|′|″)$")
        i=rx.indexIn(L1)
        if i==-1:
            tip="提示：L1可能是错误的!\n\r值："+L1
            QMessageBox.critical(self.ui,
            self.tr("错误"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(B1)
        if i==-1:
            tip="提示：B1可能是错误的!\n\r值："+B1
            QMessageBox.critical(self.ui,
            self.tr("错误"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(L2)
        if i==-1:
            tip="提示：L2可能是错误的!\n\r值："+L2
            QMessageBox.critical(self.ui,
            self.tr("错误"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(B2)
        if i==-1:
            tip="提示：B2可能是错误的!\n\r值："+B2
            QMessageBox.critical(self.ui,
            self.tr("错误"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        (S,A1,A2)=self.geoProblemISolutionCal(L1,B1,L2,B2)
        (d,m,s)=self.geo.deg_60(A1)
        s=s.quantize(Decimal("1.000"))
        if m<10:
            m="0"+str(m)
            pass
        if s<10:
            s="0"+str(s)
            pass
        A1=str(d)+"°"+str(m)+"′"+str(s)+"″"
        (d,m,s)=self.geo.deg_60(A2)
        s=s.quantize(Decimal("1.000"))
        if m<10:
            m="0"+str(m)
            pass
        if s<10:
            s="0"+str(s)
            pass
        A2=str(d)+"°"+str(m)+"′"+str(s)+"″"
        S=str(Decimal(str(S)).quantize(Decimal("1.000")))
        self.ui.gsLEdit2.setText(S)
        self.ui.ga1LEdit2.setText(A1)
        self.ui.ga2LEdit2.setText(A2)
        pass

    #批量大地问题反解
    def batGeoProblemISolutionCal(self):
        sum=self.ui.tableWidget11.rowCount()
        if sum<1:
            return
        i=0
        self.ui.progressBar.setVisible(True)
        self.ui.progressLabel.setText("进度：")
        self.ui.progressBar.setValue(i)
        self.ui.tableWidget12.setRowCount(sum)
        self.eList[5]=self.ui.ellipsoidCBox.currentText()+"    椭球参数(a="+str(self.geo.a)+"m,"+"f="+str(self.geo.f)+")"
        while i<sum:
            L1=self.ui.tableWidget11.item(i,0).text()
            B1=self.ui.tableWidget11.item(i,1).text()
            L2=self.ui.tableWidget11.item(i,2).text()
            B2=self.ui.tableWidget11.item(i,3).text()
            (S,A1,A2)=self.geoProblemISolutionCal(L1,B1,L2,B2)
            (d,m,s)=self.geo.deg_60(A1)
            s=s.quantize(Decimal("1.000"))
            if m<10:
                m="0"+str(m)
                pass
            if s<10:
                s="0"+str(s)
                pass
            A1=str(d)+"°"+str(m)+"′"+str(s)+"″"
            (d,m,s)=self.geo.deg_60(A2)
            s=s.quantize(Decimal("1.000"))
            if m<10:
                m="0"+str(m)
                pass
            if s<10:
                s="0"+str(s)
                pass
            A2=str(d)+"°"+str(m)+"′"+str(s)+"″"
            S=str(Decimal(str(S)).quantize(Decimal("1.000")))

            item=QTableWidgetItem(S)
            flags=item.flags()
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget12.setItem(i,0,item)
            item=QTableWidgetItem(A1)
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget12.setItem(i,1,item)
            item=QTableWidgetItem(A2)
            item.setFlags(flags&~Qt.ItemIsEditable)
            self.ui.tableWidget12.setItem(i,2,item)
            i+=1
            self.ui.progressBar.setValue(i/sum*100)
            pass
        self.ui.progressBar.setVisible(False)
        self.ui.progressLabel.setText("")
        pass
    #槽函数
    ######

    #选择椭球处理
    def selectEllipsoid(self,text):
        if text=="CGCS 2000 椭球":
            self.geo.setEllipsoidParameter2(6378137,1/298.257222101)
            self.ui.longLEdit.setDisabled(True)
            self.ui.oblatenessLEdit.setDisabled(True)
            pass

        elif  text=="克拉索夫斯基椭球":
            self.geo.setEllipsoidParameter2(6378245,1/298.3)
            self.ui.longLEdit.setDisabled(True)
            self.ui.oblatenessLEdit.setDisabled(True)
            pass
        elif  text=="IUGG 1975 椭球":
            self.geo.setEllipsoidParameter2(6378140,1/298.257)
            self.ui.longLEdit.setDisabled(True)
            self.ui.oblatenessLEdit.setDisabled(True)
            pass
        else:
            self.ui.longLEdit.setDisabled(False)
            self.ui.oblatenessLEdit.setDisabled(False)
            pass
        self.updateEllipsoidParameter()
        pass


    #自动计算自定义椭球参数用
    def customCalculation(self):
        if(self.ui.longLEdit.isEnabled()==True):
            self.geo.setEllipsoidParameter2(Decimal(self.ui.longLEdit.text()),Decimal(self.ui.oblatenessLEdit.text()))
            self.updateEllipsoidParameter()
            pass
        pass

    #计算类型改变
    def calTypeChanged(self,typeID):
        if typeID==2 or typeID==3:
            self.ui.d6Label.setVisible(True)
            self.ui.radioButton2.setVisible(True)
            pass
        else:
            self.ui.d6Label.setVisible(False)
            self.ui.radioButton2.setVisible(False)
            pass
        if self.ui.radioButton.isChecked():
            self.ui.stackedWidget.setCurrentIndex(typeID*2+1)
            pass
        else:
            self.ui.stackedWidget.setCurrentIndex(typeID*2)
            pass
        pass

    #批量处理改变
    def batHandleChanged(self,checked):
        if checked:
            self.ui.batTipLabel.show()
            self.ui.stackedWidget.setCurrentIndex(self.ui.calCBox.currentIndex()*2+1)
            pass
        else:
            self.ui.batTipLabel.hide()
            self.ui.stackedWidget.setCurrentIndex(self.ui.calCBox.currentIndex()*2)
            pass
        pass

    #经纬度输入时动态提示补全
    def lbhCompletiuon(self,text):
        lineEdit=self.sender()
        comp=None
        wordList=None
        di=text.find("°")
        length=len(text)

        def qss():
            if comp is not None and self.qss is not None:
                comp.popup().setStyleSheet(self.qss )
                pass
            return

        if di==-1:
            if (length!=0 and text[0]!="-") or (length>1):
                wordList=text+"°"
                #self.ui不能为lineEdit,形成引用环
                comp=QCompleter([wordList],self.ui)
                lineEdit.setCompleter(comp)
                pass
            else:
                comp=QCompleter([None],self.ui)
                lineEdit.setCompleter(comp)
                pass
            return qss()
        else:
            if di==length-1:
                comp=QCompleter([None],self.ui)
                lineEdit.setCompleter(comp)
                return qss()
            wordList=text[0:di+1]
            fi=text.find("′")
            if fi==-1:
                ft=text[di+1:length]
                wordList+=ft+"′"
                #self.ui不能为lineEdit,形成引用环
                comp=QCompleter([wordList],self.ui)
                lineEdit.setCompleter(comp)
                return qss()
            else:
                ft=text[di+1:fi]
                wordList+=ft+"′"
                if length-1==fi:
                    wordList=[wordList]

                    #self.ui不能为lineEdit,形成引用环
                    comp=QCompleter(wordList,self.ui)
                    lineEdit.setCompleter(comp)
                    return qss()
                else:
                    mi=text.find("″")
                    mt=None
                    if mi==-1:
                        mt=text[fi+1:length]
                        pass
                    else:
                        mt=text[fi+1:length-1]
                        pass
                    di=mt.find(".")
                    if di==-1:
                        wordList+= mt+"″"
                        #self.ui不能为lineEdit,形成引用环
                        comp=QCompleter([wordList],self.ui)
                        lineEdit.setCompleter(comp)
                        return qss()
                    else:
                        if di==len(mt)-1:
                            return
                        else:
                            t=mt[0:di]
                            wordList+= mt+"″"
                            #self.ui不能为lineEdit,形成引用环
                            comp=QCompleter([wordList],self.ui)
                            lineEdit.setCompleter(comp)
                            return qss()
                        pass
                    pass
                pass
            pass
        pass

    def importData(self):
        (fileName,__) = QFileDialog.getOpenFileName(self,
        self.tr("打开数据文件"), "./", self.tr("All Files (*)"))
        if fileName.strip():
            index=self.ui.calCBox.currentIndex()
            f = open(fileName, 'r',encoding="utf_8")
            row=0

            def showTip(row,rowText,tableWidget):
                QMessageBox.critical(self.ui,
                self.tr("错误"),
                "数据格式不正确!\n\r每行应是用空格隔开坐标数据\n\r位于行:"+str(row)+"\n\r内容："+rowText,
                QMessageBox.Ok,
                QMessageBox.Ok)
                f.close()
                tableWidget.setRowCount(0)
                pass

            if index==0:
                self.ui.tableWidget1.setRowCount(0)
                rxl = QRegExp("(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))°(\d|[0-5]\d)′(\d|[0-5]\d)(\.[0-9]{1,3})?″)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))°(\d|[0-5]\d)′$)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))°$)")
                rxb=QRegExp("(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))°(\d|[0-5]\d)′(\d|[0-5]\d)(\.[0-9]{1,3})?″$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))°(\d|[0-5]\d)′$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))°$)")
                rxh=QRegExp("(^((-)?[1-9])\d*(\.\d+)?$)|(^((-)?0)(\.\d+)?$)")
                r,rt=0,''
                while True:
                    content = f.readline()

                    if content=='':
                        break
                    r+=1
                    rt=content
                    content = content.strip().split(" ")
                    content =list(filter(lambda x:x!='',content))
                    if len(content)==0:
                        continue
                    if content[0][0]=="#":
                        continue
                    if len(content)<3:
                        showTip(r,rt,self.ui.tableWidget1)
                        return
                    if rxl.indexIn(content[0])==-1 or rxb.indexIn(content[1])==-1 or rxh.indexIn(content[2])==-1:
                        showTip(r,rt,self.ui.tableWidget1)
                        return
                    self.ui.tableWidget1.setRowCount(row+1)
                    item=QTableWidgetItem(content[0])
                    flags=item.flags()
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget1.setItem(row,0,item)
                    item=QTableWidgetItem(content[1])
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget1.setItem(row,1,item)
                    item=QTableWidgetItem(content[2])
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget1.setItem(row,2,item)
                    row+=1
                    pass
                pass
            elif index==1:
                self.ui.tableWidget3.setRowCount(0)
                rx = QRegExp("(^((-)?[1-9])\d*(\.\d+)?$)|(^((-)?0)(\.\d+)?$)")
                r,rt=0,''
                while True:
                    content = f.readline()
                    if content=='':
                        break
                    r+=1
                    rt=content
                    content = content.strip().split(" ")
                    content =list(filter(lambda x:x!='',content))
                    if len(content)==0:
                        continue
                    if str(content[0])[0]=="#":
                        continue
                    if len(content)<3:
                        showTip(r,rt,self.ui.tableWidget3)
                        return
                    if rx.indexIn(content[0])==-1 or rx.indexIn(content[1])==-1 or rx.indexIn(content[2])==-1:
                        showTip(r,rt,self.ui.tableWidget3)
                        return
                    self.ui.tableWidget3.setRowCount(row+1)
                    item=QTableWidgetItem(content[0])
                    flags=item.flags()
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget3.setItem(row,0,item)
                    item=QTableWidgetItem(content[1])
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget3.setItem(row,1,item)
                    item=QTableWidgetItem(content[2])
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget3.setItem(row,2,item)
                    row+=1
                    pass
                pass
            elif index==2:
                self.ui.tableWidget5.setRowCount(0)
                rxl = QRegExp("(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))°(\d|[0-5]\d)′(\d|[0-5]\d)(\.[0-9]{1,3})?″)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))°(\d|[0-5]\d)′$)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))°$)")
                rxb=QRegExp("(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))°(\d|[0-5]\d)′(\d|[0-5]\d)(\.[0-9]{1,3})?″$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))°(\d|[0-5]\d)′$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))°$)")
                r,rt=0,''
                while True:
                    content = f.readline()
                    if content=='':
                        break
                    r+=1
                    rt=content
                    content = content.strip().split(" ")
                    content =list(filter(lambda x:x!='',content))
                    if len(content)==0:
                        continue
                    if content[0][0]=="#":
                        continue
                    if len(content)<2:
                        showTip(r,rt,self.ui.tableWidget5)
                        return
                    if rxl.indexIn(content[0])==-1 or rxb.indexIn(content[1])==-1:
                        showTip(r,rt,self.ui.tableWidget5)
                        return
                    self.ui.tableWidget5.setRowCount(row+1)
                    item=QTableWidgetItem(content[0])
                    flags=item.flags()
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget5.setItem(row,0,item)
                    item=QTableWidgetItem(content[1])
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget5.setItem(row,1,item)
                    row+=1
                    pass
                pass
            elif index==3:
                self.ui.tableWidget7.setRowCount(0)
                rxp = QRegExp("(^[1-9]\d*(\.\d+)?$)|(^(0)(\.\d+)?$)")
                rx = QRegExp("(^((-)?[1-9])\d*(\.\d+)?$)|(^((-)?0)(\.\d+)?$)")
                r,rt=0,''
                while True:
                    content = f.readline()
                    if content=='':
                        break
                    r+=1
                    rt=content
                    content = content.strip().split(" ")
                    content =list(filter(lambda x:x!='',content))
                    if len(content)==0:
                        continue
                    if content[0][0]=="#":
                        continue
                    if len(content)<3:
                        showTip(r,rt,self.ui.tableWidget7)
                        return
                    if rxp.indexIn(content[0])==-1 or rx.indexIn(content[1])==-1 or rxp.indexIn(content[2])==-1:
                        showTip(r,rt,self.ui.tableWidget7)
                        return
                    self.ui.tableWidget7.setRowCount(row+1)
                    item=QTableWidgetItem(content[0])
                    flags=item.flags()
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget7.setItem(row,0,item)
                    item=QTableWidgetItem(content[1])
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget7.setItem(row,1,item)
                    item=QTableWidgetItem(content[2])
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget7.setItem(row,2,item)
                    row+=1
                    pass
                pass
            elif index==4:
                self.ui.tableWidget9.setRowCount(0)

                rxp = QRegExp("(^[1-9]\d*(\.\d+)?$)|(^(0)(\.\d+)?$)")
                rxl = QRegExp("(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))°(\d|[0-5]\d)′(\d|[0-5]\d)(\.[0-9]{1,3})?″)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))°(\d|[0-5]\d)′$)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))°$)")
                rxb=QRegExp("(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))°(\d|[0-5]\d)′(\d|[0-5]\d)(\.[0-9]{1,3})?″$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))°(\d|[0-5]\d)′$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))°$)")
                r,rt=0,''
                while True:
                    content = f.readline()
                    if content=='':
                        break
                    r+=1
                    rt=content
                    content = content.strip().split(" ")
                    content =list(filter(lambda x:x!='',content))
                    if len(content)==0:
                        continue
                    if content[0][0]=="#":
                        continue
                    if len(content)<4:
                        showTip(r,rt,self.ui.tableWidget9)
                        return
                    if rxp.indexIn(content[2])==-1 or rxl.indexIn(content[0])==-1 or rxb.indexIn(content[1])==-1 or rxl.indexIn(content[3])==-1:
                        showTip(r,rt,self.ui.tableWidget9)
                        return
                    self.ui.tableWidget9.setRowCount(row+1)
                    item=QTableWidgetItem(content[0])
                    flags=item.flags()
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget9.setItem(row,0,item)
                    item=QTableWidgetItem(content[1])
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget9.setItem(row,1,item)
                    item=QTableWidgetItem(content[2])
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget9.setItem(row,2,item)
                    item=QTableWidgetItem(content[3])
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget9.setItem(row,3,item)
                    row+=1
                    pass
                pass
            elif index==5:
                self.ui.tableWidget9.setRowCount(0)
                rxl = QRegExp("(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))°(\d|[0-5]\d)′(\d|[0-5]\d)(\.[0-9]{1,3})?″)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))°(\d|[0-5]\d)′$)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))°$)")
                rxb=QRegExp("(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))°(\d|[0-5]\d)′(\d|[0-5]\d)(\.[0-9]{1,3})?″$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))°(\d|[0-5]\d)′$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))°$)")
                r,rt=0,''
                while True:
                    content = f.readline()
                    if content=='':
                        break
                    r+=1
                    rt=content
                    content = content.strip().split(" ")
                    content =list(filter(lambda x:x!='',content))
                    if len(content)==0:
                        continue
                    if content[0][0]=="#":
                        continue
                    if len(content)<4:
                        showTip(r,rt,self.ui.tableWidget11)
                        return
                    if  rxl.indexIn(content[0])==-1 or rxb.indexIn(content[1])==-1 or\
                    rxl.indexIn(content[2])==-1 or rxb.indexIn(content[3])==-1 :
                        showTip(r,rt,self.ui.tableWidget11)
                        return
                    self.ui.tableWidget11.setRowCount(row+1)
                    item=QTableWidgetItem(content[0])
                    flags=item.flags()
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget11.setItem(row,0,item)
                    item=QTableWidgetItem(content[1])
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget11.setItem(row,1,item)
                    item=QTableWidgetItem(content[2])
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget11.setItem(row,2,item)
                    item=QTableWidgetItem(content[3])
                    item.setFlags(flags&~Qt.ItemIsEditable)
                    self.ui.tableWidget11.setItem(row,3,item)
                    row+=1
                    pass
                pass
            f.close()
            pass
        pass

    #导出数据
    def exportData(self):
        index=self.ui.calCBox.currentIndex()

        def ft():
            (fileName,__)=QFileDialog.getSaveFileName(self.ui, self.tr("保存数据文件"),
            "./",
            self.tr("All Files (*)"))
            return fileName

        if index==0:
            sum=self.ui.tableWidget2.rowCount()
            if sum<1:
                return
            fileName=ft()
            if not fileName.strip():
                return
            f= open(fileName,"w+",encoding="utf-8")
            f.write("#大地坐标与大地空间直角坐标正算结果\n#大地空间直角坐标(X Y Z),单位:m,%s\n"% (self.eList[index]))
            for i in range(sum):
                X=self.ui.tableWidget2.item(i,0).text()
                Y=self.ui.tableWidget2.item(i,1).text()
                Z=self.ui.tableWidget2.item(i,2).text()
                f.write('{:<16s}  {:<16s}  {:<16s}\n'.format(X,Y,Z))
                pass
            f.close()
            pass
        elif index==1:
            sum=self.ui.tableWidget4.rowCount()
            if sum<1:
                return
            fileName=ft()
            if not fileName.strip():
                return
            f= open(fileName,"w+",encoding="utf-8")
            f.write("#大地坐标与大地空间直角坐标反算结果\n#大地坐标(L B H),H单位:m,%s\n"% (self.eList[index]))
            for i in range(sum):
                L=self.ui.tableWidget4.item(i,0).text()
                B=self.ui.tableWidget4.item(i,1).text()
                H=self.ui.tableWidget4.item(i,2).text()
                f.write('{:<16s}  {:<16s}  {:<16s}\n'.format(L,B,H))
                pass
            f.close()
            pass
        elif index==2:
            sum=self.ui.tableWidget6.rowCount()
            if sum<1:
                return
            fileName=ft()
            if not fileName.strip():
                return
            f= open(fileName,"w+",encoding="utf-8")
            f.write("#高斯投影正算结果\n#高斯平面直角坐标(x y y假定),单位:m,%s\n"% (self.eList[index]))
            for i in range(sum):
                x=self.ui.tableWidget6.item(i,0).text()
                y=self.ui.tableWidget6.item(i,1).text()
                yf=self.ui.tableWidget6.item(i,2).text()
                f.write('{:<16s}  {:<16s}  {:<16s}\n'.format(x,y,yf))
                pass
            f.close()
            pass
        elif index==3:
            sum=self.ui.tableWidget8.rowCount()
            if sum<1:
                return
            fileName=ft()
            if not fileName.strip():
                return
            f= open(fileName,"w+",encoding="utf-8")
            f.write("#高斯投影反算结果\n#大地坐标(L B),%s\n"% (self.eList[index]))
            for i in range(sum):
                L=self.ui.tableWidget8.item(i,0).text()
                B=self.ui.tableWidget8.item(i,1).text()
                f.write('{:<16s}  {:<16s}\n'.format(L,B))
                pass
            f.close()
            pass
        elif index==4:
            sum=self.ui.tableWidget10.rowCount()
            if sum<1:
                return
            fileName=ft()
            if not fileName.strip():
                return
            f= open(fileName,"w+",encoding="utf-8")
            f.write("#大地主题正解结果(L2 B2 A2),%s\n"% (self.eList[index]))
            for i in range(sum):
                L2=self.ui.tableWidget10.item(i,0).text()
                B2=self.ui.tableWidget10.item(i,1).text()
                A2=self.ui.tableWidget10.item(i,2).text()
                f.write('{:<16s}  {:<16s}  {:<16s}\n'.format(L2,B2,A2))
                pass
            f.close()
            pass
        elif index==5:
            sum=self.ui.tableWidget12.rowCount()
            if sum<1:
                return
            fileName=ft()
            if not fileName.strip():
                return
            f= open(fileName,"w+",encoding="utf-8")
            f.write("#大地主题反解结果(S A1 A2),%s\n"% (self.eList[index]))
            for i in range(sum):
                S=self.ui.tableWidget12.item(i,0).text()
                A1=self.ui.tableWidget12.item(i,1).text()
                A2=self.ui.tableWidget12.item(i,2).text()
                f.write('{:<16s}  {:<16s}  {:<16s}\n'.format(S,A1,A2))
                pass
            f.close()
            pass
        pass

    #大地测量综合计算
    def calBtnClicked(self):
        index=self.ui.calCBox.currentIndex()
        rc=self.ui.radioButton.isChecked()
        if index==0:
            if rc:
                self.batGeoToGeoSpatialCal()
                pass
            else:
                self.singleGeoToGeoSpatialCal()
                pass
            pass
        elif index==1:
            if rc:
                self.batInvertedGeoToGeoSpatialCal()
                pass
            else:
                self.singleInvertedGeoToGeoSpatialCal()
                pass
            pass
        elif index==2:
            X=self.ui.ellipsoidCBox.currentIndex()
            if X==self.ui.ellipsoidCBox.count()-1:
                X=0
                pass
            else:
                X+=1
                pass
            if rc:
                self.batGeoToGuassCal(X)
                pass
            else:
                self.singleGeoToGuassCal(X)
                pass
            pass
        elif index==3:
            Bf=self.ui.ellipsoidCBox.currentIndex()
            if Bf==self.ui.ellipsoidCBox.count()-1:
                Bf=0
                pass
            else:
                Bf+=1
                pass
            if rc:
                self.batGeoToGuassInvertedCal(Bf)
                pass
            else:
                self.singleGeoToGuassInvertedCal(Bf)
                pass
            pass
        elif index==4:
            if rc:
                self.batGeoProblemPSolutionCal()
                pass
            else:
                self.singleGeoProblemPSolutionCal()
                pass
            pass
        elif index==5:
            if rc:
                self.batGeoProblemISolutionCal()
                pass
            else:
                self.singleGeoProblemISolutionCal()
                pass
            pass

        pass


    pass
