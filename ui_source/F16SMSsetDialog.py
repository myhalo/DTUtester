# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F16SMSsetDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(284, 186)
        Dialog.setMinimumSize(QtCore.QSize(284, 186))
        Dialog.setMaximumSize(QtCore.QSize(284, 186))
        self.groupBox = QtWidgets.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 20, 243, 110))
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.gridLayout = QtWidgets.QGridLayout(self.groupBox)
        self.gridLayout.setObjectName("gridLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.gridLayout.addWidget(self.label, 0, 0, 1, 1)
        self.SMSset_comboBox = QtWidgets.QComboBox(self.groupBox)
        self.SMSset_comboBox.setObjectName("SMSset_comboBox")
        self.SMSset_comboBox.addItem("")
        self.SMSset_comboBox.addItem("")
        self.gridLayout.addWidget(self.SMSset_comboBox, 0, 1, 1, 1)
        self.SMSset_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.SMSset_lineEdit.setObjectName("SMSset_lineEdit")
        self.gridLayout.addWidget(self.SMSset_lineEdit, 2, 1, 1, 1)
        self.admin_lineEdit = QtWidgets.QLineEdit(self.groupBox)
        self.admin_lineEdit.setObjectName("admin_lineEdit")
        self.gridLayout.addWidget(self.admin_lineEdit, 3, 1, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 3, 0, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 2, 0, 1, 1)
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(120, 150, 61, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(200, 150, 61, 23))
        self.pushButton_3.setObjectName("pushButton_3")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.SMSset_comboBox, self.SMSset_lineEdit)
        Dialog.setTabOrder(self.SMSset_lineEdit, self.admin_lineEdit)
        Dialog.setTabOrder(self.admin_lineEdit, self.pushButton_2)
        Dialog.setTabOrder(self.pushButton_2, self.pushButton_3)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "    短信配置："))
        self.SMSset_comboBox.setItemText(0, _translate("Dialog", "关闭"))
        self.SMSset_comboBox.setItemText(1, _translate("Dialog", "开启"))
        self.label_3.setText(_translate("Dialog", "  管理员号码："))
        self.label_2.setText(_translate("Dialog", "短信配置密码："))
        self.pushButton_2.setText(_translate("Dialog", "配置"))
        self.pushButton_3.setText(_translate("Dialog", "取消"))

