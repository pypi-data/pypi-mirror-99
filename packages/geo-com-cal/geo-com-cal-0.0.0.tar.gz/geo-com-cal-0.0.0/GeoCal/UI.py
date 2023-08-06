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
    #������ʶ
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
        #����ʱ���õ����������Ϣ�б��¼
        self.eList=[None,None,None,None,None,None]
        #�������Ա
        self.geo=None
        #ui
        self.ui=None
        #��ʽ
        self.qss=None
        self.load_ui()
        #������ʾ
        deskRect=QApplication.desktop().availableGeometry()
        self.move((deskRect.width()-self.ui.width())/2, (deskRect.height()-self.ui.height())/2)
        self.setFixedSize(self.ui.width(),self.ui.height())
        #�ӿؼ�
        temp="""      ���棺��˹ͶӰ���������õ������߻���X������γ��Bf������������֪���򣬼���X��Bfʱʹ�õ��Ǵ�ֵ��ʽ����˸�˹ͶӰ�ļ��������ȴﵽ0.001m������δ��¼������"""
        temp+=""",����X��Bf�Ǹ��ݴ�ͳ��չ����10���ݵ������߻�����ʽ�����㣬��ʹ�ø�˹ͶӰ����ڶ�������¿�����λ��"""
        rl=RollLabel(temp,self.ui)
        rl.move(140,175)
        rl.resize(520,20)
        rl.setObjectName("warning")
        rl.setToolTip(temp)
        # ����QSS
        self.load_qss()
        #���ñ�ͷ��ǩ
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
        labels=["x","y","y�ٶ�"]
        self.ui.tableWidget6.setHorizontalHeaderLabels(labels)
        self.ui.tableWidget6.verticalHeader().setSectionResizeMode(QHeaderView.ResizeToContents)

        self.ui.tableWidget7.setColumnCount(3)
        labels=["x","y","y�ٶ�"]
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

        #��������ʼ��������
        self.ui.progressBar.setVisible(False)
        self.ui.progressLabel.setText("")

        self.ui.d6Label.setVisible(False)
        self.ui.radioButton2.setVisible(False)

        #��������
        #������
        rx = QRegExp("^(6378)\d{3,3}(\.\d+)$?")
        lValidator = QRegExpValidator(rx, self.ui)
        self.ui.longLEdit.setValidator(lValidator)
        rx = QRegExp("^(0\.003352)\d{0,8}$")
        oValidator = QRegExpValidator(rx, self.ui)
        self.ui.oblatenessLEdit.setValidator(oValidator)

        #x y z
        #3С���㸡����
        dValidator=QDoubleValidator()
        dValidator.setDecimals(3)
        self.ui.x2LEdit.setValidator(dValidator)
        self.ui.y2LEdit.setValidator(dValidator)
        self.ui.z2LEdit.setValidator(dValidator)

        #��֪
        #L
        rx = QRegExp("(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))��(\d|[0-5]\d)��(\d|[0-5]\d)(\.[0-9]{1,3})?��")
        lValidator = QRegExpValidator(rx, self.ui)
        self.ui.l1LEdit.setValidator(lValidator)
        self.ui.l3LEdit.setValidator(lValidator)
        self.ui.gl1LEdit1.setValidator(lValidator)
        self.ui.gl1LEdit2.setValidator(lValidator)
        self.ui.gl2LEdit2.setValidator(lValidator)
        #��λ��
        self.ui.ga1LEdit1.setValidator(lValidator)
        #B
        rx = QRegExp("(-)?(\d|[1-9]\d|(1[0-7]\d|180))��(\d|[0-5]\d)��(\d|[0-5]\d)(\.[0-9]{1,3})?��")
        bValidator = QRegExpValidator(rx, self.ui)
        self.ui.b3LEdit.setValidator(bValidator)
        self.ui.b1LEdit.setValidator(bValidator)
        self.ui.gb1LEdit1.setValidator(bValidator)
        self.ui.gb1LEdit2.setValidator(bValidator)
        self.ui.gb2LEdit2.setValidator(bValidator)
        #h
        self.ui.h1LEdit.setValidator(dValidator)
        #x y y�ٶ�
        #y����Ϊ����
        self.ui.y4LEdit.setValidator(dValidator)

        dpValidator=QDoubleValidator()
        dpValidator.setRange(0,math.pow(2,31),3)
        self.ui.x4LEdit.setValidator(dpValidator)
        self.ui.yf4LEdit.setValidator(dpValidator)
        self.ui.gsLEdit1.setValidator(dpValidator)


        #ʵ����������
        self.geo=Geo()
        #��ʼ������
        self.updateEllipsoidParameter()
        #�����ź�
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
        self.setWindowTitle("��ز����ۺϼ���")
        loader = QUiLoader()
        path = os.path.join(os.path.dirname(__file__), "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        self.ui=loader.load(ui_file, self)
        ui_file.close()
        pass

    def load_qss(self):
        # ����QSS
        path= os.path.join(os.path.dirname(__file__), "QSS/task_ui.qss")
        with open(path, "r",encoding='gbk') as qs:
            self.qss=qs.read()
            self.setStyleSheet(self.qss)
            pass
        pass

    #���²���
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


    #����������ؿռ���������
    #�����������ʽ��L B �Լ�H
    #���� X Y Z
    def geoToGeoSpatial(self,L,B,H):
        #l����ת����
        list=L.split("��")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("��")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("��")
                m=list[0]
                pass

            pass

        #����ת����
        L=self.geo.degToRad(d,f,m)
        #b����ת����
        list=B.split("��")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("��")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("��")
                m=list[0]
                pass

            pass
        #����ת����
        B=self.geo.degToRad(d,f,m)
        return self.geo.geoAndGeoSpatialCal(L,B,H)


    #��������������ؿռ���������
    def singleGeoToGeoSpatialCal(self):
        L=self.ui.l1LEdit.text()
        B=self.ui.b1LEdit.text()
        H=self.ui.h1LEdit.text()
        rx=QRegExp(".+(��|��|��)$")
        i=rx.indexIn(L)
        if not L.strip() or not B.strip() or not H.strip():
            tip="��Ϣ������û������\n\r"
            QMessageBox.information(self.ui,
            self.tr("��ʾ"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        if i==-1:
            tip="��ʾ����ؾ��ȿ����Ǵ����!\n\rֵ��"+L
            QMessageBox.critical(self.ui,
            self.tr("����"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(B)
        if i==-1:
            tip="��ʾ�����γ�ȿ����Ǵ����!\n\rֵ��"+B
            QMessageBox.critical(self.ui,
            self.tr("����"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        (X,Y,Z)=self.geoToGeoSpatial(L,B,H)
        self.ui.x1LEdit.setText(str(X.quantize(Decimal("1.0000"))))
        self.ui.y1LEdit.setText(str(Y.quantize(Decimal("1.0000"))))
        self.ui.z1LEdit.setText(str(Z.quantize(Decimal("1.0000"))))
        pass

    #��������������ؿռ���������
    def batGeoToGeoSpatialCal(self):
        sum=self.ui.tableWidget1.rowCount()
        if sum<1:
            return
        i=0
        self.ui.progressBar.setVisible(True)
        self.ui.progressLabel.setText("���ȣ�")
        self.ui.progressBar.setValue(i)
        self.ui.tableWidget2.setRowCount(sum)
        self.eList[0]=self.ui.ellipsoidCBox.currentText()+"    �������(a="+str(self.geo.a)+"m,"+"f="+str(self.geo.f)+")"
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

    #����������ؿռ����귴��
    #������X Y Z
    #���� L B�������������� H decimal����
    def invertedGeoToGeoSpatial(self,X,Y,Z):
        return self.geo.geoAndGeoSpatialInvertedCal(X,Y,Z)

    #���������ռ�ֱ�Ƿ���
    def singleInvertedGeoToGeoSpatialCal(self):
        X=self.ui.x2LEdit.text()
        Y=self.ui.y2LEdit.text()
        Z=self.ui.z2LEdit.text()
        if not X.strip() or not Y.strip() or not Z.strip():
            tip="��Ϣ������û������\n\r"
            QMessageBox.information(self.ui,
            self.tr("��ʾ"),
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
        L=str(d)+"��"+str(m)+"��"+str(s)+"��"
        (d,m,s)=self.geo.deg_60(B)
        s=s.quantize(Decimal("1.0000"))
        if m<10:
            m="0"+str(m)
            pass
        if s<10:
            s="0"+str(s)
            pass
        B=str(d)+"��"+str(m)+"��"+str(s)+"��"
        self.ui.l2LEdit.setText(L)
        self.ui.b2LEdit.setText(B)
        self.ui.h2LEdit.setText(str(H.quantize(Decimal("1.0000"))))
        pass

    #���������ռ�ֱ�Ƿ���
    def batInvertedGeoToGeoSpatialCal(self):
        sum=self.ui.tableWidget3.rowCount()
        if sum<1:
            return
        i=0
        self.ui.progressBar.setValue(i)
        self.ui.progressBar.setVisible(True)
        self.ui.progressLabel.setText("���ȣ�")
        self.ui.tableWidget4.setRowCount(sum)
        self.eList[1]=self.ui.ellipsoidCBox.currentText()+"    �������(a="+str(self.geo.a)+"m,"+"f="+str(self.geo.f)+")"
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
            L=str(d)+"��"+str(m)+"��"+str(s)+"��"
            (d,m,s)=self.geo.deg_60(B)
            s=s.quantize(Decimal("1.0000"))
            if m<10:
                m="0"+str(m)
                pass
            if s<10:
                s="0"+str(s)
                pass
            B=str(d)+"��"+str(m)+"��"+str(s)+"��"
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

    #��˹ͶӰ����
    #���� L B���ȷ��룩 d3��bool�� trueΪ3�ȴ��� X ��ֵ�� ����ָ����ʽ���������߻���(0�����Զ���������չ��10���ݵĶ���ʽ��ʽ �侫�ȵͣ�1 2 3�ֱ�����󻡳�ʹ���˶�Ӧ�����б����ֵ��ʽ�����ȿɿ�)
    #���� x y yf��y�ٶ���
    def geoToGuass(self,L,B,d3,X):
        #l����ת����
        list=L.split("��")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("��")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("��")
                m=list[0]
                pass

            pass

        #����ת����
        L=self.geo.degToRad(d,f,m)
        #b����ת����
        list=B.split("��")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("��")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("��")
                m=list[0]
                pass

            pass
        #����ת����
        B=self.geo.degToRad(d,f,m)
        if X:
            X=self.geo.getX3(B,X-1)
            pass
        else:
            X=self.geo.getX(B)
            pass
        return self.geo.geoAndGuassCal(L,B,d3,X)

    #������˹ͶӰ����
    #������X ��ֵ�� ����ָ����ʽ���������߻���(0�����Զ���������չ��10���ݵĶ���ʽ��ʽ��1 2 3�ֱ�����󻡳�ʹ���˶�Ӧ�����б����ֵ��ʽ�����ȿɿ�)
    def singleGeoToGuassCal(self,X):
        L=self.ui.l3LEdit.text()
        B=self.ui.b3LEdit.text()
        rx=QRegExp(".+(��|��|��)$")
        i=rx.indexIn(L)
        if not L.strip() or not B.strip():
            tip="��Ϣ������û������\n\r"
            QMessageBox.information(self.ui,
            self.tr("��ʾ"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        if i==-1:
            tip="��ʾ����ؾ��ȿ����Ǵ����!\n\rֵ��"+L
            QMessageBox.critical(self.ui,
            self.tr("����"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(B)
        if i==-1:
            tip="��ʾ�����γ�ȿ����Ǵ����!\n\rֵ��"+B
            QMessageBox.critical(self.ui,
            self.tr("����"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        (x,y,yf)=self.geoToGuass(L,B,not self.ui.radioButton2.isChecked(),X)
        self.ui.x3LEdit.setText(str(x.quantize(Decimal("1.000"))))
        self.ui.y3LEdit.setText(str(y.quantize(Decimal("1.000"))))
        self.ui.y3fLEdit.setText(str(yf.quantize(Decimal("1.000"))))
        pass

    #������˹ͶӰ����
    #����X ��ֵ�� ����ָ����ʽ���������߻���(0�����Զ���������չ��10���ݵĶ���ʽ��ʽ��1 2 3�ֱ�����󻡳�ʹ���˶�Ӧ�����б����ֵ��ʽ�����ȿɿ�)
    def batGeoToGuassCal(self,X):
        sum=self.ui.tableWidget5.rowCount()
        if sum<1:
            return
        i=0
        d3=not self.ui.radioButton2.isChecked()
        self.ui.progressBar.setValue(i)
        self.ui.progressLabel.setText("���ȣ�")
        self.ui.progressBar.setVisible(True)
        self.ui.tableWidget6.setRowCount(sum)
        temp=self.ui.ellipsoidCBox.currentText()+"    �������(a="+str(self.geo.a)+"m,"+"f="+str(self.geo.f)+")"
        if self.ui.radioButton2.isChecked():
            temp+=",ͶӰ�ִ���6���"
            pass
        else:
            temp+=",ͶӰ�ִ���3���"
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

    #��˹ͶӰ����
    #���� x y yf��y�ٶ��� d3��bool�� trueΪ3�ȴ��� Bf ��ֵ�� ����ָ����ʽ���㴹��γ��(0�����Զ���������չ��10���ݵĶ���ʽ��ʽ����Bf ��1 2 3�ֱ�����󻡳�ʹ���˶�Ӧ�����б����ֵ��ʽ�����ȿɿ�)
    #����L B ��λ:��
    def geoToGuassInverted(self,x,y,yf,d3,Bf):
        if Bf:
            Bf=self.geo.getBf3(x,Bf-1)
            pass
        else:
            Bf=self.geo.getBf(x)
            pass
        return self.geo.geoAndGuassInvertedCal(x,y,yf,d3,Bf)

    #������˹ͶӰ����
    #������Bf ��ֵ�� ����ָ����ʽ���㴹��γ��(0�����Զ���������չ��10���ݵĶ���ʽ��ʽ����Bf ��1 2 3�ֱ�����󻡳�ʹ���˶�Ӧ�����б����ֵ��ʽ�����ȿɿ�)
    def singleGeoToGuassInvertedCal(self,Bf):
        x=self.ui.x4LEdit.text()
        y=self.ui.y4LEdit.text()
        yf=self.ui.yf4LEdit.text()
        if not x.strip() or not y.strip() or  not yf.strip():
            tip="��Ϣ������û������\n\r"
            QMessageBox.information(self.ui,
            self.tr("��ʾ"),
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
        L=str(d)+"��"+str(m)+"��"+str(s)+"��"
        (d,m,s)=self.geo.deg_60(B)
        s=s.quantize(Decimal("1.000"))
        if m<10:
            m="0"+str(m)
            pass
        if s<10:
            s="0"+str(s)
            pass
        B=str(d)+"��"+str(m)+"��"+str(s)+"��"
        self.ui.l4LEdit.setText(L)
        self.ui.b4LEdit.setText(B)
        pass
    #������˹ͶӰ����
    #����Bf ��ֵ�� ����ָ����ʽ���㴹��γ��(0�����Զ���������չ��10���ݵĶ���ʽ��ʽ���� ��1 2 3�ֱ�����󻡳�ʹ���˶�Ӧ�����б����ֵ��ʽ�����ȿɿ�)
    def batGeoToGuassInvertedCal(self,Bf):
        sum=self.ui.tableWidget7.rowCount()
        if sum<1:
            return
        i=0
        d3=not self.ui.radioButton2.isChecked()
        self.ui.progressBar.setValue(i)
        self.ui.progressLabel.setText("���ȣ�")
        self.ui.progressBar.setVisible(True)
        self.ui.tableWidget8.setRowCount(sum)
        temp=self.ui.ellipsoidCBox.currentText()+"    �������(a="+str(self.geo.a)+"m,"+"f="+str(self.geo.f)+")"
        if self.ui.radioButton2.isChecked():
            temp+=",ͶӰ�ִ���6���"
            pass
        else:
            temp+=",ͶӰ�ִ���3���"
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
            L=str(d)+"��"+str(m)+"��"+str(s)+"��"
            (d,m,s)=self.geo.deg_60(B)
            s=s.quantize(Decimal("1.000"))
            if m<10:
                m="0"+str(m)
                pass
            if s<10:
                s="0"+str(s)
                pass
            B=str(d)+"��"+str(m)+"��"+str(s)+"��"
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
    #�����������
    #���� p1��Ĵ������L1 B1 p1p2֮��Ĵ���߳�S,����ط�λ��A1
    #���� p2��Ĵ������L2 B2 �Լ��������p2��Ĵ�ط���λ�� A2
    def geoProblemPSolutionCal(self,L1,B1,S,A1):
        #l����
        list=L1.split("��")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("��")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("��")
                m=list[0]
                pass
            pass

        #l����
        L1=self.geo.degToRad(d,f,m)
        L1=math.degrees(L1)
        #b����
        list=B1.split("��")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("��")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("��")
                m=list[0]
                pass

            pass
        #����ת����
        B1=self.geo.degToRad(d,f,m)
        B1=math.degrees(B1)
        #a1����ת����
        list=A1.split("��")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("��")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("��")
                m=list[0]
                pass

            pass
        #����ת����
        A1=self.geo.degToRad(d,f,m)
        A1=math.degrees(A1)
        return  self.geo.geoProblemPSolutionCal(L1,B1,S,A1)

    #���������������
    def singleGeoProblemPSolutionCal(self):
        L1=self.ui.gl1LEdit1.text()
        B1=self.ui.gb1LEdit1.text()
        S=self.ui.gsLEdit1.text()
        A1=self.ui.ga1LEdit1.text()
        rx=QRegExp(".+(��|��|��)$")
        if not L1.strip() or not B1.strip() or not S.strip() or not A1.strip():
            tip="��Ϣ������û������\n\r"
            QMessageBox.information(self.ui,
            self.tr("��ʾ"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(L1)
        if i==-1:
            tip="��ʾ����ؾ��ȿ����Ǵ����!\n\rֵ��"+L1
            QMessageBox.critical(self.ui,
            self.tr("����"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(B1)
        if i==-1:
            tip="��ʾ�����γ�ȿ����Ǵ����!\n\rֵ��"+B1
            QMessageBox.critical(self.ui,
            self.tr("����"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(A1)
        if i==-1:
            tip="��ʾ����ط�λ�ǿ����Ǵ����!\n\rֵ��"+A1
            QMessageBox.critical(self.ui,
            self.tr("����"),
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
        L2=str(d)+"��"+str(m)+"��"+str(s)+"��"
        (d,m,s)=self.geo.deg_60(B2)
        s=s.quantize(Decimal("1.000"))
        if m<10:
            m="0"+str(m)
            pass
        if s<10:
            s="0"+str(s)
            pass
        B2=str(d)+"��"+str(m)+"��"+str(s)+"��"
        (d,m,s)=self.geo.deg_60(A2)
        s=s.quantize(Decimal("1.000"))
        if m<10:
            m="0"+str(m)
            pass
        if s<10:
            s="0"+str(s)
            pass
        A2=str(d)+"��"+str(m)+"��"+str(s)+"��"
        self.ui.gl2LEdit1.setText(L2)
        self.ui.gb2LEdit1.setText(B2)
        self.ui.ga2LEdit1.setText(A2)
        pass
    #���������������
    def batGeoProblemPSolutionCal(self):
        sum=self.ui.tableWidget9.rowCount()
        if sum<1:
            return
        i=0
        self.ui.progressBar.setVisible(True)
        self.ui.progressLabel.setText("���ȣ�")
        self.ui.progressBar.setValue(i)
        self.ui.tableWidget10.setRowCount(sum)
        self.eList[4]=self.ui.ellipsoidCBox.currentText()+"    �������(a="+str(self.geo.a)+"m,"+"f="+str(self.geo.f)+")"
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
            L2=str(d)+"��"+str(m)+"��"+str(s)+"��"
            (d,m,s)=self.geo.deg_60(B2)
            s=s.quantize(Decimal("1.000"))
            if m<10:
                m="0"+str(m)
                pass
            if s<10:
                s="0"+str(s)
                pass
            B2=str(d)+"��"+str(m)+"��"+str(s)+"��"
            (d,m,s)=self.geo.deg_60(A2)
            s=s.quantize(Decimal("1.000"))
            if m<10:
                m="0"+str(m)
                pass
            if s<10:
                s="0"+str(s)
                pass
            A2=str(d)+"��"+str(m)+"��"+str(s)+"��"
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
    #������ⷴ��
    #���� 2��Ĵ������
    #���� p1�ķ�λ��A1 p2�Ĵ�ط���λ��A2 ����߳�S
    def geoProblemISolutionCal(self,L1,B1,L2,B2):
        #l����
        list=L1.split("��")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("��")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("��")
                m=list[0]
                pass
            pass

        #l1����
        L1=self.geo.degToRad(d,f,m)
        L1=math.degrees(L1)
        #b1����
        list=B1.split("��")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("��")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("��")
                m=list[0]
                pass

            pass
        #b1����ת����
        B1=self.geo.degToRad(d,f,m)
        B1=math.degrees(B1)
        #l2����
        list=L2.split("��")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("��")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("��")
                m=list[0]
                pass
            pass

        #l2����
        L2=self.geo.degToRad(d,f,m)
        L2=math.degrees(L2)
        #b2����
        list=B2.split("��")
        d=list[0]
        f=0
        m=0
        list=list[1]
        if  list.strip():
            list=list.split("��")
            f=list[0]
            list=list[1]
            if list.strip():
                list=list.split("��")
                m=list[0]
                pass

            pass
        #����ת����
        B2=self.geo.degToRad(d,f,m)
        B2=math.degrees(B2)

        return self.geo.geoProblemISolutionCal(L1,B1,L2,B2)

    #����������ⷴ��
    def singleGeoProblemISolutionCal(self):
        L1=self.ui.gl1LEdit2.text()
        B1=self.ui.gb1LEdit2.text()
        L2=self.ui.gl2LEdit2.text()
        B2=self.ui.gb2LEdit2.text()

        if not L1.strip() or not B1.strip() or not L2.strip() or not B2.strip():
            tip="��Ϣ������û������\n\r"
            QMessageBox.information(self.ui,
            self.tr("��ʾ"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        rx=QRegExp(".+(��|��|��)$")
        i=rx.indexIn(L1)
        if i==-1:
            tip="��ʾ��L1�����Ǵ����!\n\rֵ��"+L1
            QMessageBox.critical(self.ui,
            self.tr("����"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(B1)
        if i==-1:
            tip="��ʾ��B1�����Ǵ����!\n\rֵ��"+B1
            QMessageBox.critical(self.ui,
            self.tr("����"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(L2)
        if i==-1:
            tip="��ʾ��L2�����Ǵ����!\n\rֵ��"+L2
            QMessageBox.critical(self.ui,
            self.tr("����"),
            tip,
            QMessageBox.Ok,
            QMessageBox.Ok)
            return
        i=rx.indexIn(B2)
        if i==-1:
            tip="��ʾ��B2�����Ǵ����!\n\rֵ��"+B2
            QMessageBox.critical(self.ui,
            self.tr("����"),
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
        A1=str(d)+"��"+str(m)+"��"+str(s)+"��"
        (d,m,s)=self.geo.deg_60(A2)
        s=s.quantize(Decimal("1.000"))
        if m<10:
            m="0"+str(m)
            pass
        if s<10:
            s="0"+str(s)
            pass
        A2=str(d)+"��"+str(m)+"��"+str(s)+"��"
        S=str(Decimal(str(S)).quantize(Decimal("1.000")))
        self.ui.gsLEdit2.setText(S)
        self.ui.ga1LEdit2.setText(A1)
        self.ui.ga2LEdit2.setText(A2)
        pass

    #����������ⷴ��
    def batGeoProblemISolutionCal(self):
        sum=self.ui.tableWidget11.rowCount()
        if sum<1:
            return
        i=0
        self.ui.progressBar.setVisible(True)
        self.ui.progressLabel.setText("���ȣ�")
        self.ui.progressBar.setValue(i)
        self.ui.tableWidget12.setRowCount(sum)
        self.eList[5]=self.ui.ellipsoidCBox.currentText()+"    �������(a="+str(self.geo.a)+"m,"+"f="+str(self.geo.f)+")"
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
            A1=str(d)+"��"+str(m)+"��"+str(s)+"��"
            (d,m,s)=self.geo.deg_60(A2)
            s=s.quantize(Decimal("1.000"))
            if m<10:
                m="0"+str(m)
                pass
            if s<10:
                s="0"+str(s)
                pass
            A2=str(d)+"��"+str(m)+"��"+str(s)+"��"
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
    #�ۺ���
    ######

    #ѡ��������
    def selectEllipsoid(self,text):
        if text=="CGCS 2000 ����":
            self.geo.setEllipsoidParameter2(6378137,1/298.257222101)
            self.ui.longLEdit.setDisabled(True)
            self.ui.oblatenessLEdit.setDisabled(True)
            pass

        elif  text=="��������˹������":
            self.geo.setEllipsoidParameter2(6378245,1/298.3)
            self.ui.longLEdit.setDisabled(True)
            self.ui.oblatenessLEdit.setDisabled(True)
            pass
        elif  text=="IUGG 1975 ����":
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


    #�Զ������Զ������������
    def customCalculation(self):
        if(self.ui.longLEdit.isEnabled()==True):
            self.geo.setEllipsoidParameter2(Decimal(self.ui.longLEdit.text()),Decimal(self.ui.oblatenessLEdit.text()))
            self.updateEllipsoidParameter()
            pass
        pass

    #�������͸ı�
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

    #��������ı�
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

    #��γ������ʱ��̬��ʾ��ȫ
    def lbhCompletiuon(self,text):
        lineEdit=self.sender()
        comp=None
        wordList=None
        di=text.find("��")
        length=len(text)

        def qss():
            if comp is not None and self.qss is not None:
                comp.popup().setStyleSheet(self.qss )
                pass
            return

        if di==-1:
            if (length!=0 and text[0]!="-") or (length>1):
                wordList=text+"��"
                #self.ui����ΪlineEdit,�γ����û�
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
            fi=text.find("��")
            if fi==-1:
                ft=text[di+1:length]
                wordList+=ft+"��"
                #self.ui����ΪlineEdit,�γ����û�
                comp=QCompleter([wordList],self.ui)
                lineEdit.setCompleter(comp)
                return qss()
            else:
                ft=text[di+1:fi]
                wordList+=ft+"��"
                if length-1==fi:
                    wordList=[wordList]

                    #self.ui����ΪlineEdit,�γ����û�
                    comp=QCompleter(wordList,self.ui)
                    lineEdit.setCompleter(comp)
                    return qss()
                else:
                    mi=text.find("��")
                    mt=None
                    if mi==-1:
                        mt=text[fi+1:length]
                        pass
                    else:
                        mt=text[fi+1:length-1]
                        pass
                    di=mt.find(".")
                    if di==-1:
                        wordList+= mt+"��"
                        #self.ui����ΪlineEdit,�γ����û�
                        comp=QCompleter([wordList],self.ui)
                        lineEdit.setCompleter(comp)
                        return qss()
                    else:
                        if di==len(mt)-1:
                            return
                        else:
                            t=mt[0:di]
                            wordList+= mt+"��"
                            #self.ui����ΪlineEdit,�γ����û�
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
        self.tr("�������ļ�"), "./", self.tr("All Files (*)"))
        if fileName.strip():
            index=self.ui.calCBox.currentIndex()
            f = open(fileName, 'r',encoding="utf_8")
            row=0

            def showTip(row,rowText,tableWidget):
                QMessageBox.critical(self.ui,
                self.tr("����"),
                "���ݸ�ʽ����ȷ!\n\rÿ��Ӧ���ÿո������������\n\rλ����:"+str(row)+"\n\r���ݣ�"+rowText,
                QMessageBox.Ok,
                QMessageBox.Ok)
                f.close()
                tableWidget.setRowCount(0)
                pass

            if index==0:
                self.ui.tableWidget1.setRowCount(0)
                rxl = QRegExp("(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))��(\d|[0-5]\d)��(\d|[0-5]\d)(\.[0-9]{1,3})?��)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))��(\d|[0-5]\d)��$)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))��$)")
                rxb=QRegExp("(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))��(\d|[0-5]\d)��(\d|[0-5]\d)(\.[0-9]{1,3})?��$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))��(\d|[0-5]\d)��$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))��$)")
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
                rxl = QRegExp("(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))��(\d|[0-5]\d)��(\d|[0-5]\d)(\.[0-9]{1,3})?��)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))��(\d|[0-5]\d)��$)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))��$)")
                rxb=QRegExp("(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))��(\d|[0-5]\d)��(\d|[0-5]\d)(\.[0-9]{1,3})?��$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))��(\d|[0-5]\d)��$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))��$)")
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
                rxl = QRegExp("(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))��(\d|[0-5]\d)��(\d|[0-5]\d)(\.[0-9]{1,3})?��)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))��(\d|[0-5]\d)��$)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))��$)")
                rxb=QRegExp("(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))��(\d|[0-5]\d)��(\d|[0-5]\d)(\.[0-9]{1,3})?��$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))��(\d|[0-5]\d)��$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))��$)")
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
                rxl = QRegExp("(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))��(\d|[0-5]\d)��(\d|[0-5]\d)(\.[0-9]{1,3})?��)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))��(\d|[0-5]\d)��$)|(^(\d|[1-9]\d|([1-2]\d\d|3([0-5]\d)|360))��$)")
                rxb=QRegExp("(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))��(\d|[0-5]\d)��(\d|[0-5]\d)(\.[0-9]{1,3})?��$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))��(\d|[0-5]\d)��$)|(^((-)?(\d|[1-9]\d|(1[0-7]\d|180)))��$)")
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

    #��������
    def exportData(self):
        index=self.ui.calCBox.currentIndex()

        def ft():
            (fileName,__)=QFileDialog.getSaveFileName(self.ui, self.tr("���������ļ�"),
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
            f.write("#����������ؿռ�ֱ������������\n#��ؿռ�ֱ������(X Y Z),��λ:m,%s\n"% (self.eList[index]))
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
            f.write("#����������ؿռ�ֱ�����귴����\n#�������(L B H),H��λ:m,%s\n"% (self.eList[index]))
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
            f.write("#��˹ͶӰ������\n#��˹ƽ��ֱ������(x y y�ٶ�),��λ:m,%s\n"% (self.eList[index]))
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
            f.write("#��˹ͶӰ������\n#�������(L B),%s\n"% (self.eList[index]))
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
            f.write("#�������������(L2 B2 A2),%s\n"% (self.eList[index]))
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
            f.write("#������ⷴ����(S A1 A2),%s\n"% (self.eList[index]))
            for i in range(sum):
                S=self.ui.tableWidget12.item(i,0).text()
                A1=self.ui.tableWidget12.item(i,1).text()
                A2=self.ui.tableWidget12.item(i,2).text()
                f.write('{:<16s}  {:<16s}  {:<16s}\n'.format(S,A1,A2))
                pass
            f.close()
            pass
        pass

    #��ز����ۺϼ���
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
