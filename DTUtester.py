import image_qr
import serial
from serial.tools import list_ports
import sys
import time
from datetime import datetime
import threading
import re
from PyQt5.QtWidgets import QApplication, QMessageBox, QLabel, QPushButton, QStackedLayout, QWidget, QDialog
from PyQt5.QtCore import QTimer, QRegExp, QThread, pyqtSignal, Qt
from PyQt5.QtGui import QTextCursor, QRegExpValidator, QIcon
from ui_source.DTU测试助手 import *
from one_panel import *
from three_panel import *
from ui_source import inputIPandPORTDialog
from ui_source import COMsetDialog
from ui_source import WORKmodelDialog
from ui_source import FrameDialog
from ui_source import F16COMsetDialog
from ui_source import F16SMSsetDialog
from ui_source import F16IPandPORTsetDialog
from ui_source import F16WORKtypeDialog

# class MyThread(threading.Thread):
#     def __init__(self, func, args=()):
#         super(MyThread, self).__init__()
#         self.func = func
#         self.args = args
#
#     def run(self):
#         self.result = self.func(*self.args)
#
#     def get_result(self):
#         try:
#             return self.result  # 如果子线程不使用join方法，此处可能会报没有self.result的错误
#         except Exception:
#             return None


class COMcheck_state_thread(QThread):
    signal = pyqtSignal()

    def __init__(self):
        super(COMcheck_state_thread, self).__init__()

    def run(self):
        time.sleep(1)
        self.signal.emit()


