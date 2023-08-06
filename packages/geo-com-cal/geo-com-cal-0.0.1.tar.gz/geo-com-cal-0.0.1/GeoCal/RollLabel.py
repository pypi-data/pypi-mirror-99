# This Python file uses the following encoding:gbk
from PySide2.QtWidgets import QLabel
from PySide2.QtCore import QTimer,SIGNAL


class RollLabel(QLabel):
    def __init__(self,text,*args, **kwargs):
        super(RollLabel,self).__init__(*args, **kwargs)
        #记录文本位置
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

    #槽函数

    #滚动字幕
    def scrollCaption(self):
        #当截取的位置比字符串长时，从头开始
        if self.nPos > len(self.strScrollCation):
            self.nPos = 0
            pass
        self.setText(self.strScrollCation[self.nPos:])
        self.nPos+=1
        pass

    pass


pass
