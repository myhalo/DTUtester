# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'F16WORKtypeDialog.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(512, 542)
        Dialog.setMinimumSize(QtCore.QSize(512, 542))
        Dialog.setMaximumSize(QtCore.QSize(512, 542))
        self.label = QtWidgets.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 20, 61, 21))
        self.label.setObjectName("label")
        self.protocolType_comboBox = QtWidgets.QComboBox(Dialog)
        self.protocolType_comboBox.setGeometry(QtCore.QRect(80, 20, 69, 22))
        self.protocolType_comboBox.setObjectName("protocolType_comboBox")
        self.protocolType_comboBox.addItem("")
        self.protocolType_comboBox.addItem("")
        self.protocolType_comboBox.addItem("")
        self.protocolType_comboBox.addItem("")
        self.protocolType_comboBox.addItem("")
        self.protocolType_comboBox.addItem("")
        self.protocolType_comboBox.addItem("")
        self.protocolType_comboBox.addItem("")
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setGeometry(QtCore.QRect(20, 50, 481, 201))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.prot_frame = QtWidgets.QFrame(self.frame)
        self.prot_frame.setGeometry(QtCore.QRect(0, 0, 581, 201))
        self.prot_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.prot_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.prot_frame.setObjectName("prot_frame")
        self.label_2 = QtWidgets.QLabel(self.prot_frame)
        self.label_2.setGeometry(QtCore.QRect(50, 20, 54, 21))
        self.label_2.setObjectName("label_2")
        self.lineEdit = QtWidgets.QLineEdit(self.prot_frame)
        self.lineEdit.setGeometry(QtCore.QRect(100, 20, 113, 20))
        self.lineEdit.setObjectName("lineEdit")
        self.label_3 = QtWidgets.QLabel(self.prot_frame)
        self.label_3.setGeometry(QtCore.QRect(280, 20, 61, 21))
        self.label_3.setObjectName("label_3")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.prot_frame)
        self.lineEdit_2.setGeometry(QtCore.QRect(340, 20, 113, 20))
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.label_4 = QtWidgets.QLabel(self.prot_frame)
        self.label_4.setGeometry(QtCore.QRect(10, 60, 91, 21))
        self.label_4.setObjectName("label_4")
        self.comboBox = QtWidgets.QComboBox(self.prot_frame)
        self.comboBox.setGeometry(QtCore.QRect(100, 60, 113, 20))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("")
        self.comboBox.addItem("")
        self.DCUDPandDCTCP_frame = QtWidgets.QFrame(self.frame)
        self.DCUDPandDCTCP_frame.setGeometry(QtCore.QRect(0, 0, 581, 201))
        self.DCUDPandDCTCP_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.DCUDPandDCTCP_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.DCUDPandDCTCP_frame.setObjectName("DCUDPandDCTCP_frame")
        self.label_43 = QtWidgets.QLabel(self.DCUDPandDCTCP_frame)
        self.label_43.setGeometry(QtCore.QRect(40, 20, 61, 21))
        self.label_43.setObjectName("label_43")
        self.lineEdit_23 = QtWidgets.QLineEdit(self.DCUDPandDCTCP_frame)
        self.lineEdit_23.setGeometry(QtCore.QRect(100, 20, 113, 20))
        self.lineEdit_23.setObjectName("lineEdit_23")
        self.TRNS_frame = QtWidgets.QFrame(self.frame)
        self.TRNS_frame.setGeometry(QtCore.QRect(0, 120, 421, 31))
        self.TRNS_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.TRNS_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.TRNS_frame.setObjectName("TRNS_frame")
        self.SMSCLI_frame = QtWidgets.QFrame(self.frame)
        self.SMSCLI_frame.setGeometry(QtCore.QRect(-1, -1, 581, 201))
        self.SMSCLI_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.SMSCLI_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SMSCLI_frame.setObjectName("SMSCLI_frame")
        self.label_44 = QtWidgets.QLabel(self.SMSCLI_frame)
        self.label_44.setGeometry(QtCore.QRect(20, 20, 81, 21))
        self.label_44.setObjectName("label_44")
        self.lineEdit_24 = QtWidgets.QLineEdit(self.SMSCLI_frame)
        self.lineEdit_24.setGeometry(QtCore.QRect(100, 20, 361, 20))
        self.lineEdit_24.setObjectName("lineEdit_24")
        self.label_45 = QtWidgets.QLabel(self.SMSCLI_frame)
        self.label_45.setGeometry(QtCore.QRect(20, 50, 81, 21))
        self.label_45.setObjectName("label_45")
        self.lineEdit_25 = QtWidgets.QLineEdit(self.SMSCLI_frame)
        self.lineEdit_25.setGeometry(QtCore.QRect(100, 50, 361, 20))
        self.lineEdit_25.setObjectName("lineEdit_25")
        self.label_46 = QtWidgets.QLabel(self.SMSCLI_frame)
        self.label_46.setGeometry(QtCore.QRect(20, 80, 81, 21))
        self.label_46.setObjectName("label_46")
        self.lineEdit_26 = QtWidgets.QLineEdit(self.SMSCLI_frame)
        self.lineEdit_26.setGeometry(QtCore.QRect(100, 80, 361, 20))
        self.lineEdit_26.setObjectName("lineEdit_26")
        self.label_47 = QtWidgets.QLabel(self.SMSCLI_frame)
        self.label_47.setGeometry(QtCore.QRect(20, 110, 81, 16))
        self.label_47.setObjectName("label_47")
        self.lineEdit_27 = QtWidgets.QLineEdit(self.SMSCLI_frame)
        self.lineEdit_27.setGeometry(QtCore.QRect(100, 110, 361, 20))
        self.lineEdit_27.setObjectName("lineEdit_27")
        self.label_48 = QtWidgets.QLabel(self.SMSCLI_frame)
        self.label_48.setGeometry(QtCore.QRect(20, 140, 81, 16))
        self.label_48.setObjectName("label_48")
        self.lineEdit_28 = QtWidgets.QLineEdit(self.SMSCLI_frame)
        self.lineEdit_28.setGeometry(QtCore.QRect(100, 140, 361, 20))
        self.lineEdit_28.setObjectName("lineEdit_28")
        self.label_49 = QtWidgets.QLabel(self.SMSCLI_frame)
        self.label_49.setGeometry(QtCore.QRect(10, 170, 91, 20))
        self.label_49.setObjectName("label_49")
        self.comboBox_18 = QtWidgets.QComboBox(self.SMSCLI_frame)
        self.comboBox_18.setGeometry(QtCore.QRect(100, 170, 69, 22))
        self.comboBox_18.setObjectName("comboBox_18")
        self.comboBox_18.addItem("")
        self.comboBox_18.addItem("")
        self.label_50 = QtWidgets.QLabel(self.SMSCLI_frame)
        self.label_50.setGeometry(QtCore.QRect(190, 170, 111, 21))
        self.label_50.setObjectName("label_50")
        self.comboBox_19 = QtWidgets.QComboBox(self.SMSCLI_frame)
        self.comboBox_19.setGeometry(QtCore.QRect(300, 170, 69, 22))
        self.comboBox_19.setObjectName("comboBox_19")
        self.comboBox_19.addItem("")
        self.comboBox_19.addItem("")
        self.SMSSER_frame = QtWidgets.QFrame(self.frame)
        self.SMSSER_frame.setGeometry(QtCore.QRect(-1, -1, 581, 201))
        self.SMSSER_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.SMSSER_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SMSSER_frame.setObjectName("SMSSER_frame")
        self.label_51 = QtWidgets.QLabel(self.SMSSER_frame)
        self.label_51.setGeometry(QtCore.QRect(10, 20, 91, 21))
        self.label_51.setObjectName("label_51")
        self.comboBox_20 = QtWidgets.QComboBox(self.SMSSER_frame)
        self.comboBox_20.setGeometry(QtCore.QRect(100, 20, 91, 22))
        self.comboBox_20.setObjectName("comboBox_20")
        self.comboBox_20.addItem("")
        self.comboBox_20.addItem("")
        self.label_52 = QtWidgets.QLabel(self.SMSSER_frame)
        self.label_52.setGeometry(QtCore.QRect(220, 20, 121, 21))
        self.label_52.setObjectName("label_52")
        self.comboBox_21 = QtWidgets.QComboBox(self.SMSSER_frame)
        self.comboBox_21.setGeometry(QtCore.QRect(340, 20, 91, 22))
        self.comboBox_21.setObjectName("comboBox_21")
        self.comboBox_21.addItem("")
        self.comboBox_21.addItem("")
        self.http_frame = QtWidgets.QFrame(self.frame)
        self.http_frame.setGeometry(QtCore.QRect(-1, -1, 581, 201))
        self.http_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.http_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.http_frame.setObjectName("http_frame")
        self.label_72 = QtWidgets.QLabel(self.http_frame)
        self.label_72.setGeometry(QtCore.QRect(10, 20, 91, 21))
        self.label_72.setObjectName("label_72")
        self.comboBox_30 = QtWidgets.QComboBox(self.http_frame)
        self.comboBox_30.setGeometry(QtCore.QRect(100, 20, 101, 22))
        self.comboBox_30.setObjectName("comboBox_30")
        self.comboBox_30.addItem("")
        self.comboBox_30.addItem("")
        self.custom_frame = QtWidgets.QFrame(self.frame)
        self.custom_frame.setGeometry(QtCore.QRect(0, 0, 581, 201))
        self.custom_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.custom_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.custom_frame.setObjectName("custom_frame")
        self.label_73 = QtWidgets.QLabel(self.custom_frame)
        self.label_73.setGeometry(QtCore.QRect(30, 20, 61, 21))
        self.label_73.setObjectName("label_73")
        self.comboBox_31 = QtWidgets.QComboBox(self.custom_frame)
        self.comboBox_31.setGeometry(QtCore.QRect(100, 20, 121, 22))
        self.comboBox_31.setObjectName("comboBox_31")
        self.comboBox_31.addItem("")
        self.comboBox_31.addItem("")
        self.label_74 = QtWidgets.QLabel(self.custom_frame)
        self.label_74.setGeometry(QtCore.QRect(240, 20, 61, 21))
        self.label_74.setObjectName("label_74")
        self.comboBox_32 = QtWidgets.QComboBox(self.custom_frame)
        self.comboBox_32.setGeometry(QtCore.QRect(310, 20, 121, 20))
        self.comboBox_32.setObjectName("comboBox_32")
        self.comboBox_32.addItem("")
        self.comboBox_32.addItem("")
        self.label_75 = QtWidgets.QLabel(self.custom_frame)
        self.label_75.setGeometry(QtCore.QRect(30, 50, 71, 21))
        self.label_75.setObjectName("label_75")
        self.lineEdit_39 = QtWidgets.QLineEdit(self.custom_frame)
        self.lineEdit_39.setGeometry(QtCore.QRect(100, 50, 121, 20))
        self.lineEdit_39.setObjectName("lineEdit_39")
        self.label_76 = QtWidgets.QLabel(self.custom_frame)
        self.label_76.setGeometry(QtCore.QRect(20, 50, 71, 21))
        self.label_76.setObjectName("label_76")
        self.comboBox_33 = QtWidgets.QComboBox(self.custom_frame)
        self.comboBox_33.setGeometry(QtCore.QRect(100, 50, 121, 22))
        self.comboBox_33.setObjectName("comboBox_33")
        self.comboBox_33.addItem("")
        self.comboBox_33.addItem("")
        self.label_24 = QtWidgets.QLabel(self.custom_frame)
        self.label_24.setGeometry(QtCore.QRect(30, 80, 61, 21))
        self.label_24.setObjectName("label_24")
        self.comboBox_10 = QtWidgets.QComboBox(self.custom_frame)
        self.comboBox_10.setGeometry(QtCore.QRect(100, 80, 121, 20))
        self.comboBox_10.setObjectName("comboBox_10")
        self.comboBox_10.addItem("")
        self.comboBox_10.addItem("")
        self.label_25 = QtWidgets.QLabel(self.custom_frame)
        self.label_25.setGeometry(QtCore.QRect(30, 110, 61, 21))
        self.label_25.setObjectName("label_25")
        self.lineEdit_13 = QtWidgets.QLineEdit(self.custom_frame)
        self.lineEdit_13.setGeometry(QtCore.QRect(100, 110, 121, 20))
        self.lineEdit_13.setObjectName("lineEdit_13")
        self.label_26 = QtWidgets.QLabel(self.custom_frame)
        self.label_26.setGeometry(QtCore.QRect(30, 140, 61, 21))
        self.label_26.setObjectName("label_26")
        self.lineEdit_14 = QtWidgets.QLineEdit(self.custom_frame)
        self.lineEdit_14.setGeometry(QtCore.QRect(100, 140, 121, 20))
        self.lineEdit_14.setObjectName("lineEdit_14")
        self.label_27 = QtWidgets.QLabel(self.custom_frame)
        self.label_27.setGeometry(QtCore.QRect(230, 110, 71, 21))
        self.label_27.setObjectName("label_27")
        self.lineEdit_15 = QtWidgets.QLineEdit(self.custom_frame)
        self.lineEdit_15.setGeometry(QtCore.QRect(310, 110, 121, 20))
        self.lineEdit_15.setObjectName("lineEdit_15")
        self.label_28 = QtWidgets.QLabel(self.custom_frame)
        self.label_28.setGeometry(QtCore.QRect(230, 140, 71, 20))
        self.label_28.setObjectName("label_28")
        self.lineEdit_16 = QtWidgets.QLineEdit(self.custom_frame)
        self.lineEdit_16.setGeometry(QtCore.QRect(310, 140, 121, 20))
        self.lineEdit_16.setObjectName("lineEdit_16")
        self.pushButton_2 = QtWidgets.QPushButton(Dialog)
        self.pushButton_2.setGeometry(QtCore.QRect(300, 490, 75, 23))
        self.pushButton_2.setObjectName("pushButton_2")
        self.pushButton_3 = QtWidgets.QPushButton(Dialog)
        self.pushButton_3.setGeometry(QtCore.QRect(400, 490, 75, 23))
        self.pushButton_3.setObjectName("pushButton_3")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setGeometry(QtCore.QRect(20, 250, 481, 231))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(20, 0, 81, 41))
        self.label_5.setObjectName("label_5")
        self.activeType_comboBox = QtWidgets.QComboBox(self.frame_2)
        self.activeType_comboBox.setGeometry(QtCore.QRect(100, 10, 113, 20))
        self.activeType_comboBox.setObjectName("activeType_comboBox")
        self.activeType_comboBox.addItem("")
        self.activeType_comboBox.addItem("")
        self.activeType_comboBox.addItem("")
        self.activeType_comboBox.addItem("")
        self.activeType_comboBox.addItem("")
        self.activeType_comboBox.addItem("")
        self.active_frame = QtWidgets.QFrame(self.frame_2)
        self.active_frame.setGeometry(QtCore.QRect(0, 30, 481, 191))
        self.active_frame.setMinimumSize(QtCore.QSize(0, 0))
        self.active_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.active_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.active_frame.setObjectName("active_frame")
        self.autoActive_frame = QtWidgets.QFrame(self.active_frame)
        self.autoActive_frame.setGeometry(QtCore.QRect(10, 80, 531, 41))
        self.autoActive_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.autoActive_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.autoActive_frame.setObjectName("autoActive_frame")
        self.SMSActive_frame = QtWidgets.QFrame(self.active_frame)
        self.SMSActive_frame.setGeometry(QtCore.QRect(0, 0, 581, 171))
        self.SMSActive_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.SMSActive_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.SMSActive_frame.setObjectName("SMSActive_frame")
        self.label_6 = QtWidgets.QLabel(self.SMSActive_frame)
        self.label_6.setGeometry(QtCore.QRect(10, 10, 91, 41))
        self.label_6.setObjectName("label_6")
        self.lineEdit_3 = QtWidgets.QLineEdit(self.SMSActive_frame)
        self.lineEdit_3.setGeometry(QtCore.QRect(100, 20, 113, 20))
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.label_7 = QtWidgets.QLabel(self.SMSActive_frame)
        self.label_7.setGeometry(QtCore.QRect(10, 50, 91, 21))
        self.label_7.setObjectName("label_7")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.SMSActive_frame)
        self.lineEdit_4.setGeometry(QtCore.QRect(100, 50, 113, 20))
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.phone_frame = QtWidgets.QFrame(self.SMSActive_frame)
        self.phone_frame.setGeometry(QtCore.QRect(0, 0, 581, 171))
        self.phone_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.phone_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.phone_frame.setObjectName("phone_frame")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.phone_frame)
        self.lineEdit_5.setGeometry(QtCore.QRect(100, 20, 113, 20))
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.label_8 = QtWidgets.QLabel(self.phone_frame)
        self.label_8.setGeometry(QtCore.QRect(10, 10, 101, 41))
        self.label_8.setObjectName("label_8")
        self.comActive_frame = QtWidgets.QFrame(self.phone_frame)
        self.comActive_frame.setGeometry(QtCore.QRect(-10, 0, 581, 171))
        self.comActive_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.comActive_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.comActive_frame.setObjectName("comActive_frame")
        self.label_9 = QtWidgets.QLabel(self.comActive_frame)
        self.label_9.setGeometry(QtCore.QRect(40, 20, 61, 21))
        self.label_9.setObjectName("label_9")
        self.lineEdit_6 = QtWidgets.QLineEdit(self.comActive_frame)
        self.lineEdit_6.setGeometry(QtCore.QRect(100, 20, 113, 20))
        self.lineEdit_6.setObjectName("lineEdit_6")
        self.label_10 = QtWidgets.QLabel(self.comActive_frame)
        self.label_10.setGeometry(QtCore.QRect(40, 50, 61, 21))
        self.label_10.setObjectName("label_10")
        self.comboBox_2 = QtWidgets.QComboBox(self.comActive_frame)
        self.comboBox_2.setGeometry(QtCore.QRect(100, 50, 113, 20))
        self.comboBox_2.setObjectName("comboBox_2")
        self.comboBox_2.addItem("")
        self.comboBox_2.addItem("")
        self.label_11 = QtWidgets.QLabel(self.comActive_frame)
        self.label_11.setGeometry(QtCore.QRect(270, 20, 71, 21))
        self.label_11.setObjectName("label_11")
        self.lineEdit_7 = QtWidgets.QLineEdit(self.comActive_frame)
        self.lineEdit_7.setGeometry(QtCore.QRect(340, 20, 113, 20))
        self.lineEdit_7.setObjectName("lineEdit_7")
        self.label_12 = QtWidgets.QLabel(self.comActive_frame)
        self.label_12.setGeometry(QtCore.QRect(270, 50, 61, 21))
        self.label_12.setObjectName("label_12")
        self.comboBox_5 = QtWidgets.QComboBox(self.comActive_frame)
        self.comboBox_5.setGeometry(QtCore.QRect(340, 50, 113, 20))
        self.comboBox_5.setObjectName("comboBox_5")
        self.comboBox_5.addItem("")
        self.comboBox_5.addItem("")
        self.allActive_frame = QtWidgets.QFrame(self.comActive_frame)
        self.allActive_frame.setGeometry(QtCore.QRect(0, 0, 581, 171))
        self.allActive_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.allActive_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.allActive_frame.setObjectName("allActive_frame")
        self.label_13 = QtWidgets.QLabel(self.allActive_frame)
        self.label_13.setGeometry(QtCore.QRect(10, 20, 81, 21))
        self.label_13.setObjectName("label_13")
        self.lineEdit_9 = QtWidgets.QLineEdit(self.allActive_frame)
        self.lineEdit_9.setGeometry(QtCore.QRect(100, 20, 113, 20))
        self.lineEdit_9.setObjectName("lineEdit_9")
        self.label_14 = QtWidgets.QLabel(self.allActive_frame)
        self.label_14.setGeometry(QtCore.QRect(253, 21, 81, 21))
        self.label_14.setObjectName("label_14")
        self.lineEdit_10 = QtWidgets.QLineEdit(self.allActive_frame)
        self.lineEdit_10.setGeometry(QtCore.QRect(340, 20, 113, 20))
        self.lineEdit_10.setObjectName("lineEdit_10")
        self.label_15 = QtWidgets.QLabel(self.allActive_frame)
        self.label_15.setGeometry(QtCore.QRect(30, 50, 81, 21))
        self.label_15.setObjectName("label_15")
        self.lineEdit_11 = QtWidgets.QLineEdit(self.allActive_frame)
        self.lineEdit_11.setGeometry(QtCore.QRect(100, 50, 113, 20))
        self.lineEdit_11.setObjectName("lineEdit_11")
        self.label_16 = QtWidgets.QLabel(self.allActive_frame)
        self.label_16.setGeometry(QtCore.QRect(270, 50, 61, 21))
        self.label_16.setObjectName("label_16")
        self.lineEdit_12 = QtWidgets.QLineEdit(self.allActive_frame)
        self.lineEdit_12.setGeometry(QtCore.QRect(340, 50, 113, 20))
        self.lineEdit_12.setObjectName("lineEdit_12")
        self.label_17 = QtWidgets.QLabel(self.allActive_frame)
        self.label_17.setGeometry(QtCore.QRect(20, 80, 81, 21))
        self.label_17.setObjectName("label_17")
        self.comboBox_3 = QtWidgets.QComboBox(self.allActive_frame)
        self.comboBox_3.setGeometry(QtCore.QRect(100, 80, 113, 20))
        self.comboBox_3.setObjectName("comboBox_3")
        self.comboBox_3.addItem("")
        self.comboBox_3.addItem("")
        self.label_18 = QtWidgets.QLabel(self.allActive_frame)
        self.label_18.setGeometry(QtCore.QRect(270, 80, 61, 21))
        self.label_18.setObjectName("label_18")
        self.comboBox_4 = QtWidgets.QComboBox(self.allActive_frame)
        self.comboBox_4.setGeometry(QtCore.QRect(340, 80, 113, 20))
        self.comboBox_4.setObjectName("comboBox_4")
        self.comboBox_4.addItem("")
        self.comboBox_4.addItem("")
        self.label_19 = QtWidgets.QLabel(self.allActive_frame)
        self.label_19.setGeometry(QtCore.QRect(50, 110, 41, 21))
        self.label_19.setObjectName("label_19")
        self.comboBox_6 = QtWidgets.QComboBox(self.allActive_frame)
        self.comboBox_6.setGeometry(QtCore.QRect(100, 110, 113, 20))
        self.comboBox_6.setObjectName("comboBox_6")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.comboBox_6.addItem("")
        self.label_20 = QtWidgets.QLabel(self.allActive_frame)
        self.label_20.setGeometry(QtCore.QRect(300, 110, 41, 21))
        self.label_20.setObjectName("label_20")
        self.comboBox_7 = QtWidgets.QComboBox(self.allActive_frame)
        self.comboBox_7.setGeometry(QtCore.QRect(340, 110, 113, 20))
        self.comboBox_7.setObjectName("comboBox_7")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.comboBox_7.addItem("")
        self.label_21 = QtWidgets.QLabel(self.allActive_frame)
        self.label_21.setGeometry(QtCore.QRect(10, 140, 91, 21))
        self.label_21.setObjectName("label_21")
        self.lineEdit_8 = QtWidgets.QLineEdit(self.allActive_frame)
        self.lineEdit_8.setGeometry(QtCore.QRect(100, 140, 113, 20))
        self.lineEdit_8.setObjectName("lineEdit_8")
        self.IOActive_frame = QtWidgets.QFrame(self.allActive_frame)
        self.IOActive_frame.setGeometry(QtCore.QRect(0, 0, 491, 201))
        self.IOActive_frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.IOActive_frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.IOActive_frame.setObjectName("IOActive_frame")
        self.label_22 = QtWidgets.QLabel(self.IOActive_frame)
        self.label_22.setGeometry(QtCore.QRect(20, 20, 81, 21))
        self.label_22.setObjectName("label_22")
        self.comboBox_8 = QtWidgets.QComboBox(self.IOActive_frame)
        self.comboBox_8.setGeometry(QtCore.QRect(100, 20, 113, 20))
        self.comboBox_8.setObjectName("comboBox_8")
        self.comboBox_8.addItem("")
        self.label_23 = QtWidgets.QLabel(self.IOActive_frame)
        self.label_23.setGeometry(QtCore.QRect(40, 50, 61, 21))
        self.label_23.setObjectName("label_23")
        self.comboBox_9 = QtWidgets.QComboBox(self.IOActive_frame)
        self.comboBox_9.setGeometry(QtCore.QRect(100, 50, 113, 20))
        self.comboBox_9.setObjectName("comboBox_9")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")
        self.comboBox_9.addItem("")

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.label.setText(_translate("Dialog", "工作协议："))
        self.protocolType_comboBox.setItemText(0, _translate("Dialog", "PROT"))
        self.protocolType_comboBox.setItemText(1, _translate("Dialog", "DCUDP"))
        self.protocolType_comboBox.setItemText(2, _translate("Dialog", "DCTCP"))
        self.protocolType_comboBox.setItemText(3, _translate("Dialog", "TRNS"))
        self.protocolType_comboBox.setItemText(4, _translate("Dialog", "SMSCLI"))
        self.protocolType_comboBox.setItemText(5, _translate("Dialog", "SMSSER"))
        self.protocolType_comboBox.setItemText(6, _translate("Dialog", "HTTP"))
        self.protocolType_comboBox.setItemText(7, _translate("Dialog", "自定义"))
        self.label_2.setText(_translate("Dialog", "设备ID："))
        self.label_3.setText(_translate("Dialog", "手机号码："))
        self.label_4.setText(_translate("Dialog", " 数据是否转义："))
        self.comboBox.setItemText(0, _translate("Dialog", "是"))
        self.comboBox.setItemText(1, _translate("Dialog", "否"))
        self.label_43.setText(_translate("Dialog", "手机号码："))
        self.label_44.setText(_translate("Dialog", "短信号码组1："))
        self.label_45.setText(_translate("Dialog", "短信号码组2："))
        self.label_46.setText(_translate("Dialog", "短信号码组3："))
        self.label_47.setText(_translate("Dialog", "短信号码组4："))
        self.label_48.setText(_translate("Dialog", "短信号码组5："))
        self.label_49.setText(_translate("Dialog", " 是否显示号码："))
        self.comboBox_18.setItemText(0, _translate("Dialog", "关"))
        self.comboBox_18.setItemText(1, _translate("Dialog", "开"))
        self.label_50.setText(_translate("Dialog", "16进制强制转文本："))
        self.comboBox_19.setItemText(0, _translate("Dialog", "关"))
        self.comboBox_19.setItemText(1, _translate("Dialog", "开"))
        self.label_51.setText(_translate("Dialog", "是否显示号码："))
        self.comboBox_20.setItemText(0, _translate("Dialog", "关"))
        self.comboBox_20.setItemText(1, _translate("Dialog", "开"))
        self.label_52.setText(_translate("Dialog", "16进制强制转换文本："))
        self.comboBox_21.setItemText(0, _translate("Dialog", "关"))
        self.comboBox_21.setItemText(1, _translate("Dialog", "开"))
        self.label_72.setText(_translate("Dialog", "HTTP请求方式："))
        self.comboBox_30.setItemText(0, _translate("Dialog", "GET"))
        self.comboBox_30.setItemText(1, _translate("Dialog", "POST"))
        self.label_73.setText(_translate("Dialog", "设备模式："))
        self.comboBox_31.setItemText(0, _translate("Dialog", "服务端模式"))
        self.comboBox_31.setItemText(1, _translate("Dialog", "客户端模式"))
        self.label_74.setText(_translate("Dialog", "传输协议："))
        self.comboBox_32.setItemText(0, _translate("Dialog", "TCP"))
        self.comboBox_32.setItemText(1, _translate("Dialog", "UDP"))
        self.label_75.setText(_translate("Dialog", "监听端口："))
        self.label_76.setText(_translate("Dialog", "注册及心跳："))
        self.comboBox_33.setItemText(0, _translate("Dialog", "开启"))
        self.comboBox_33.setItemText(1, _translate("Dialog", "关闭"))
        self.label_24.setText(_translate("Dialog", "  包格式："))
        self.comboBox_10.setItemText(0, _translate("Dialog", "Text"))
        self.comboBox_10.setItemText(1, _translate("Dialog", "Hex"))
        self.label_25.setText(_translate("Dialog", "  注册包："))
        self.label_26.setText(_translate("Dialog", "  心跳包："))
        self.label_27.setText(_translate("Dialog", "注册包回应："))
        self.label_28.setText(_translate("Dialog", "心跳包回应："))
        self.pushButton_2.setText(_translate("Dialog", "配置"))
        self.pushButton_3.setText(_translate("Dialog", "取消"))
        self.label_5.setText(_translate("Dialog", "   激活方式："))
        self.activeType_comboBox.setItemText(0, _translate("Dialog", "自动"))
        self.activeType_comboBox.setItemText(1, _translate("Dialog", "短信激活"))
        self.activeType_comboBox.setItemText(2, _translate("Dialog", "电话激活"))
        self.activeType_comboBox.setItemText(3, _translate("Dialog", "串口激活"))
        self.activeType_comboBox.setItemText(4, _translate("Dialog", "混合激活"))
        self.activeType_comboBox.setItemText(5, _translate("Dialog", "I/O激活"))
        self.label_6.setText(_translate("Dialog", " 短信激活号码："))
        self.label_7.setText(_translate("Dialog", " 短信激活密码："))
        self.label_8.setText(_translate("Dialog", "电话激活号码："))
        self.label_9.setText(_translate("Dialog", "上线数据："))
        self.label_10.setText(_translate("Dialog", "激活接口："))
        self.comboBox_2.setItemText(0, _translate("Dialog", "串口1"))
        self.comboBox_2.setItemText(1, _translate("Dialog", "串口2"))
        self.label_11.setText(_translate("Dialog", " 下线数据："))
        self.label_12.setText(_translate("Dialog", " 数据格式："))
        self.comboBox_5.setItemText(0, _translate("Dialog", "Text"))
        self.comboBox_5.setItemText(1, _translate("Dialog", "Hex"))
        self.label_13.setText(_translate("Dialog", "电话激活号码："))
        self.label_14.setText(_translate("Dialog", "短信激活号码："))
        self.label_15.setText(_translate("Dialog", " 上线数据："))
        self.label_16.setText(_translate("Dialog", " 下线数据："))
        self.label_17.setText(_translate("Dialog", "   激活接口："))
        self.comboBox_3.setItemText(0, _translate("Dialog", "串口1"))
        self.comboBox_3.setItemText(1, _translate("Dialog", "串口2"))
        self.label_18.setText(_translate("Dialog", " 数据格式："))
        self.comboBox_4.setItemText(0, _translate("Dialog", "Text"))
        self.comboBox_4.setItemText(1, _translate("Dialog", "Hex"))
        self.label_19.setText(_translate("Dialog", "  I/O1："))
        self.comboBox_6.setItemText(0, _translate("Dialog", "未启用"))
        self.comboBox_6.setItemText(1, _translate("Dialog", "激活"))
        self.comboBox_6.setItemText(2, _translate("Dialog", "上下线控制"))
        self.label_20.setText(_translate("Dialog", "I/O2："))
        self.comboBox_7.setItemText(0, _translate("Dialog", "未启用"))
        self.comboBox_7.setItemText(1, _translate("Dialog", "激活"))
        self.comboBox_7.setItemText(2, _translate("Dialog", "上下线控制"))
        self.label_21.setText(_translate("Dialog", " 短信激活密码："))
        self.label_22.setText(_translate("Dialog", "I/O激活方式："))
        self.comboBox_8.setItemText(0, _translate("Dialog", "休眠/唤醒"))
        self.label_23.setText(_translate("Dialog", "I/O选择："))
        self.comboBox_9.setItemText(0, _translate("Dialog", "I/O1"))
        self.comboBox_9.setItemText(1, _translate("Dialog", "I/O2"))
        self.comboBox_9.setItemText(2, _translate("Dialog", "I/O3"))
