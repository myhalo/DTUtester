# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'FrameDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(431, 424)
        Dialog.setMinimumSize(QtCore.QSize(431, 424))
        Dialog.setMaximumSize(QtCore.QSize(431, 424))
        self.gridLayoutWidget = QtWidgets.QWidget(Dialog)
        self.gridLayoutWidget.setGeometry(QtCore.QRect(20, 20, 391, 331))
        self.gridLayoutWidget.setObjectName("gridLayoutWidget")
        self.gridLayout = QtWidgets.QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.LoginAcFrameType_comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.LoginAcFrameType_comboBox.setObjectName("LoginAcFrameType_comboBox")
        self.LoginAcFrameType_comboBox.addItem("")
        self.LoginAcFrameType_comboBox.addItem("")
        self.gridLayout.addWidget(self.LoginAcFrameType_comboBox, 2, 1, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.LoginFrameType_comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.LoginFrameType_comboBox.setObjectName("LoginFrameType_comboBox")
        self.LoginFrameType_comboBox.addItem("")
        self.LoginFrameType_comboBox.addItem("")
        self.gridLayout.addWidget(self.LoginFrameType_comboBox, 0, 1, 1, 1)
        self.LoginFrame_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.LoginFrame_lineEdit.setObjectName("LoginFrame_lineEdit")
        self.gridLayout.addWidget(self.LoginFrame_lineEdit, 1, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.HeartFrameType_comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.HeartFrameType_comboBox.setObjectName("HeartFrameType_comboBox")
        self.HeartFrameType_comboBox.addItem("")
        self.HeartFrameType_comboBox.addItem("")
        self.gridLayout.addWidget(self.HeartFrameType_comboBox, 4, 1, 1, 1)
        self.label_6 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_6.setObjectName("label_6")
        self.gridLayout.addWidget(self.label_6, 5, 0, 1, 1)
        self.label_10 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_10.setObjectName("label_10")
        self.gridLayout.addWidget(self.label_10, 9, 0, 1, 1)
        self.HeartFrame_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.HeartFrame_lineEdit.setObjectName("HeartFrame_lineEdit")
        self.gridLayout.addWidget(self.HeartFrame_lineEdit, 5, 1, 1, 1)
        self.LoginAcFrame_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.LoginAcFrame_lineEdit.setObjectName("LoginAcFrame_lineEdit")
        self.gridLayout.addWidget(self.LoginAcFrame_lineEdit, 3, 1, 1, 1)
        self.OutFrame_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.OutFrame_lineEdit.setObjectName("OutFrame_lineEdit")
        self.gridLayout.addWidget(self.OutFrame_lineEdit, 9, 1, 1, 1)
        self.label_7 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_7.setObjectName("label_7")
        self.gridLayout.addWidget(self.label_7, 6, 0, 1, 1)
        self.HeartAcFrameType_comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.HeartAcFrameType_comboBox.setObjectName("HeartAcFrameType_comboBox")
        self.HeartAcFrameType_comboBox.addItem("")
        self.HeartAcFrameType_comboBox.addItem("")
        self.gridLayout.addWidget(self.HeartAcFrameType_comboBox, 6, 1, 1, 1)
        self.label_5 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_5.setObjectName("label_5")
        self.gridLayout.addWidget(self.label_5, 4, 0, 1, 1)
        self.OutAcFrameType_comboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.OutAcFrameType_comboBox.setObjectName("OutAcFrameType_comboBox")
        self.OutAcFrameType_comboBox.addItem("")
        self.OutAcFrameType_comboBox.addItem("")
        self.gridLayout.addWidget(self.OutAcFrameType_comboBox, 10, 1, 1, 1)
        self.HeartAcFrame_lineEdit = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.HeartAcFrame_lineEdit.setObjectName("HeartAcFrame_lineEdit")
        self.gridLayout.addWidget(self.HeartAcFrame_lineEdit, 7, 1, 1, 1)
        self.label_8 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_8.setObjectName("label_8")
        self.gridLayout.addWidget(self.label_8, 7, 0, 1, 1)
        self.OutFrameTypecomboBox = QtWidgets.QComboBox(self.gridLayoutWidget)
        self.OutFrameTypecomboBox.setObjectName("OutFrameTypecomboBox")
        self.OutFrameTypecomboBox.addItem("")
        self.OutFrameTypecomboBox.addItem("")
        self.gridLayout.addWidget(self.OutFrameTypecomboBox, 8, 1, 1, 1)
        self.label_11 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_11.setObjectName("label_11")
        self.gridLayout.addWidget(self.label_11, 10, 0, 1, 1)
        self.label_9 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_9.setObjectName("label_9")
        self.gridLayout.addWidget(self.label_9, 8, 0, 1, 1)
        self.label_12 = QtWidgets.QLabel(self.gridLayoutWidget)
        self.label_12.setObjectName("label_12")
        self.gridLayout.addWidget(self.label_12, 11, 0, 1, 1)
        self.OutFrame_lineEdit_2 = QtWidgets.QLineEdit(self.gridLayoutWidget)
        self.OutFrame_lineEdit_2.setObjectName("OutFrame_lineEdit_2")
        self.gridLayout.addWidget(self.OutFrame_lineEdit_2, 11, 1, 1, 1)
        self.read_pushButton = QtWidgets.QPushButton(Dialog)
        self.read_pushButton.setGeometry(QtCore.QRect(171, 374, 75, 23))
        self.read_pushButton.setObjectName("read_pushButton")
        self.ok_pushButton = QtWidgets.QPushButton(Dialog)
        self.ok_pushButton.setGeometry(QtCore.QRect(253, 374, 75, 23))
        self.ok_pushButton.setObjectName("ok_pushButton")
        self.cancel_pushButton = QtWidgets.QPushButton(Dialog)
        self.cancel_pushButton.setGeometry(QtCore.QRect(334, 374, 75, 23))
        self.cancel_pushButton.setObjectName("cancel_pushButton")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.LoginFrameType_comboBox, self.LoginFrame_lineEdit)
        Dialog.setTabOrder(self.LoginFrame_lineEdit, self.LoginAcFrameType_comboBox)
        Dialog.setTabOrder(self.LoginAcFrameType_comboBox, self.LoginAcFrame_lineEdit)
        Dialog.setTabOrder(self.LoginAcFrame_lineEdit, self.HeartFrameType_comboBox)
        Dialog.setTabOrder(self.HeartFrameType_comboBox, self.HeartFrame_lineEdit)
        Dialog.setTabOrder(self.HeartFrame_lineEdit, self.HeartAcFrameType_comboBox)
        Dialog.setTabOrder(self.HeartAcFrameType_comboBox, self.HeartAcFrame_lineEdit)
        Dialog.setTabOrder(self.HeartAcFrame_lineEdit, self.OutFrameTypecomboBox)
        Dialog.setTabOrder(self.OutFrameTypecomboBox, self.OutFrame_lineEdit)
        Dialog.setTabOrder(self.OutFrame_lineEdit, self.OutAcFrameType_comboBox)
        Dialog.setTabOrder(self.OutAcFrameType_comboBox, self.OutFrame_lineEdit_2)
        Dialog.setTabOrder(self.OutFrame_lineEdit_2, self.read_pushButton)
        Dialog.setTabOrder(self.read_pushButton, self.ok_pushButton)
        Dialog.setTabOrder(self.ok_pushButton, self.cancel_pushButton)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "登录帧类型："))
        self.label_3.setText(_translate("Dialog", "登录应答帧类型："))
        self.LoginAcFrameType_comboBox.setItemText(0, _translate("Dialog", "ASCII"))
        self.LoginAcFrameType_comboBox.setItemText(1, _translate("Dialog", "HEX"))
        self.label_4.setText(_translate("Dialog", "登录应答帧："))
        self.LoginFrameType_comboBox.setItemText(0, _translate("Dialog", "ASCII"))
        self.LoginFrameType_comboBox.setItemText(1, _translate("Dialog", "HEX"))
        self.label_2.setText(_translate("Dialog", "登录帧："))
        self.HeartFrameType_comboBox.setItemText(0, _translate("Dialog", "ASCII"))
        self.HeartFrameType_comboBox.setItemText(1, _translate("Dialog", "HEX"))
        self.label_6.setText(_translate("Dialog", "心跳帧："))
        self.label_10.setText(_translate("Dialog", "退出帧："))
        self.label_7.setText(_translate("Dialog", "心跳应答帧类型："))
        self.HeartAcFrameType_comboBox.setItemText(0, _translate("Dialog", "ASCII"))
        self.HeartAcFrameType_comboBox.setItemText(1, _translate("Dialog", "HEX"))
        self.label_5.setText(_translate("Dialog", "心跳帧类型："))
        self.OutAcFrameType_comboBox.setItemText(0, _translate("Dialog", "ASCII"))
        self.OutAcFrameType_comboBox.setItemText(1, _translate("Dialog", "HEX"))
        self.label_8.setText(_translate("Dialog", "心跳应答帧："))
        self.OutFrameTypecomboBox.setItemText(0, _translate("Dialog", "ASCII"))
        self.OutFrameTypecomboBox.setItemText(1, _translate("Dialog", "HEX"))
        self.label_11.setText(_translate("Dialog", "退出应答帧类型："))
        self.label_9.setText(_translate("Dialog", "退出帧类型："))
        self.label_12.setText(_translate("Dialog", "退出应答帧："))
        self.read_pushButton.setText(_translate("Dialog", "读取"))
        self.ok_pushButton.setText(_translate("Dialog", "配置"))
        self.cancel_pushButton.setText(_translate("Dialog", "取消"))

