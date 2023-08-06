# This Python file uses the following encoding: gbk
from .UI import UI
from .Geo import Geo
from decimal import Decimal


class Task:
    def __init__(self):
        #ui
        self.__ui_Task_785=None
        #计算类成员
        self.geo=Geo()
        pass

    #call ui
    def show(self):
        self.__ui_Task_785=UI()
        self.__ui_Task_785.show()
        pass

    pass
