from PyQt5.QtWidgets import QMainWindow
from ui_source.three import *

class three_panel(QMainWindow,Ui_Frame):
    def __init__(self):
        super(three_panel,self).__init__()
        self.setupUi(self)