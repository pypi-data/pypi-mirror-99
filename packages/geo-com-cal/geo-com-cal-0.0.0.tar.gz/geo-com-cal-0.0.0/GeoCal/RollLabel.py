# This Python file uses the following encoding:gbk
from PySide2.QtWidgets import QLabel
from PySide2.QtCore import QTimer,SIGNAL


class RollLabel(QLabel):
    def __init__(self,text,*args, **kwargs):
        super(RollLabel,self).__init__(*args, **kwargs)
        #��¼�ı�λ��
        self.nPos = 0
        self.setText(text)
        self.timer = QTimer(self)
        self.connect(self.timer, SIGNAL("timeout()"), self.scrollCaption)
        self.timer.start(500)
        self.strScrollCation=self.text()
        pass

    def setStrScrollCation(self,text):
        self.strScrollCation=text
        pass

    #�ۺ���

    #������Ļ
    def scrollCaption(self):
        #����ȡ��λ�ñ��ַ�����ʱ����ͷ��ʼ
        if self.nPos > len(self.strScrollCation):
            self.nPos = 0
            pass
        self.setText(self.strScrollCation[self.nPos:])
        self.nPos+=1
        pass

    pass


pass
