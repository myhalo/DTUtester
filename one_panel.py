from PyQt5.QtWidgets import QMainWindow
from ui_source.one import *

class one_panel(QMainWindow,Ui_Frame):
    def __init__(self):
        super(one_panel,self).__init__()
        self.setupUi(self)