class win(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(win, self).__init__()
        self.setupUi(self)

        self.ser = serial.Serial()
        # 运行时先获取串口列表
        self.port_check()
        # 初始波特率comboBox
        self.baudrates = [
            600,
            1200,
            2400,
            4800,
            9600,
            14400,
            19200,
            38400,
            56000,
            57600,
            115200]
        for baudrate in self.baudrates:
            self.baudrate_comboBox.addItem(str(baudrate))
        self.baudrate_comboBox.setCurrentIndex(10)  # 默认为115200
        # 初始化数据位
        self.Databits = [5, 6, 7, 8]
        for databits in self.Databits:
            self.Databits_comboBox.addItem(str(databits))
        self.Databits_comboBox.setCurrentIndex(3)  # 默认为8
        # 初始化校验位
        self.paritys = ['N', 'O', 'E']
        for parity in self.paritys:
            self.parity_comboBox.addItem(parity)
        # 初始化停止位
        self.Stopbits = ['1', '2']
        for stopbits in self.Stopbits:
            self.Stopbits_comboBox.addItem(stopbits)
        # 初始化接收数量和发送数量
        self.data_num_received = 0
        self.data_num_sended = 0

        # 设置接收数据的定时器，连接到显示数据的函数show_Data
        self.show_timer = QTimer()
        self.show_timer.timeout.connect(self.show_Data)
        # 设置定时发送数据的定时器，连接到发送数据的函数send_Data
        self.send_timer = QTimer()
        self.send_timer.timeout.connect(self.send_Data)
        self.flag = True  # 设置定时发送标志
        self.send_time = 1000
        self.time_lineEdit.setText(str(self.send_time))  # 定时发送时间默认1秒
        regx = QRegExp("^[1-9][0-9]*$")
        validator = QRegExpValidator(regx, self.time_lineEdit)
        self.time_lineEdit.setValidator(validator)  # 限制只能输入大于0的整数
        # 堆叠布局,窗口切换
        self.qsl = QStackedLayout(self.frame_2)  # 设置堆叠布局给主窗体得farm2容器
        self.one = one_panel()
        self.three = three_panel()
        self.qsl.addWidget(self.one)
        self.qsl.addWidget(self.three)
        self.F2X14_16_D_pushButton.clicked.connect(self.F2X14_16_D_panel)
        self.F2X16_pushButton.clicked.connect(self.F2X16_panel)
        # 默认显示F2x14-D的窗体，所以一开始把F2x14-D的按钮设置不可用
        self.F2X14_16_D_pushButton.setEnabled(False)

        # 绑定控件相关事件
        self.comDetection_pushButton.clicked.connect(self.port_check)
        self.open_pushButton.clicked.connect(self.open_port)
        self.close_pushButton.clicked.connect(self.close_port)
        self.send_pushButton.clicked.connect(self.send_PushButton_state)
        self.HEXsend_checkBox.stateChanged.connect(self.HEXsend_checkBox_state)
        self.clearDATA_pushButton.clicked.connect(self.clear_received)
        self.clearLog_pushButton.clicked.connect(self.clear_log)
        self.time_checkBox.stateChanged.connect(self.time_checkBox_state)
        self.saveDATA_pushButton.clicked.connect(self.save_data)
        self.COM_Box.currentIndexChanged.connect(self.port_changed)
        self.baudrate_comboBox.currentIndexChanged.connect(self.port_changed)
        self.parity_comboBox.currentIndexChanged.connect(self.port_changed)
        self.Databits_comboBox.currentIndexChanged.connect(self.port_changed)
        self.Stopbits_comboBox.currentIndexChanged.connect(self.port_changed)
        self.TOP_checkBox.stateChanged.connect(self.setTOP)
        self.one.IPandPORT_pushButton.clicked.connect(
            self.open_IPandPORT_dialog)

        # 设置部分控件初始状态
        self.send_pushButton.setEnabled(False)  # 设置发送按钮不可用
        self.close_pushButton.setEnabled(False)  # 设置关闭按钮不可用
        self.groupBox_5.setEnabled(False)

        # 状态栏，将发送和接收统计显示到状态栏
        self.statusBar.showMessage('DTU测试助手')
        self.received_label = QLabel()
        self.send_label = QLabel()
        self.reset_pushButton = QPushButton()
        self.reset_pushButton.clicked.connect(self.num_reset)
        self.received_label.setText("接收：0")
        self.send_label.setText("发送：0")
        self.reset_pushButton.setText("计数复位")
        self.statusBar.addPermanentWidget(self.send_label)
        self.statusBar.addPermanentWidget(self.received_label)
        self.statusBar.addPermanentWidget(self.reset_pushButton)
        # 鼠标悬停在控件上时状态栏消息提示
        self.open_pushButton.setStatusTip("打开串口")
        self.comDetection_pushButton.setStatusTip("串口检测")
        self.COM_Box.setStatusTip("选择串口")
        self.baudrate_comboBox.setStatusTip("选择波特率")
        self.Databits_comboBox.setStatusTip("选择数据位")
        self.parity_comboBox.setStatusTip("选择校验位")
        self.Stopbits_comboBox.setStatusTip("选择停止位")
        self.clearDATA_pushButton.setStatusTip("清除接收窗口")
        self.clearLog_pushButton.setStatusTip("清除日志窗口")
        self.close_pushButton.setStatusTip("关闭串口")
        self.saveDATA_pushButton.setStatusTip("保存数据")
        self.HEXShow_checkBox.setStatusTip("以HEX显示")
        self.hh_checkBox.setStatusTip("添加回车换行发送")
        self.time_checkBox.setStatusTip("定时发送")
        self.HEXsend_checkBox.setStatusTip("以HEX发送")
        self.send_pushButton.setStatusTip("发送")
        self.send_label.setStatusTip("发送统计")
        self.received_label.setStatusTip("接收统计")
        self.reset_pushButton.setStatusTip("计数复位")
        self.TOP_checkBox.setStatusTip("置顶窗口")

        # 设置每个按钮属性
        self.send_pushButton.setProperty('name', 'btn')
        self.open_pushButton.setProperty('name', 'btn')
        self.comDetection_pushButton.setProperty('name', 'btn')
        self.close_pushButton.setProperty('name', 'btn')
        self.clearDATA_pushButton.setProperty('name', 'btn')
        self.clearLog_pushButton.setProperty('name', 'btn')
        self.saveDATA_pushButton.setProperty('name', 'btn')
        self.reset_pushButton.setProperty('name', 'btn')
        self.F2X14_16_D_pushButton.setProperty('name', 'btn')
        self.F2X16_pushButton.setProperty('name', 'btn')
        self.one.IPandPORT_pushButton.setProperty('name', 'btn')
        self.one.COMset_pushButton.setProperty('name', 'btn')
        self.one.workModel_pushButton.setProperty('name', 'btn')
        self.one.frame_pushButton.setProperty('name', 'btn')
        self.one.version_pushButton.setProperty('name', 'btn')
        self.one.read_pushButton.setProperty('name', 'btn')
        self.one.ok_pushButton.setProperty('name', 'btn')
        self.one.reset_pushButton.setProperty('name', 'btn')
        self.one.reset_pushButton_2.setProperty('name','btn')
        self.three.reset_pushButton.setProperty('name', 'btn')
        self.three.ok_pushButton.setProperty('name', 'btn')
        self.three.read_pushButton.setProperty('name', 'btn')
        self.three.version_pushButton.setProperty('name', 'btn')
        self.three.state_pushButton.setProperty('name', 'btn')
        self.three.COMset_pushButton.setProperty('name', 'btn')
        self.three.connectSet_pushButton.setProperty('name', 'btn')
        self.three.SMSset_pushButton.setProperty('name', 'btn')
        self.three.IPandPORT_pushButton.setProperty('name', 'btn')
        self.three.pushButton.setProperty('name','btn')
        self.three.worknet_pushButton.setProperty('name','btn')

        # 14(16)-D中心ip和端口设置页面相关
        self.IPandPORT_dialog = QDialog(self, Qt.WindowCloseButtonHint)
        self.IPandPORT_ui = inputIPandPORTDialog.Ui_Dialog()
        self.IPandPORT_ui.setupUi(self.IPandPORT_dialog)
        self.IPandPORT_ui.ok_pushButton.setProperty("name", "btn")
        self.IPandPORT_ui.cancel_pushButton.setProperty("name", "btn")
        self.IPandPORT_ui.IP_lineEdit.setInputMask("000.000.000.000; ")
        self.IPandPORT_ui.IP1_lineEdit.setInputMask("000.000.000.000; ")
        self.IPandPORT_ui.IP2_lineEdit.setInputMask("000.000.000.000; ")
        self.IPandPORT_ui.IP3_lineEdit.setInputMask("000.000.000.000; ")
        self.IPandPORT_ui.IP4_lineEdit.setInputMask("000.000.000.000; ")
        self.IPandPORT_ui.read_pushButton.setProperty('name', 'btn')

        # 14(16)-D串口设置页面相关
        self.COMset_dialog = QDialog(self, Qt.WindowCloseButtonHint)
        self.COMset_ui = COMsetDialog.Ui_Dialog()
        self.COMset_ui.setupUi(self.COMset_dialog)
        self.one.COMset_pushButton.clicked.connect(self.open_COMset_dialog)
        self.COMset_ui.read_pushButton.setProperty('name', 'btn')
        self.COMset_ui.ok_pushButton.setProperty('name', 'btn')
        self.COMset_ui.cancel_pushButton.setProperty('name', 'btn')

        # 14(16)-D工作模式设置页面相关
        self.WORKmodel_dialog = QDialog(self, Qt.WindowCloseButtonHint)
        self.WORKmodel_ui = WORKmodelDialog.Ui_Dialog()
        self.WORKmodel_ui.setupUi(self.WORKmodel_dialog)
        self.one.workModel_pushButton.clicked.connect(
            self.open_WORKmodel_dialog)
        self.WORKmodel_ui.read_pushButton.setProperty('name', 'btn')
        self.WORKmodel_ui.ok_pushButton.setProperty('name', 'btn')
        self.WORKmodel_ui.cancel_pushButton.setProperty('name', 'btn')

        # 14(16)-D自定义帧设置页面相关
        self.Frame_dialog = QDialog(self, Qt.WindowCloseButtonHint)
        self.Frame_ui = FrameDialog.Ui_Dialog()
        self.Frame_ui.setupUi(self.Frame_dialog)
        self.one.frame_pushButton.clicked.connect(self.open_Frame_dialog)
        self.Frame_ui.read_pushButton.setProperty('name', 'btn')
        self.Frame_ui.ok_pushButton.setProperty('name', 'btn')
        self.Frame_ui.cancel_pushButton.setProperty('name', 'btn')

        # 16串口设置页面相关
        self.F16COMset_dialog = QDialog(self, Qt.WindowCloseButtonHint)
        self.F16COMset_ui = F16COMsetDialog.Ui_Dialog()
        self.F16COMset_ui.setupUi(self.F16COMset_dialog)
        self.three.COMset_pushButton.clicked.connect(
            self.open_F16COMset_dialog)
        self.F16COMset_ui.ok_pushButton.setProperty('name', 'btn')
        self.F16COMset_ui.cancel_pushButton.setProperty('name', 'btn')

        # 16短信设置页面相关
        self.F16SMSset_dialog = QDialog(self, Qt.WindowCloseButtonHint)
        self.F16SMSset_ui = F16SMSsetDialog.Ui_Dialog()
        self.F16SMSset_ui.setupUi(self.F16SMSset_dialog)
        self.three.SMSset_pushButton.clicked.connect(
            self.open_F16SMSset_dialog)
        self.F16SMSset_ui.pushButton_2.setProperty('name', 'btn')
        self.F16SMSset_ui.pushButton_3.setProperty('name', 'btn')
        self.F16SMSset_ui.SMSset_comboBox.currentTextChanged.connect(self.F16SMSset_ONorOFF)
        self.F16SMSset_ui.label_2.hide()
        self.F16SMSset_ui.label_3.hide()
        self.F16SMSset_ui.SMSset_lineEdit.hide()
        self.F16SMSset_ui.admin_lineEdit.hide()

        # 16中心服务设置页面相关
        self.F16IPandPORTset_dialog = QDialog(self, Qt.WindowCloseButtonHint)
        self.F16IPandPORTset_ui = F16IPandPORTsetDialog.Ui_Dialog()
        self.F16IPandPORTset_ui.setupUi(self.F16IPandPORTset_dialog)
        self.three.IPandPORT_pushButton.clicked.connect(
            self.open_F16IPandPORTset_dialog)
        self.F16IPandPORTset_ui.pushButton_2.setProperty('name', 'btn')
        self.F16IPandPORTset_ui.pushButton_3.setProperty('name', 'btn')
        self.F16IPandPORTset_ui.serverNum_comboBox.currentIndexChanged.connect(
            self.F16server_num)
        self.F16IPandPORTset_ui.label_6.hide()
        self.F16IPandPORTset_ui.label_7.hide()
        self.F16IPandPORTset_ui.label_8.hide()
        self.F16IPandPORTset_ui.label_9.hide()
        self.F16IPandPORTset_ui.label_10.hide()
        self.F16IPandPORTset_ui.label_11.hide()
        self.F16IPandPORTset_ui.label_12.hide()
        self.F16IPandPORTset_ui.label_13.hide()
        self.F16IPandPORTset_ui.server2_lineEdit.hide()
        self.F16IPandPORTset_ui.port2_lineEdit.hide()
        self.F16IPandPORTset_ui.server3_lineEdit.hide()
        self.F16IPandPORTset_ui.port3_lineEdit.hide()
        self.F16IPandPORTset_ui.server4_lineEdit.hide()
        self.F16IPandPORTset_ui.port4_lineEdit.hide()
        self.F16IPandPORTset_ui.server5_lineEdit.hide()
        self.F16IPandPORTset_ui.port5_lineEdit.hide()

        # 16工作模式设置页面相关
        self.F16WORKtype_dialog = QDialog(self, Qt.WindowCloseButtonHint)
        self.F16WORKtype_ui = F16WORKtypeDialog.Ui_Dialog()
        self.F16WORKtype_ui.setupUi(self.F16WORKtype_dialog)
        self.three.connectSet_pushButton.clicked.connect(
            self.open_F16WORKtype_dialog)
        # 创建一个堆叠窗口，当选择不同工作协议时，窗口进行相应变化
        self.qsl1 = QStackedLayout(self.F16WORKtype_ui.frame)
        self.qsl1.addWidget(self.F16WORKtype_ui.prot_frame)
        self.qsl1.addWidget(self.F16WORKtype_ui.DCUDPandDCTCP_frame)
        self.qsl1.addWidget(self.F16WORKtype_ui.TRNS_frame)
        self.qsl1.addWidget(self.F16WORKtype_ui.SMSCLI_frame)
        self.qsl1.addWidget(self.F16WORKtype_ui.SMSSER_frame)
        self.qsl1.addWidget(self.F16WORKtype_ui.http_frame)
        self.qsl1.addWidget(self.F16WORKtype_ui.custom_frame)
        self.F16WORKtype_ui.protocolType_comboBox.currentIndexChanged.connect(
            self.protocolTypeChange)
        # 创建一个堆叠窗口,当选择不同激活模式时，窗口进行相应变化
        self.qsl2 = QStackedLayout(self.F16WORKtype_ui.active_frame)
        self.qsl2.addWidget(self.F16WORKtype_ui.autoActive_frame)
        self.qsl2.addWidget(self.F16WORKtype_ui.SMSActive_frame)
        self.qsl2.addWidget(self.F16WORKtype_ui.phone_frame)
        self.qsl2.addWidget(self.F16WORKtype_ui.comActive_frame)
        self.qsl2.addWidget(self.F16WORKtype_ui.allActive_frame)
        self.qsl2.addWidget(self.F16WORKtype_ui.IOActive_frame)
        self.F16WORKtype_ui.activeType_comboBox.currentIndexChanged.connect(
            self.activeTypeChange)
        self.F16WORKtype_ui.comboBox_31.currentIndexChanged.connect(
            self.ClientORServer)  # 选择自定义模式时，选择客户端或者服务端时页面相应变化
        self.F16WORKtype_ui.comboBox_33.currentIndexChanged.connect(
            self.heartOPENorCLOSE)
        self.F16WORKtype_ui.label_76.hide()
        self.F16WORKtype_ui.comboBox_33.hide()
        self.F16WORKtype_ui.label_24.hide()
        self.F16WORKtype_ui.comboBox_10.hide()
        self.F16WORKtype_ui.label_25.hide()
        self.F16WORKtype_ui.label_26.hide()
        self.F16WORKtype_ui.label_27.hide()
        self.F16WORKtype_ui.label_28.hide()
        self.F16WORKtype_ui.lineEdit_13.hide()
        self.F16WORKtype_ui.lineEdit_14.hide()
        self.F16WORKtype_ui.lineEdit_15.hide()
        self.F16WORKtype_ui.lineEdit_16.hide()
        self.F16WORKtype_ui.pushButton_2.setProperty('name', 'btn')
        self.F16WORKtype_ui.pushButton_3.setProperty('name', 'btn')

        # 设置QSS样式表
        self.setStyleSheet(
            """
                QPushButton[name='btn']{
                    border-top:2px solid white;
                    border-left:2px solid white;
                    border-right:2px solid gray;
                    border-bottom:2px solid gray;
                    outline:none;
                }
                QPushButton[name='btn']:focus{
                    border-top:1px solid gray;
                    border-left:1px solid gray;
                    border-right:2px solid gray;
                    border-bottom:2px solid gray;
                }


                QPushButton[name='btn']:pressed
                                    {
                                    padding-left:3px;
                                    padding-top:3px;
                                    border:2px solid gray
                                    }

                QLineEdit { background: yellow }

                QCheckBox:checked{background:yellow}

            """)

        # 设置型号选择按钮颜色
        self.F2X14_16_D_pushButton.setStyleSheet("color: rgb(170, 0, 255);")
        self.log_textEdit.append(
            "<font color='mediumblue'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;====F2x14(16)-D====\n</font>")

        self.one.version_pushButton.clicked.connect(self.ver_check)
        self.one.read_pushButton.clicked.connect(self.one_read)
        self.one.reset_pushButton.clicked.connect(self.reset)
        self.one.ok_pushButton.clicked.connect(self.set_ok)
        self.one.reset_pushButton_2.clicked.connect(self.reboot)

        self.ATresult = None
        self.netmodes = {
            "自动": 0,
            "强制2G": 1,
            '强制3G': 2,
            '强制4G': 3,
            '2/3G自适应': 21}
        self.debug = {"否": 0, "是[串口1]": 1, "是[串口2]": 2}
        self.enctype = {'不加密': 0, '网络加密': 1, '串口加密': 2}
        self.bauds = {
            '600': 0,
            '1200': 1,
            '2400': 2,
            '4800': 3,
            '9600': 4,
            '14400': 5,
            '19200': 6,
            '38400': 7,
            '56000': 8,
            '57600': 9,
            '115200': 10}
        self.databits = {"5": 0, '6': 1, '7': 2, '8': 3}
        self.paritybits = {'N': 0, 'O': 1, 'E': 2}

        self.COMset_ui.read_pushButton.clicked.connect(self.COMset_read)
        self.COMset_ui.cancel_pushButton.clicked.connect(self.COMset_cancel)
        self.COMset_ui.ok_pushButton.clicked.connect(self.COMset_set)

        self.WORKmodel_ui.read_pushButton.clicked.connect(self.WORKmodel_read)
        self.WORKmodel_ui.cancel_pushButton.clicked.connect(
            self.WORKmodel_cancel)
        self.WORKmodel_ui.ok_pushButton.clicked.connect(self.WORKmodel_set)

        self.IPandPORT_ui.cancel_pushButton.clicked.connect(
            self.IPandPORT_cancel)
        self.IPandPORT_ui.read_pushButton.clicked.connect(self.IPandPORT_read)
        self.IPandPORT_ui.ok_pushButton.clicked.connect(self.IPandPORT_set)

        self.Frame_ui.cancel_pushButton.clicked.connect(self.Frame_cancel)
        self.Frame_ui.read_pushButton.clicked.connect(self.Frame_read)
        self.Frame_ui.ok_pushButton.clicked.connect(self.Frame_set)

        self.three.state_pushButton.clicked.connect(self.status_read)
        self.three.version_pushButton.clicked.connect(self.F16ver_check)
        self.three.read_pushButton.clicked.connect(self.F16_read)
        self.three.reset_pushButton.clicked.connect(self.F16_reset)
        self.three.pushButton.clicked.connect(self.F16_reboot)
        self.three.worknet_pushButton.clicked.connect(self.F16_worknet)

        self.activeTYPE={'AUTO':0,'SMSD':1,'CTRL':2,'DATA':3,'MIXD':4,'DIO':5}
        self.protocolTYPE={'PROT':0,'DCUDP':1,'DCTCP':2,'TRNS':3,'SMSCLI':4,'SMSSER':5,'HTTP':6,'CUST':7}
        self.bindingCENTER={'0':0,'1':1,'2':2,'4':3,"8":4,'16':5,'255':6}
        self.bindingCENTERset={'关闭':0,'数据中心1':1,'数据中心2':2,'数据中心3':4,'数据中心4':8,'数据中心5':16,'所有中心':255}

        self.three.ok_pushButton.clicked.connect(self.F16_set)
        self.F16WORKtype_ui.pushButton_2.clicked.connect(self.F16_workmode_set)
        self.F16WORKtype_ui.pushButton_3.clicked.connect(self.F16_Workmode_cancel)

        self.F16IPandPORTset_ui.pushButton_3.clicked.connect(self.F16_IPandPORT_cancel)
        self.F16IPandPORTset_ui.pushButton_2.clicked.connect(self.F16_IPandPORT_set)

        self.F16COMset_ui.cancel_pushButton.clicked.connect(self.F16_COMset_cancel)
        self.F16COMset_ui.ok_pushButton.clicked.connect(self.F16_COMset_set)

        self.F16SMSset_ui.pushButton_3.clicked.connect(self.F16_SMSset_cancel)
        self.F16SMSset_ui.pushButton_2.clicked.connect(self.F16_SMSset_set)

    def F16_SMSset_set(self):
        self.log_textEdit.append("<font color='forestgreen'>下载短信配置：\n</font>")
        self.F16SMSset_dialog.setEnabled(False)

        self.F16SMSset_thread=threading.Thread(target=self.F16_SMSset_thread)
        self.F16SMSset_thread.setDaemon(True)
        self.F16SMSset_thread_timer=QTimer()
        self.F16SMSset_thread_timer.timeout.connect(self.F16_SMSset_thread_check)
        self.F16SMSset_thread.start()
        self.F16SMSset_thread_timer.start(100)
    def F16_SMSset_thread_check(self):
        if self.F16SMSset_thread.is_alive():
            pass
        else:
            self.F16SMSset_thread_timer.stop()
            self.F16SMSset_dialog.setEnabled(True)
            if self.F16SMSset_ui.SMSset_comboBox.currentText() == "关闭":
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;短信配置：关闭</font>")
            else:
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;短信配置：开启</font>")
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;短信配置密码：%s</font>"%self.F16SMSset_ui.SMSset_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;管理员号码：%s</font>"%self.F16SMSset_ui.admin_lineEdit.text())
    def F16_SMSset_thread(self):
        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        if self.F16SMSset_ui.SMSset_comboBox.currentText()=="关闭":
            at='at+smscf=%d'%self.F16SMSset_ui.SMSset_comboBox.currentIndex()
            self.set_at_write(at)
        else:
            at='at+smscf=%d'%self.F16SMSset_ui.SMSset_comboBox.currentIndex()
            at1='at+smscpw=%s'%self.F16SMSset_ui.SMSset_lineEdit.text()[0:8]
            at2='at+smsadmnum=%s'%self.F16SMSset_ui.admin_lineEdit.text()[0:30]
            self.set_at_write(at)
            self.set_at_write(at1)
            self.set_at_write(at2)
        quit_at = 'at+quit'
        self.set_at_write(quit_at)

    def F16_SMSset_cancel(self):
        self.F16SMSset_dialog.close()

    #配置串口
    def F16_COMset_set(self):
        self.log_textEdit.append("<font color='forestgreen'>下载配置串口：\n</font>")
        self.F16COMset_dialog.setEnabled(False)

        self.F16COMset_thread=threading.Thread(target=self.F16_COMset_thread)
        self.F16COMset_thread.setDaemon(True)
        self.F16COMset_thread_timer=QTimer()
        self.F16COMset_thread_timer.timeout.connect(self.F16_COMset_thread_check)
        self.F16COMset_thread.start()
        self.F16COMset_thread_timer.start(100)
    def F16_COMset_thread_check(self):
        if self.F16COMset_thread.is_alive():
            pass
        else:
            self.F16COMset_thread_timer.stop()
            self.F16COMset_dialog.setEnabled(True)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口1波特率：%s</font>" % self.F16COMset_ui.com1_baudrate_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口1校验：%s</font>" % self.F16COMset_ui.com1_parity_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口1通信绑定：%s</font>" % self.F16COMset_ui.com1_bind_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口2波特率：%s</font>" % self.F16COMset_ui.com2_baudrate_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口2校验：%s</font>" % self.F16COMset_ui.com2_parity_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口2通信绑定：%s</font>" % self.F16COMset_ui.com2_bind_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;RS485波特率：%s</font>" % self.F16COMset_ui.rs485_baudrate_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;RS485校验：%s</font>" % self.F16COMset_ui.rs485_parity_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;RS485通信绑定：%s</font>" % self.F16COMset_ui.rs485_bind_comboBox.currentText())
    def F16_COMset_thread(self):
        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        at='at+ipr=%s'%self.F16COMset_ui.com1_baudrate_comboBox.currentText()
        at2='at+sermode=%s'%self.F16COMset_ui.com1_parity_comboBox.currentText()
        at3='at+serbindcnt=%d'%self.bindingCENTERset.get(self.F16COMset_ui.com1_bind_comboBox.currentText())
        at4='at+setipr2=%s'%self.F16COMset_ui.com2_baudrate_comboBox.currentText()
        at5='at+sermode2=%s'%self.F16COMset_ui.com2_parity_comboBox.currentText()
        at6='at+serbindcnt2=%d'%self.bindingCENTERset.get(self.F16COMset_ui.com2_bind_comboBox.currentText())
        at7='at+RS485ipr=%s'%self.F16COMset_ui.rs485_baudrate_comboBox.currentText()
        at8='at+RS485sermode=%s'%self.F16COMset_ui.rs485_parity_comboBox.currentText()
        at9='at+RS485bindcnt=%d'%self.bindingCENTERset.get(self.F16COMset_ui.rs485_bind_comboBox.currentText())
        self.set_at_write(at)
        self.set_at_write(at2)
        self.set_at_write(at3)
        self.set_at_write(at4)
        self.set_at_write(at5)
        self.set_at_write(at6)
        self.set_at_write(at7)
        self.set_at_write(at8)
        self.set_at_write(at9)
        quit_at = 'at+quit'
        self.set_at_write(quit_at)
    def F16_COMset_cancel(self):
        self.F16COMset_dialog.close()

    #配置中心服务器
    def F16_IPandPORT_set(self):
        self.log_textEdit.append("<font color='forestgreen'>下载配置中心服务器：\n</font>")
        self.F16IPandPORTset_dialog.setEnabled(False)

        self.F16IPandPORTset_thread=threading.Thread(target=self.F16_IPandPORT_set_thread)
        self.F16IPandPORTset_thread.setDaemon(True)
        self.F16IPandPORTset_thread_timer=QTimer()
        self.F16IPandPORTset_thread_timer.timeout.connect(self.F16_IPandPORT_set_thread_check)
        self.F16IPandPORTset_thread.start()
        self.F16IPandPORTset_thread_timer.start(100)
    def F16_IPandPORT_set_thread_check(self):
        if self.F16IPandPORTset_thread.is_alive():
            pass
        else:
            self.F16IPandPORTset_thread_timer.stop()
            self.F16IPandPORTset_dialog.setEnabled(True)

            sernum = self.F16IPandPORTset_ui.serverNum_comboBox.currentText()
            if sernum=='1':
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;服务器数量：1</font>")
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;主服务器IP：%s</font>" % self.F16IPandPORTset_ui.server_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;主服务器端口：%s</font>" % self.F16IPandPORTset_ui.port_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;备服务器IP：%s</font>" % self.F16IPandPORTset_ui.server1_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;备服务器端口：%s</font>" % self.F16IPandPORTset_ui.port1_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;返回主中心：%s</font>" % self.F16IPandPORTset_ui.reserver_comboBox.currentText())
            elif sernum=='2':
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;服务器数量：2</font>")
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;主服务器IP：%s</font>" % self.F16IPandPORTset_ui.server_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;主服务器端口：%s</font>" % self.F16IPandPORTset_ui.port_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器2IP：%s</font>" % self.F16IPandPORTset_ui.server2_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器2端口：%s</font>" % self.F16IPandPORTset_ui.port2_lineEdit.text())
            elif sernum=='3':
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;服务器数量：3</font>")
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;主服务器IP：%s</font>" % self.F16IPandPORTset_ui.server_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;主服务器端口：%s</font>" % self.F16IPandPORTset_ui.port_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器2IP：%s</font>" % self.F16IPandPORTset_ui.server2_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器2端口：%s</font>" % self.F16IPandPORTset_ui.port2_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器3IP：%s</font>" % self.F16IPandPORTset_ui.server3_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器3端口：%s</font>" % self.F16IPandPORTset_ui.port3_lineEdit.text())
            elif sernum=='4':
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;服务器数量：4</font>")
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;主服务器IP：%s</font>" % self.F16IPandPORTset_ui.server_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;主服务器端口：%s</font>" % self.F16IPandPORTset_ui.port_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器2IP：%s</font>" % self.F16IPandPORTset_ui.server2_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器2端口：%s</font>" % self.F16IPandPORTset_ui.port2_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器3IP：%s</font>" % self.F16IPandPORTset_ui.server3_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器3端口：%s</font>" % self.F16IPandPORTset_ui.port3_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器4IP：%s</font>" % self.F16IPandPORTset_ui.server4_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器4端口：%s</font>" % self.F16IPandPORTset_ui.port4_lineEdit.text())
            elif sernum=='5':
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;服务器数量：5</font>")
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;主服务器IP：%s</font>" % self.F16IPandPORTset_ui.server_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;主服务器端口：%s</font>" % self.F16IPandPORTset_ui.port_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器2IP：%s</font>" % self.F16IPandPORTset_ui.server2_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器2端口：%s</font>" % self.F16IPandPORTset_ui.port2_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器3IP：%s</font>" % self.F16IPandPORTset_ui.server3_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器3端口：%s</font>" % self.F16IPandPORTset_ui.port3_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器4IP：%s</font>" % self.F16IPandPORTset_ui.server4_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器4端口：%s</font>" % self.F16IPandPORTset_ui.port4_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器5IP：%s</font>" % self.F16IPandPORTset_ui.server5_lineEdit.text())
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;服务器5端口：%s</font>" % self.F16IPandPORTset_ui.port5_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;重连间隔：%s</font>" % self.F16IPandPORTset_ui.reconnect_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;重连次数：%s</font>" % self.F16IPandPORTset_ui.reconnectTimes_lineEdit.text())

    def F16_IPandPORT_set_thread(self):
        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        sernum=self.F16IPandPORTset_ui.serverNum_comboBox.currentText()
        if sernum=='1':
            at='at+svrcnt=1'
            at1='at+ipad=%s'%self.F16IPandPORTset_ui.server_lineEdit.text()
            at2='at+port=%s'%self.F16IPandPORTset_ui.port_lineEdit.text()
            at3='at+ipsec=%s'%self.F16IPandPORTset_ui.server1_lineEdit.text()
            at4='at+ptsec=%s'%self.F16IPandPORTset_ui.port1_lineEdit.text()
            at5='at+retmain=%d'%self.F16IPandPORTset_ui.reserver_comboBox.currentIndex()
            self.set_at_write(at)
            self.set_at_write(at1)
            self.set_at_write(at2)
            self.set_at_write(at3)
            self.set_at_write(at4)
            self.set_at_write(at5)
        elif sernum=='2':
            at='at+svrcnt=2'
            at1='at+ipad=%s'%self.F16IPandPORTset_ui.server_lineEdit.text()
            at2='at+port=%s'%self.F16IPandPORTset_ui.port_lineEdit.text()
            at3='at+ipad1=%s'%self.F16IPandPORTset_ui.server2_lineEdit.text()
            at4='at+port1=%s'%self.F16IPandPORTset_ui.port2_lineEdit.text()
            self.set_at_write(at)
            self.set_at_write(at1)
            self.set_at_write(at2)
            self.set_at_write(at3)
            self.set_at_write(at4)
        elif sernum=='3':
            at='at+svrcnt=3'
            at1='at+ipad=%s'%self.F16IPandPORTset_ui.server_lineEdit.text()
            at2='at+port=%s'%self.F16IPandPORTset_ui.port_lineEdit.text()
            at3='at+ipad1=%s'%self.F16IPandPORTset_ui.server2_lineEdit.text()
            at4='at+port1=%s'%self.F16IPandPORTset_ui.port2_lineEdit.text()
            at5='at+ipad2=%s'%self.F16IPandPORTset_ui.server3_lineEdit.text()
            at6='at+port2=%s'%self.F16IPandPORTset_ui.port3_lineEdit.text()
            self.set_at_write(at)
            self.set_at_write(at1)
            self.set_at_write(at2)
            self.set_at_write(at3)
            self.set_at_write(at4)
            self.set_at_write(at5)
            self.set_at_write(at6)
        elif sernum=='4':
            at='at+svrcnt=4'
            at1='at+ipad=%s'%self.F16IPandPORTset_ui.server_lineEdit.text()
            at2='at+port=%s'%self.F16IPandPORTset_ui.port_lineEdit.text()
            at3='at+ipad1=%s'%self.F16IPandPORTset_ui.server2_lineEdit.text()
            at4='at+port1=%s'%self.F16IPandPORTset_ui.port2_lineEdit.text()
            at5='at+ipad2=%s'%self.F16IPandPORTset_ui.server3_lineEdit.text()
            at6='at+port2=%s'%self.F16IPandPORTset_ui.port3_lineEdit.text()
            at7='at+ipad3=%s'%self.F16IPandPORTset_ui.server4_lineEdit.text()
            at8='at+port3=%s'%self.F16IPandPORTset_ui.port4_lineEdit.text()
            self.set_at_write(at)
            self.set_at_write(at1)
            self.set_at_write(at2)
            self.set_at_write(at3)
            self.set_at_write(at4)
            self.set_at_write(at5)
            self.set_at_write(at6)
            self.set_at_write(at7)
            self.set_at_write(at8)
        elif sernum=='5':
            at='at+svrcnt=5'
            at1='at+ipad=%s'%self.F16IPandPORTset_ui.server_lineEdit.text()
            at2='at+port=%s'%self.F16IPandPORTset_ui.port_lineEdit.text()
            at3='at+ipad1=%s'%self.F16IPandPORTset_ui.server2_lineEdit.text()
            at4='at+port1=%s'%self.F16IPandPORTset_ui.port2_lineEdit.text()
            at5='at+ipad2=%s'%self.F16IPandPORTset_ui.server3_lineEdit.text()
            at6='at+port2=%s'%self.F16IPandPORTset_ui.port3_lineEdit.text()
            at7='at+ipad3=%s'%self.F16IPandPORTset_ui.server4_lineEdit.text()
            at8='at+port3=%s'%self.F16IPandPORTset_ui.port4_lineEdit.text()
            at9='at+ipad4=%s'%self.F16IPandPORTset_ui.server5_lineEdit.text()
            at10='at+port4=%s'%self.F16IPandPORTset_ui.port5_lineEdit.text()
            self.set_at_write(at)
            self.set_at_write(at1)
            self.set_at_write(at2)
            self.set_at_write(at3)
            self.set_at_write(at4)
            self.set_at_write(at5)
            self.set_at_write(at6)
            self.set_at_write(at7)
            self.set_at_write(at8)
            self.set_at_write(at9)
            self.set_at_write(at10)
        at11='at+rdlwt=%s'%self.F16IPandPORTset_ui.reconnect_lineEdit.text()
        at12='at+retry=%s'%self.F16IPandPORTset_ui.reconnectTimes_lineEdit.text()
        self.set_at_write(at11)
        self.set_at_write(at12)
        quit_at = 'at+quit'
        self.set_at_write(quit_at)
    def F16_IPandPORT_cancel(self):
        self.F16IPandPORTset_dialog.close()

    def F16_Workmode_cancel(self):
        self.F16WORKtype_dialog.close()

    #配置工作模式
    def F16_workmode_set(self):
        self.F16WORKtype_dialog.setEnabled(False)
        self.log_textEdit.append("<font color='forestgreen'>下载配置工作模式：\n</font>")


        self.F16workmode_thread=threading.Thread(target=self.F16_workmode_set_thread)
        self.F16workmode_thread.setDaemon(True)
        self.F16workmode_thread_timer=QTimer()
        self.F16workmode_thread_timer.timeout.connect(self.F16_workmode_set_thread_check)
        self.F16workmode_thread.start()
        self.F16workmode_thread_timer.start(100)
    def F16_workmode_set_thread_check(self):
        if self.F16workmode_thread.is_alive():
            pass
        else:
            self.F16workmode_thread_timer.stop()
            self.F16WORKtype_dialog.setEnabled(True)
            work_protocol = self.F16WORKtype_ui.protocolType_comboBox.currentText()
            if work_protocol == 'PROT':
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;工作协议：PROT</font>")
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;设备ID：%s</font>"%(self.F16WORKtype_ui.lineEdit.text()[0:8]))
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;手机号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_2.text()[0:11]))
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;数据转义：%s</font>"%self.F16WORKtype_ui.comboBox.currentText())
                active_type = self.F16WORKtype_ui.activeType_comboBox.currentText()
                if active_type == '自动':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：自动</font>")
                elif active_type=='短信激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：短信激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_3.text()[0:30]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活密码：%s</font>"%(self.F16WORKtype_ui.lineEdit_4.text()[0:8]))
                elif active_type == '电话激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：电话激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;电话激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_5.text()[0:30]))
                elif active_type == '串口激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：串口激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活接口：%s</font>"%self.F16WORKtype_ui.comboBox_2.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;数据格式：%s</font>"%self.F16WORKtype_ui.comboBox_5.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;上线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_6.text()[0:20]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;下线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_7.text()[0:20]))
                elif active_type == '混合激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：混合激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;电话激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_9.text()[0:30]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_10.text()[0:30]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;上线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_11.text()[0:20]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;下线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_12.text()[0:20]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活接口：%s</font>"%self.F16WORKtype_ui.comboBox_3.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;数据格式：%s</font>"%self.F16WORKtype_ui.comboBox_4.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O1：%s</font>"%self.F16WORKtype_ui.comboBox_6.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O2：%s</font>"%self.F16WORKtype_ui.comboBox_7.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活密码：%s</font>"%(self.F16WORKtype_ui.lineEdit_8.text()[0:8]))
                elif active_type == 'I/O激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：I/O激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O激活方式：休眠/唤醒</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O选择：%s</font>"%self.F16WORKtype_ui.comboBox_9.currentText())
            elif work_protocol == 'DCTCP':
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;工作协议：DCTCP</font>")
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;手机号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_23.text()[0:11]))
                active_type = self.F16WORKtype_ui.activeType_comboBox.currentText()
                if active_type == '自动':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：自动</font>")
                elif active_type=='短信激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：短信激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_3.text()[0:30]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活密码：%s</font>"%(self.F16WORKtype_ui.lineEdit_4.text()[0:8]))
                elif active_type == '电话激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：电话激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;电话激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_5.text()[0:30]))
                elif active_type == '串口激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：串口激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活接口：%s</font>"%self.F16WORKtype_ui.comboBox_2.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;数据格式：%s</font>"%self.F16WORKtype_ui.comboBox_5.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;上线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_6.text()[0:20]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;下线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_7.text()[0:20]))
                elif active_type == '混合激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：混合激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;电话激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_9.text()[0:30]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_10.text()[0:30]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;上线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_11.text()[0:20]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;下线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_12.text()[0:20]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活接口：%s</font>"%self.F16WORKtype_ui.comboBox_3.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;数据格式：%s</font>"%self.F16WORKtype_ui.comboBox_4.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O1：%s</font>"%self.F16WORKtype_ui.comboBox_6.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O2：%s</font>"%self.F16WORKtype_ui.comboBox_7.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活密码：%s</font>"%(self.F16WORKtype_ui.lineEdit_8.text()[0:8]))
                elif active_type == 'I/O激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：I/O激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O激活方式：休眠/唤醒</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O选择：%s</font>"%self.F16WORKtype_ui.comboBox_9.currentText())
            elif work_protocol=='DCUDP':
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;工作协议：DCUDP</font>")
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;手机号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_23.text()[0:11]))
                active_type = self.F16WORKtype_ui.activeType_comboBox.currentText()
                if active_type == '自动':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：自动</font>")
                elif active_type=='短信激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：短信激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_3.text()[0:30]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活密码：%s</font>"%(self.F16WORKtype_ui.lineEdit_4.text()[0:8]))
                elif active_type == '电话激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：电话激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;电话激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_5.text()[0:30]))
                elif active_type == '串口激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：串口激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活接口：%s</font>"%self.F16WORKtype_ui.comboBox_2.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;数据格式：%s</font>"%self.F16WORKtype_ui.comboBox_5.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;上线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_6.text()[0:20]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;下线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_7.text()[0:20]))
                elif active_type == '混合激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：混合激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;电话激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_9.text()[0:30]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_10.text()[0:30]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;上线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_11.text()[0:20]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;下线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_12.text()[0:20]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活接口：%s</font>"%self.F16WORKtype_ui.comboBox_3.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;数据格式：%s</font>"%self.F16WORKtype_ui.comboBox_4.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O1：%s</font>"%self.F16WORKtype_ui.comboBox_6.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O2：%s</font>"%self.F16WORKtype_ui.comboBox_7.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活密码：%s</font>"%(self.F16WORKtype_ui.lineEdit_8.text()[0:8]))
                elif active_type == 'I/O激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：I/O激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O激活方式：休眠/唤醒</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O选择：%s</font>"%self.F16WORKtype_ui.comboBox_9.currentText())
            elif work_protocol == 'TRNS':
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;工作协议：TRNS</font>")
            elif work_protocol == 'SMSCLI':
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;工作协议：SMSCLI</font>")
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信号码组1：%s</font>"%self.F16WORKtype_ui.lineEdit_24.text())
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信号码组2：%s</font>"%self.F16WORKtype_ui.lineEdit_25.text())
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信号码组3：%s</font>"%self.F16WORKtype_ui.lineEdit_26.text())
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信号码组4：%s</font>"%self.F16WORKtype_ui.lineEdit_27.text())
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信号码组5：%s</font>"%self.F16WORKtype_ui.lineEdit_28.text())
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;是否显示号码：%s</font>"%self.F16WORKtype_ui.comboBox_18.currentText())
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;16进制强制转文本：%s</font>"%self.F16WORKtype_ui.comboBox_19.currentText())
            elif work_protocol == 'SMSSER':
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;工作协议：SMSSER</font>")
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;是否显示号码：%s</font>"%self.F16WORKtype_ui.comboBox_20.currentText())
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;16进制强制转文本：%s</font>"%self.F16WORKtype_ui.comboBox_21.currentText())
            elif work_protocol == 'HTTP':
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;工作协议：HTTP</font>")
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;HTTP请求方式：%s</font>"%self.F16WORKtype_ui.comboBox_30.currentText())
                active_type = self.F16WORKtype_ui.activeType_comboBox.currentText()
                if active_type == '自动':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：自动</font>")
                elif active_type=='短信激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：短信激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_3.text()[0:30]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活密码：%s</font>"%(self.F16WORKtype_ui.lineEdit_4.text()[0:8]))
                elif active_type == '电话激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：电话激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;电话激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_5.text()[0:30]))
                elif active_type == '串口激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：串口激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活接口：%s</font>"%self.F16WORKtype_ui.comboBox_2.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;数据格式：%s</font>"%self.F16WORKtype_ui.comboBox_5.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;上线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_6.text()[0:20]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;下线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_7.text()[0:20]))
                elif active_type == '混合激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：混合激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;电话激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_9.text()[0:30]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_10.text()[0:30]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;上线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_11.text()[0:20]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;下线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_12.text()[0:20]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活接口：%s</font>"%self.F16WORKtype_ui.comboBox_3.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;数据格式：%s</font>"%self.F16WORKtype_ui.comboBox_4.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O1：%s</font>"%self.F16WORKtype_ui.comboBox_6.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O2：%s</font>"%self.F16WORKtype_ui.comboBox_7.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活密码：%s</font>"%(self.F16WORKtype_ui.lineEdit_8.text()[0:8]))
                elif active_type == 'I/O激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：I/O激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O激活方式：休眠/唤醒</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O选择：%s</font>"%self.F16WORKtype_ui.comboBox_9.currentText())
            elif work_protocol == '自定义':
                self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;工作协议：自定义</font>")
                devmode = self.F16WORKtype_ui.comboBox_31.currentText()
                if devmode == '服务端模式':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;设备模式：服务端模式</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;传输协议：%s</font>"%self.F16WORKtype_ui.comboBox_32.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;监听端口：%s</font>"%self.F16WORKtype_ui.lineEdit_39.text())
                else:
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;设备模式：客户端模式</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;传输协议：%s</font>"%self.F16WORKtype_ui.comboBox_32.currentText())
                    heart = self.F16WORKtype_ui.comboBox_33.currentText()
                    if heart == '开启':
                        self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;注册及心跳：开启</font>")
                        self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;包格式：%s</font>"%self.F16WORKtype_ui.comboBox_10.currentText())
                        self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;注册包：%s</font>"%self.F16WORKtype_ui.lineEdit_13.text())
                        self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;注册包回应：%s</font>"%self.F16WORKtype_ui.lineEdit_15.text())
                        self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;心跳包：%s</font>"%self.F16WORKtype_ui.lineEdit_14.text())
                        self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;心跳包回应：%s</font>"%self.F16WORKtype_ui.lineEdit_16.text())
                    else:
                        self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;注册及心跳：关闭</font>")

                active_type = self.F16WORKtype_ui.activeType_comboBox.currentText()
                if active_type == '自动':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：自动</font>")
                elif active_type=='短信激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：短信激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_3.text()[0:30]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活密码：%s</font>"%(self.F16WORKtype_ui.lineEdit_4.text()[0:8]))
                elif active_type == '电话激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：电话激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;电话激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_5.text()[0:30]))
                elif active_type == '串口激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：串口激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活接口：%s</font>"%self.F16WORKtype_ui.comboBox_2.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;数据格式：%s</font>"%self.F16WORKtype_ui.comboBox_5.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;上线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_6.text()[0:20]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;下线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_7.text()[0:20]))
                elif active_type == '混合激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：混合激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;电话激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_9.text()[0:30]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活号码：%s</font>"%(self.F16WORKtype_ui.lineEdit_10.text()[0:30]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;上线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_11.text()[0:20]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;下线数据：%s</font>"%(self.F16WORKtype_ui.lineEdit_12.text()[0:20]))
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活接口：%s</font>"%self.F16WORKtype_ui.comboBox_3.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;数据格式：%s</font>"%self.F16WORKtype_ui.comboBox_4.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O1：%s</font>"%self.F16WORKtype_ui.comboBox_6.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O2：%s</font>"%self.F16WORKtype_ui.comboBox_7.currentText())
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;短信激活密码：%s</font>"%(self.F16WORKtype_ui.lineEdit_8.text()[0:8]))
                elif active_type == 'I/O激活':
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;激活方式：I/O激活</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O激活方式：休眠/唤醒</font>")
                    self.log_textEdit.append("<font color='darkviolet'>&nbsp;&nbsp;I/O选择：%s</font>"%self.F16WORKtype_ui.comboBox_9.currentText())
    def F16_workmode_set_thread(self):
        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        work_protocol=self.F16WORKtype_ui.protocolType_comboBox.currentText()
        if work_protocol=='PROT':
            at='at+promode=PROT'
            at1='at+idnt=%s'%(self.F16WORKtype_ui.lineEdit.text()[0:8])
            at2='at+phon=%s'%(self.F16WORKtype_ui.lineEdit_2.text()[0:11])
            at3='at+straight=%d'%self.F16WORKtype_ui.comboBox.currentIndex()
            self.set_at_write(at)
            self.set_at_write(at1)
            self.set_at_write(at2)
            self.set_at_write(at3)

            active_type=self.F16WORKtype_ui.activeType_comboBox.currentText()
            if active_type=='自动':
                at4='at+acti=AUTO'
                self.set_at_write(at4)
            elif active_type=='短信激活':
                at4='at+acti=SMSD'
                at5='at+actsmsno=%s'%(self.F16WORKtype_ui.lineEdit_3.text()[0:30])
                at6='at+smsdpswd=%s'%(self.F16WORKtype_ui.lineEdit_4.text()[0:8])
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
            elif active_type=='电话激活':
                at4='at+acti=ctrl'
                at5='at+ctrlno=%s'%(self.F16WORKtype_ui.lineEdit_5.text()[0:30])
                self.set_at_write(at4)
                self.set_at_write(at5)
            elif active_type=='串口激活':
                at4='at+acti=data'
                at5='at+actserlno=%d'%(self.F16WORKtype_ui.comboBox_2.currentIndex()+1)
                at6='at+actdatafmt=%d'%self.F16WORKtype_ui.comboBox_5.currentIndex()
                at7='at+donpswd=%s'%(self.F16WORKtype_ui.lineEdit_6.text()[0:20])
                at8='at+doffpswd=%s'%(self.F16WORKtype_ui.lineEdit_7.text()[0:20])
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
                self.set_at_write(at7)
                self.set_at_write(at8)
            elif active_type=='混合激活':
                at4='at+acti=mixd'
                at5='at+ctrlno=%s'%(self.F16WORKtype_ui.lineEdit_9.text()[0:30])
                at6='at+actsmsno=%s'%(self.F16WORKtype_ui.lineEdit_10.text()[0:30])
                at7='at+donpswd=%s'%(self.F16WORKtype_ui.lineEdit_11.text()[0:20])
                at8='at+doffpswd=%s'%(self.F16WORKtype_ui.lineEdit_12.text()[0:20])
                at9='at+actserlno=%d'%(self.F16WORKtype_ui.comboBox_3.currentIndex()+1)
                at10='at+actdatafmt=%d'%self.F16WORKtype_ui.comboBox_4.currentIndex()
                at11='at+smsdpswd=%s'%(self.F16WORKtype_ui.lineEdit_8.text()[0:8])
                io1=self.F16WORKtype_ui.comboBox_6.currentText()
                if io1=='未启用':
                    io1=0
                elif io1=='激活':
                    io1=4
                else:
                    io1=5
                at12='at+dioworkmode1=%d'%io1
                io2=self.F16WORKtype_ui.comboBox_7.currentText()
                if io2=='未启用':
                    io2=0
                elif io2=='激活':
                    io2=4
                else:
                    io2=5
                at13='at+dioworkmode2=%d'%io2
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
                self.set_at_write(at7)
                self.set_at_write(at8)
                self.set_at_write(at9)
                self.set_at_write(at10)
                self.set_at_write(at11)
                self.set_at_write(at12)
                self.set_at_write(at13)
            elif active_type=='I/O激活':
                at4='at+acti=dio'
                if self.F16WORKtype_ui.comboBox_9.currentIndex()==0:
                    at5='at+dioworkmode1=4'
                    at6='at+dioworkmode2=0'
                    at7='at+dioworkmode3=0'
                elif self.F16WORKtype_ui.comboBox_9.currentIndex()==1:
                    at5='at+dioworkmode1=0'
                    at6='at+dioworkmode2=4'
                    at7='at+dioworkmode3=0'
                else:
                    at5='at+dioworkmode1=0'
                    at6='at+dioworkmode2=0'
                    at7='at+dioworkmode3=4'
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
                self.set_at_write(at7)
            quit_at='at+quit'
            self.set_at_write(quit_at)
        elif work_protocol=='DCTCP' or work_protocol=='DCUDP':
            at='at+phon=%s'%(self.F16WORKtype_ui.lineEdit_23.text()[0:11])
            if work_protocol=='DCTCP':
                at1='at+promode=DCTCP'
            else:
                at1='at+promode=DCUDP'
            self.set_at_write(at1)
            self.set_at_write(at)
            active_type=self.F16WORKtype_ui.activeType_comboBox.currentText()
            if active_type=='自动':
                at4='at+acti=AUTO'
                self.set_at_write(at4)
            elif active_type=='短信激活':
                at4='at+acti=SMSD'
                at5='at+actsmsno=%s'%(self.F16WORKtype_ui.lineEdit_3.text()[0:30])
                at6='at+smsdpswd=%s'%(self.F16WORKtype_ui.lineEdit_4.text()[0:8])
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
            elif active_type=='电话激活':
                at4='at+acti=ctrl'
                at5='at+ctrlno=%s'%(self.F16WORKtype_ui.lineEdit_5.text()[0:30])
                self.set_at_write(at4)
                self.set_at_write(at5)
            elif active_type=='串口激活':
                at4='at+acti=data'
                at5='at+actserlno=%d'%(self.F16WORKtype_ui.comboBox_2.currentIndex()+1)
                at6='at+actdatafmt=%d'%self.F16WORKtype_ui.comboBox_5.currentIndex()
                at7='at+donpswd=%s'%(self.F16WORKtype_ui.lineEdit_6.text()[0:20])
                at8='at+doffpswd=%s'%(self.F16WORKtype_ui.lineEdit_7.text()[0:20])
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
                self.set_at_write(at7)
                self.set_at_write(at8)
            elif active_type=='混合激活':
                at4='at+acti=mixd'
                at5='at+ctrlno=%s'%(self.F16WORKtype_ui.lineEdit_5.text()[0:30])
                at6='at+actsmsno=%s'%(self.F16WORKtype_ui.lineEdit_3.text()[0:30])
                at7='at+donpswd=%s'%(self.F16WORKtype_ui.lineEdit_6.text()[0:20])
                at8='at+doffpswd=%s'%(self.F16WORKtype_ui.lineEdit_7.text()[0:20])
                at9='at+actserlno=%d'%(self.F16WORKtype_ui.comboBox_2.currentIndex()+1)
                at10='at+actdatafmt=%d'%self.F16WORKtype_ui.comboBox_5.currentIndex()
                at11='at+smsdpswd=%s'%(self.F16WORKtype_ui.lineEdit_4.text()[0:8])
                io1=self.F16WORKtype_ui.comboBox_6.currentText()
                if io1=='未启用':
                    io1=0
                elif io1=='激活':
                    io1=4
                else:
                    io1=5
                at12='at+dioworkmode1=%d'%io1
                io2=self.F16WORKtype_ui.comboBox_7.currentText()
                if io2=='未启用':
                    io2=0
                elif io2=='激活':
                    io2=4
                else:
                    io2=5
                at13='at+dioworkmode2=%d'%io2
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
                self.set_at_write(at7)
                self.set_at_write(at8)
                self.set_at_write(at9)
                self.set_at_write(at10)
                self.set_at_write(at11)
                self.set_at_write(at12)
                self.set_at_write(at13)
            elif active_type=='I/O激活':
                at4='at+acti=dio'
                if self.F16WORKtype_ui.comboBox_9.currentIndex()==0:
                    at5='at+dioworkmode1=4'
                    at6='at+dioworkmode2=0'
                    at7='at+dioworkmode3=0'
                elif self.F16WORKtype_ui.comboBox_9.currentIndex()==1:
                    at5='at+dioworkmode1=0'
                    at6='at+dioworkmode2=4'
                    at7='at+dioworkmode3=0'
                else:
                    at5='at+dioworkmode1=0'
                    at6='at+dioworkmode2=0'
                    at7='at+dioworkmode3=4'
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
                self.set_at_write(at7)
            quit_at='at+quit'
            self.set_at_write(quit_at)
        elif work_protocol=='TRNS':
            at='at+promode=TRNS'
            self.set_at_write(at)
            quit_at='at+quit'
            self.set_at_write(quit_at)
        elif work_protocol=='SMSCLI':
            at='at+promode=SMSCLI'
            at1='at+phone1=%s'%self.F16WORKtype_ui.lineEdit_24.text()
            at2='at+phone2=%s'%self.F16WORKtype_ui.lineEdit_25.text()
            at3='at+phone3=%s'%self.F16WORKtype_ui.lineEdit_26.text()
            at4='at+phone4=%s'%self.F16WORKtype_ui.lineEdit_27.text()
            at5='at+phone5=%s'%self.F16WORKtype_ui.lineEdit_28.text()
            at6='at+phonenoshow=%d'%self.F16WORKtype_ui.comboBox_18.currentIndex()
            at7='at+encodehexsms=%d'%self.F16WORKtype_ui.comboBox_19.currentIndex()
            self.set_at_write(at)
            self.set_at_write(at1)
            self.set_at_write(at2)
            self.set_at_write(at3)
            self.set_at_write(at4)
            self.set_at_write(at5)
            self.set_at_write(at6)
            self.set_at_write(at7)
            quit_at='at+quit'
            self.set_at_write(quit_at)
        elif work_protocol=='SMSSER':
            at='at+promode=SMSSER'
            at1='at+phonenoshow=%d'%self.F16WORKtype_ui.comboBox_20.currentIndex()
            at2='at+encodehexsms=%d'%self.F16WORKtype_ui.comboBox_21.currentIndex()
            self.set_at_write(at)
            self.set_at_write(at1)
            self.set_at_write(at2)
            quit_at='at+quit'
            self.set_at_write(quit_at)
        elif work_protocol=='HTTP':
            at='at+promode=HTTP'
            at1='at+httpreqmode=%d'%self.F16WORKtype_ui.comboBox_30.currentIndex()
            self.set_at_write(at)
            self.set_at_write(at1)
            active_type=self.F16WORKtype_ui.activeType_comboBox.currentText()
            if active_type=='自动':
                at4='at+acti=AUTO'
                self.set_at_write(at4)
            elif active_type=='短信激活':
                at4='at+acti=SMSD'
                at5='at+actsmsno=%s'%(self.F16WORKtype_ui.lineEdit_3.text()[0:30])
                at6='at+smsdpswd=%s'%(self.F16WORKtype_ui.lineEdit_4.text()[0:8])
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
            elif active_type=='电话激活':
                at4='at+acti=ctrl'
                at5='at+ctrlno=%s'%(self.F16WORKtype_ui.lineEdit_5.text()[0:30])
                self.set_at_write(at4)
                self.set_at_write(at5)
            elif active_type=='串口激活':
                at4='at+acti=data'
                at5='at+actserlno=%d'%(self.F16WORKtype_ui.comboBox_2.currentIndex()+1)
                at6='at+actdatafmt=%d'%self.F16WORKtype_ui.comboBox_5.currentIndex()
                at7='at+donpswd=%s'%(self.F16WORKtype_ui.lineEdit_6.text()[0:20])
                at8='at+doffpswd=%s'%(self.F16WORKtype_ui.lineEdit_7.text()[0:20])
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
                self.set_at_write(at7)
                self.set_at_write(at8)
            elif active_type=='混合激活':
                at4='at+acti=mixd'
                at5='at+ctrlno=%s'%(self.F16WORKtype_ui.lineEdit_5.text()[0:30])
                at6='at+actsmsno=%s'%(self.F16WORKtype_ui.lineEdit_3.text()[0:30])
                at7='at+donpswd=%s'%(self.F16WORKtype_ui.lineEdit_6.text()[0:20])
                at8='at+doffpswd=%s'%(self.F16WORKtype_ui.lineEdit_7.text()[0:20])
                at9='at+actserlno=%d'%(self.F16WORKtype_ui.comboBox_2.currentIndex()+1)
                at10='at+actdatafmt=%d'%self.F16WORKtype_ui.comboBox_5.currentIndex()
                at11='at+smsdpswd=%s'%(self.F16WORKtype_ui.lineEdit_4.text()[0:8])
                io1=self.F16WORKtype_ui.comboBox_6.currentText()
                if io1=='未启用':
                    io1=0
                elif io1=='激活':
                    io1=4
                else:
                    io1=5
                at12='at+dioworkmode1=%d'%io1
                io2=self.F16WORKtype_ui.comboBox_7.currentText()
                if io2=='未启用':
                    io2=0
                elif io2=='激活':
                    io2=4
                else:
                    io2=5
                at13='at+dioworkmode2=%d'%io2
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
                self.set_at_write(at7)
                self.set_at_write(at8)
                self.set_at_write(at9)
                self.set_at_write(at10)
                self.set_at_write(at11)
                self.set_at_write(at12)
                self.set_at_write(at13)
            elif active_type=='I/O激活':
                at4='at+acti=dio'
                if self.F16WORKtype_ui.comboBox_9.currentIndex()==0:
                    at5='at+dioworkmode1=4'
                    at6='at+dioworkmode2=0'
                    at7='at+dioworkmode3=0'
                elif self.F16WORKtype_ui.comboBox_9.currentIndex()==1:
                    at5='at+dioworkmode1=0'
                    at6='at+dioworkmode2=4'
                    at7='at+dioworkmode3=0'
                else:
                    at5='at+dioworkmode1=0'
                    at6='at+dioworkmode2=0'
                    at7='at+dioworkmode3=4'
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
                self.set_at_write(at7)
            quit_at='at+quit'
            self.set_at_write(quit_at)
        elif work_protocol=='自定义':
            at='at+promode=cust'
            self.set_at_write(at)
            devmode=self.F16WORKtype_ui.comboBox_31.currentText()
            if devmode=='服务端模式':
                at1='at+devmode=SVR'
                at2='at+trnpro=%s'%self.F16WORKtype_ui.comboBox_32.currentText()
                at3='at+lport=%s'%self.F16WORKtype_ui.lineEdit_39.text()
                self.set_at_write(at1)
                self.set_at_write(at2)
                self.set_at_write(at3)
            else:
                at1='at+devmode=CLI'
                at2='at+trnpro=%s'%self.F16WORKtype_ui.comboBox_32.currentText()
                self.set_at_write(at1)
                self.set_at_write(at2)
                heart=self.F16WORKtype_ui.comboBox_33.currentText()
                if heart=='开启':
                    at3='at+enhrt=1'
                    at4='at+hexlogin=%d'%self.F16WORKtype_ui.comboBox_10.currentIndex()
                    at5='at+connrgst=%s'%self.F16WORKtype_ui.lineEdit_13.text()
                    at6='at+connrgstrep=%s'%self.F16WORKtype_ui.lineEdit_15.text()
                    at7='at+linkrgst=%s'%self.F16WORKtype_ui.lineEdit_14.text()
                    at8='at+linkrgstrep=%s'%self.F16WORKtype_ui.lineEdit_16.text()
                    self.set_at_write(at3)
                    self.set_at_write(at4)
                    self.set_at_write(at5)
                    self.set_at_write(at6)
                    self.set_at_write(at7)
                    self.set_at_write(at8)
                else:
                    at3='at+enhrt=0'
                    self.set_at_write(at3)
            active_type=self.F16WORKtype_ui.activeType_comboBox.currentText()
            if active_type=='自动':
                at4='at+acti=AUTO'
                self.set_at_write(at4)
            elif active_type=='短信激活':
                at4='at+acti=SMSD'
                at5='at+actsmsno=%s'%(self.F16WORKtype_ui.lineEdit_3.text()[0:30])
                at6='at+smsdpswd=%s'%(self.F16WORKtype_ui.lineEdit_4.text()[0:8])
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
            elif active_type=='电话激活':
                at4='at+acti=ctrl'
                at5='at+ctrlno=%s'%(self.F16WORKtype_ui.lineEdit_5.text()[0:30])
                self.set_at_write(at4)
                self.set_at_write(at5)
            elif active_type=='串口激活':
                at4='at+acti=data'
                at5='at+actserlno=%d'%(self.F16WORKtype_ui.comboBox_2.currentIndex()+1)
                at6='at+actdatafmt=%d'%self.F16WORKtype_ui.comboBox_5.currentIndex()
                at7='at+donpswd=%s'%(self.F16WORKtype_ui.lineEdit_6.text()[0:20])
                at8='at+doffpswd=%s'%(self.F16WORKtype_ui.lineEdit_7.text()[0:20])
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
                self.set_at_write(at7)
                self.set_at_write(at8)
            elif active_type=='混合激活':
                at4='at+acti=mixd'
                at5='at+ctrlno=%s'%(self.F16WORKtype_ui.lineEdit_5.text()[0:30])
                at6='at+actsmsno=%s'%(self.F16WORKtype_ui.lineEdit_3.text()[0:30])
                at7='at+donpswd=%s'%(self.F16WORKtype_ui.lineEdit_6.text()[0:20])
                at8='at+doffpswd=%s'%(self.F16WORKtype_ui.lineEdit_7.text()[0:20])
                at9='at+actserlno=%d'%(self.F16WORKtype_ui.comboBox_2.currentIndex()+1)
                at10='at+actdatafmt=%d'%self.F16WORKtype_ui.comboBox_5.currentIndex()
                at11='at+smsdpswd=%s'%(self.F16WORKtype_ui.lineEdit_4.text()[0:8])
                io1=self.F16WORKtype_ui.comboBox_6.currentText()
                if io1=='未启用':
                    io1=0
                elif io1=='激活':
                    io1=4
                else:
                    io1=5
                at12='at+dioworkmode1=%d'%io1
                io2=self.F16WORKtype_ui.comboBox_7.currentText()
                if io2=='未启用':
                    io2=0
                elif io2=='激活':
                    io2=4
                else:
                    io2=5
                at13='at+dioworkmode2=%d'%io2
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
                self.set_at_write(at7)
                self.set_at_write(at8)
                self.set_at_write(at9)
                self.set_at_write(at10)
                self.set_at_write(at11)
                self.set_at_write(at12)
                self.set_at_write(at13)
            elif active_type=='I/O激活':
                at4='at+acti=dio'
                if self.F16WORKtype_ui.comboBox_9.currentIndex()==0:
                    at5='at+dioworkmode1=4'
                    at6='at+dioworkmode2=0'
                    at7='at+dioworkmode3=0'
                elif self.F16WORKtype_ui.comboBox_9.currentIndex()==1:
                    at5='at+dioworkmode1=0'
                    at6='at+dioworkmode2=4'
                    at7='at+dioworkmode3=0'
                else:
                    at5='at+dioworkmode1=0'
                    at6='at+dioworkmode2=0'
                    at7='at+dioworkmode3=4'
                self.set_at_write(at4)
                self.set_at_write(at5)
                self.set_at_write(at6)
                self.set_at_write(at7)
            quit_at='at+quit'
            self.set_at_write(quit_at)

    #配置网络模式、调试等级、log输出串口
    def F16_set(self):
        self.log_textEdit.append("<font color='forestgreen'>下载配置网络模式、调试等级、输出接口：\n</font>")
        self.three.setEnabled(False)

        self.F16_setthread=threading.Thread(target=self.F16_set_thread)
        self.F16_setthread.setDaemon(True)
        self.F16_setthread_timer=QTimer()
        self.F16_setthread_timer.timeout.connect(self.F16_set_thread_check)
        self.F16_setthread.start()
        self.F16_setthread_timer.start(100)
    def F16_set_thread_check(self):
        if self.F16_setthread.is_alive():
            pass
        else:
            self.F16_setthread_timer.stop()
            self.three.setEnabled(True)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;网络模式：%s</font>" %
                self.three.NetModel_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;调试等级：%s</font>" %
                self.three.log_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;输出接口：%s</font>" %
                self.three.log_out_comboBox.currentText())
    def F16_set_thread(self):
        if self.three.NetModel_comboBox.currentIndex()==9:
            at='at+netmode=21'
        else:
            at='at+netmode=%d'%self.three.NetModel_comboBox.currentIndex()

        at1='at+debug=%d'%self.three.log_comboBox.currentIndex()
        at2='at+debugport=%d'%(self.three.log_out_comboBox.currentIndex()+1)
        quit_at='at+quit'
        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        self.set_at_write(at)
        self.set_at_write(at1)
        self.set_at_write(at2)
        self.set_at_write(quit_at)



    #查询搜网模式
    def F16_worknet(self):
        self.log_textEdit.append("<font color='forestgreen'>查询模块搜网模式：\n</font>")
        self.three.setEnabled(False)

        self.F16_worknet_thread=threading.Thread(target=self.F16_worknet_ATsend)
        self.F16_worknet_thread.setDaemon(True)
        self.F16_worknet_thread_timer=QTimer()
        self.F16_worknet_thread_timer.timeout.connect(self.F16_worknet_thread_check)
        self.F16_worknet_thread.start()
        self.F16_worknet_thread_timer.start(100)
    def F16_worknet_thread_check(self):
        if self.F16_worknet_thread.is_alive():
            pass
        else:
            self.F16_worknet_thread_timer.stop()
            self.three.setEnabled(True)
            try:
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;%s</font>" %
                    self.FINDNETMODE)
            except:
                pass
    def F16_worknet_ATsend(self):
        old_data = self.receive_textEdit.toPlainText()
        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        self.ser.write(('AT+FINDNETMODE' + '\r\n').encode(encoding='gbk'))
        time.sleep(0.5)
        new_data = self.receive_textEdit.toPlainText()
        self.ser.write(('at+quit' + '\r\n').encode(encoding='gbk'))
        result_data = new_data.replace(old_data, '')
        if result_data == '':
            result_data = old_data
        try:
            self.FINDNETMODE = re.search('FINDNETMODE:(.*?)\n',result_data,re.S).group(1)
        except:
            pass
    #16重启设备
    def F16_reboot(self):
        self.log_textEdit.append("<font color='forestgreen'>重启设备\n</font>")
        at = 'at+reset'
        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        self.set_at_write(at)
        quit_at = 'at+quit'
        self.set_at_write(quit_at)
    #恢复出厂设置
    def F16_reset(self):
        self.log_textEdit.append("<font color='forestgreen'>恢复出厂设置:\n</font>")
        at='at+factory'
        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        self.set_at_write(at)
        self.log_textEdit.append(
            "<font color='darkviolet'>&nbsp;&nbsp;OK</font>")
        quit_at='at+quit'
        self.set_at_write(quit_at)

    #读取配置
    def F16_read(self):
        self.log_textEdit.append("<font color='forestgreen'>读取配置\n</font>")
        self.three.setEnabled(False)

        self.F16_read_thread = threading.Thread(target=self.F16AT_show)
        self.F16_read_thread.setDaemon(True)
        self.F16_read_thread_timer = QTimer()
        self.F16_read_thread_timer.timeout.connect(self.F16_read_thread_check)
        self.F16_read_thread.start()
        self.F16_read_thread_timer.start(100)

    def F16_read_thread_check(self):
        if self.F16_read_thread.is_alive():
            pass
        else:
            self.F16_read_thread_timer.stop()
            self.three.setEnabled(True)
            try:
                net_mode = re.search('net mode:(.*?)\n',self.F16_show_result,re.S).group(1)  # 网路模式
                debug_level = re.search('Debug Level :(.*?)\n',self.F16_show_result,re.S).group(1)  # 调试等级
                debug_port = re.search('Debugging information out port:(.*?)\n',self.F16_show_result,re.S).group(1)  # log输出串口
                work_mode = re.search('Protocol model:(.*?)\n',self.F16_show_result,re.S).group(1)  # 工作协议
                modem_id = re.search('Modem\'s ID number:(.*?)\n',self.F16_show_result,re.S).group(1)  # 设备ID
                phone_num = re.search('Modem\'s Phone Number:(.*?)\n',self.F16_show_result,re.S).group(1)  # 设备手机号码
                data_transferred = re.search('Deliver Recved Tcp Data Directly:(.*?)\n',self.F16_show_result,re.S).group(1)  # 数据是否转义
                activate_method = re.search('Activate Method:(.*?)\n',self.F16_show_result,re.S).group(1)  # 激活方式
                control_phone_N = re.search('Control Phone No.:(.*?)\n',self.F16_show_result,re.S).group(1)  # 电话激活号码
                sms_activation_N = re.search('SMS activation number:(.*?)\n',self.F16_show_result,re.S).group(1)  # 短信激活号码
                sms_daemon_password = re.search('Sms Daemon Password:(.*?)\n',self.F16_show_result,re.S).group(1)  # 短信激活密码
                activate_serial_N = re.search('Activate the serial no:(.*?)\n',self.F16_show_result,re.S).group(1)  # 串口激活接口
                activation_data_format = re.search('The activation data format:(.*?)\n',self.F16_show_result,re.S).group(1)  # 数据激活数据格式
                data_daemon_ppp_on_password = re.search('Data Daemon PPP On Password:(.*?)\n',self.F16_show_result,re.S).group(1)  # 数据激活上线数据
                data_daemon_ppp_off_password = re.search('Data Daemon PPP Off Password:(.*?)\n',self.F16_show_result,re.S).group(1)  # 数据激活下线数据
                io1_workmode = re.search('DIO1 workmode:(.*?)\n',self.F16_show_result,re.S).group(1)  # IO1工作模式
                io2_workmode = re.search('DIO2 workmode:(.*?)\n',self.F16_show_result,re.S).group(1)  # IO2工作模式
                io3_workmode = re.search('DIO3 workmode:(.*?)\n',self.F16_show_result,re.S).group(1)  # IO3工作模式
                sms_phone1_N = re.search('sms Phone1 No.:(.*?)\n',self.F16_show_result,re.S).group(1)  # 短信号码组1
                sms_phone2_N = re.search('sms Phone2 No.:(.*?)\n',self.F16_show_result,re.S).group(1)  # 短信号码组2
                sms_phone3_N = re.search('sms Phone3 No.:(.*?)\n',self.F16_show_result,re.S).group(1)  # 短信号码组3
                sms_phone4_N = re.search('sms Phone4 No.:(.*?)\n',self.F16_show_result,re.S).group(1)  # 短信号码组4
                sms_phone5_N = re.search('sms Phone5 No.:(.*?)\n',self.F16_show_result,re.S).group(1)  # 短信号码组5
                show_phone_N = re.search('Show Phone NO:(.*?)\n',self.F16_show_result,re.S).group(1)  # 是否显示电话号码
                enconde_hex_sms = re.search('Encode Hex SMS:(.*?)\n',self.F16_show_result,re.S).group(1)  # 16进制短信是否转换成文本
                try:
                    http_request_mode = re.search('HTTP Request Mode:(.*?)\n',self.F16_show_result,re.S).group(1)  # http请求方式
                except:
                    pass
                device_model = re.search('Device model:(.*?)\n',self.F16_show_result,re.S).group(1)  # 设备模式（客户端，服务端）
                transfer_protocol = re.search('Transfer protocol:(.*?)\n',self.F16_show_result,re.S).group(1)  # 传输协议
                listen_on_port = re.search('Listen on port:(.*?)\n',self.F16_show_result,re.S).group(1)  # 监听端口
                register_and_heart = re.search('Registration and heart function:(.*?)\n',self.F16_show_result,re.S).group(1)  # 是否开启心跳
                hexlogin = re.search('Register And Keep Online Info Is Hex:(.*?)\n',self.F16_show_result,re.S).group(1)  # 包格式是否16进制
                custom_register_info = re.search('Custom Register Info:(.*?)\n',self.F16_show_result,re.S).group(1)  # 注册包
                custom_register_reply_info = re.search('Custom Register reply Info:(.*?)\n',self.F16_show_result,re.S).group(1)  # 注册包回应
                custom_keeponline_info = re.search('Custom Keep Online Info:(.*?)\n',self.F16_show_result,re.S).group(1)  # 心跳包
                custom_keeponline_reply_info = re.search('Custom Keep Onlinereply Info:(.*?)\n',self.F16_show_result,re.S).group(1)  # 心跳包回应
                dtu_sms_configure = re.search('DTU SMS configure fun:(.*?)\n',self.F16_show_result,re.S).group(1)  # 短信配置
                dtu_sms_configure_password = re.search('DTU SMS configure password:(.*?)\n',self.F16_show_result,re.S).group(1)  # 短信配置密码
                dtu_sms_admin_N = re.search('DTU SMS administrator number:(.*?)\n',self.F16_show_result,re.S).group(1)  # 管理员号码
                com1_baudrate = re.search('Serial Baudrate:(.*?)\n',self.F16_show_result,re.S).group(1)  # 串口1波特率
                com2_baudrate = re.search('Serial 2 Baudrate:(.*?)\n',self.F16_show_result,re.S).group(1)  # 串口2波特率
                RS485_baudrate = re.search('RS485 Baudrate:(.*?)\n',self.F16_show_result,re.S).group(1)  # 485串口波特率
                com1_commu_mode = re.search('Serial port commu mode:(.*?)\n',self.F16_show_result,re.S).group(1)  # 串口1校验
                com2_commu_mode = re.search('Serial 2 port commu mode:(.*?)\n',self.F16_show_result,re.S).group(1)  # 串口2校验
                RS485_commu_mode = re.search('RS485 port commu mode:(.*?)\n',self.F16_show_result,re.S).group(1)  # 485串口校验
                com1_binding_center = re.search('A serial port binding center:(.*?)\n',self.F16_show_result,re.S).group(1)  # 串口1邦定中心
                com2_binding_center = re.search('A serial 2 port binding center:(.*?)\n',self.F16_show_result,re.S).group(1)  # 串口2绑定中心
                RS485_binding_center = re.search('RS485 port binding center:(.*?)\n',self.F16_show_result,re.S).group(1)  # 485串口绑定中心
                total_servers = re.search('Total Servers:(.*?)\n',self.F16_show_result,re.S).group(1)  # 服务器数量
                servers1_IP = re.search('Server\'s Ip:(.*?)\n',self.F16_show_result,re.S).group(1)  # 主中心IP
                servers2_IP = re.search('Server1\'s Ip:(.*?)\n',self.F16_show_result,re.S).group(1)  # 服务器2IP
                servers3_IP = re.search('Server2\'s Ip:(.*?)\n',self.F16_show_result,re.S).group(1)  # 服务器3IP
                servers4_IP = re.search('Server3\'s Ip:(.*?)\n',self.F16_show_result,re.S).group(1)  # 服务器4IP
                servers5_IP = re.search('Server4\'s Ip:(.*?)\n',self.F16_show_result,re.S).group(1)  # 服务器5IP
                servers1_port = re.search('Server\'s Port:(.*?)\n',self.F16_show_result,re.S).group(1)  # 主中心端口
                servers2_port = re.search('Server1\'s Port:(.*?)\n',self.F16_show_result,re.S).group(1)  # 服务器2端口
                servers3_port = re.search('Server2\'s Port:(.*?)\n',self.F16_show_result,re.S).group(1)  # 服务器3端口
                servers4_port = re.search('Server3\'s Port:(.*?)\n',self.F16_show_result,re.S).group(1)  # 服务器4端口
                servers5_port = re.search('Server4\'s Port:(.*?)\n',self.F16_show_result,re.S).group(1)  # 服务器5端口
                secondary_servers_IP = re.search('Secondary Server\'s Ip:(.*?)\n',self.F16_show_result,re.S).group(1)  # 备服务器IP
                secondary_servers_port = re.search('Secondary Server\'s Port:(.*?)\n',self.F16_show_result,re.S).group(1)  # 备服务器端口
                wait_time_dial_failures = re.search('Wait Time Between Dial Failures:(.*?)\n',self.F16_show_result,re.S).group(1)  # 重连间隔
                link_retry_times = re.search('Link Fail Retry Times:(.*?)\n',self.F16_show_result,re.S).group(1)  # 重连次数
                return_main_server = re.search('Should Return To Main Server:(.*?)\n',self.F16_show_result,re.S).group(1)  # 是否返回主中心


                net_mode=int(net_mode.strip())
                if net_mode==21:
                    self.three.NetModel_comboBox.setCurrentIndex(9)
                else:
                    self.three.NetModel_comboBox.setCurrentIndex(net_mode)
                debug_level=int(debug_level.strip())
                self.three.log_comboBox.setCurrentIndex(debug_level)
                debug_port=int(debug_port.strip())
                self.three.log_out_comboBox.setCurrentIndex(debug_port-1)
                work_mode=work_mode.strip()
                self.F16WORKtype_ui.protocolType_comboBox.setCurrentIndex(self.protocolTYPE.get(work_mode))
                modem_id=modem_id.strip()
                self.F16WORKtype_ui.lineEdit.setText(modem_id)
                phone_num=phone_num.strip()
                self.F16WORKtype_ui.lineEdit_2.setText(phone_num)
                data_transferred=int(data_transferred.strip())
                self.F16WORKtype_ui.comboBox.setCurrentIndex(data_transferred)
                activate_method=activate_method.strip()
                self.F16WORKtype_ui.activeType_comboBox.setCurrentIndex(self.activeTYPE.get(activate_method))
                control_phone_N=control_phone_N.strip()
                self.F16WORKtype_ui.lineEdit_5.setText(control_phone_N)
                sms_activation_N=sms_activation_N.strip()
                self.F16WORKtype_ui.lineEdit_3.setText(sms_activation_N)
                sms_daemon_password=sms_daemon_password.strip()
                self.F16WORKtype_ui.lineEdit_4.setText(sms_daemon_password)
                activate_serial_N=int(activate_serial_N.strip())
                self.F16WORKtype_ui.comboBox_2.setCurrentIndex(activate_serial_N-1)
                activation_data_format=int(activation_data_format.strip())
                self.F16WORKtype_ui.comboBox_5.setCurrentIndex(activation_data_format)
                data_daemon_ppp_on_password=data_daemon_ppp_on_password.strip()
                self.F16WORKtype_ui.lineEdit_6.setText(data_daemon_ppp_on_password)
                data_daemon_ppp_off_password=data_daemon_ppp_off_password.strip()
                self.F16WORKtype_ui.lineEdit_7.setText(data_daemon_ppp_off_password)
                io1_workmode=int(io1_workmode.strip())
                if io1_workmode==0:
                    self.F16WORKtype_ui.comboBox_6.setCurrentIndex(0)
                elif io1_workmode==4:
                    self.F16WORKtype_ui.comboBox_6.setCurrentIndex(1)
                elif io1_workmode==5:
                    self.F16WORKtype_ui.comboBox_6.setCurrentIndex(2)
                io2_workmode=int(io2_workmode.strip())
                if io2_workmode==0:
                    self.F16WORKtype_ui.comboBox_7.setCurrentIndex(0)
                elif io2_workmode==4:
                    self.F16WORKtype_ui.comboBox_7.setCurrentIndex(1)
                elif io2_workmode==5:
                    self.F16WORKtype_ui.comboBox_7.setCurrentIndex(2)

                self.F16WORKtype_ui.lineEdit_9.setText(control_phone_N)
                self.F16WORKtype_ui.lineEdit_10.setText(sms_activation_N)
                self.F16WORKtype_ui.lineEdit_11.setText(data_daemon_ppp_on_password)
                self.F16WORKtype_ui.lineEdit_12.setText(data_daemon_ppp_off_password)
                self.F16WORKtype_ui.comboBox_3.setCurrentIndex(activate_serial_N-1)
                self.F16WORKtype_ui.comboBox_4.setCurrentIndex(activation_data_format)
                self.F16WORKtype_ui.lineEdit_8.setText(sms_daemon_password)
                io3_workmode=int(io3_workmode.strip())
                if io1_workmode==4 and io2_workmode==0 and io3_workmode==0:
                    self.F16WORKtype_ui.comboBox_9.setCurrentIndex(0)
                elif io1_workmode==0 and io2_workmode==4 and io3_workmode==0:
                    self.F16WORKtype_ui.comboBox_9.setCurrentIndex(1)
                elif io1_workmode==0 and io2_workmode==0 and io3_workmode==4:
                    self.F16WORKtype_ui.comboBox_9.setCurrentIndex(2)

                self.F16WORKtype_ui.lineEdit_23.setText(phone_num)

                sms_phone1_N=sms_phone1_N.strip()
                self.F16WORKtype_ui.lineEdit_24.setText(sms_phone1_N)
                sms_phone2_N=sms_phone2_N.strip()
                self.F16WORKtype_ui.lineEdit_25.setText(sms_phone2_N)
                sms_phone3_N=sms_phone3_N.strip()
                self.F16WORKtype_ui.lineEdit_26.setText(sms_phone3_N)
                sms_phone4_N=sms_phone4_N.strip()
                self.F16WORKtype_ui.lineEdit_27.setText(sms_phone4_N)
                sms_phone5_N=sms_phone5_N.strip()
                self.F16WORKtype_ui.lineEdit_28.setText(sms_phone5_N)
                show_phone_N=int(show_phone_N.strip())
                self.F16WORKtype_ui.comboBox_18.setCurrentIndex(show_phone_N)
                enconde_hex_sms=int(enconde_hex_sms.strip())
                self.F16WORKtype_ui.comboBox_19.setCurrentIndex(enconde_hex_sms)
                self.F16WORKtype_ui.comboBox_20.setCurrentIndex(show_phone_N)
                self.F16WORKtype_ui.comboBox_21.setCurrentIndex(enconde_hex_sms)
                try:
                    http_request_mode=int(http_request_mode.strip())
                    self.F16WORKtype_ui.comboBox_30.setCurrentIndex(http_request_mode)
                except:
                    pass
                device_model=device_model.strip()
                if device_model=='SVR':
                    self.F16WORKtype_ui.comboBox_31.setCurrentIndex(0)
                elif device_model=='CLI':
                    self.F16WORKtype_ui.comboBox_31.setCurrentIndex(1)
                transfer_protocol=transfer_protocol.strip()
                self.F16WORKtype_ui.comboBox_32.setCurrentText(transfer_protocol)
                listen_on_port=listen_on_port.strip()
                self.F16WORKtype_ui.lineEdit_39.setText(listen_on_port)
                register_and_heart=int(register_and_heart.strip())
                self.F16WORKtype_ui.comboBox_33.setCurrentIndex(register_and_heart)
                hexlogin=int(hexlogin.strip())
                self.F16WORKtype_ui.comboBox_10.setCurrentIndex(hexlogin)
                custom_register_info=custom_register_info.strip()
                self.F16WORKtype_ui.lineEdit_13.setText(custom_register_info)
                custom_register_reply_info=custom_register_reply_info.strip()
                self.F16WORKtype_ui.lineEdit_15.setText(custom_register_reply_info)
                custom_keeponline_info=custom_keeponline_info.strip()
                self.F16WORKtype_ui.lineEdit_14.setText(custom_keeponline_info)
                custom_keeponline_reply_info=custom_keeponline_reply_info.strip()
                self.F16WORKtype_ui.lineEdit_16.setText(custom_keeponline_reply_info)
                dtu_sms_configure=int(dtu_sms_configure.strip())
                self.F16SMSset_ui.SMSset_comboBox.setCurrentIndex(dtu_sms_configure)
                dtu_sms_configure_password=dtu_sms_configure_password.strip()
                self.F16SMSset_ui.SMSset_lineEdit.setText(dtu_sms_configure_password)
                dtu_sms_admin_N=dtu_sms_admin_N.strip()
                self.F16SMSset_ui.admin_lineEdit.setText(dtu_sms_admin_N)
                com1_baudrate=com1_baudrate.strip()
                self.F16COMset_ui.com1_baudrate_comboBox.setCurrentText(com1_baudrate)
                com1_commu_mode=com1_commu_mode.strip()
                self.F16COMset_ui.com1_parity_comboBox.setCurrentText(com1_commu_mode)
                com1_binding_center= com1_binding_center.strip()
                self.F16COMset_ui.com1_bind_comboBox.setCurrentIndex(self.bindingCENTER.get(com1_binding_center))
                com2_baudrate=com2_baudrate.strip()
                self.F16COMset_ui.com2_baudrate_comboBox.setCurrentText(com2_baudrate)
                com2_commu_mode=com2_commu_mode.strip()
                self.F16COMset_ui.com2_parity_comboBox.setCurrentText(com2_commu_mode)
                com2_binding_center=com2_binding_center.strip()
                self.F16COMset_ui.com2_bind_comboBox.setCurrentIndex(self.bindingCENTER.get(com2_binding_center))
                RS485_baudrate=RS485_baudrate.strip()
                self.F16COMset_ui.rs485_baudrate_comboBox.setCurrentText(RS485_baudrate)
                RS485_commu_mode=RS485_commu_mode.strip()
                self.F16COMset_ui.rs485_parity_comboBox.setCurrentText(RS485_commu_mode)
                RS485_binding_center=RS485_binding_center.strip()
                self.F16COMset_ui.rs485_bind_comboBox.setCurrentIndex(self.bindingCENTER.get(RS485_binding_center))
                total_servers=int(total_servers.strip())
                self.F16IPandPORTset_ui.serverNum_comboBox.setCurrentIndex(total_servers-1)
                servers1_IP=servers1_IP.strip()
                self.F16IPandPORTset_ui.server_lineEdit.setText(servers1_IP)
                servers2_IP=servers2_IP.strip()
                self.F16IPandPORTset_ui.server2_lineEdit.setText(servers2_IP)
                servers3_IP=servers3_IP.strip()
                self.F16IPandPORTset_ui.server3_lineEdit.setText(servers3_IP)
                servers4_IP=servers4_IP.strip()
                self.F16IPandPORTset_ui.server4_lineEdit.setText(servers4_IP)
                servers5_IP=servers5_IP.strip()
                self.F16IPandPORTset_ui.server5_lineEdit.setText(servers5_IP)
                servers1_port=servers1_port.strip()
                self.F16IPandPORTset_ui.port_lineEdit.setText(servers1_port)
                servers2_port=servers2_port.strip()
                self.F16IPandPORTset_ui.port2_lineEdit.setText(servers2_port)
                servers3_port=servers3_port.strip()
                self.F16IPandPORTset_ui.port3_lineEdit.setText(servers3_port)
                servers4_port=servers4_port.strip()
                self.F16IPandPORTset_ui.port4_lineEdit.setText(servers4_port)
                servers5_port=servers5_port.strip()
                self.F16IPandPORTset_ui.port5_lineEdit.setText(servers5_port)
                secondary_servers_IP=secondary_servers_IP.strip()
                self.F16IPandPORTset_ui.server1_lineEdit.setText(secondary_servers_IP)
                secondary_servers_port=secondary_servers_port.strip()
                self.F16IPandPORTset_ui.port1_lineEdit.setText(secondary_servers_port)
                wait_time_dial_failures=wait_time_dial_failures.strip()
                self.F16IPandPORTset_ui.reconnect_lineEdit.setText(wait_time_dial_failures)
                link_retry_times=link_retry_times.strip()
                self.F16IPandPORTset_ui.reconnectTimes_lineEdit.setText(link_retry_times)
                return_main_server=int(return_main_server.strip())
                self.F16IPandPORTset_ui.reserver_comboBox.setCurrentIndex(return_main_server)


            except:
                pass


            # print(net_mode)
            # print(debug_level)
            # print(debug_port)
            # print(work_mode)
            # print(modem_id)
            # print(phone_num)
            # print(data_transferred)
            # print(activate_method)
            # print(control_phone_N)
            # print(sms_activation_N)
            # print(sms_daemon_password)
            # print(activate_serial_N)
            # print(activation_data_format)
            # print(data_daemon_ppp_on_password)
            # print(data_daemon_ppp_off_password)
            # print(io1_workmode)
            # print(io2_workmode)
            # print(io3_workmode)
            # print(sms_phone1_N)
            # print(sms_phone2_N)
            # print(sms_phone3_N)
            # print(sms_phone4_N)
            # print(sms_phone5_N)
            # print(show_phone_N)
            # print(enconde_hex_sms)
            # print(http_request_mode)
            # print(device_model)
            # print(listen_on_port)
            # print(hexlogin)
            # print(custom_register_info)
            # print(custom_register_reply_info)
            # print(custom_keeponline_info)
            # print(custom_keeponline_reply_info)
            # print(dtu_sms_admin_N)
            # print(dtu_sms_configure)
            # print(dtu_sms_configure_password)
            # print(com1_baudrate)
            # print(com2_baudrate)
            # print(RS485_baudrate)
            # print(com1_commu_mode)
            # print(com2_commu_mode)
            # print(RS485_commu_mode)
            # print(com1_binding_center)
            # print(com2_binding_center)
            # print(RS485_binding_center)
            # print(total_servers)
            # print(servers1_IP)
            # print(servers2_IP)
            # print(servers3_IP)
            # print(servers4_IP)
            # print(servers5_IP)
            # print(servers1_port)
            # print(servers2_port)
            # print(servers3_port)
            # print(servers4_port)
            # print(servers5_port)
            # print(secondary_servers_IP)
            # print(secondary_servers_port)
            # print(wait_time_dial_failures)
            # print(link_retry_times)
            # print(return_main_server)

            # self.log_textEdit.append(
            #     "<font color='darkviolet'>&nbsp;&nbsp;===：%s</font>" % self.F16_show_result)

    def F16AT_show(self):
        old_data = self.receive_textEdit.toPlainText()
        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        self.ser.write(('at+show' + '\r\n').encode(encoding='gbk'))
        time.sleep(1.8)
        new_data = self.receive_textEdit.toPlainText()
        self.ser.write(('at+quit' + '\r\n').encode(encoding='gbk'))
        result_data = new_data.replace(old_data, '')
        if result_data == '':
            result_data = old_data
        self.F16_show_result = result_data

    # 16版本检测
    def F16ver_check(self):
        self.log_textEdit.append("<font color='forestgreen'>版本检测：\n</font>")
        self.three.setEnabled(False)

        self.F16ver_check_thread = threading.Thread(target=self.F16ver_ATsend)
        self.F16ver_check_thread.setDaemon(True)
        self.F16ver_check_thread_timer = QTimer()
        self.F16ver_check_thread_timer.timeout.connect(
            self.F16ver_check_thread_check)
        self.F16ver_check_thread.start()
        self.F16ver_check_thread_timer.start(100)

    def F16ver_check_thread_check(self):
        if self.F16ver_check_thread.is_alive():
            pass
        else:
            self.F16ver_check_thread_timer.stop()
            self.three.setEnabled(True)
            try:
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;BOOTLOADER VERSION：%s</font>" %
                    self.BOOTLOADER_ver)
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;OS VERSION：%s</font>" %
                    self.OS_ver)
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;APPLICATION VERSION：%s</font>" %
                    self.APPLICATION_ver)
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;CUSTOMIZATION：%s</font>" %
                    self.CUSTOMIZATION)
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;Release Time：%s</font>" %
                    self.Release_Time)
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;Lib version：%s</font>" %
                    self.Lib_ver)
            except BaseException:
                pass

    def F16ver_ATsend(self):
        old_data = self.receive_textEdit.toPlainText()
        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        self.ser.write(('at+ver?' + '\r\n').encode(encoding='gbk'))
        time.sleep(0.5)
        new_data = self.receive_textEdit.toPlainText()
        self.ser.write(('at+quit' + '\r\n').encode(encoding='gbk'))
        result_data = new_data.replace(old_data, '')
        if result_data == '':
            result_data = old_data
        try:
            self.BOOTLOADER_ver = re.search(
                'BOOTLOADER VERSION:(.*?)\n', result_data, re.S).group(1)
            self.OS_ver = re.search(
                'OS VERSION:(.*?)\n',
                result_data,
                re.S).group(1)
            self.APPLICATION_ver = re.search(
                'APPLICATION VERSION:(.*?)\n', result_data, re.S).group(1)
            self.CUSTOMIZATION = re.search(
                'CUSTOMIZATION:(.*?)\n', result_data, re.S).group(1)
            self.Release_Time = re.search(
                'Release Time:(.*?)\n', result_data, re.S).group(1)
            self.Lib_ver = re.search(
                'Lib version:(.*?)\n',
                result_data,
                re.S).group(1)
        except:
            pass

    # 16 状态查询

    def status_read(self):
        self.log_textEdit.append("<font color='forestgreen'>设备状态：\n</font>")
        self.three.setEnabled(False)

        # self.log_textEdit.append(
        #     "<font color='darkviolet'>&nbsp;&nbsp;当前用的SIM卡：%s</font>" % SIM)

        self.status_read_thread = threading.Thread(target=self.statusAT_send)
        self.status_read_thread.setDaemon(True)
        self.status_read_thread_timer = QTimer()
        self.status_read_thread_timer.timeout.connect(
            self.status_read_thread_check)
        self.status_read_thread.start()
        self.status_read_thread_timer.start(100)

    def status_read_thread_check(self):
        if self.status_read_thread.is_alive():
            pass
        else:
            self.status_read_thread_timer.stop()
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;当前用的SIM卡：%s</font>" %
                self.SIM_type)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;当前SIM卡状态：%s</font>" %
                self.SIM_state)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;模块状态：%s</font>" %
                self.MODULER_state)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;模块型号内容：%s</font>" %
                self.MODULER_info)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;信号值：%s</font>" %
                self.CSQ)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;注册网络制式：%s</font>" %
                self.NETWORK_mode)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;当前用的SIM获取到的IP：%s</font>" %
                self.IP_addr)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;主服务器状态：%s</font>" %
                self.DATAcenter1)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;服务器2状态：%s</font>" %
                self.DATAcenter2)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;服务器3状态：%s</font>" %
                self.DATAcenter3)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;服务器4状态：%s</font>" %
                self.DATAcenter4)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;服务器5状态：%s</font>" %
                self.DATAcenter5)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;管理平台连接情况：%s</font>" %
                self.Management)
            self.log_textEdit.moveCursor(QTextCursor.End)
            self.three.setEnabled(True)

    def statusAT_send(self):
        old_data = self.receive_textEdit.toPlainText()
        self.ser.write(('AT+CURSTATUESHOW' + '\r\n').encode(encoding='gbk'))
        time.sleep(0.5)
        new_data = self.receive_textEdit.toPlainText()
        result_data = new_data.replace(old_data, '')
        if result_data == '':
            result_data = old_data
        SIM = re.search('ISP:(.*?)\n', result_data, re.S)
        if SIM is not None:
            self.SIM_type = SIM.group(1)
        else:
            self.SIM_type = None

        self.SIM_state = re.search(
            'SIM card status:(.*?)\n', result_data, re.S)
        if self.SIM_state is not None:
            self.SIM_state = self.SIM_state.group(1)
        else:
            self.SIM_state = None

        self.MODULER_state = re.search(
            'Moduler status:(.*?)\n', result_data, re.S)
        if self.MODULER_state is not None:
            self.MODULER_state = self.MODULER_state.group(1)
        else:
            self.MODULER_state = None

        self.MODULER_info = re.search(
            'Moduler info:(.*?)\n', result_data, re.S)
        if self.MODULER_info is not None:
            self.MODULER_info = self.MODULER_info.group(1)
        else:
            self.MODULER_info = None

        self.CSQ = re.search('CSQ:(.*?)\n', result_data, re.S)
        if self.CSQ is not None:
            self.CSQ = self.CSQ.group(1)
        else:
            self.CSQ = None

        self.NETWORK_mode = re.search(
            'Network mode:(.*?)\n', result_data, re.S)
        if self.NETWORK_mode is not None:
            self.NETWORK_mode = self.NETWORK_mode.group(1)
        else:
            self.NETWORK_mode = None

        self.IP_addr = re.search('IP addr:(.*?)\n', result_data, re.S)
        if self.IP_addr is not None:
            self.IP_addr = self.IP_addr.group(1)
        else:
            self.IP_addr = None

        self.DATAcenter1 = re.search(
            'Data center 1:(.*?)\n', result_data, re.S)
        if self.DATAcenter1 is not None:
            self.DATAcenter1 = self.DATAcenter1.group(1)
        else:
            self.DATAcenter1 = None

        self.DATAcenter2 = re.search(
            'Data center 2:(.*?)\n', result_data, re.S)
        if self.DATAcenter2 is not None:
            self.DATAcenter2 = self.DATAcenter2.group(1)
        else:
            self.DATAcenter2 = None

        self.DATAcenter3 = re.search(
            'Data center 3:(.*?)\n', result_data, re.S)
        if self.DATAcenter3 is not None:
            self.DATAcenter3 = self.DATAcenter3.group(1)
        else:
            self.DATAcenter3 = None

        self.DATAcenter4 = re.search(
            'Data center 4:(.*?)\n', result_data, re.S)
        if self.DATAcenter4 is not None:
            self.DATAcenter4 = self.DATAcenter4.group(1)
        else:
            self.DATAcenter4 = None

        self.DATAcenter5 = re.search(
            'Data center 5:(.*?)\n', result_data, re.S)
        if self.DATAcenter5 is not None:
            self.DATAcenter5 = self.DATAcenter5.group(1)
        else:
            self.DATAcenter5 = None

        self.Management = re.search(
            'Management platfrom :(.*?)\n', result_data, re.S)
        if self.Management is not None:
            self.Management = self.Management.group(1)
        else:
            self.Management = None

    #14（16）-重启设备
    def reboot(self):
        self.log_textEdit.append(
            "<font color='forestgreen'>重启设备\n</font>")
        at='at+reset'
        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        self.set_at_write(at)

    # 14(16)-D自定义帧配置
    def Frame_set(self):
        self.log_textEdit.append(
            "<font color='forestgreen'>下载自定义帧配置：\n</font>")
        self.Frame_dialog.setEnabled(False)

        self.Frame_setthread=threading.Thread(target=self.Frame_set_thread)
        self.Frame_setthread.setDaemon(True)
        self.Frame_setthread_timer=QTimer()
        self.Frame_setthread_timer.timeout.connect(self.Frame_set_thread_check)
        self.Frame_setthread.start()
        self.Frame_setthread_timer.start(100)
    def Frame_set_thread_check(self):
        if self.Frame_setthread.is_alive():
            pass
        else:
            self.Frame_setthread_timer.stop()
            self.Frame_dialog.setEnabled(True)

            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;登录帧类型：%s</font>" %
                self.Frame_ui.LoginFrameType_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;登录帧：%s</font>" %
                self.Frame_ui.LoginFrame_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;登录应答帧类型：%s</font>" %
                self.Frame_ui.LoginAcFrameType_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;登录应答帧：%s</font>" %
                self.Frame_ui.LoginAcFrame_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;心跳帧类型：%s</font>" %
                self.Frame_ui.HeartFrameType_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;心跳帧：%s</font>" %
                self.Frame_ui.HeartFrame_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;心跳应答帧类型：%s</font>" %
                self.Frame_ui.HeartAcFrameType_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;心跳应答帧：%s</font>" %
                self.Frame_ui.HeartAcFrame_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;退出帧类型：%s</font>" %
                self.Frame_ui.OutFrameTypecomboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;退出帧：%s</font>" %
                self.Frame_ui.OutFrame_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;退出应答帧类型：%s</font>" %
                self.Frame_ui.OutAcFrameType_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;退出应答帧：%s</font>" %
                self.Frame_ui.OutFrame_lineEdit_2.text())
            self.log_textEdit.moveCursor(QTextCursor.End)

            button = QMessageBox.question(
                self,
                "Question",
                '配置完成是否重启设备？',
                QMessageBox.Ok | QMessageBox.Cancel,
                QMessageBox.Ok)
            if button == QMessageBox.Ok:
                reset = 'at+reset'
                self.ser.write('+++'.encode(encoding='gbk'))
                time.sleep(0.2)
                self.set_at_write(reset)
                self.log_textEdit.append("<font color='forestgreen'>设备重启</font>")
            else:
                pass
            self.Frame_dialog.close()


    def Frame_set_thread(self):
        at = 'LOGINTYPE=%s' % self.Frame_ui.LoginFrameType_comboBox.currentText()
        at1 = 'LOGINPKT=%s' % self.Frame_ui.LoginFrame_lineEdit.text()
        at2 = 'LOGINACKTYPE=%s' % self.Frame_ui.LoginAcFrameType_comboBox.currentText()
        at3 = 'LOGINACKPKT=%s' % self.Frame_ui.LoginAcFrame_lineEdit.text()
        at4 = 'HEARTTYPE=%s' % self.Frame_ui.HeartFrameType_comboBox.currentText()
        at5 = 'HEARTPKT=%s' % self.Frame_ui.HeartFrame_lineEdit.text()
        at6 = 'HEARTACKTYPE=%s' % self.Frame_ui.HeartAcFrameType_comboBox.currentText()
        at7 = 'HEARTACKPKT=%s' % self.Frame_ui.HeartAcFrame_lineEdit.text()
        at8 = 'QUITTTYPE=%s' % self.Frame_ui.OutFrameTypecomboBox.currentText()
        at9 = 'QUITPKT=%s' % self.Frame_ui.OutFrame_lineEdit.text()
        at10 = 'QUITACKTYPE=%s' % self.Frame_ui.OutAcFrameType_comboBox.currentText()
        at11 = 'QUITACKPKT=%s' % self.Frame_ui.OutFrame_lineEdit_2.text()
        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        self.set_at_write(at)
        self.set_at_write(at1)
        self.set_at_write(at2)
        self.set_at_write(at3)
        self.set_at_write(at4)
        self.set_at_write(at5)
        self.set_at_write(at6)
        self.set_at_write(at7)
        self.set_at_write(at8)
        self.set_at_write(at9)
        self.set_at_write(at10)
        self.set_at_write(at11)



    #14(16)-D读取自定义帧配置
    def Frame_read(self):
        self.Frame_dialog.setEnabled(False)
        self.log_textEdit.append(
            "<font color='forestgreen'>读取自定义帧配置：\n</font>")

        at = 'LOGINTYPE?'
        self.LOGINTYPEthread = threading.Thread(
            target=self.at_test, args=(at,))
        self.LOGINTYPEthread.setDaemon(True)
        self.LOGINTYPEthread_timer = QTimer()
        self.LOGINTYPEthread_timer.timeout.connect(
            lambda: self.LOGINTYPEthread_check(
                self.LOGINTYPEthread, self.LOGINTYPEthread_timer))
        self.LOGINTYPEthread.start()
        self.LOGINTYPEthread_timer.start(100)

        at1 = 'LOGINPKT?'
        self.LOGINPKTthread = threading.Thread(
            target=self.at_test, args=(at1,))
        self.LOGINPKTthread.setDaemon(True)
        self.LOGINPKTthread_timer = QTimer()
        self.LOGINPKTthread_timer.timeout.connect(
            lambda: self.LOGINPKTthread_check(
                self.LOGINPKTthread, self.LOGINPKTthread_timer))

        at2 = 'LOGINACKTYPE?'
        self.LOGINACKTYPEthread = threading.Thread(
            target=self.at_test, args=(at2,))
        self.LOGINACKTYPEthread.setDaemon(True)
        self.LOGINACKTYPEthread_timer = QTimer()
        self.LOGINACKTYPEthread_timer.timeout.connect(
            lambda: self.LOGINACKTYPEthread_check(
                self.LOGINACKTYPEthread,
                self.LOGINACKTYPEthread_timer))

        at3 = 'LOGINACKPKT?'
        self.LOGINACKPKTthread = threading.Thread(
            target=self.at_test, args=(at3,))
        self.LOGINACKPKTthread.setDaemon(True)
        self.LOGINACKPKTthread_timer = QTimer()
        self.LOGINACKPKTthread_timer.timeout.connect(
            lambda: self.LOGINACKPKTthread_check(
                self.LOGINACKPKTthread,
                self.LOGINACKPKTthread_timer))

        at4 = 'HEARTTYPE?'
        self.HEARTTYPEthread = threading.Thread(
            target=self.at_test, args=(at4,))
        self.HEARTTYPEthread.setDaemon(True)
        self.HEARTTYPEthread_timer = QTimer()
        self.HEARTTYPEthread_timer.timeout.connect(
            lambda: self.HEARTTYPEthread_check(
                self.HEARTTYPEthread, self.HEARTTYPEthread_timer))

        at5 = 'HEARTPKT?'
        self.HEARTPKTthread = threading.Thread(
            target=self.at_test, args=(at5,))
        self.HEARTPKTthread.setDaemon(True)
        self.HEARTPKTthread_timer = QTimer()
        self.HEARTPKTthread_timer.timeout.connect(
            lambda: self.HEARTPKTthread_check(
                self.HEARTPKTthread, self.HEARTPKTthread_timer))

        at6 = 'HEARTACKTYPE?'
        self.HEARTACKTYPEthread = threading.Thread(
            target=self.at_test, args=(at6,))
        self.HEARTACKTYPEthread.setDaemon(True)
        self.HEARTACKTYPEthread_timer = QTimer()
        self.HEARTACKTYPEthread_timer.timeout.connect(
            lambda: self.HEARTACKTYPEthread_check(
                self.HEARTACKTYPEthread,
                self.HEARTACKTYPEthread_timer))

        at7 = 'HEARTACKPKT?'
        self.HEARTACKPKTthread = threading.Thread(
            target=self.at_test, args=(at7,))
        self.HEARTACKPKTthread.setDaemon(True)
        self.HEARTACKPKTthread_timer = QTimer()
        self.HEARTACKPKTthread_timer.timeout.connect(
            lambda: self.HEARTACKPKTthread_check(
                self.HEARTACKPKTthread,
                self.HEARTACKPKTthread_timer))

        at8 = 'QUITTTYPE?'
        self.QUITTTYPEthread = threading.Thread(
            target=self.at_test, args=(at8,))
        self.QUITTTYPEthread.setDaemon(True)
        self.QUITTTYPEthread_timer = QTimer()
        self.QUITTTYPEthread_timer.timeout.connect(
            lambda: self.QUITTTYPEthread_check(
                self.QUITTTYPEthread, self.QUITTTYPEthread_timer))

        at9 = 'QUITPKT?'
        self.QUITPKTthread = threading.Thread(target=self.at_test, args=(at9,))
        self.QUITPKTthread.setDaemon(True)
        self.QUITPKTthread_timer = QTimer()
        self.QUITPKTthread_timer.timeout.connect(
            lambda: self.QUITPKTthread_check(
                self.QUITPKTthread, self.QUITPKTthread_timer))

        at10 = 'QUITACKTYPE?'
        self.QUITACKTYPEthread = threading.Thread(
            target=self.at_test, args=(at10,))
        self.QUITACKTYPEthread.setDaemon(True)
        self.QUITACKTYPEthread_timer = QTimer()
        self.QUITACKTYPEthread_timer.timeout.connect(
            lambda: self.QUITACKTYPEthread_check(
                self.QUITACKTYPEthread,
                self.QUITACKTYPEthread_timer))

        at11 = 'QUITACKPKT?'
        self.QUITACKPKTthread = threading.Thread(
            target=self.at_test, args=(at11,))
        self.QUITACKPKTthread.setDaemon(True)
        self.QUITACKPKTthread_timer = QTimer()
        self.QUITACKPKTthread_timer.timeout.connect(
            lambda: self.QUITACKPKTthread_check(
                self.QUITACKPKTthread, self.QUITACKPKTthread_timer))

    def QUITACKPKTthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            QUITACKPKT = self.ATresult.replace('OK', '')
            QUITACKPKT = QUITACKPKT.strip()
            self.Frame_ui.OutFrame_lineEdit_2.setText(QUITACKPKT)
            timername.stop()
            self.Frame_dialog.setEnabled(True)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;登录帧类型：%s</font>" %
                self.Frame_ui.LoginFrameType_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;登录帧：%s</font>" %
                self.Frame_ui.LoginFrame_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;登录应答帧类型：%s</font>" %
                self.Frame_ui.LoginAcFrameType_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;登录应答帧：%s</font>" %
                self.Frame_ui.LoginAcFrame_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;心跳帧类型：%s</font>" %
                self.Frame_ui.HeartFrameType_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;心跳帧：%s</font>" %
                self.Frame_ui.HeartFrame_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;心跳应答帧类型：%s</font>" %
                self.Frame_ui.HeartAcFrameType_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;心跳应答帧：%s</font>" %
                self.Frame_ui.HeartAcFrame_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;退出帧类型：%s</font>" %
                self.Frame_ui.OutFrameTypecomboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;退出帧：%s</font>" %
                self.Frame_ui.OutFrame_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;退出应答帧类型：%s</font>" %
                self.Frame_ui.OutAcFrameType_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;退出应答帧：%s</font>" %
                self.Frame_ui.OutFrame_lineEdit_2.text())
            self.log_textEdit.moveCursor(QTextCursor.End)

    def QUITACKTYPEthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            QUITACKTYPE = self.ATresult.replace('OK', '')
            QUITACKTYPE = QUITACKTYPE.strip()
            self.Frame_ui.OutAcFrameType_comboBox.setCurrentText(QUITACKTYPE)
            timername.stop()
            self.QUITACKPKTthread.start()
            self.QUITACKPKTthread_timer.start(100)

    def QUITPKTthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            QUITPKT = self.ATresult.replace('OK', '')
            QUITPKT = QUITPKT.strip()
            self.Frame_ui.OutFrame_lineEdit.setText(QUITPKT)
            timername.stop()
            self.QUITACKTYPEthread.start()
            self.QUITACKTYPEthread_timer.start(100)

    def QUITTTYPEthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            QUITTTYPE = self.ATresult.replace('OK', '')
            QUITTTYPE = QUITTTYPE.strip()
            self.Frame_ui.OutFrameTypecomboBox.setCurrentText(QUITTTYPE)
            timername.stop()
            self.QUITPKTthread.start()
            self.QUITPKTthread_timer.start(100)

    def HEARTACKPKTthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            HEARTACKPKT = self.ATresult.replace('OK', '')
            HEARTACKPKT = HEARTACKPKT.strip()
            self.Frame_ui.HeartAcFrame_lineEdit.setText(HEARTACKPKT)
            timername.stop()
            self.QUITTTYPEthread.start()
            self.QUITTTYPEthread_timer.start(100)

    def HEARTACKTYPEthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            HEARTACKTYPE = self.ATresult.replace('OK', '')
            HEARTACKTYPE = HEARTACKTYPE.strip()
            self.Frame_ui.HeartAcFrameType_comboBox.setCurrentText(
                HEARTACKTYPE)
            timername.stop()
            self.HEARTACKPKTthread.start()
            self.HEARTACKPKTthread_timer.start(100)

    def HEARTPKTthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            HEARTPKT = self.ATresult.replace('OK', '')
            HEARTPKT = HEARTPKT.strip()
            self.Frame_ui.HeartFrame_lineEdit.setText(HEARTPKT)
            timername.stop()
            self.HEARTACKTYPEthread.start()
            self.HEARTACKTYPEthread_timer.start(100)

    def HEARTTYPEthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            HEARTTYPE = self.ATresult.replace('OK', '')
            HEARTTYPE = HEARTTYPE.strip()
            self.Frame_ui.HeartFrameType_comboBox.setCurrentText(HEARTTYPE)
            timername.stop()
            self.HEARTPKTthread.start()
            self.HEARTPKTthread_timer.start(100)

    def LOGINACKPKTthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            LOGINACKPKT = self.ATresult.replace('OK', '')
            LOGINACKPKT = LOGINACKPKT.strip()
            self.Frame_ui.LoginAcFrame_lineEdit.setText(LOGINACKPKT)
            timername.stop()
            self.HEARTTYPEthread.start()
            self.HEARTTYPEthread_timer.start(100)

    def LOGINACKTYPEthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            LOGINACKTYPE = self.ATresult.replace('OK', '')
            LOGINACKTYPE = LOGINACKTYPE.strip()
            self.Frame_ui.LoginAcFrameType_comboBox.setCurrentText(
                LOGINACKTYPE)
            timername.stop()
            self.LOGINACKPKTthread.start()
            self.LOGINACKPKTthread_timer.start(100)

    def LOGINPKTthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            LOGINPKT = self.ATresult.replace('OK', '')
            LOGINPKT = LOGINPKT.strip()
            self.Frame_ui.LoginFrame_lineEdit.setText(LOGINPKT)
            timername.stop()
            self.LOGINACKTYPEthread.start()
            self.LOGINACKTYPEthread_timer.start(100)

    def LOGINTYPEthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            LOGINTYPE = self.ATresult.replace('OK', '')
            LOGINTYPE = LOGINTYPE.strip()
            self.Frame_ui.LoginFrameType_comboBox.setCurrentText(LOGINTYPE)
            timername.stop()
            self.LOGINPKTthread.start()
            self.LOGINPKTthread_timer.start(100)

    def Frame_cancel(self):
        self.Frame_dialog.close()
    # 14(16)-D企业中心IP和端口配置

    def IPandPORT_set(self):
        self.log_textEdit.append(
            "<font color='forestgreen'>下载企业中心配置：\n</font>")
        self.IPandPORT_dialog.setEnabled(False)

        self.IPandPORT_setthread=threading.Thread(target=self.IPandPORT_set_thread)
        self.IPandPORT_setthread.setDaemon(True)
        self.IPandPORT_setthread_timer=QTimer()
        self.IPandPORT_setthread_timer.timeout.connect(self.IPandPORT_set_thread_check)
        self.IPandPORT_setthread.start()
        self.IPandPORT_setthread_timer.start(100)

    def IPandPORT_set_thread_check(self):
        if self.IPandPORT_setthread.is_alive():
            pass
        else:
            self.IPandPORT_setthread_timer.stop()
            self.IPandPORT_dialog.setEnabled(True)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;主中心IP：%s</font>" %
                self.IPandPORT_ui.IP_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;主中心端口：%s</font>" %
                self.IPandPORT_ui.PORT_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展1中心IP：%s</font>" %
                self.IPandPORT_ui.IP1_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展1中心端口：%s</font>" %
                self.IPandPORT_ui.PORT1_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展2中心IP：%s</font>" %
                self.IPandPORT_ui.IP2_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展2中心端口：%s</font>" %
                self.IPandPORT_ui.PORT2_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展3中心IP：%s</font>" %
                self.IPandPORT_ui.IP3_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展3中心端口：%s</font>" %
                self.IPandPORT_ui.PORT3_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展4中心IP：%s</font>" %
                self.IPandPORT_ui.IP4_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展4中心端口：%s</font>" %
                self.IPandPORT_ui.PORT4_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;是否轮询模式：%s</font>" %
                self.IPandPORT_ui.comboBox.currentText())

            self.log_textEdit.moveCursor(QTextCursor.End)

            button = QMessageBox.question(
                self,
                "Question",
                '配置完成是否重启设备？',
                QMessageBox.Ok | QMessageBox.Cancel,
                QMessageBox.Ok)
            if button == QMessageBox.Ok:
                reset = 'at+reset'
                self.ser.write('+++'.encode(encoding='gbk'))
                time.sleep(0.2)
                self.set_at_write(reset)
                self.log_textEdit.append("<font color='forestgreen'>设备重启</font>")
            else:
                pass
            self.IPandPORT_dialog.close()


    def IPandPORT_set_thread(self):
        at = 'IPAD=%s:%s' % (self.IPandPORT_ui.IP_lineEdit.text(
        ), self.IPandPORT_ui.PORT_lineEdit.text())
        at1 = 'IPAD1=%s:%s' % (self.IPandPORT_ui.IP1_lineEdit.text(
        ), self.IPandPORT_ui.PORT1_lineEdit.text())
        at2 = 'IPAD2=%s:%s' % (self.IPandPORT_ui.IP2_lineEdit.text(
        ), self.IPandPORT_ui.PORT2_lineEdit.text())
        at3 = 'IPAD3=%s:%s' % (self.IPandPORT_ui.IP3_lineEdit.text(
        ), self.IPandPORT_ui.PORT3_lineEdit.text())
        at4 = 'IPAD4=%s:%s' % (self.IPandPORT_ui.IP4_lineEdit.text(
        ), self.IPandPORT_ui.PORT4_lineEdit.text())
        at5 = 'POLLMODE=%s' % self.IPandPORT_ui.comboBox.currentText()
        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        self.set_at_write(at)
        self.set_at_write(at1)
        self.set_at_write(at2)
        self.set_at_write(at3)
        self.set_at_write(at4)
        self.set_at_write(at5)


    def IPandPORT_read(self):
        self.IPandPORT_dialog.setEnabled(False)
        self.log_textEdit.append(
            "<font color='forestgreen'>读取企业中心配置：\n</font>")

        at = 'IPAD?'
        self.IPADthread = threading.Thread(target=self.at_test, args=(at,))
        self.IPADthread.setDaemon(True)
        self.IPADthread_timer = QTimer()
        self.IPADthread_timer.timeout.connect(
            lambda: self.IPADthread_check(
                self.IPADthread, self.IPADthread_timer))
        self.IPADthread.start()
        self.IPADthread_timer.start(100)

        at1 = 'port?'
        self.PORTthread = threading.Thread(target=self.at_test, args=(at1,))
        self.PORTthread.setDaemon(True)
        self.PORTthread_timer = QTimer()
        self.PORTthread_timer.timeout.connect(
            lambda: self.PORTthread_check(
                self.PORTthread, self.PORTthread_timer))

        at2 = 'IPAD1?'
        self.IPAD1thread = threading.Thread(target=self.at_test, args=(at2,))
        self.IPAD1thread.setDaemon(True)
        self.IPAD1thread_timer = QTimer()
        self.IPAD1thread_timer.timeout.connect(
            lambda: self.IPAD1thread_check(
                self.IPAD1thread, self.IPAD1thread_timer))

        at3 = 'port1?'
        self.PORT1thread = threading.Thread(target=self.at_test, args=(at3,))
        self.PORT1thread.setDaemon(True)
        self.PORT1thread_timer = QTimer()
        self.PORT1thread_timer.timeout.connect(
            lambda: self.PORT1thread_check(
                self.PORT1thread, self.PORT1thread_timer))

        at4 = 'IPAD2?'
        self.IPAD2thread = threading.Thread(target=self.at_test, args=(at4,))
        self.IPAD2thread.setDaemon(True)
        self.IPAD2thread_timer = QTimer()
        self.IPAD2thread_timer.timeout.connect(
            lambda: self.IPAD2thread_check(
                self.IPAD2thread, self.IPAD2thread_timer))

        at5 = 'port2?'
        self.PORT2thread = threading.Thread(target=self.at_test, args=(at5,))
        self.PORT2thread.setDaemon(True)
        self.PORT2thread_timer = QTimer()
        self.PORT2thread_timer.timeout.connect(
            lambda: self.PORT2thread_check(
                self.PORT2thread, self.PORT2thread_timer))

        at6 = 'IPAD3?'
        self.IPAD3thread = threading.Thread(target=self.at_test, args=(at6,))
        self.IPAD3thread.setDaemon(True)
        self.IPAD3thread_timer = QTimer()
        self.IPAD3thread_timer.timeout.connect(
            lambda: self.IPAD3thread_check(
                self.IPAD3thread, self.IPAD3thread_timer))

        at7 = 'port3?'
        self.PORT3thread = threading.Thread(target=self.at_test, args=(at7,))
        self.PORT3thread.setDaemon(True)
        self.PORT3thread_timer = QTimer()
        self.PORT3thread_timer.timeout.connect(
            lambda: self.PORT3thread_check(
                self.PORT3thread, self.PORT3thread_timer))

        at8 = 'IPAD4?'
        self.IPAD4thread = threading.Thread(target=self.at_test, args=(at8,))
        self.IPAD4thread.setDaemon(True)
        self.IPAD4thread_timer = QTimer()
        self.IPAD4thread_timer.timeout.connect(
            lambda: self.IPAD4thread_check(
                self.IPAD4thread, self.IPAD4thread_timer))

        at9 = 'port4?'
        self.PORT4thread = threading.Thread(target=self.at_test, args=(at9,))
        self.PORT4thread.setDaemon(True)
        self.PORT4thread_timer = QTimer()
        self.PORT4thread_timer.timeout.connect(
            lambda: self.PORT4thread_check(
                self.PORT4thread, self.PORT4thread_timer))

        at10 = 'POLLMODE?'
        self.POLLMODEthread = threading.Thread(
            target=self.at_test, args=(at10,))
        self.POLLMODEthread.setDaemon(True)
        self.POLLMODEthread_timer = QTimer()
        self.POLLMODEthread_timer.timeout.connect(
            lambda: self.POLLMODEthread_check(
                self.POLLMODEthread, self.POLLMODEthread_timer))

    def POLLMODEthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            POLLMODE = self.ATresult.replace('OK', '').strip()
            self.IPandPORT_ui.comboBox.setCurrentText(POLLMODE)
            timername.stop()
            self.IPandPORT_dialog.setEnabled(True)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;主中心IP：%s</font>" %
                self.IPandPORT_ui.IP_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;主中心端口：%s</font>" %
                self.IPandPORT_ui.PORT_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展1中心IP：%s</font>" %
                self.IPandPORT_ui.IP1_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展1中心端口：%s</font>" %
                self.IPandPORT_ui.PORT1_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展2中心IP：%s</font>" %
                self.IPandPORT_ui.IP2_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展2中心端口：%s</font>" %
                self.IPandPORT_ui.PORT2_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展3中心IP：%s</font>" %
                self.IPandPORT_ui.IP3_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展3中心端口：%s</font>" %
                self.IPandPORT_ui.PORT3_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展4中心IP：%s</font>" %
                self.IPandPORT_ui.IP4_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;扩展4中心端口：%s</font>" %
                self.IPandPORT_ui.PORT4_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;是否轮询模式：%s</font>" %
                self.IPandPORT_ui.comboBox.currentText())
            self.log_textEdit.moveCursor(QTextCursor.End)

    def PORT4thread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            PORT4 = self.ATresult.strip()
            self.IPandPORT_ui.PORT4_lineEdit.setText(PORT4)
            timername.stop()
            self.POLLMODEthread.start()
            self.POLLMODEthread_timer.start(100)

    def IPAD4thread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            IP4 = self.ATresult.replace('OK', '')
            self.IPandPORT_ui.IP4_lineEdit.setText(IP4)
            timername.stop()
            self.PORT4thread.start()
            self.PORT4thread_timer.start(100)

    def PORT3thread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            PORT3 = self.ATresult.strip()
            self.IPandPORT_ui.PORT3_lineEdit.setText(PORT3)
            timername.stop()
            self.IPAD4thread.start()
            self.IPAD4thread_timer.start(100)

    def IPAD3thread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            IP3 = self.ATresult.replace('OK', '')
            self.IPandPORT_ui.IP3_lineEdit.setText(IP3)
            timername.stop()
            self.PORT3thread.start()
            self.PORT3thread_timer.start(100)

    def PORT2thread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            PORT2 = self.ATresult.strip()
            self.IPandPORT_ui.PORT2_lineEdit.setText(PORT2)
            timername.stop()
            self.IPAD3thread.start()
            self.IPAD3thread_timer.start(100)

    def IPAD2thread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            IP2 = self.ATresult.replace('OK', '')
            self.IPandPORT_ui.IP2_lineEdit.setText(IP2)
            timername.stop()
            self.PORT2thread.start()
            self.PORT2thread_timer.start(100)

    def PORT1thread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            PORT1 = self.ATresult.strip()
            self.IPandPORT_ui.PORT1_lineEdit.setText(PORT1)
            timername.stop()
            self.IPAD2thread.start()
            self.IPAD2thread_timer.start(100)

    def IPAD1thread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            IP1 = self.ATresult.replace('OK', '')
            self.IPandPORT_ui.IP1_lineEdit.setText(IP1)
            timername.stop()
            self.PORT1thread.start()
            self.PORT1thread_timer.start(100)

    def PORTthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            PORT1 = self.ATresult.strip()
            self.IPandPORT_ui.PORT_lineEdit.setText(PORT1)
            timername.stop()
            self.IPAD1thread.start()
            self.IPAD1thread_timer.start(100)

    def IPADthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            IP = self.ATresult.replace('OK', '')
            self.IPandPORT_ui.IP_lineEdit.setText(IP)
            timername.stop()
            self.PORTthread.start()
            self.PORTthread_timer.start(100)

    def IPandPORT_cancel(self):
        self.IPandPORT_dialog.close()
    # 14(16)-D工作模式配置

    def WORKmodel_set(self):
        self.log_textEdit.append(
            "<font color='forestgreen'>下载工作模式配置：\n</font>")
        self.WORKmodel_dialog.setEnabled(False)

        self.WORKmodel_setthread=threading.Thread(target=self.WORKmodel_set_thread)
        self.WORKmodel_setthread.setDaemon(True)
        self.WORKmodel_setthread_timer=QTimer()
        self.WORKmodel_setthread_timer.timeout.connect(self.WORKmodel_set_thread_check)
        self.WORKmodel_setthread.start()
        self.WORKmodel_setthread_timer.start(100)
    def WORKmodel_set_thread_check(self):
        if self.WORKmodel_setthread.is_alive():
            pass
        else:
            self.WORKmodel_setthread_timer.stop()
            self.WORKmodel_dialog.setEnabled(True)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;连接方式：%s</font>" %
                self.WORKmodel_ui.connectType_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;电话激活：%s</font>" %
                self.WORKmodel_ui.phone_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;短信激活：%s</font>" %
                self.WORKmodel_ui.sms_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;数据激活：%s</font>" %
                self.WORKmodel_ui.data_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;定时激活：%s(分)</font>" %
                self.WORKmodel_ui.active_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;定时下线：%s(分)</font>" %
                self.WORKmodel_ui.offline_lineEdit.text())
            self.log_textEdit.moveCursor(QTextCursor.End)

            button = QMessageBox.question(
                self,
                "Question",
                '配置完成是否重启设备？',
                QMessageBox.Ok | QMessageBox.Cancel,
                QMessageBox.Ok)
            if button == QMessageBox.Ok:
                reset = 'at+reset'
                self.ser.write('+++'.encode(encoding='gbk'))
                time.sleep(0.2)
                self.set_at_write(reset)
                self.log_textEdit.append("<font color='forestgreen'>设备重启</font>")
            else:
                pass
            self.WORKmodel_dialog.close()

    def WORKmodel_set_thread(self):

        if self.WORKmodel_ui.connectType_comboBox.currentText() == '长连接':
            at = 'AT+TRIGGER=NONE'
            self.ser.write('+++'.encode(encoding='gbk'))
            time.sleep(0.2)
            self.set_at_write(at)
        else:
            if self.WORKmodel_ui.phone_comboBox.currentText() == '打开':
                at1 = 'AT+TRIGGER=CALL ON'
            else:
                at1 = 'AT+TRIGGER=CALL OFF'
            if self.WORKmodel_ui.sms_comboBox.currentText() == '打开':
                at2 = 'AT+TRIGGER=SMS ON'
            else:
                at2 = 'AT+TRIGGER=SMS OFF'
            if self.WORKmodel_ui.data_comboBox.currentText() == '打开':
                at3 = 'AT+TRIGGER=DATA ON'
            else:
                at3 = 'AT+TRIGGER=DATA OFF'
            try:
                activetime = int(self.WORKmodel_ui.active_lineEdit.text())
                if 5 <= activetime <= 1440:
                    at4 = 'AT+TRIGGER=TIME:%d' % activetime
                else:
                    self.WORKmodel_ui.active_lineEdit.setText('5')
                    at4 = 'AT+TRIGGER=TIME:5'
            except BaseException:
                self.WORKmodel_ui.active_lineEdit.setText('5')
                at4 = 'AT+TRIGGER=TIME:5'
            try:
                offtime = int(self.WORKmodel_ui.offline_lineEdit.text())
                if 1 <= offtime <= 60:
                    at5 = 'AT+IDLE=%d' % offtime
                else:
                    self.WORKmodel_ui.offline_lineEdit.setText('3')
                    at5 = 'AT+IDLE=3'
            except BaseException:
                self.WORKmodel_ui.offline_lineEdit.setText('3')
                at5 = 'AT+IDLE=3'
            self.ser.write('+++'.encode(encoding='gbk'))
            time.sleep(0.2)
            self.set_at_write(at1)
            self.set_at_write(at2)
            self.set_at_write(at3)
            self.set_at_write(at4)
            self.set_at_write(at5)



    def WORKmodel_cancel(self):
        self.WORKmodel_dialog.close()
    # 14(16)-D工作模式参数读取

    def WORKmodel_read(self):
        self.WORKmodel_dialog.setEnabled(False)
        self.log_textEdit.append(
            "<font color='forestgreen'>读取工作模式配置：\n</font>")

        at = 'TRIGGER?'
        self.TYPEthread = threading.Thread(target=self.at_test, args=(at,))
        self.TYPEthread.setDaemon(True)
        self.TYPEthread_timer = QTimer()
        self.TYPEthread_timer.timeout.connect(
            lambda: self.TYPEthread_check(
                self.TYPEthread, self.TYPEthread_timer))
        self.TYPEthread.start()
        self.TYPEthread_timer.start(100)

        at1 = 'IDLE?'
        self.Offlinethread = threading.Thread(target=self.at_test, args=(at1,))
        self.Offlinethread.setDaemon(True)
        self.Offlinethread_timer = QTimer()
        self.Offlinethread_timer.timeout.connect(
            lambda: self.Offlinethread_check(
                self.Offlinethread, self.Offlinethread_timer))

    def Offlinethread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            self.ATresult = self.ATresult.replace('OK', '')
            self.WORKmodel_ui.offline_lineEdit.setText(self.ATresult.strip())
            timername.stop()
            self.WORKmodel_dialog.setEnabled(True)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;连接方式：%s</font>" %
                self.WORKmodel_ui.connectType_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;电话激活：%s</font>" %
                self.WORKmodel_ui.phone_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;短信激活：%s</font>" %
                self.WORKmodel_ui.sms_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;数据激活：%s</font>" %
                self.WORKmodel_ui.data_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;定时激活：%s(分)</font>" %
                self.WORKmodel_ui.active_lineEdit.text())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;定时下线：%s(分)</font>" %
                self.WORKmodel_ui.offline_lineEdit.text())
            self.log_textEdit.moveCursor(QTextCursor.End)

    # 14(16)-D查询连接方式线程的检查和结果显示
    def TYPEthread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            if 'NONE' in self.ATresult:
                self.WORKmodel_ui.connectType_comboBox.setCurrentIndex(0)
                self.WORKmodel_ui.active_lineEdit.setText('5')
                self.WORKmodel_ui.phone_comboBox.setCurrentIndex(0)
                self.WORKmodel_ui.sms_comboBox.setCurrentIndex(0)
                self.WORKmodel_ui.data_comboBox.setCurrentIndex(0)

            else:
                if 'CALL' in self.ATresult:
                    self.WORKmodel_ui.phone_comboBox.setCurrentIndex(0)
                else:
                    self.WORKmodel_ui.phone_comboBox.setCurrentIndex(1)
                if 'SMS' in self.ATresult:
                    self.WORKmodel_ui.sms_comboBox.setCurrentIndex(0)
                else:
                    self.WORKmodel_ui.sms_comboBox.setCurrentIndex(1)
                if 'DATA' in self.ATresult:
                    self.WORKmodel_ui.data_comboBox.setCurrentIndex(0)
                else:
                    self.WORKmodel_ui.data_comboBox.setCurrentIndex(1)
                if 'TIME' in self.ATresult:
                    activetime = self.ATresult.strip()[-1:]
                    self.WORKmodel_ui.active_lineEdit.setText(activetime)
                else:
                    self.WORKmodel_ui.active_lineEdit.setText('5')

                self.WORKmodel_ui.connectType_comboBox.setCurrentIndex(1)

            timername.stop()
            self.Offlinethread.start()
            self.Offlinethread_timer.start(100)

    # 14(16)-D串口设置
    def COMset_set(self):
        self.log_textEdit.append("<font color='forestgreen'>下载串口配置：</font>")
        self.COMset_dialog.setEnabled(False)

        self.COMset_setthread=threading.Thread(target=self.COMset_set_thread)
        self.COMset_setthread.setDaemon(True)
        self.COMset_setthread_timer=QTimer()
        self.COMset_setthread_timer.timeout.connect(self.COMset_set_thread_check)
        self.COMset_setthread.start()
        self.COMset_setthread_timer.start(100)
    def COMset_set_thread_check(self):
        if self.COMset_setthread.is_alive():
            pass
        else:
            self.COMset_setthread_timer.stop()
            self.COMset_dialog.setEnabled(True)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口1波特率：%s</font>" %
                self.COMset_ui.COM1_baudrates_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口1数据位：%s</font>" %
                self.COMset_ui.COM1_Databits_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口1停止位：%s</font>" %
                self.COMset_ui.COM1_Stopbits_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口1校验位：%s</font>" %
                self.COMset_ui.COM1_paritys_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口2波特率：%s</font>" %
                self.COMset_ui.COM2_baudrates_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口2数据位：%s</font>" %
                self.COMset_ui.COM2_Databits_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口2停止位：%s</font>" %
                self.COMset_ui.COM2_Stopbits_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口2校验位：%s</font>" %
                self.COMset_ui.COM2_paritys_comboBox.currentText())
            self.log_textEdit.moveCursor(QTextCursor.End)

            button = QMessageBox.question(
                self,
                "Question",
                '配置完成是否重启设备？',
                QMessageBox.Ok | QMessageBox.Cancel,
                QMessageBox.Ok)
            if button == QMessageBox.Ok:
                reset = 'at+reset'
                self.ser.write('+++'.encode(encoding='gbk'))
                time.sleep(0.2)
                self.set_at_write(reset)
                self.log_textEdit.append("<font color='forestgreen'>设备重启</font>")
            else:
                pass
            self.COMset_dialog.close()
    def COMset_set_thread(self):
        at = 'AT+IPR1=%s' % self.COMset_ui.COM1_baudrates_comboBox.currentText()
        DPS = self.COMset_ui.COM1_Databits_comboBox.currentText() + self.COMset_ui.COM1_paritys_comboBox.currentText() + \
            self.COMset_ui.COM1_Stopbits_comboBox.currentText()
        at1 = 'AT+SCOM1=%s' % DPS

        at2 = 'AT+IPR2=%s' % self.COMset_ui.COM2_baudrates_comboBox.currentText()
        DPS2 = self.COMset_ui.COM2_Databits_comboBox.currentText() + self.COMset_ui.COM2_paritys_comboBox.currentText() + \
            self.COMset_ui.COM2_Stopbits_comboBox.currentText()
        at3 = 'AT+SCOM2=%s' % DPS2

        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        self.set_at_write(at)
        self.set_at_write(at1)
        self.set_at_write(at2)
        self.set_at_write(at3)



    def COMset_cancel(self):
        self.COMset_dialog.close()
    # 14(16)-D串口配置读取

    def COMset_read(self):
        self.COMset_dialog.setEnabled(False)
        self.log_textEdit.append("<font color='forestgreen'>读取串口配置：\n</font>")

        at = 'IPR1?'
        self.IPR1thread = threading.Thread(target=self.at_test, args=(at,))
        self.IPR1thread.setDaemon(True)
        self.IPR1thread_timer = QTimer()
        self.IPR1thread_timer.timeout.connect(
            lambda: self.IPR1thread_check(
                self.IPR1thread, self.IPR1thread_timer))
        self.IPR1thread.start()
        self.IPR1thread_timer.start(100)

        at1 = 'SCOM1?'
        self.SCOM1thread = threading.Thread(target=self.at_test, args=(at1,))
        self.SCOM1thread.setDaemon(True)
        self.SCOM1thread_timer = QTimer()
        self.SCOM1thread_timer.timeout.connect(
            lambda: self.SCOM1thread_check(
                self.SCOM1thread, self.SCOM1thread_timer))

        at2 = 'IPR2?'
        self.IPR2thread = threading.Thread(target=self.at_test, args=(at2,))
        self.IPR2thread.setDaemon(True)
        self.IPR2thread_timer = QTimer()
        self.IPR2thread_timer.timeout.connect(
            lambda: self.IPR2thread_check(
                self.IPR2thread, self.IPR2thread_timer))

        at3 = 'SCOM2?'
        self.SCOM2thread = threading.Thread(target=self.at_test, args=(at3,))
        self.SCOM2thread.setDaemon(True)
        self.SCOM2thread_timer = QTimer()
        self.SCOM2thread_timer.timeout.connect(
            lambda: self.SCOM2thread_check(
                self.SCOM2thread, self.SCOM2thread_timer))

    def SCOM2thread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            self.ATresult = self.ATresult.strip()
            databit = self.ATresult[0:1]
            self.COMset_ui.COM2_Databits_comboBox.setCurrentIndex(
                self.databits.get(databit))
            paritybit = self.ATresult[1:2]
            self.COMset_ui.COM2_paritys_comboBox.setCurrentIndex(
                self.paritybits.get(paritybit))
            stopbit = self.ATresult[2:3]
            try:
                stopbit = int(stopbit)
            except BaseException:
                stopbit = 1
            self.COMset_ui.COM2_Stopbits_comboBox.setCurrentIndex(stopbit - 1)
            timername.stop()
            self.COMset_dialog.setEnabled(True)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口1波特率：%s</font>" %
                self.COMset_ui.COM1_baudrates_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口1数据位：%s</font>" %
                self.COMset_ui.COM1_Databits_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口1停止位：%s</font>" %
                self.COMset_ui.COM1_Stopbits_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口1校验位：%s</font>" %
                self.COMset_ui.COM1_paritys_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口2波特率：%s</font>" %
                self.COMset_ui.COM2_baudrates_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口2数据位：%s</font>" %
                self.COMset_ui.COM2_Databits_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口2停止位：%s</font>" %
                self.COMset_ui.COM2_Stopbits_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;串口2校验位：%s</font>" %
                self.COMset_ui.COM2_paritys_comboBox.currentText())
            self.log_textEdit.moveCursor(QTextCursor.End)

    def IPR2thread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            baud = self.ATresult.replace('OK', '')
            baud = baud.strip()
            try:
                self.COMset_ui.COM2_baudrates_comboBox.setCurrentIndex(
                    self.bauds.get(baud))
            except:
                pass

            timername.stop()
            self.SCOM2thread.start()
            self.SCOM2thread_timer.start(100)

    def SCOM1thread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            self.ATresult = self.ATresult.strip()
            databit = self.ATresult[0:1]
            self.COMset_ui.COM1_Databits_comboBox.setCurrentIndex(
                self.databits.get(databit))
            paritybit = self.ATresult[1:2]
            self.COMset_ui.COM1_paritys_comboBox.setCurrentIndex(
                self.paritybits.get(paritybit))
            stopbit = self.ATresult[2:3]
            try:
                stopbit = int(stopbit)
            except BaseException:
                stopbit = 1
            self.COMset_ui.COM1_Stopbits_comboBox.setCurrentIndex(stopbit - 1)
            timername.stop()
            self.IPR2thread.start()
            self.IPR2thread_timer.start(100)

    def IPR1thread_check(self, threadname, timername):
        if threadname.is_alive():
            pass
        else:
            baud = self.ATresult.replace('OK', '')
            baud = baud.strip()
            self.COMset_ui.COM1_baudrates_comboBox.setCurrentIndex(
                self.bauds.get(baud))
            timername.stop()
            self.SCOM1thread.start()
            self.SCOM1thread_timer.start(100)
    # 14(16)-D 网络模式、连接方式、调试模式、DTU设备号、加密类型配置

    def set_ok(self):
        self.log_textEdit.append("<font color='forestgreen'>下载配置：</font>")
        self.one.setEnabled(False)

        self.set_okthread=threading.Thread(target=self.set_ok_thread)
        self.set_okthread.setDaemon(True)
        self.set_okthread_timer=QTimer()
        self.set_okthread_timer.timeout.connect(self.set_ok_thread_check)
        self.set_okthread.start()
        self.set_okthread_timer.start(100)


    def set_ok_thread_check(self):
        if self.set_okthread.is_alive():
            pass
        else:
            self.set_okthread_timer.stop()
            self.one.setEnabled(True)
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;网络模式：%s</font>" %
                self.one.netModel_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;连接方式：%s</font>" %
                self.one.connectMode_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;调试模式：%s</font>" %
                self.one.log_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;加密类型：%s</font>" %
                self.one.encryType_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;&nbsp;设备号：%s</font>" %
                self.one.ID_lineEdit.text())
            self.log_textEdit.moveCursor(QTextCursor.End)

            button = QMessageBox.question(
                self,
                "Question",
                '配置完成是否重启设备？',
                QMessageBox.Ok | QMessageBox.Cancel,
                QMessageBox.Ok)
            if button == QMessageBox.Ok:
                reset = 'at+reset'
                self.set_at_write(reset)
                self.log_textEdit.append("<font color='forestgreen'>设备重启</font>")
            else:
                pass


    def set_ok_thread(self):
        netmode = self.netmodes.get(self.one.netModel_comboBox.currentText())
        at = 'at+netmode=%d' % netmode
        at1 = 'at+workpro=%s' % self.one.connectMode_comboBox.currentText()
        at2 = 'at+debug=%d' % self.debug.get(
            self.one.log_comboBox.currentText())
        dtuid = self.one.ID_lineEdit.text()[0:11]
        if dtuid == '':
            dtuid = '00000000001'
            self.one.ID_lineEdit.setText(dtuid)
        at3 = 'at+dtuid=%s' % dtuid
        at4 = 'at+enctype=%d' % self.enctype.get(
            self.one.encryType_comboBox.currentText())
        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        self.set_at_write(at1)
        self.set_at_write(at2)
        self.set_at_write(at3)
        self.set_at_write(at4)
        if netmode == 21:
            loginat = [85, 170, 85, 170, 5, 0, 17, 129, 16, 0, 3, 97,
                       100, 109, 129, 17, 0, 6, 49, 50, 51, 52, 53, 54, 31, 68]
            setat = [85, 170, 85, 170, 1, 0, 5, 145, 17, 0, 1, 21, 151, 44]
            loginat = bytes(loginat)
            setat = bytes(setat)
            self.ser.write(loginat)
            time.sleep(0.1)
            self.ser.write(setat)
            quit = 'at+quit'
            self.set_at_write(quit)
        else:
            self.set_at_write(at)



    # 发送配置的at指令

    def set_at_write(self, AT):
        # self.ser.write('+++'.encode(encoding='gbk'))
        # time.sleep(0.2)
        self.ser.write((AT + '\r\n').encode(encoding='gbk'))
        time.sleep(0.2)
    # 14(16)-D恢复出厂设置

    def reset(self):
        self.frame_2.setEnabled(False)
        self.log_textEdit.append("<font color='forestgreen'>恢复出厂设置：</font>")
        at = 'at+factory'
        self.resetthread = threading.Thread(target=self.at_test, args=(at,))
        self.resetthread.setDaemon(True)
        self.resetthread_timer = QTimer()
        self.resetthread_timer.timeout.connect(
            lambda: self.resetthread_check(
                self.resetthread, self.resetthread_timer))
        self.resetthread.start()
        self.resetthread_timer.start(100)

    # 14(16)-D版本检测
    def ver_check(self):
        self.frame_2.setEnabled(False)
        self.log_textEdit.append("<font color='forestgreen'>版本查询：\n</font>")
        at = 'ver?'
        # self.atthread=MyThread(self.at_test,args=(at,))
        self.atthread = threading.Thread(target=self.at_test, args=(at,))
        self.atthread.setDaemon(True)

        self.thread_timer = QTimer()
        self.thread_timer.timeout.connect(
            lambda: self.thread_check(
                self.atthread, self.thread_timer))
        self.atthread.start()
        self.thread_timer.start(100)

        # self.ver_btnshow=COMcheck_state_thread()
        # self.ver_btnshow.signal.connect(lambda :self.one.version_pushButton.setEnabled(True))
        # self.ver_btnshow.start()

     # 14(16)-D网络模式、连接方式、调试模式、设备号、加密类型配置查询
    def one_read(self):
        self.frame_2.setEnabled(False)
        self.log_textEdit.append("<font color='forestgreen'>读取配置：\n</font>")

        at = 'dtuid?'  # 查询设备号
        self.IDthread = threading.Thread(target=self.at_test, args=(at,))
        self.IDthread.setDaemon(True)
        self.IDthread_timer = QTimer()
        self.IDthread_timer.timeout.connect(
            lambda: self.IDthread_check(
                self.IDthread, self.IDthread_timer))
        self.IDthread.start()
        self.IDthread_timer.start(100)

        at1 = 'debug?'  # 查询调试模式
        self.Debugthread = threading.Thread(target=self.at_test, args=(at1,))
        self.Debugthread.setDaemon(True)
        self.Debugthread_timer = QTimer()
        self.Debugthread_timer.timeout.connect(
            lambda: self.Debugthread_check(
                self.Debugthread, self.Debugthread_timer))

        at2 = 'netmode?'  # 查询网络模式
        self.Netmodethread = threading.Thread(target=self.at_test, args=(at2,))
        self.Netmodethread.setDaemon(True)
        self.Netmodethread_timer = QTimer()
        self.Netmodethread_timer.timeout.connect(
            lambda: self.Netmodethread_check(
                self.Netmodethread, self.Netmodethread_timer))

        at3 = 'workpro?'  # 查询工作模式
        self.Workprothread = threading.Thread(target=self.at_test, args=(at3,))
        self.Workprothread.setDaemon(True)
        self.Workprothread_timer = QTimer()
        self.Workprothread_timer.timeout.connect(
            lambda: self.Workprothread_check(
                self.Workprothread, self.Workprothread_timer))

        at4 = 'ENCTYPE?'  # 查询加密模式
        self.Enctypethread = threading.Thread(target=self.at_test, args=(at4,))
        self.Enctypethread.setDaemon(True)
        self.Enctypethread_timer = QTimer()
        self.Enctypethread_timer.timeout.connect(
            lambda: self.Enctypethread_check(
                self.Enctypethread, self.Enctypethread_timer))

        # self.read_btnshow = COMcheck_state_thread()
        # self.read_btnshow.signal.connect(lambda: self.one.read_pushButton.setEnabled(True))
        # self.read_btnshow.start()
    # 出厂设置的线程检测和结果显示
    def resetthread_check(self, threadname, timername):

        if threadname.is_alive():
            pass
        else:
            if self.ATresult and 'ComNetCmdProcess return' in self.ATresult:
                self.log_textEdit.append(
                    "<font color='darkviolet'>&nbsp;&nbsp;OK</font>")
            else:
                if self.ATresult and "OK" in self.ATresult:
                    self.log_textEdit.append(
                        "<font color='darkviolet'>&nbsp;&nbsp;OK</font>")
            timername.stop()
            self.one_read()
           # self.frame_2.setEnabled(True)

    # 查询加密模式的线程检测和结果显示
    def Enctypethread_check(self, threadname, timername):
        # print(threadname.is_alive())
        if threadname.is_alive():
            pass
        else:
            if self.ATresult == '' or 'ERROR' in self.ATresult:
                self.one.encryType_comboBox.setCurrentIndex(0)
            else:
                Enctype = self.ATresult.replace("OK", "")
                try:
                    Enctype = int(Enctype.strip())
                    self.one.encryType_comboBox.setCurrentIndex(Enctype)
                except BaseException:
                    self.one.encryType_comboBox.setCurrentIndex(0)

            # self.show_log(self.ATresult)
            timername.stop()
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;网络模式：%s</font>" %
                self.one.netModel_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;连接方式：%s</font>" %
                self.one.connectMode_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;调试模式：%s</font>" %
                self.one.log_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;加密类型：%s</font>" %
                self.one.encryType_comboBox.currentText())
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;&nbsp;设备号：%s</font>" %
                self.one.ID_lineEdit.text())
            self.frame_2.setEnabled(True)
            self.log_textEdit.moveCursor(QTextCursor.End)

    # 查询工作模式的线程检测和结果显示
    def Workprothread_check(self, threadname, timername):
        # print(threadname.is_alive())
        if threadname.is_alive():
            pass
        else:
            Workpro = self.ATresult.replace("OK", "")
            Workpro = Workpro.strip()
            self.one.connectMode_comboBox.setCurrentText(Workpro)
            # self.show_log(self.ATresult)
            timername.stop()
            self.Enctypethread.start()
            self.Enctypethread_timer.start(100)
    # 查询网络模式的线程检测和结果显示

    def Netmodethread_check(self, threadname, timername):
        # print(threadname.is_alive())
        if threadname.is_alive():
            pass
        else:
            Netmode = self.ATresult.replace("OK", "")
            try:
                Netmode = int(Netmode.strip())
                if Netmode == 0:
                    self.one.netModel_comboBox.setCurrentIndex(0)
                elif Netmode == 1:
                    self.one.netModel_comboBox.setCurrentIndex(3)
                elif Netmode == 2:
                    self.one.netModel_comboBox.setCurrentIndex(1)
                elif Netmode == 3:
                    self.one.netModel_comboBox.setCurrentIndex(2)
                elif Netmode == 21:
                    self.one.netModel_comboBox.setCurrentIndex(4)
            except BaseException:
                pass
            # self.show_log(self.ATresult)
            timername.stop()
            self.Workprothread.start()
            self.Workprothread_timer.start(100)
    # 查询调试模式的线程检测和结果显示

    def Debugthread_check(self, threadname, timername):
        # print(threadname.is_alive())
        if threadname.is_alive():
            pass
        else:
            Debug = self.ATresult.replace("OK", "")
            try:
                Debug = int(Debug.strip())
                self.one.log_comboBox.setCurrentIndex(Debug)
            except BaseException:
                pass
            # self.show_log(self.ATresult)
            timername.stop()
            self.Netmodethread.start()
            self.Netmodethread_timer.start(100)
    # 查询设备号的线程检测和结果显示

    def IDthread_check(self, threadname, timername):
       # print(threadname.is_alive())
        if threadname.is_alive():
            pass
        else:

            DTUID = self.ATresult.replace("OK", "")
            DTUID = DTUID.strip()
            self.one.ID_lineEdit.setText(DTUID)
            # self.show_log(self.ATresult)
            timername.stop()
            self.Debugthread.start()
            self.Debugthread_timer.start(100)
    # 发送at指令，并解析返回结果

    def at_test(self, AT):
        old_data = self.receive_textEdit.toPlainText()
        self.ser.write('+++'.encode(encoding='gbk'))
        time.sleep(0.2)
        self.ser.write((AT + '\r\n').encode(encoding='gbk'))
        time.sleep(0.7)
        new_data = self.receive_textEdit.toPlainText()
        result_data = new_data.replace(old_data, '')
        # print(old_data)
        # print('======OLD======')
        # print(new_data)
        # print('======NEW=======')
        # print(result_data)
        if 'rsp'in result_data:
            rsp = re.search('rsp:(.*?)\n', result_data, re.S)
            if rsp is not None:
                # print(rsp.group(1)=='')
                self.ATresult = rsp.group(1)
            else:
                pass
        else:
            if len(new_data) == len(old_data) * 2:
                result_data = old_data
            self.ATresult = result_data.replace("ENTER OK", "")
    # 版本查询线程的检测和结果显示

    def thread_check(self, threadname, timername):
       # print(threadname.is_alive())
        if threadname.is_alive():
            pass
        else:
            self.log_textEdit.append(
                "<font color='darkviolet'>&nbsp;&nbsp;%s</font>" %
                self.ATresult)
            # self.show_log(self.ATresult)
            timername.stop()
            self.frame_2.setEnabled(True)
    # 短信配置开关时，页面进行相应的变化
    def F16SMSset_ONorOFF(self):
        if self.F16SMSset_ui.SMSset_comboBox.currentText()=='关闭':
            self.F16SMSset_ui.label_2.hide()
            self.F16SMSset_ui.label_3.hide()
            self.F16SMSset_ui.SMSset_lineEdit.hide()
            self.F16SMSset_ui.admin_lineEdit.hide()
        else:
            self.F16SMSset_ui.label_2.show()
            self.F16SMSset_ui.label_3.show()
            self.F16SMSset_ui.SMSset_lineEdit.show()
            self.F16SMSset_ui.admin_lineEdit.show()

    # 中心服务器数量变化时，页面进行相应的变化
    def F16server_num(self):
        if self.F16IPandPORTset_ui.serverNum_comboBox.currentText() == '1':
            self.F16IPandPORTset_ui.label_6.hide()
            self.F16IPandPORTset_ui.label_7.hide()
            self.F16IPandPORTset_ui.label_8.hide()
            self.F16IPandPORTset_ui.label_9.hide()
            self.F16IPandPORTset_ui.label_10.hide()
            self.F16IPandPORTset_ui.label_11.hide()
            self.F16IPandPORTset_ui.label_12.hide()
            self.F16IPandPORTset_ui.label_13.hide()
            self.F16IPandPORTset_ui.server2_lineEdit.hide()
            self.F16IPandPORTset_ui.port2_lineEdit.hide()
            self.F16IPandPORTset_ui.server3_lineEdit.hide()
            self.F16IPandPORTset_ui.port3_lineEdit.hide()
            self.F16IPandPORTset_ui.server4_lineEdit.hide()
            self.F16IPandPORTset_ui.port4_lineEdit.hide()
            self.F16IPandPORTset_ui.server5_lineEdit.hide()
            self.F16IPandPORTset_ui.port5_lineEdit.hide()
            self.F16IPandPORTset_ui.label_4.show()
            self.F16IPandPORTset_ui.label_5.show()
            self.F16IPandPORTset_ui.server1_lineEdit.show()
            self.F16IPandPORTset_ui.port1_lineEdit.show()
            self.F16IPandPORTset_ui.label_16.show()
            self.F16IPandPORTset_ui.reserver_comboBox.show()
        elif self.F16IPandPORTset_ui.serverNum_comboBox.currentText()=='2':
            self.F16IPandPORTset_ui.label_4.hide()
            self.F16IPandPORTset_ui.label_5.hide()
            self.F16IPandPORTset_ui.server1_lineEdit.hide()
            self.F16IPandPORTset_ui.port1_lineEdit.hide()
            self.F16IPandPORTset_ui.label_6.show()
            self.F16IPandPORTset_ui.label_7.show()
            self.F16IPandPORTset_ui.label_8.hide()
            self.F16IPandPORTset_ui.label_9.hide()
            self.F16IPandPORTset_ui.label_10.hide()
            self.F16IPandPORTset_ui.label_11.hide()
            self.F16IPandPORTset_ui.label_12.hide()
            self.F16IPandPORTset_ui.label_13.hide()
            self.F16IPandPORTset_ui.server2_lineEdit.show()
            self.F16IPandPORTset_ui.port2_lineEdit.show()
            self.F16IPandPORTset_ui.server3_lineEdit.hide()
            self.F16IPandPORTset_ui.port3_lineEdit.hide()
            self.F16IPandPORTset_ui.server4_lineEdit.hide()
            self.F16IPandPORTset_ui.port4_lineEdit.hide()
            self.F16IPandPORTset_ui.server5_lineEdit.hide()
            self.F16IPandPORTset_ui.port5_lineEdit.hide()
            self.F16IPandPORTset_ui.label_16.hide()
            self.F16IPandPORTset_ui.reserver_comboBox.hide()
        elif self.F16IPandPORTset_ui.serverNum_comboBox.currentText()=='3':
            self.F16IPandPORTset_ui.label_4.hide()
            self.F16IPandPORTset_ui.label_5.hide()
            self.F16IPandPORTset_ui.server1_lineEdit.hide()
            self.F16IPandPORTset_ui.port1_lineEdit.hide()
            self.F16IPandPORTset_ui.label_6.show()
            self.F16IPandPORTset_ui.label_7.show()
            self.F16IPandPORTset_ui.label_8.show()
            self.F16IPandPORTset_ui.label_9.show()
            self.F16IPandPORTset_ui.label_10.hide()
            self.F16IPandPORTset_ui.label_11.hide()
            self.F16IPandPORTset_ui.label_12.hide()
            self.F16IPandPORTset_ui.label_13.hide()
            self.F16IPandPORTset_ui.server2_lineEdit.show()
            self.F16IPandPORTset_ui.port2_lineEdit.show()
            self.F16IPandPORTset_ui.server3_lineEdit.show()
            self.F16IPandPORTset_ui.port3_lineEdit.show()
            self.F16IPandPORTset_ui.server4_lineEdit.hide()
            self.F16IPandPORTset_ui.port4_lineEdit.hide()
            self.F16IPandPORTset_ui.server5_lineEdit.hide()
            self.F16IPandPORTset_ui.port5_lineEdit.hide()
            self.F16IPandPORTset_ui.label_16.hide()
            self.F16IPandPORTset_ui.reserver_comboBox.hide()
        elif self.F16IPandPORTset_ui.serverNum_comboBox.currentText()=='4':
            self.F16IPandPORTset_ui.label_4.hide()
            self.F16IPandPORTset_ui.label_5.hide()
            self.F16IPandPORTset_ui.server1_lineEdit.hide()
            self.F16IPandPORTset_ui.port1_lineEdit.hide()
            self.F16IPandPORTset_ui.label_6.show()
            self.F16IPandPORTset_ui.label_7.show()
            self.F16IPandPORTset_ui.label_8.show()
            self.F16IPandPORTset_ui.label_9.show()
            self.F16IPandPORTset_ui.label_10.show()
            self.F16IPandPORTset_ui.label_11.show()
            self.F16IPandPORTset_ui.label_12.hide()
            self.F16IPandPORTset_ui.label_13.hide()
            self.F16IPandPORTset_ui.server2_lineEdit.show()
            self.F16IPandPORTset_ui.port2_lineEdit.show()
            self.F16IPandPORTset_ui.server3_lineEdit.show()
            self.F16IPandPORTset_ui.port3_lineEdit.show()
            self.F16IPandPORTset_ui.server4_lineEdit.show()
            self.F16IPandPORTset_ui.port4_lineEdit.show()
            self.F16IPandPORTset_ui.server5_lineEdit.hide()
            self.F16IPandPORTset_ui.port5_lineEdit.hide()
            self.F16IPandPORTset_ui.label_16.hide()
            self.F16IPandPORTset_ui.reserver_comboBox.hide()
        elif self.F16IPandPORTset_ui.serverNum_comboBox.currentText()=='5':
            self.F16IPandPORTset_ui.label_4.hide()
            self.F16IPandPORTset_ui.label_5.hide()
            self.F16IPandPORTset_ui.server1_lineEdit.hide()
            self.F16IPandPORTset_ui.port1_lineEdit.hide()
            self.F16IPandPORTset_ui.label_6.show()
            self.F16IPandPORTset_ui.label_7.show()
            self.F16IPandPORTset_ui.label_8.show()
            self.F16IPandPORTset_ui.label_9.show()
            self.F16IPandPORTset_ui.label_10.show()
            self.F16IPandPORTset_ui.label_11.show()
            self.F16IPandPORTset_ui.label_12.show()
            self.F16IPandPORTset_ui.label_13.show()
            self.F16IPandPORTset_ui.server2_lineEdit.show()
            self.F16IPandPORTset_ui.port2_lineEdit.show()
            self.F16IPandPORTset_ui.server3_lineEdit.show()
            self.F16IPandPORTset_ui.port3_lineEdit.show()
            self.F16IPandPORTset_ui.server4_lineEdit.show()
            self.F16IPandPORTset_ui.port4_lineEdit.show()
            self.F16IPandPORTset_ui.server5_lineEdit.show()
            self.F16IPandPORTset_ui.port5_lineEdit.show()
            self.F16IPandPORTset_ui.label_16.hide()
            self.F16IPandPORTset_ui.reserver_comboBox.hide()


    # 16 自定义模式选择客户端时，选择心跳开启或关闭时页面进行相应变化
    def heartOPENorCLOSE(self):
        if self.F16WORKtype_ui.comboBox_33.currentText() == '开启':
            self.F16WORKtype_ui.label_24.show()
            self.F16WORKtype_ui.comboBox_10.show()
            self.F16WORKtype_ui.label_25.show()
            self.F16WORKtype_ui.label_26.show()
            self.F16WORKtype_ui.label_27.show()
            self.F16WORKtype_ui.label_28.show()
            self.F16WORKtype_ui.lineEdit_13.show()
            self.F16WORKtype_ui.lineEdit_14.show()
            self.F16WORKtype_ui.lineEdit_15.show()
            self.F16WORKtype_ui.lineEdit_16.show()
        else:
            self.F16WORKtype_ui.label_24.hide()
            self.F16WORKtype_ui.comboBox_10.hide()
            self.F16WORKtype_ui.label_25.hide()
            self.F16WORKtype_ui.label_26.hide()
            self.F16WORKtype_ui.label_27.hide()
            self.F16WORKtype_ui.label_28.hide()
            self.F16WORKtype_ui.lineEdit_13.hide()
            self.F16WORKtype_ui.lineEdit_14.hide()
            self.F16WORKtype_ui.lineEdit_15.hide()
            self.F16WORKtype_ui.lineEdit_16.hide()

    # 自定义模式时，选择客户端或者服务端时，设置页进行相应变化

    def ClientORServer(self):
        if self.F16WORKtype_ui.comboBox_31.currentText() == '客户端模式':
            self.F16WORKtype_ui.label_75.hide()
            self.F16WORKtype_ui.lineEdit_39.hide()
            self.F16WORKtype_ui.label_76.show()
            self.F16WORKtype_ui.comboBox_33.show()
            if self.F16WORKtype_ui.comboBox_33.currentText() == '开启':
                self.F16WORKtype_ui.label_24.show()
                self.F16WORKtype_ui.comboBox_10.show()
                self.F16WORKtype_ui.label_25.show()
                self.F16WORKtype_ui.label_26.show()
                self.F16WORKtype_ui.label_27.show()
                self.F16WORKtype_ui.label_28.show()
                self.F16WORKtype_ui.lineEdit_13.show()
                self.F16WORKtype_ui.lineEdit_14.show()
                self.F16WORKtype_ui.lineEdit_15.show()
                self.F16WORKtype_ui.lineEdit_16.show()
        elif self.F16WORKtype_ui.comboBox_31.currentText() == '服务端模式':
            self.F16WORKtype_ui.label_75.show()
            self.F16WORKtype_ui.lineEdit_39.show()
            self.F16WORKtype_ui.label_76.hide()
            self.F16WORKtype_ui.comboBox_33.hide()

            self.F16WORKtype_ui.label_24.hide()
            self.F16WORKtype_ui.comboBox_10.hide()
            self.F16WORKtype_ui.label_25.hide()
            self.F16WORKtype_ui.label_26.hide()
            self.F16WORKtype_ui.label_27.hide()
            self.F16WORKtype_ui.label_28.hide()
            self.F16WORKtype_ui.lineEdit_13.hide()
            self.F16WORKtype_ui.lineEdit_14.hide()
            self.F16WORKtype_ui.lineEdit_15.hide()
            self.F16WORKtype_ui.lineEdit_16.hide()

    # 16选择不同的工作模式时，工作模式设置页面进行相应的变化

    def protocolTypeChange(self):
        if self.F16WORKtype_ui.protocolType_comboBox.currentText() == 'PROT':
            self.qsl1.setCurrentIndex(0)
            self.F16WORKtype_ui.frame_2.show()
        elif self.F16WORKtype_ui.protocolType_comboBox.currentText() == 'DCUDP' or self.F16WORKtype_ui.protocolType_comboBox.currentText() == 'DCTCP':
            self.qsl1.setCurrentIndex(1)
            self.F16WORKtype_ui.frame_2.show()
        elif self.F16WORKtype_ui.protocolType_comboBox.currentText() == 'TRNS':
            self.qsl1.setCurrentIndex(2)
            self.F16WORKtype_ui.frame_2.hide()
        elif self.F16WORKtype_ui.protocolType_comboBox.currentText() == 'SMSCLI':
            self.qsl1.setCurrentIndex(3)
            self.F16WORKtype_ui.frame_2.hide()
        elif self.F16WORKtype_ui.protocolType_comboBox.currentText() == 'SMSSER':
            self.qsl1.setCurrentIndex(4)
            self.F16WORKtype_ui.frame_2.hide()
        elif self.F16WORKtype_ui.protocolType_comboBox.currentText() == 'HTTP':
            self.qsl1.setCurrentIndex(5)
            self.F16WORKtype_ui.frame_2.show()
        elif self.F16WORKtype_ui.protocolType_comboBox.currentText() == '自定义':
            self.qsl1.setCurrentIndex(6)
            self.F16WORKtype_ui.frame_2.show()

    # 16选择不同的激活模式时，激活模式设置部分进行相应的变化
    def activeTypeChange(self):
        if self.F16WORKtype_ui.activeType_comboBox.currentText() == '自动':
            self.qsl2.setCurrentIndex(0)
        elif self.F16WORKtype_ui.activeType_comboBox.currentText() == '短信激活':
            self.qsl2.setCurrentIndex(1)
        elif self.F16WORKtype_ui.activeType_comboBox.currentText() == '电话激活':
            self.qsl2.setCurrentIndex(2)
        elif self.F16WORKtype_ui.activeType_comboBox.currentText() == '串口激活':
            self.qsl2.setCurrentIndex(3)
        elif self.F16WORKtype_ui.activeType_comboBox.currentText() == '混合激活':
            self.qsl2.setCurrentIndex(4)
        elif self.F16WORKtype_ui.activeType_comboBox.currentText() == 'I/O激活':
            self.qsl2.setCurrentIndex(5)
    # 16打开工作模式设置页面

    def open_F16WORKtype_dialog(self):
        self.F16WORKtype_dialog.setWindowTitle('工作模式设置')
        self.F16WORKtype_dialog.setWindowModality(Qt.WindowModal)
        self.F16WORKtype_dialog.show()
    # 16打开中心服务设置页面

    def open_F16IPandPORTset_dialog(self):
        self.F16IPandPORTset_dialog.setWindowTitle("中心服务设置")
        self.F16IPandPORTset_dialog.setWindowModality(Qt.WindowModal)
        self.F16IPandPORTset_dialog.show()

    # 16打开短信设置页面
    def open_F16SMSset_dialog(self):
        self.F16SMSset_dialog.setWindowTitle("短信管理")
        self.F16SMSset_dialog.setWindowModality(Qt.WindowModal)
        self.F16SMSset_dialog.show()
    # 16打开串口设置页面

    def open_F16COMset_dialog(self):
        self.F16COMset_dialog.setWindowTitle("串口设置")
        self.F16COMset_dialog.setWindowModality(Qt.WindowModal)
        self.F16COMset_dialog.show()
    # 14(16)-D打开自定义帧设置页

    def open_Frame_dialog(self):
        self.Frame_dialog.setWindowTitle("自定义帧设置")
        self.Frame_dialog.setWindowModality(Qt.WindowModal)
        self.Frame_dialog.show()

    # 14(16)-D打开工作模式设置页
    def open_WORKmodel_dialog(self):
        self.WORKmodel_dialog.setWindowTitle("工作模式设置")
        self.WORKmodel_dialog.setWindowModality(Qt.WindowModal)
        self.WORKmodel_dialog.show()

    # 14(16)-D打开串口设置页
    def open_COMset_dialog(self):
        self.COMset_dialog.setWindowTitle("串口设置")
        self.COMset_dialog.setWindowModality(Qt.WindowModal)
        self.COMset_dialog.show()

    # 14(16)-D弹窗设置中心ip和端口

    def open_IPandPORT_dialog(self):
        #  u=Ui_Dialog()
        #  u.setupUi(self.di)
        # 设置窗口图标
      #   icon = QIcon()
      #  icon.addPixmap(QtGui.QPixmap("DTU.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
       # self.di.setWindowIcon(icon)
       # self.di.setWindowModality(Qt.ApplicationModal)
      #  self.di.setWindowFlags(Qt.WindowTitleHint|Qt.WindowCloseButtonHint|Qt.WindowStaysOnTopHint)
        # self.di.setWindowFlags(Qt.ToolTip)
       # self.di.setWindowFlags(Qt.WindowTitleHint)

        # self.di.setWindowFlag(Qt.WindowStaysOnTopHint)
        self.IPandPORT_dialog.setWindowTitle("企业中心IP和端口设置")
        self.IPandPORT_dialog.setWindowModality(Qt.WindowModal)
        self.IPandPORT_dialog.show()
       # self.di.show()
        # self.di.exec_()
        # self.di.show()

    # 通过索引切换显示的界面(选择DTU型号进行配置)
    def F2X14_16_D_panel(self):
        self.log_textEdit.append(
            "<font color='mediumblue'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;====F2x14(16)-D====\n</font>")

        self.qsl.setCurrentIndex(0)
        self.F2X16_pushButton.setEnabled(True)
        self.F2X14_16_D_pushButton.setEnabled(False)
        self.F2X14_16_D_pushButton.setStyleSheet("color: rgb(170, 0, 255);")
        self.F2X16_pushButton.setStyleSheet("color: black;")

    def F2X16_panel(self):
        self.log_textEdit.append(
            "<font color='mediumblue'>&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;=======F2x16=======\n</font>")

        self.qsl.setCurrentIndex(1)
        self.F2X16_pushButton.setEnabled(False)
        self.F2X14_16_D_pushButton.setEnabled(True)
        self.F2X14_16_D_pushButton.setStyleSheet("color: black;")
        self.F2X16_pushButton.setStyleSheet("color: rgb(170, 0, 255);")

    # 窗口置顶

    def setTOP(self):
        if self.TOP_checkBox.isChecked():
            self.hide()
            self.setWindowFlags(Qt.WindowStaysOnTopHint)
            self.show()
        else:
            self.hide()
            self.setWindowFlags(Qt.Widget)
            self.show()

    # 串口检测
    def port_check(self):

        self.comDetection_pushButton.setEnabled(False)

        port_list = list(list_ports.comports())
        port_dic = {}
        now_port = ''
        if self.ser.isOpen():  # 点击检测按钮时先判断串口是否已经打开
            self.close_port()
            now_port = self.COM_Box.currentText()
        self.COM_Box.clear()
        i = 0
        for port in port_list:
            port_dic[port[0]] = i
            i += 1
            self.COM_Box.addItem(port[0])
        # print(port_dic)
        if now_port in port_dic.keys():
            self.COM_Box.setCurrentIndex(port_dic.get(now_port))
            self.open_port()
            self.comDetection_pushButton.setEnabled(False)

        # 开启线程，线程结束时发出信号，触发把串口检测按钮设为可用的函数
        self.showthread = COMcheck_state_thread()
        self.showthread.signal.connect(
            lambda: self.comDetection_pushButton.setEnabled(True))
        self.showthread.start()

    # 当选中的串口(包括波特率校验位停止位等参数)改变时，关闭当前串口，打开重新选中的串口
    def port_changed(self):
        if self.ser.isOpen():
            self.close_port()
            self.open_port()
    # 打开串口

    def open_port(self):
        self.ser.port = self.COM_Box.currentText()
        self.ser.baudrate = int(self.baudrate_comboBox.currentText())
        self.ser.bytesize = int(self.Databits_comboBox.currentText())

        self.ser.stopbits = int(self.Stopbits_comboBox.currentText())
        self.ser.parity = self.parity_comboBox.currentText()
        self.ser.timeout = 0
        try:
            self.ser.open()
            # 打开串口后将串口相关按钮置灰
          #  self.comDetection_pushButton.setEnabled(False)
          #  self.COM_Box.setEnabled(False)
          #   self.baudrate_comboBox.setEnabled(False)
          #   self.Databits_comboBox.setEnabled(False)
          #   self.parity_comboBox.setEnabled(False)
          #   self.Stopbits_comboBox.setEnabled(False)
            self.close_pushButton.setEnabled(True)
            self.open_pushButton.setEnabled(False)
            # 打开串口后将相关控件重新启用
            self.send_pushButton.setEnabled(True)  # 重新开启发送按钮
            self.groupBox_5.setEnabled(True)  # 重新开启DTU设置页
           # print(self.ser)
        except BaseException:
            QMessageBox.critical(self, "Port Error", "此串口不能被打开！串口被占用或参数错误！")
            return None
        self.show_timer.start(10)
    # 关闭串口

    def close_port(self):
        self.show_timer.stop()
        self.send_timer.stop()
        try:
            self.ser.close()
            # 串口关闭后重新开放相关按钮
            self.comDetection_pushButton.setEnabled(True)
            self.COM_Box.setEnabled(True)
            self.baudrate_comboBox.setEnabled(True)
            self.Databits_comboBox.setEnabled(True)
            self.parity_comboBox.setEnabled(True)
            self.Stopbits_comboBox.setEnabled(True)
            self.open_pushButton.setEnabled(True)
            self.send_pushButton.setEnabled(False)  # 关闭串口后再次将发送按钮设置不可用
            self.send_pushButton.setText('发送')  # 当定时发送时关闭串口后，将按钮恢复成“发送”
            self.close_pushButton.setEnabled(False)  # 关闭串口后将关闭按钮设为不可用
            self.groupBox_5.setEnabled(False)  # 关闭串口后DTU设置页设为不可用
        except BaseException:
            pass
    # 接收数据显示到窗口

    def show_Data(self):
        try:
            num = self.ser.inWaiting()
            data = self.ser.readline()
        except BaseException:
            self.close_port()
            return None
        if num > 0:
            # 每次显示数据时先将光标置到尾部
            self.receive_textEdit.moveCursor(QTextCursor.End)
            # hex显示
            if self.HEXShow_checkBox.checkState():
                out_s = ''
                for i in range(0, len(data)):
                    out_s = out_s + '{:02X}'.format(data[i]) + ' '
                self.receive_textEdit.insertPlainText(out_s)
                #self.receive_textEdit.append(out_s)
            else:
                self.receive_textEdit.insertPlainText(
                    data.decode('gbk', 'ignore'))
                #self.receive_textEdit.append(data.decode('gbk', 'ignore'))
            # 统计接收的数量
            self.data_num_received += len(data)
            self.received_label.setText("接收：" + str(self.data_num_received))
            # 再次将光标置于底部
            self.receive_textEdit.moveCursor(QTextCursor.End)
        else:
            pass
    # 发送数据

    def send_Data(self):
        d = self.textEdit.toPlainText()
        try:
            # hex发送
            if self.HEXsend_checkBox.isChecked():
                d = d.strip()
                send_list = []
                while d != '':
                    try:
                        num = int(d[0:2], 16)
                    except ValueError:
                        QMessageBox.critical(
                            self, 'Wrong Data', '请输入十六进制数据,以空格分开!')
                        return None
                    d = d[2:].strip()
                    send_list.append(num)
                d = bytes(send_list)
                self.ser.write(d)
            else:
                if self.hh_checkBox.isChecked():
                    self.ser.write((d + '\r\n').encode(encoding='GBK'))

                else:
                    self.ser.write(d.encode(encoding='GBK'))
            # 统计发送数量
            self.data_num_sended += len(d)
            self.send_label.setText("发送：" + str(self.data_num_sended))
        except BaseException:
            QMessageBox.critical(
                self, "Port Error", "串口被拔出或参数错误！请先检查好再重新打开串口！")
            self.close_port()
    # 清除接收

    def clear_received(self):
        self.receive_textEdit.clear()
    # 清除日志

    def clear_log(self):
        self.log_textEdit.clear()

    # 计数复位
    def num_reset(self):
        self.received_label.setText("接收：0")
        self.send_label.setText("发送：0")
        self.data_num_received = 0
        self.data_num_sended = 0
    # 发送按钮状态(开启定时发送时，按钮变成“停止”，启动定时发送的定时器，若未开启定时发送则正常发送)

    def send_PushButton_state(self):
        if self.flag:
            if self.time_checkBox.isChecked():
                self.send_time = int(self.time_lineEdit.text())
                print(self.time_lineEdit.text())
                self.send_timer.start(self.send_time)
                self.send_pushButton.setText('停止')
                self.flag = False

            else:
                self.send_timer.stop()
                self.send_Data()
        else:
            self.send_timer.stop()
            self.send_pushButton.setText('发送')
            self.flag = True
    # 定时发送选框状态，取消勾选时停止定时发送，并将“停止”重置为“发送”，flag重置为True

    def time_checkBox_state(self):
        if self.time_checkBox.isChecked():
            self.time_lineEdit.setEnabled(False)
        else:
            self.time_lineEdit.setEnabled(True)
            self.send_pushButton.setText('发送')
            self.send_timer.stop()
            self.flag = True
    # 如果按HEX发送时，添加换行不可用

    def HEXsend_checkBox_state(self):
        if self.HEXsend_checkBox.isChecked():
            self.hh_checkBox.setEnabled(False)
            self.hh_checkBox.setChecked(False)
        else:
            self.hh_checkBox.setEnabled(True)

    # 显示log日志
    def show_log(self, test_log):
        self.log_textEdit.moveCursor(QTextCursor.End)
        self.log_textEdit.insertPlainText(test_log)
        self.log_textEdit.moveCursor(QTextCursor.End)

    # 保存数据
    def save_data(self):
        receive_data = self.receive_textEdit.toPlainText()
        LOG = self.log_textEdit.toPlainText()
        t = datetime.strftime(datetime.now(), '%Y-%m-%d_%H-%M-%S')
        received_path = "SAVE_RECEIVED" + t + ".txt"
        log_path = "SAVE_LOG" + t + ".txt"
        with open(received_path, "a+", encoding='utf-8') as f:
            f.write(receive_data)
        with open(log_path, "a+", encoding="utf-8") as f:
            f.write(LOG)
        QMessageBox.information(self, "提示", "接收数据和日志已保存")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    w = win()
    # 设置窗口图标
  #  icon = QIcon()
  #  icon.addPixmap(
        #QtGui.QPixmap("DTU.ico"),
       # QtGui.QIcon.Normal,
       # QtGui.QIcon.Off)
    w.setWindowIcon(QtGui.QIcon(':/DTU.ico'))

    w.show()
    sys.exit(app.exec_())
