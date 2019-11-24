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

        self.buttonConnect()

        self.user_info = StoreMysql().get_userinfo()
        self.userType = ""
        self.current_user_id = 0
        self.current_user_name = "cbr"

        self.my_view()

        self.data = StoreMysql().get_devices_info()

        self.pay = 0.0

        self.status_dict = {0: 'Error', 1: 'Normal', 2: 'Fixing'}

        # self.fixer_fixing_status.addItem()

    @staticmethod
    def calculate_md5(src):
        m = hashlib.md5()
        m.update(src.encode('UTF-8'))
        return m.hexdigest()

    # 退出登录
    def logout(self):
        self.stackedWidget.setCurrentWidget(self.loginwidget)

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
                if username in info:
                    print("md5密码：", info[2])
                    if pwd == info[2]:
                        # print('密码输入正常')
                        self.loginmessage.setText("密码输入正常")
                        self.userType = info[3]
                        self.welcomeUser.setText("欢迎您：{}".format(info[1]))
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

        if self.userType == 'admin':
            self.stackedWidget.setCurrentWidget(self.adminwidget)
        elif self.userType == 'sale':
            self.stackedWidget.setCurrentWidget(self.salewidget)
            # self.stackedWidget.setCurrentIndex(1)
        elif self.userType == 'analyst':
            self.stackedWidget.setCurrentWidget(self.analysiswidget)
        elif self.userType == 'ware':
            self.stackedWidget.setCurrentWidget(self.record_drives_widget)
        else:
            ...
        # print(username,password)

    # 添加设备
    def press_drives_entry_btn(self):
        print("添加货物")
        drives_uuid = self.drive_uuid.text()
        drive_type = self.drive_type.text()
        drive_product = self.drive_product.text()
        drive_name = self.drive_name.text()
        drive_version = self.drive_version.text()
        drive_specification = self.drive_specification.text()
        drive_number = int(self.drive_number.text())
        drive_status = 1
        drive_department = "company"
        drive_etype = "0"
        drive_ereason = "0"

        status = StoreMysql().add_drives2ware(drives_uuid=drives_uuid, drive_name=drive_name, drive_type=drive_type,
                                              drive_status=drive_status, drive_version=drive_version,
                                              drive_specification=drive_specification, drive_product=drive_product,
                                              drive_department=drive_department,
                                              drive_etype=drive_etype, drive_ereason=drive_ereason)
        if status:
            self.ware_message.setText('成功添加')
            self.my_view()
            # self.statusbar.setStatusTip("成功添加")
        else:
            self.ware_message.setText('添加失败')
            # self.statusbar.setStatusTip("添加失败")

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
            self.ware_message.setText('成功修改')
            self.my_view()
        else:
            self.ware_message.setText('修改失败')

    def press_drives_delete_btn(self):
        now_row = self.tableWidget.currentRow()
        print("当前行", now_row)
        drives_uuid = self.tableWidget.item(now_row, 0).text()
        status = StoreMysql().delete_devices_info(drives_uuid)
        if status:
            self.ware_message.setText('删除成功')
            self.my_view()
        else:
            self.ware_message.setText('删除失败')
        return True

    def press_drives_query_btn(self):
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

    def my_view(self):
        _translate = QtCore.QCoreApplication.translate
        # self.tableWidget.verticalHeader().setVisible(False)
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "进货价格"))
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

        # old_id = self.data[now_row][0]
        #
        # print(log_id, record, user_id)
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

    def press_search_drives_btn(self):
        print('搜索商品信息')
        # self.count.setText()
        drives_id = self.fixer_search_drives.text()
        if drives_id != '':
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

                record = "user {} 接入 {} 设备ID:{} 进行维修".format(self.current_user_name, data[1], data[0])

                status = StoreMysql().record_logs(data[0], record, self.current_user_id)
                if status:
                    print("日志记录成功")
            else:
                self.fixer_message.setText("找不到该设备")
        else:
            self.fixer_message.setText("请输入条形码")

    def press_fixer_commit_btn(self):

        # todo 重构所有SQL执行
        current_drives_id = self.fixer_drive_id.text()
        current_drives_status = self.fixer_fixing_status.currentIndex()

        status = StoreMysql().update_drives_table(current_drives_id, current_drives_status)
        if status:
            self.fixer_message.setText("更新设备状态成功")
        else:
            self.fixer_message.setText("更新设备状态失败")
        # self.listWidget.clear()
        # self.barcode.clear()
        # self.price.clear()
        # self.search_barcode.clear()
        # self.need_pay.clear()
        # self.goodsname.clear()
        # self.customername.clear()

    def managerUser(self):
        self.adminstacked.setCurrentWidget(self.manager_man)

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

    def delete_user(self):
        username = self.delete_username.text()
        if username != '':
            status = StoreMysql().delete_user(username)
            if status:
                self.delete_username.clear()
                self.loginmessage_3.setText('成功删除')
                self.my_view()
            else:
                self.delete_username.clear()

                self.loginmessage_3.setText('删除失败')
        else:
            self.delete_username.clear()
            self.loginmessage_3.setText('输入用户名')

    def changeUser(self):
        username = self.change_username.text()
        usertype = self.change_type.currentText()
        if username != '':
            statu = StoreMysql().change_user(usertype, username)
            if statu:
                self.change_username.clear()
                self.loginmessage_4.setText('成功修改')
                self.my_view()
            else:
                self.change_username.clear()
                self.loginmessage_4.setText('修改失败')
        else:
            self.change_username.clear()
            self.loginmessage_4.setText('输入用户名')

    def customerInfo(self):
        self.adminstacked.setCurrentWidget(self.customer)
        data = StoreMysql().get_customerinfo()
        self.customer_table.setRowCount(len(data))
        for x, info in enumerate(data):
            print(x, info)
            for y, cell in enumerate(info):
                print(y, cell)
                if y < 4:
                    try:
                        item = QtWidgets.QTableWidgetItem(str(cell))
                        self.customer_table.setItem(x, y, item)
                    except:
                        pass
                else:
                    pass

    def press_drives_record_btn(self):
        self.stackedWidget.setCurrentWidget(self.record_drives_widget)

        # self.search_and_add = QtWidgets.QPushButton(self.horizontalLayoutWidget_8)
        self.btn = QtWidgets.QPushButton(self)

        self.btn.setText("返回")

        self.btn.setGeometry(QtCore.QRect(840, 620, 121, 41))
        self.btn.setObjectName("btn")
        self.btn.clicked.connect(self.goBack)
        # self.resign.clicked.connect(self.resignMan)
        self.btn.show()

    def goBack(self):
        self.stackedWidget.setCurrentWidget(self.adminwidget)
        self.btn.hide()

    # def changeProfit(self):
    #     self.adminstacked.setCurrentWidget(self.changeProfitwidget)
    #     self.profitreflash()
    # profitreflash

    def press_change_logs(self):
        self.adminstacked.setCurrentWidget(self.change_log_widget)
        self.refresh_logs_widget()
        # profitreflash

    def queryCustomerInfo(self):
        # item = QtWidgets.QTableWidgetItem()
        # item.setText('customer')
        # self.tableWidget.setHorizontalHeaderItem(0, item)
        # item.setText('customername')
        # self.tableWidget.setHorizontalHeaderItem(1, item)
        mydata = StoreMysql().get_column_name('customerinfo')
        self.execltableWidget.setColumnCount(len(mydata))
        for index, i in enumerate(mydata):
            print(index)
            print(i)
            item = QtWidgets.QTableWidgetItem()
            item.setText(i[0])
            self.execltableWidget.setHorizontalHeaderItem(index, item)

        data = StoreMysql().get_customerinfo()
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

    def queryCustomerInfo(self):
        # item = QtWidgets.QTableWidgetItem()
        # item.setText('customer')
        # self.tableWidget.setHorizontalHeaderItem(0, item)
        # item.setText('customername')
        # self.tableWidget.setHorizontalHeaderItem(1, item)
        mydata = StoreMysql().get_column_name('customerinfo')
        self.execltableWidget.setColumnCount(len(mydata))
        for index, i in enumerate(mydata):
            print(index)
            print(i)
            item = QtWidgets.QTableWidgetItem()
            item.setText(i[0])
            self.execltableWidget.setHorizontalHeaderItem(index, item)

        data = StoreMysql().get_customerinfo()
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

    def querySalesInfo(self):
        mydata = StoreMysql().get_column_name('salesinfo')
        self.execltableWidget.setColumnCount(len(mydata))
        for index, i in enumerate(mydata):
            print(index)
            print(i)
            item = QtWidgets.QTableWidgetItem()
            item.setText(i[0])
            self.execltableWidget.setHorizontalHeaderItem(index, item)

        data = StoreMysql().get_logs_records()
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

    def queryWarehouseInfo(self):
        mydata = StoreMysql().get_column_name('warehouse')
        self.execltableWidget.setColumnCount(len(mydata))
        for index, i in enumerate(mydata):
            print(index)
            print(i)
            item = QtWidgets.QTableWidgetItem()
            item.setText(i[0])
            self.execltableWidget.setHorizontalHeaderItem(index, item)

        data = StoreMysql().get_warehouseinfo()
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

    # TODO:需要考虑一下合并同一品牌商品的所有商品
    def queryTop10BankInfo(self):
        # mydata = StoreMysql().get_column_name('salesinfo')
        # self.execltableWidget.setColumnCount(len(mydata))
        # for index, i in enumerate(mydata):
        #     print(index)
        #     print(i)
        #     item = QtWidgets.QTableWidgetItem()
        #     item.setText(i[0])
        #     self.execltableWidget.setHorizontalHeaderItem(index, item)

        data = StoreMysql().get_top10_bank
        self.execltableWidget.setColumnCount(len(data[0]))
        item = QtWidgets.QTableWidgetItem()
        item.setText("商品ID")
        self.execltableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("品牌")
        self.execltableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("品牌最高售出数量")
        self.execltableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("利润")
        self.execltableWidget.setHorizontalHeaderItem(3, item)
        self.execltableWidget.setRowCount(len(data))
        for x, info in enumerate(data):
            print(x, info)
            for y, cell in enumerate(info):
                print(y, cell)
                if y < len(data[0]):
                    try:
                        item = QtWidgets.QTableWidgetItem(str(cell))
                        self.execltableWidget.setItem(x, y, item)
                    except:
                        pass
                else:
                    pass
        # for x, info in enumerate(data):
        #     print(x, info)
        #     for y, cell in enumerate(info):
        #         print(y, cell)
        #         if y < len(data[0]):
        #             try:
        #                 if str(cell) != data[x - 1][1]:
        #                     item = QtWidgets.QTableWidgetItem(str(cell))
        #                     self.execltableWidget.setItem(x, y, item)
        #                 elif str(cell) == data[x - 1][1]:
        #                     try:
        #                         item = QtWidgets.QTableWidgetItem(str(float( info[-1]) + float(data[x - 1][-1])))
        #                         self.execltableWidget.setItem(x, y + 1, item)
        #                         # self.execltableWidget.removeRow(y-1)
        #                     except:
        #                         pass
        #
        #                     # pass
        #             except:
        #                 pass
        #         else:
        #             pass

        # self.execltableWidget.setSortingEnabled()

        self.execltableWidget.sortByColumn(3, Qt.AscendingOrder)

    def queryTop100GoodsInfo(self):
        data = StoreMysql().get_top100_goods()
        self.execltableWidget.setColumnCount(len(data[0]))
        item = QtWidgets.QTableWidgetItem()
        item.setText("商品ID")
        self.execltableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("商品名")
        self.execltableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("品牌")
        self.execltableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("条形码")
        self.execltableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setText("销售数量")
        self.execltableWidget.setHorizontalHeaderItem(4, item)
        self.execltableWidget.setRowCount(len(data))
        for x, info in enumerate(data):
            print(x, info)
            for y, cell in enumerate(info):
                print(y, cell)
                if y < len(data[0]):
                    try:
                        item = QtWidgets.QTableWidgetItem(str(cell))
                        self.execltableWidget.setItem(x, y, item)
                    except:
                        pass
                else:
                    pass

    def queryGoodsDetailInfo(self):
        mydata = StoreMysql().get_column_name('allgoodsinfo')
        self.execltableWidget.setColumnCount(len(mydata))
        for index, i in enumerate(mydata):
            print(index)
            print(i)
            item = QtWidgets.QTableWidgetItem()
            item.setText(i[0])
            self.execltableWidget.setHorizontalHeaderItem(index, item)

        data = StoreMysql().get_goods_detail_info()
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

    def queryRemainLessThan10(self):
        mydata = StoreMysql().get_column_name('saleview')
        self.execltableWidget.setColumnCount(len(mydata))
        for index, i in enumerate(mydata):
            print(index)
            print(i)
            item = QtWidgets.QTableWidgetItem()
            item.setText(i[0])
            self.execltableWidget.setHorizontalHeaderItem(index, item)

        data = StoreMysql().get_remain_less_than_10()
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

    def querySuggestedPromotionalItems(self):
        mydata = StoreMysql().get_column_name('saleview')
        self.execltableWidget.setColumnCount(len(mydata))
        for index, i in enumerate(mydata):
            print(index)
            print(i)
            item = QtWidgets.QTableWidgetItem()
            item.setText(i[0])
            self.execltableWidget.setHorizontalHeaderItem(index, item)

        data = StoreMysql().get_suggested_promotional_items()
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

    def buttonConnect(self):
        self.login.clicked.connect(self.try_login)
        self.logoutButton.clicked.connect(self.logout)

        self.drives_entry.clicked.connect(self.press_drives_entry_btn)
        self.drives_change.clicked.connect(self.press_drives_change_btn)
        self.drives_delete.clicked.connect(self.press_drives_delete_btn)
        self.drives_query.clicked.connect(self.press_drives_query_btn)

        self.fixer_search_drives_and_add.clicked.connect(self.press_search_drives_btn)
        self.fixer_commit.clicked.connect(self.press_fixer_commit_btn)

        self.admin_change_log.clicked.connect(self.press_change_logs_btn)

        self.admin_manager_user.clicked.connect(self.managerUser)
        self.admin_registered.clicked.connect(self.registered_user)
        self.admin_delete_user.clicked.connect(self.delete_user)
        self.admin_change_user.clicked.connect(self.changeUser)

        self.customer_button.clicked.connect(self.customerInfo)
        self.changestoresattributes.clicked.connect(self.press_drives_record_btn)
        self.record_drives.clicked.connect(self.press_drives_record_btn)
        self.change_logs.clicked.connect(self.press_change_logs)
        self.buttonexportexecl.clicked.connect(self.exportExecl)
        self.queryCustomerInfoButton.clicked.connect(self.queryCustomerInfo)
        self.querySalesInfoButton.clicked.connect(self.querySalesInfo)
        self.queryWarehouseInfoButton.clicked.connect(self.queryWarehouseInfo)
        self.queryTop10BankInfoButton.clicked.connect(self.queryTop10BankInfo)
        self.queryTop100GoodsInfopushButton.clicked.connect(self.queryTop100GoodsInfo)
        self.queryGoodsDetailInfoButton.clicked.connect(self.queryGoodsDetailInfo)
        self.queryRemainLessThan10Button.clicked.connect(self.queryRemainLessThan10)
        self.querySuggestedPromotionalItemsButton.clicked.connect(self.querySuggestedPromotionalItems)
        self.buttonprintexecl.clicked.connect(self.printExecl)

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
        except:
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
        except:
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
