# -*- coding: utf-8 -*-
# @Time    : 10/23/2019 5:36 PM
# @Author  : HR
# @File    : mainwindow.py

import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtSql import (QSqlDatabase, QSqlQuery, QSqlTableModel)
from PyQt5.QtCore import (QFile, QVariant, Qt)
from PyQt5.QtWidgets import (QApplication, QDialog, QDialogButtonBox, QMenu,
                             QMessageBox, QTableView, QVBoxLayout)
from PyQt5.QtGui import QFontDatabase, QFont
from PyQt5.QtWidgets import QPushButton
import hashlib
from storeUi.store import Ui_MainWindow
from PyQt5.QtCore import QTimer
from MyDataBase import StoreMysql
import xlwt
import win32api
import win32print
import sys
import datetime


# import DatabaseModel


class MainWindow(QtWidgets.QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent)
        self.setupUi(self)
        # self.stackedWidget.setCurrentIndex(0)

        self.drive_number.hide()
        self.label_30.hide()

        self.button_connect()

        self.user_info = StoreMysql().get_userinfo()
        self.userType = ""
        self.current_user_id = 0
        self.current_user_name = "cbr"

        self.welcomeUser.setText("")

        self.data = StoreMysql().get_devices_info()

        self.pay = 0.0

        self.status_dict = {0: 'Error', 1: 'Normal', 2: 'Fixing'}

        # self.horizontalWidget.hide()

        # 拍照片定时器
        self.timer = QTimer(self)  # 初始化一个定时器
        self.timer.timeout.connect(self.auto_update_user_info)
        self.timer.start(1000 * 60 * 5)  # 设置计时间隔并启动
        # self.fixer_fixing_status.addItem()

        self.message_clear = QTimer(self)

        self.message_clear.timeout.connect(self.auto_clear_message)
        self.message_clear.start(1000 * 4)  # 设置计时间隔并启动

    # 计算MD5
    @staticmethod
    def calculate_md5(src):
        m = hashlib.md5()
        m.update(src.encode('UTF-8'))
        return m.hexdigest()

    # 退出登录
    def logout(self):
        self.userType = ""
        self.current_user_id = 0
        self.current_user_name = ""
        self.welcomeUser.setText("")
        self.stackedWidget.setCurrentWidget(self.loginwidget)
        self.record_to_log(self.current_user_name, "退出登录", "退出登录", "退出登录", "成功")

    # 自动更新用户信息表
    def auto_update_user_info(self):
        self.user_info = StoreMysql().get_userinfo()

    # 自动删除提示
    def auto_clear_message(self):
        self.fixer_message.setText("")
        self.query_message.setText("")
        self.ware_message.setText("")
        self.loginmessage.setText("")
        self.loginmessage_2.setText("")
        self.loginmessage_3.setText("")
        self.loginmessage_4.setText("")

    # 登录
    def try_login(self):
        print("准备登陆")
        username = self.username.text()
        password = self.password.text()
        if '' != username or '' != password:
            print(username, password)
            pwd = self.calculate_md5(password)
            print("加密", pwd)
            for info in self.user_info:
                if username == info[1]:
                    print("md5密码：", info[2])
                    if pwd == info[2]:
                        self.loginmessage.setText("密码输入成功")
                        self.userType = info[3]

                        self.current_user_id = info[0]
                        self.current_user_name = info[1]
                        break
                    else:
                        ...
            if self.userType == '':
                self.loginmessage.setText("账号或密码错误")
        else:
            print("请输入账号和密码")
            self.loginmessage.setText('请输入账号和密码')

        self.username.setText("")
        self.password.setText("")

        if self.userType == 'admin':
            self.welcomeUser.setText("欢迎您：Admin:\t{}".format(self.current_user_name))
            self.stackedWidget.setCurrentWidget(self.adminwidget)
        elif self.userType == 'recorder':
            self.welcomeUser.setText("欢迎您：Recorder:\t{}".format(self.current_user_name))
            self.stackedWidget.setCurrentWidget(self.record_drives_widget)
            # self.stackedWidget.setCurrentIndex(1)
        elif self.userType == 'fixer':
            self.welcomeUser.setText("欢迎您：Fixer:\t{}".format(self.current_user_name))
            self.stackedWidget.setCurrentWidget(self.fixerwidget)
        else:
            ...
        # print(username,password)

    # 记录到日志表
    def record_to_log(self, user_name, drive_name, drive_id, opers, status):
        record = "user {} 操作 {} 设备ID:{} {}，设备当前状态：{}".format(user_name, drive_name, drive_id, opers, status)

        status = StoreMysql().record_logs(drive_id, record, self.current_user_id)
        return status

    # 添加设备
    def press_drives_entry_btn(self):
        print("添加货物")
        drives_uuid = self.drive_uuid.text()
        drive_type = self.drive_type.text()
        drive_product = self.drive_product.text()
        drive_name = self.drive_name.text()
        drive_version = self.drive_version.text()
        drive_specification = self.drive_specification.text()
        # TODO 后面解释的时候需要说明 ，设备的情况是根据编号进行唯一确定，不进行后期分配
        # drive_number = int(self.drive_number.text())
        drive_status = 1
        drive_department = "company"
        drive_etype = "0"
        drive_ereason = "0"
        now = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        status = StoreMysql().add_drives2ware(drives_uuid=drives_uuid, drive_name=drive_name, drive_type=drive_type,
                                              drive_status=drive_status, drive_version=drive_version,
                                              drive_specification=drive_specification, drive_product=drive_product,
                                              drive_department=drive_department,
                                              drive_etype=drive_etype, drive_ereason=drive_ereason, now=now)
        if status:
            # user_name, drive_name, drive_id, opers, status
            self.record_to_log(self.current_user_name, drive_name, drives_uuid, "采购录入", "成功")

            self.ware_message.setText('成功添加')
            self.reflash_drive_widget()
        else:
            self.ware_message.setText('添加失败')

    # 修改设备信息
    def press_drives_change_btn(self):
        now_row = self.tableWidget.currentRow()
        print("当前行", now_row)
        # a,b,c,d,e,f

        drives_uuid = self.tableWidget.item(now_row, 0).text()
        drive_name = self.tableWidget.item(now_row, 1).text()
        drive_type = self.tableWidget.item(now_row, 2).text()
        drive_status = self.tableWidget.item(now_row, 3).text()
        drive_version = self.tableWidget.item(now_row, 4).text()
        drive_specification = self.tableWidget.item(now_row, 5).text()
        drive_product = self.tableWidget.item(now_row, 6).text()
        drive_department = self.tableWidget.item(now_row, 7).text()
        drive_etype = self.tableWidget.item(now_row, 8).text()
        drive_ereason = self.tableWidget.item(now_row, 9).text()

        # uuid, name, type, status, version, specification, product, department, etpye, ereason
        status = StoreMysql().update_devices_info(drives_uuid, drive_name, drive_type, drive_status, drive_version,
                                                  drive_specification, drive_product, drive_department, drive_etype,
                                                  drive_ereason)
        if status:
            # user_name, drive_name, drive_id, opers, status
            self.record_to_log(self.current_user_name, drive_name, drives_uuid, "修改设备信息", "成功")
            self.ware_message.setText('成功修改')
            self.reflash_drive_widget()
        else:
            self.record_to_log(self.current_user_name, drive_name, drives_uuid, "修改设备信息", "失败")
            self.ware_message.setText('修改失败')

    # 删除设备
    def press_drives_delete_btn(self):
        now_row = self.tableWidget.currentRow()
        print("当前行", now_row)
        drives_uuid = self.tableWidget.item(now_row, 0).text()
        drive_name = self.tableWidget.item(now_row, 1).text()
        status = StoreMysql().delete_devices_info(drives_uuid)
        if status:
            # user_name, drive_name, drive_id, opers, status
            self.record_to_log(self.current_user_name, drive_name, drives_uuid, "删除设备", "成功")
            self.ware_message.setText('删除成功')
            self.reflash_drive_widget()
        else:
            self.record_to_log(self.current_user_name, drive_name, drives_uuid, "尝试删除设备", "失败")
            self.ware_message.setText('删除失败')
        return True

    # 查询设备
    def press_drives_query_btn(self):
        self.reflash_drive_widget()
        name = self.drive_name.text()
        flag = 0
        if name != '':
            print('查询')
            data = StoreMysql().get_devices_info()
            for x, info in enumerate(data):
                print(x, info)
                for y, cell in enumerate(info):
                    print(y, cell)
                    if name == cell:
                        self.tableWidget.selectRow(x)
                        flag = 1
                        break
                    else:
                        pass
        else:
            ...
        if flag:
            self.ware_message.setText("查找成功")
        else:
            self.ware_message.setText("查找失败")

    # 更新设备信息
    def reflash_drive_widget(self):
        _translate = QtCore.QCoreApplication.translate
        # self.tableWidget.verticalHeader().setVisible(False)
        item = self.tableWidget.horizontalHeaderItem(5)
        # item = self.tableWidget.item(0, 0)

        self.data = StoreMysql().get_devices_info()

        self.tableWidget.setRowCount(len(self.data))
        for x, info in enumerate(self.data):
            print(x, info)
            for y, cell in enumerate(info):
                print(y, cell)
                if y < 10:
                    try:
                        item = QtWidgets.QTableWidgetItem(str(cell))
                        self.tableWidget.setItem(x, y, item)
                        # item = self.tableWidget.item(x, y)
                        # item.setText(_translate("MainWindow",str(cell)))
                    except:
                        pass
                else:
                    pass

    # 修改日志信息
    def press_change_logs_btn(self):
        now_row = self.log_widget.currentRow()

        print("当前行", now_row)
        log_id = self.log_widget.item(now_row, 0).text()
        # ppp=self.tableWidget.item
        record = self.log_widget.item(now_row, 1).text()
        user_id = self.log_widget.item(now_row, 2).text()
        user_name = self.log_widget.item(now_row, 3).text()
        drive_name = self.log_widget.item(now_row, 4).text()
        drive_id = self.log_widget.item(now_row, 5).text()
        version = self.log_widget.item(now_row, 6).text()

        # 修改数据库
        status = StoreMysql().update_admin_log_info(log_id, record, user_id, user_name, drive_name, drive_id, version)
        if status:
            self.ware_message.setText('成功修改')
            self.refresh_logs_widget()
        else:
            self.ware_message.setText('修改失败')

    # 更新日志
    def refresh_logs_widget(self):
        self.data = StoreMysql().get_logs_records()

        self.log_widget.setRowCount(len(self.data))
        for x, info in enumerate(self.data):
            print(x, info)
            for y, cell in enumerate(info):
                print(y, cell)
                if y < 7:
                    try:
                        item = QtWidgets.QTableWidgetItem(str(cell))
                        self.log_widget.setItem(x, y, item)
                    except:
                        pass
                else:
                    pass

    # 查询设备
    def press_search_drives_btn(self):
        print('搜索商品信息')
        # self.count.setText()
        drives_id = self.fixer_search_drives.text()
        if drives_id != '':
            try:
                data = StoreMysql().search_devices(drives_id=drives_id)[0]
                if data:
                    self.fixer_drive_name.setText(data[1])
                    self.fixer_drive_version.setText(data[4])
                    self.fixer_drive_id.setText(data[0])
                    self.fixer_drive_spec.setText(data[5])
                    self.fixer_drive_status.setText(self.status_dict[data[3]])
                    self.fixer_drive_etpye.setText(data[8])
                    self.fixer_drive_ereason.setText(data[9])
                    self.fixer_drive_department.setText(data[7])
                    # todo 添加信息到 日志表

                    self.fixer_fixing_status.setCurrentIndex(data[3])

                    record = "user {} 接入 {} 设备ID:{} 进行维修，设备当前状态：{}".format(self.current_user_name, data[1], data[0],
                                                                           self.status_dict[data[3]])
                    # user_name, drive_name, drive_id, opers, status
                    status = self.record_to_log(self.current_user_name, data[1], data[0], "进行维修",
                                                self.status_dict[data[3]])
                    if status:
                        self.fixer_message.setText("查找设备成功")
                else:
                    self.fixer_message.setText("找不到该设备")
            except:
                self.fixer_message.setText("找不到该设备")
        else:
            self.fixer_message.setText("请输入设备ID")

    # 维修人员提交
    def press_fixer_commit_btn(self):
        fixer_drive_ereason = self.fixer_drive_ereason.toPlainText()
        if fixer_drive_ereason == "":
            return self.fixer_message.setText("更新设备状态失败")
        else:
            ...
        if self.fixer_fixing_status.currentIndex() == 1:
            self.fixer_driver_etype_ensure.setCurrentIndex(4)
        current_drives_id = self.fixer_drive_id.text()
        current_drives_name = self.fixer_drive_name.text()
        current_drives_status = self.fixer_fixing_status.currentIndex()
        fixer_driver_etype_ensure = self.fixer_driver_etype_ensure.currentText()

        status = StoreMysql().update_drives_table(current_drives_id, fixer_driver_etype_ensure, fixer_drive_ereason,
                                                  current_drives_status)
        if status:
            self.fixer_drive_status.setText(self.status_dict[self.fixer_fixing_status.currentIndex()])
            self.fixer_drive_etpye.setText(self.fixer_driver_etype_ensure.currentText())
            # user_name, drive_name, drive_id, opers, status
            self.record_to_log(self.current_user_name, current_drives_name, current_drives_id, "维修更新设备状态", "成功")
            self.fixer_message.setText("更新设备状态成功")
        else:
            self.record_to_log(self.current_user_name, current_drives_name, current_drives_id, "维修更新设备状态", "失败")
            self.fixer_message.setText("更新设备状态失败")

    # 管理用户
    def manager_user(self):
        self.adminstacked.setCurrentWidget(self.manager_man)

    # 注册用户
    def registered_user(self):
        username = self.resigner_name.text()
        password_1 = self.resigner_password_1.text()
        password_2 = self.resigner_password_2.text()
        if (username != '') and (password_1 != '') and (password_2 != '') and password_1 == password_2:
            user_type = self.resign_type.currentText()
            pwd = self.calculate_md5(password_2)
            print("加密", pwd)

            status = StoreMysql().registered_user_to_database(username, pwd, user_type)
            if status:
                self.resigner_name.clear()
                self.resigner_password_1.clear()
                self.resigner_password_2.clear()
                self.loginmessage_2.setText('成功添加')
            else:
                self.resigner_name.clear()
                self.resigner_password_1.clear()
                self.resigner_password_2.clear()
                self.loginmessage_2.setText('添加失败')
        else:
            self.loginmessage_2.setText("错误")

    # 删除用户
    def delete_user(self):
        username = self.delete_username.text()
        if username != '':
            status = StoreMysql().delete_user(username)
            if status:
                self.delete_username.clear()
                self.loginmessage_3.setText('成功删除')
                self.reflash_drive_widget()
            else:
                self.delete_username.clear()

                self.loginmessage_3.setText('删除失败')
        else:
            self.delete_username.clear()
            self.loginmessage_3.setText('输入用户名')

    # 修改用角色
    def change_user_role(self):
        username = self.change_username.text()
        usertype = self.change_type.currentText()
        if username != '':
            statu = StoreMysql().change_user(usertype, username)
            if statu:
                self.change_username.clear()
                self.loginmessage_4.setText('成功修改')
                self.reflash_drive_widget()
            else:
                self.change_username.clear()
                self.loginmessage_4.setText('修改失败')
        else:
            self.change_username.clear()
            self.loginmessage_4.setText('输入用户名')

    # 按下设备录入按钮 - 管理员界面
    def press_drives_record_btn(self):
        self.stackedWidget.setCurrentWidget(self.record_drives_widget)

        # self.search_and_add = QtWidgets.QPushButton(self.horizontalLayoutWidget_8)
        self.btn = QtWidgets.QPushButton(self)

        self.btn.setText("返回管理页面")

        self.btn.setGeometry(QtCore.QRect(840, 620, 121, 41))
        self.btn.setObjectName("btn")
        self.btn.setStyleSheet("""background-color:rgb(255, 255, 255);
border-top-right-radius: 15px;
border-bottom-left-radius:15px;
border: 2px solid #999999;""")
        self.btn.clicked.connect(self.go_back_admin_page)
        # self.resign.clicked.connect(self.resignMan)
        self.btn.show()

    # 按下设备修复按钮 - 管理员界面
    def press_drives_fix_btn(self):
        self.stackedWidget.setCurrentWidget(self.fixerwidget)

        # self.search_and_add = QtWidgets.QPushButton(self.horizontalLayoutWidget_8)
        self.btn = QtWidgets.QPushButton(self)

        self.btn.setText("返回管理页面")

        self.btn.setGeometry(QtCore.QRect(840, 620, 121, 41))
        self.btn.setObjectName("btn")
        self.btn.setStyleSheet("""background-color:rgb(255, 255, 255);
        border-top-right-radius: 15px;
        border-bottom-left-radius:15px;
        border: 2px solid #999999;""")
        self.btn.clicked.connect(self.go_back_admin_page)
        # self.resign.clicked.connect(self.resignMan)
        self.btn.show()

    # 按下返回管理员界面- 管理员界面
    def go_back_admin_page(self):
        self.stackedWidget.setCurrentWidget(self.adminwidget)
        self.btn.hide()

    # 按下设备分析按钮 管理员界面
    def press_drives_analysis_btn(self):
        self.stackedWidget.setCurrentWidget(self.analysiswidget)

        # self.search_and_add = QtWidgets.QPushButton(self.horizontalLayoutWidget_8)
        self.btn = QtWidgets.QPushButton(self)

        self.btn.setText("返回管理页面")

        self.btn.setGeometry(QtCore.QRect(845, 670, 121, 41))
        self.btn.setObjectName("btn")
        self.btn.setStyleSheet("""background-color:rgb(255, 255, 255);
        border-top-right-radius: 15px;
        border-bottom-left-radius:15px;
        border: 2px solid #999999;""")
        self.btn.clicked.connect(self.go_back_admin_page)
        # self.resign.clicked.connect(self.resignMan)
        self.btn.show()

    # 按下修改日志 管理员界面
    def press_change_logs(self):
        self.adminstacked.setCurrentWidget(self.change_log_widget)
        self.refresh_logs_widget()
        # profitreflash

    # 查询正常设备
    def press_query_drive_good_btn(self):

        mydata = StoreMysql().get_column_name('drives')
        self.execltableWidget.setColumnCount(len(mydata))
        for index, i in enumerate(mydata):
            print(index)
            print(i)
            item = QtWidgets.QTableWidgetItem()
            item.setText(i[0])
            self.execltableWidget.setHorizontalHeaderItem(index, item)

        data = StoreMysql().get_drive_normal_info()
        self.execltableWidget.setRowCount(len(data))
        for x, info in enumerate(data):
            print(x, info)
            for y, cell in enumerate(info):
                print(y, cell)
                if y < len(mydata):
                    try:
                        item = QtWidgets.QTableWidgetItem(str(cell))
                        self.execltableWidget.setItem(x, y, item)
                    except:
                        pass
                else:
                    pass
        self.query_message.setText("查询成功")

    # 查询损坏设备
    def press_query_drive_bad_btn(self):

        mydata = StoreMysql().get_column_name('drives')
        self.execltableWidget.setColumnCount(len(mydata))
        for index, i in enumerate(mydata):
            print(index)
            print(i)
            item = QtWidgets.QTableWidgetItem()
            item.setText(i[0])
            self.execltableWidget.setHorizontalHeaderItem(index, item)

        data = StoreMysql().get_drive_bad_info()
        self.execltableWidget.setRowCount(len(data))
        for x, info in enumerate(data):
            print(x, info)
            for y, cell in enumerate(info):
                print(y, cell)
                if y < len(mydata):
                    try:
                        item = QtWidgets.QTableWidgetItem(str(cell))
                        self.execltableWidget.setItem(x, y, item)
                    except:
                        pass
                else:
                    pass

        self.query_message.setText("查询成功")

    # 查询未修设备
    def press_query_drive_not_fix_btn(self):
        mydata = StoreMysql().get_column_name('drives')
        self.execltableWidget.setColumnCount(len(mydata))
        for index, i in enumerate(mydata):
            print(index)
            print(i)
            item = QtWidgets.QTableWidgetItem()
            item.setText(i[0])
            self.execltableWidget.setHorizontalHeaderItem(index, item)

        data = StoreMysql().get_drive_not_fix_info()

        self.execltableWidget.setRowCount(len(data))
        for x, info in enumerate(data):
            print(x, info)
            for y, cell in enumerate(info):
                print(y, cell)
                if y < len(mydata):
                    try:
                        item = QtWidgets.QTableWidgetItem(str(cell))
                        self.execltableWidget.setItem(x, y, item)
                    except:
                        pass
                else:
                    pass
        self.query_message.setText("查询成功")

    # 查询正在修理设备
    def press_query_drive_fixing_btn(self):
        mydata = StoreMysql().get_column_name('drives')
        self.execltableWidget.setColumnCount(len(mydata))
        for index, i in enumerate(mydata):
            print(index)
            print(i)
            item = QtWidgets.QTableWidgetItem()
            item.setText(i[0])
            self.execltableWidget.setHorizontalHeaderItem(index, item)

        data = StoreMysql().get_drive_fixing_info()

        self.execltableWidget.setRowCount(len(data))
        for x, info in enumerate(data):
            print(x, info)
            for y, cell in enumerate(info):
                print(y, cell)
                if y < len(mydata):
                    try:
                        item = QtWidgets.QTableWidgetItem(str(cell))
                        self.execltableWidget.setItem(x, y, item)
                    except:
                        pass
                else:
                    pass
        self.query_message.setText("查询成功")

    # 查询前缀厂商设备
    def press_query_drive_by_prefix_id_btn(self):

        tmp = self.query_drive_prefix.text()
        if tmp == "":
            self.query_message.setText("请输入前缀")
            return False
        else:
            ...

        mydata = StoreMysql().get_column_name('drives')
        self.execltableWidget.setColumnCount(len(mydata))
        for index, i in enumerate(mydata):
            print(index)
            print(i)
            item = QtWidgets.QTableWidgetItem()
            item.setText(i[0])
            self.execltableWidget.setHorizontalHeaderItem(index, item)

        data = StoreMysql().get_drive_info_by_prefix_info(tmp)

        self.execltableWidget.setRowCount(len(data))
        for x, info in enumerate(data):
            print(x, info)
            for y, cell in enumerate(info):
                print(y, cell)
                if y < len(mydata):
                    try:
                        item = QtWidgets.QTableWidgetItem(str(cell))
                        self.execltableWidget.setItem(x, y, item)
                    except:
                        pass
                else:
                    pass

        self.execltableWidget.sortByColumn(3, Qt.AscendingOrder)

    # 时间段内查询采购设备
    def press_query_drive_by_time_btn(self):

        start_t = self.start_date.text()
        end_t = self.end_date.text()

        if start_t == end_t:
            self.query_message.setText("请选择不同时间段")
            return False
        else:
            ...

        mydata = StoreMysql().get_column_name('drives')
        self.execltableWidget.setColumnCount(len(mydata))
        for index, i in enumerate(mydata):
            print(index)
            print(i)
            item = QtWidgets.QTableWidgetItem()
            item.setText(i[0])
            self.execltableWidget.setHorizontalHeaderItem(index, item)

        data = StoreMysql().get_drive_info_by_time_info(start_t, end_t)

        self.execltableWidget.setRowCount(len(data))
        for x, info in enumerate(data):
            print(x, info)
            for y, cell in enumerate(info):
                print(y, cell)
                if y < len(mydata):
                    try:
                        item = QtWidgets.QTableWidgetItem(str(cell))
                        self.execltableWidget.setItem(x, y, item)
                    except:
                        pass
                else:
                    pass

    # 链接所有按钮
    def button_connect(self):
        self.login.clicked.connect(self.try_login)
        self.logoutButton.clicked.connect(self.logout)

        self.drives_entry.clicked.connect(self.press_drives_entry_btn)
        self.drives_change.clicked.connect(self.press_drives_change_btn)
        self.drives_delete.clicked.connect(self.press_drives_delete_btn)
        self.drives_query.clicked.connect(self.press_drives_query_btn)

        self.fixer_search_drives_and_add.clicked.connect(self.press_search_drives_btn)
        self.fixer_commit.clicked.connect(self.press_fixer_commit_btn)

        self.admin_change_log.clicked.connect(self.press_change_logs_btn)
        self.admin_registered.clicked.connect(self.registered_user)
        self.admin_delete_user.clicked.connect(self.delete_user)
        self.admin_change_user.clicked.connect(self.change_user_role)

        self.admin_change_logs_page.clicked.connect(self.press_change_logs)
        self.admin_manager_user_page.clicked.connect(self.manager_user)
        self.admin_record_drives_page.clicked.connect(self.press_drives_record_btn)
        self.admin_fix_drives_page.clicked.connect(self.press_drives_fix_btn)
        self.admin_manager_device_page.clicked.connect(self.press_drives_analysis_btn)

        # self.changestoresattributes.clicked.connect(self.press_drives_record_btn)
        self.buttonexportexecl.clicked.connect(self.exportExecl)
        self.buttonprintexecl.clicked.connect(self.printExecl)

        self.query_drive_bad.clicked.connect(self.press_query_drive_bad_btn)
        self.query_drive_not_fix.clicked.connect(self.press_query_drive_not_fix_btn)
        self.query_drive_fixing.clicked.connect(self.press_query_drive_fixing_btn)
        self.query_drive_good.clicked.connect(self.press_query_drive_good_btn)
        self.query_drive_by_prefix_id.clicked.connect(self.press_query_drive_by_prefix_id_btn)
        self.query_drive_by_time.clicked.connect(self.press_query_drive_by_time_btn)

        # self.queryRemainLessThan10Button.clicked.connect(self.queryRemainLessThan10)
        # self.querySuggestedPromotionalItemsButton.clicked.connect(self.querySuggestedPromotionalItems)

    # DescendingOrder
    def exportExecl(self):
        try:
            print("准备导出")
            filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)")
            print(filename)
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet("sheet1", cell_overwrite_ok=True)
            self.add2execl(sheet)
            wbk.save(filename[0])
            self.record_to_log(self.current_user_name, "导出操作", "导出操作", "导出操作", "成功")
        except:
            self.record_to_log(self.current_user_name, "导出操作", "导出操作", "导出操作", "失败")
            self.label_29.setText("导出失败")

    def printExecl(self):
        print("准备打印")
        # filename = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File', '', ".xls(*.xls)")
        # print(filename)
        try:
            wbk = xlwt.Workbook()
            sheet = wbk.add_sheet("sheet1", cell_overwrite_ok=True)
            self.add2execl(sheet)
            wbk.save('printExecl.xls')
            open('printExecl.xls', "r")
            win32api.ShellExecute(
                0,
                "print",
                'printExecl.xls',
                '/d:"%s"' % win32print.GetDefaultPrinter(),
                ".",
                0
            )
            # user_name, drive_name, drive_id, opers, status
            self.record_to_log(self.current_user_name, "打印操作", "打印操作", "打印操作", "成功")
        except:
            self.record_to_log(self.current_user_name, "打印操作", "打印操作", "打印操作", "失败")
            self.label_29.setText("打印失败")

    def add2execl(self, sheet):
        # 添加头
        for i in range(self.execltableWidget.columnCount()):
            try:
                header = self.execltableWidget.horizontalHeaderItem(i).text()
                sheet.write(0, i, header)
            except AttributeError:
                pass
        # 添加表信息
        for currentColumn in range(self.execltableWidget.columnCount()):
            for currentRow in range(self.execltableWidget.rowCount()):
                try:
                    text = str(self.execltableWidget.item(currentRow, currentColumn).text())
                    sheet.write(currentRow + 1, currentColumn, text)
                except AttributeError:
                    pass


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec_())
