# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'inputIPandPORTDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(292, 382)
        Dialog.setMinimumSize(QtCore.QSize(292, 348))
        Dialog.setFixedSize(Dialog.width(), Dialog.height())

        self.ok_pushButton = QtWidgets.QPushButton(Dialog)
        self.ok_pushButton.setGeometry(QtCore.QRect(122, 341, 75, 23))
        self.ok_pushButton.setObjectName("ok_pushButton")
        self.cancel_pushButton = QtWidgets.QPushButton(Dialog)
        self.cancel_pushButton.setGeometry(QtCore.QRect(203, 341, 75, 23))
        self.cancel_pushButton.setObjectName("cancel_pushButton")
        self.label_3 = QtWidgets.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(21, 76, 102, 16))
        self.label_3.setObjectName("label_3")
        self.IP1_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.IP1_lineEdit.setGeometry(QtCore.QRect(129, 76, 133, 20))
        self.IP1_lineEdit.setObjectName("IP1_lineEdit")
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(21, 22, 102, 16))
        self.label.setObjectName("label")
        self.IP_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.IP_lineEdit.setGeometry(QtCore.QRect(129, 22, 133, 20))
        self.IP_lineEdit.setObjectName("IP_lineEdit")
        self.label_2 = QtWidgets.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(21, 49, 102, 16))
        self.label_2.setObjectName("label_2")
        self.IP3_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.IP3_lineEdit.setGeometry(QtCore.QRect(129, 184, 133, 20))
        self.IP3_lineEdit.setObjectName("IP3_lineEdit")
        self.label_8 = QtWidgets.QLabel(Dialog)
        self.label_8.setGeometry(QtCore.QRect(21, 211, 102, 16))
        self.label_8.setObjectName("label_8")
        self.IP2_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.IP2_lineEdit.setGeometry(QtCore.QRect(129, 130, 133, 20))
        self.IP2_lineEdit.setObjectName("IP2_lineEdit")
        self.label_9 = QtWidgets.QLabel(Dialog)
        self.label_9.setGeometry(QtCore.QRect(21, 238, 102, 16))
        self.label_9.setObjectName("label_9")
        self.label_4 = QtWidgets.QLabel(Dialog)
        self.label_4.setGeometry(QtCore.QRect(21, 103, 102, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Dialog)
        self.label_5.setGeometry(QtCore.QRect(21, 130, 102, 16))
        self.label_5.setObjectName("label_5")
        self.PORT3_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.PORT3_lineEdit.setGeometry(QtCore.QRect(129, 211, 61, 20))
        self.PORT3_lineEdit.setObjectName("PORT3_lineEdit")
        self.PORT_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.PORT_lineEdit.setGeometry(QtCore.QRect(129, 49, 61, 20))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(50)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.PORT_lineEdit.sizePolicy().hasHeightForWidth())
        self.PORT_lineEdit.setSizePolicy(sizePolicy)
        self.PORT_lineEdit.setObjectName("PORT_lineEdit")
        self.PORT4_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.PORT4_lineEdit.setGeometry(QtCore.QRect(129, 265, 61, 20))
        self.PORT4_lineEdit.setObjectName("PORT4_lineEdit")
        self.label_10 = QtWidgets.QLabel(Dialog)
        self.label_10.setGeometry(QtCore.QRect(21, 265, 102, 16))
        self.label_10.setObjectName("label_10")
        self.IP4_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.IP4_lineEdit.setGeometry(QtCore.QRect(129, 238, 133, 20))
        self.IP4_lineEdit.setObjectName("IP4_lineEdit")
        self.label_7 = QtWidgets.QLabel(Dialog)
        self.label_7.setGeometry(QtCore.QRect(21, 184, 102, 16))
        self.label_7.setObjectName("label_7")
        self.PORT2_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.PORT2_lineEdit.setGeometry(QtCore.QRect(129, 157, 61, 20))
        self.PORT2_lineEdit.setObjectName("PORT2_lineEdit")
        self.label_6 = QtWidgets.QLabel(Dialog)
        self.label_6.setGeometry(QtCore.QRect(21, 157, 102, 16))
        self.label_6.setObjectName("label_6")
        self.PORT1_lineEdit = QtWidgets.QLineEdit(Dialog)
        self.PORT1_lineEdit.setGeometry(QtCore.QRect(129, 103, 61, 20))
        self.PORT1_lineEdit.setObjectName("PORT1_lineEdit")
        self.read_pushButton = QtWidgets.QPushButton(Dialog)
        self.read_pushButton.setGeometry(QtCore.QRect(41, 341, 75, 23))
        self.read_pushButton.setObjectName("read_pushButton")
        self.label_11 = QtWidgets.QLabel(Dialog)
        self.label_11.setGeometry(QtCore.QRect(20, 290, 101, 41))
        self.label_11.setObjectName("label_11")
        self.comboBox = QtWidgets.QComboBox(Dialog)
        self.comboBox.setGeometry(QtCore.QRect(130, 300, 61, 20))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.ok_pushButton.raise_()
        self.cancel_pushButton.raise_()
        self.label_3.raise_()
        self.IP1_lineEdit.raise_()
        self.label.raise_()
        self.label_2.raise_()
        self.IP3_lineEdit.raise_()
        self.label_8.raise_()
        self.IP2_lineEdit.raise_()
        self.label_9.raise_()
        self.label_4.raise_()
        self.label_5.raise_()
        self.PORT3_lineEdit.raise_()
        self.PORT_lineEdit.raise_()
        self.PORT4_lineEdit.raise_()
        self.label_10.raise_()
        self.IP4_lineEdit.raise_()
        self.label_7.raise_()
        self.PORT2_lineEdit.raise_()
        self.label_6.raise_()
        self.PORT1_lineEdit.raise_()
        self.read_pushButton.raise_()
        self.IP_lineEdit.raise_()
        self.label_11.raise_()
        self.comboBox.raise_()

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.IP_lineEdit, self.PORT_lineEdit)
        Dialog.setTabOrder(self.PORT_lineEdit, self.IP1_lineEdit)
        Dialog.setTabOrder(self.IP1_lineEdit, self.PORT1_lineEdit)
        Dialog.setTabOrder(self.PORT1_lineEdit, self.IP2_lineEdit)
        Dialog.setTabOrder(self.IP2_lineEdit, self.PORT2_lineEdit)
        Dialog.setTabOrder(self.PORT2_lineEdit, self.IP3_lineEdit)
        Dialog.setTabOrder(self.IP3_lineEdit, self.PORT3_lineEdit)
        Dialog.setTabOrder(self.PORT3_lineEdit, self.IP4_lineEdit)
        Dialog.setTabOrder(self.IP4_lineEdit, self.PORT4_lineEdit)
        Dialog.setTabOrder(self.PORT4_lineEdit, self.read_pushButton)
        Dialog.setTabOrder(self.read_pushButton, self.ok_pushButton)
        Dialog.setTabOrder(self.ok_pushButton, self.cancel_pushButton)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.ok_pushButton.setText(_translate("Dialog", "配置"))
        self.cancel_pushButton.setText(_translate("Dialog", "取消"))
        self.label_3.setText(_translate("Dialog", "扩展1中心IP地址："))
        self.label.setText(_translate("Dialog", "   主中心IP地址："))
        self.label_2.setText(_translate("Dialog", "     主中心端口："))
        self.label_8.setText(_translate("Dialog", "  扩展3中心端口："))
        self.label_9.setText(_translate("Dialog", "扩展4中心IP地址："))
        self.label_4.setText(_translate("Dialog", "  扩展1中心端口："))
        self.label_5.setText(_translate("Dialog", "扩展2中心IP地址："))
        self.label_10.setText(_translate("Dialog", "  扩展4中心端口："))
        self.label_7.setText(_translate("Dialog", "扩展3中心IP地址："))
        self.label_6.setText(_translate("Dialog", "  扩展2中心端口："))
        self.read_pushButton.setText(_translate("Dialog", "读取"))
        self.label_11.setText(_translate("Dialog", "  轮询模式(Y/N)："))
        self.comboBox.setItemText(0, _translate("Dialog", "Y"))
        self.comboBox.setItemText(1, _translate("Dialog", "N"))

