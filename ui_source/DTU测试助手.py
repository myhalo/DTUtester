# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'DTU测试助手.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(971, 643)
        MainWindow.setFixedSize(MainWindow.width(), MainWindow.height())

        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(MainWindow.sizePolicy().hasHeightForWidth())
        MainWindow.setSizePolicy(sizePolicy)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.groupBox = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox.setGeometry(QtCore.QRect(10, 20, 641, 351))
        self.groupBox.setObjectName("groupBox")
        self.receive_textEdit = QtWidgets.QTextEdit(self.groupBox)
        self.receive_textEdit.setGeometry(QtCore.QRect(10, 20, 621, 321))
        self.receive_textEdit.setObjectName("receive_textEdit")
        self.groupBox_2 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_2.setGeometry(QtCore.QRect(650, 20, 311, 351))
        self.groupBox_2.setObjectName("groupBox_2")
        self.log_textEdit = QtWidgets.QTextEdit(self.groupBox_2)
        self.log_textEdit.setGeometry(QtCore.QRect(10, 20, 291, 321))
        self.log_textEdit.setObjectName("log_textEdit")
        self.groupBox_3 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_3.setGeometry(QtCore.QRect(10, 450, 391, 101))
        self.groupBox_3.setObjectName("groupBox_3")
        self.textEdit = QtWidgets.QTextEdit(self.groupBox_3)
        self.textEdit.setGeometry(QtCore.QRect(10, 20, 371, 71))
        self.textEdit.setObjectName("textEdit")
        self.send_pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.send_pushButton.setGeometry(QtCore.QRect(320, 560, 75, 23))
        self.send_pushButton.setObjectName("send_pushButton")
        self.hh_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.hh_checkBox.setGeometry(QtCore.QRect(20, 560, 71, 21))
        self.hh_checkBox.setObjectName("hh_checkBox")
        self.groupBox_4 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_4.setGeometry(QtCore.QRect(10, 370, 961, 71))
        self.groupBox_4.setTitle("")
        self.groupBox_4.setObjectName("groupBox_4")
        self.label_2 = QtWidgets.QLabel(self.groupBox_4)
        self.label_2.setGeometry(QtCore.QRect(90, 10, 31, 21))
        self.label_2.setStyleSheet("font: 10pt \"Arial\";")
        self.label_2.setObjectName("label_2")
        self.COM_Box = QtWidgets.QComboBox(self.groupBox_4)
        self.COM_Box.setGeometry(QtCore.QRect(130, 10, 71, 21))
        self.COM_Box.setObjectName("COM_Box")
        self.label = QtWidgets.QLabel(self.groupBox_4)
        self.label.setGeometry(QtCore.QRect(210, 10, 51, 21))
        self.label.setStyleSheet("font: 10pt \"Arial\";")
        self.label.setObjectName("label")
        self.baudrate_comboBox = QtWidgets.QComboBox(self.groupBox_4)
        self.baudrate_comboBox.setGeometry(QtCore.QRect(260, 10, 69, 22))
        self.baudrate_comboBox.setObjectName("baudrate_comboBox")
        self.label_3 = QtWidgets.QLabel(self.groupBox_4)
        self.label_3.setGeometry(QtCore.QRect(340, 10, 41, 20))
        self.label_3.setObjectName("label_3")
        self.Databits_comboBox = QtWidgets.QComboBox(self.groupBox_4)
        self.Databits_comboBox.setGeometry(QtCore.QRect(390, 10, 69, 22))
        self.Databits_comboBox.setObjectName("Databits_comboBox")
        self.label_4 = QtWidgets.QLabel(self.groupBox_4)
        self.label_4.setGeometry(QtCore.QRect(470, 10, 41, 20))
        self.label_4.setObjectName("label_4")
        self.parity_comboBox = QtWidgets.QComboBox(self.groupBox_4)
        self.parity_comboBox.setGeometry(QtCore.QRect(520, 10, 69, 22))
        self.parity_comboBox.setObjectName("parity_comboBox")
        self.label_5 = QtWidgets.QLabel(self.groupBox_4)
        self.label_5.setGeometry(QtCore.QRect(600, 10, 41, 20))
        self.label_5.setObjectName("label_5")
        self.Stopbits_comboBox = QtWidgets.QComboBox(self.groupBox_4)
        self.Stopbits_comboBox.setGeometry(QtCore.QRect(650, 10, 69, 22))
        self.Stopbits_comboBox.setObjectName("Stopbits_comboBox")
        self.comDetection_pushButton = QtWidgets.QPushButton(self.groupBox_4)
        self.comDetection_pushButton.setGeometry(QtCore.QRect(10, 10, 75, 23))
        self.comDetection_pushButton.setObjectName("comDetection_pushButton")
        self.open_pushButton = QtWidgets.QPushButton(self.groupBox_4)
        self.open_pushButton.setGeometry(QtCore.QRect(10, 40, 75, 23))
        self.open_pushButton.setObjectName("open_pushButton")
        self.close_pushButton = QtWidgets.QPushButton(self.groupBox_4)
        self.close_pushButton.setGeometry(QtCore.QRect(90, 40, 75, 23))
        self.close_pushButton.setObjectName("close_pushButton")
        self.saveDATA_pushButton = QtWidgets.QPushButton(self.groupBox_4)
        self.saveDATA_pushButton.setGeometry(QtCore.QRect(170, 40, 75, 23))
        self.saveDATA_pushButton.setObjectName("saveDATA_pushButton")
        self.clearDATA_pushButton = QtWidgets.QPushButton(self.groupBox_4)
        self.clearDATA_pushButton.setGeometry(QtCore.QRect(750, 10, 75, 23))
        self.clearDATA_pushButton.setObjectName("clearDATA_pushButton")
        self.HEXShow_checkBox = QtWidgets.QCheckBox(self.groupBox_4)
        self.HEXShow_checkBox.setGeometry(QtCore.QRect(260, 40, 71, 21))
        self.HEXShow_checkBox.setStyleSheet("font: 10pt \"Arial\";")
        self.HEXShow_checkBox.setObjectName("HEXShow_checkBox")
        self.clearLog_pushButton = QtWidgets.QPushButton(self.groupBox_4)
        self.clearLog_pushButton.setGeometry(QtCore.QRect(850, 10, 75, 23))
        self.clearLog_pushButton.setObjectName("clearLog_pushButton")
        self.TOP_checkBox = QtWidgets.QCheckBox(self.groupBox_4)
        self.TOP_checkBox.setGeometry(QtCore.QRect(340, 40, 51, 21))
        self.TOP_checkBox.setStyleSheet("font: 10pt \"Arial\";")
        self.TOP_checkBox.setObjectName("TOP_checkBox")
        self.time_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.time_checkBox.setGeometry(QtCore.QRect(90, 560, 71, 21))
        self.time_checkBox.setObjectName("time_checkBox")
        self.time_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.time_lineEdit.setGeometry(QtCore.QRect(160, 560, 41, 20))
        self.time_lineEdit.setText("")
        self.time_lineEdit.setObjectName("time_lineEdit")
        self.label_6 = QtWidgets.QLabel(self.centralwidget)
        self.label_6.setGeometry(QtCore.QRect(210, 560, 21, 21))
        self.label_6.setObjectName("label_6")
        self.HEXsend_checkBox = QtWidgets.QCheckBox(self.centralwidget)
        self.HEXsend_checkBox.setGeometry(QtCore.QRect(240, 560, 71, 21))
        self.HEXsend_checkBox.setObjectName("HEXsend_checkBox")
        self.groupBox_5 = QtWidgets.QGroupBox(self.centralwidget)
        self.groupBox_5.setGeometry(QtCore.QRect(409, 449, 551, 141))
        self.groupBox_5.setObjectName("groupBox_5")
        self.frame = QtWidgets.QFrame(self.groupBox_5)
        self.frame.setGeometry(QtCore.QRect(0, -1, 81, 141))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.F2X14_16_D_pushButton = QtWidgets.QPushButton(self.frame)
        self.F2X14_16_D_pushButton.setGeometry(QtCore.QRect(0, 30, 81, 23))
        self.F2X14_16_D_pushButton.setObjectName("F2X14_16_D_pushButton")
        self.F2X16_pushButton = QtWidgets.QPushButton(self.frame)
        self.F2X16_pushButton.setGeometry(QtCore.QRect(0, 70, 81, 23))
        self.F2X16_pushButton.setObjectName("F2X16_pushButton")
        self.frame_2 = QtWidgets.QFrame(self.groupBox_5)
        self.frame_2.setGeometry(QtCore.QRect(80, 10, 471, 131))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 971, 23))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "DTU测试助手--by花蛤与蟹"))
        self.groupBox.setTitle(_translate("MainWindow", "串口接收"))
        self.receive_textEdit.setWhatsThis(_translate("MainWindow", "<html><head/><body><p><br/></p></body></html>"))
        self.groupBox_2.setTitle(_translate("MainWindow", "测试日志"))
        self.groupBox_3.setTitle(_translate("MainWindow", "串口发送"))
        self.send_pushButton.setText(_translate("MainWindow", "发送"))
        self.hh_checkBox.setText(_translate("MainWindow", "添加换行"))
        self.label_2.setText(_translate("MainWindow", "串口："))
        self.label.setText(_translate("MainWindow", "波特率："))
        self.label_3.setText(_translate("MainWindow", "数据位："))
        self.label_4.setText(_translate("MainWindow", "校验位："))
        self.label_5.setText(_translate("MainWindow", "停止位："))
        self.comDetection_pushButton.setText(_translate("MainWindow", "串口检测"))
        self.open_pushButton.setText(_translate("MainWindow", "打开"))
        self.close_pushButton.setText(_translate("MainWindow", "关闭"))
        self.saveDATA_pushButton.setText(_translate("MainWindow", "保存数据"))
        self.clearDATA_pushButton.setText(_translate("MainWindow", "清除接收"))
        self.HEXShow_checkBox.setText(_translate("MainWindow", "HEX显示"))
        self.clearLog_pushButton.setText(_translate("MainWindow", "清除日志"))
        self.TOP_checkBox.setText(_translate("MainWindow", "置顶"))
        self.time_checkBox.setText(_translate("MainWindow", "定时发送:"))
        self.label_6.setText(_translate("MainWindow", "ms"))
        self.HEXsend_checkBox.setText(_translate("MainWindow", "HEX发送"))
        self.groupBox_5.setTitle(_translate("MainWindow", "DTU设置"))
        self.F2X14_16_D_pushButton.setText(_translate("MainWindow", "F2X14(16)-D"))
        self.F2X16_pushButton.setText(_translate("MainWindow", "F2X16"))

