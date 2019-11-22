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

        self.buttonConnect()

        self.user_info = StoreMysql().get_userinfo()
        self.userType = ""
        self.my_view()

        self.data = StoreMysql().get_goodsinfo()

        self.pay = 0.0

    @staticmethod
    def calculate_md5(src):
        m = hashlib.md5()
        m.update(src.encode('UTF-8'))
        return m.hexdigest()

    def logout(self):
        self.stackedWidget.setCurrentWidget(self.loginwidget)

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
            self.stackedWidget.setCurrentWidget(self.warewidget)
        else:
            ...
        # print(username,password)

    def wareAdd(self):
        print("添加货物")
        bank = self.ware_bank.text()
        goodsname = self.ware_goodsname.text()
        purchaseprice = float(self.ware_purchaseprice.text())
        orginnumber = int(self.ware_orginnumber.text())
        barcode = self.ware_barcode.text()

        statu = StoreMysql().add_ware(bank=bank, goods_name=goodsname, purchase_price=purchaseprice,
                                      orgin_number=orginnumber, barcode=barcode)
        if statu:
            self.ware_message.setText('成功添加')
            self.my_view()
            # self.statusbar.setStatusTip("成功添加")
        else:
            self.ware_message.setText('添加失败')
            # self.statusbar.setStatusTip("添加失败")

    def wareChange(self):
        nowrow = self.tableWidget.currentRow()
        print("当前行", nowrow)
        # a,b,c,d,e,f
        id = self.tableWidget.item(nowrow, 0).text()
        # ppp=self.tableWidget.item
        bank = self.tableWidget.item(nowrow, 1).text()
        goodsname = self.tableWidget.item(nowrow, 2).text()
        barcode = self.tableWidget.item(nowrow, 3).text()
        orginnumber = self.tableWidget.item(nowrow, 4).text()
        purchaseprice = self.tableWidget.item(nowrow, 5).text()
        count = self.tableWidget.item(nowrow, 6).text()
        price = self.tableWidget.item(nowrow, 7).text()
        oldid = self.data[nowrow][0]

        print(id, bank, goodsname)
        statu = StoreMysql().update_goodsinfo(oldid, bank, goodsname, barcode, purchaseprice, orginnumber, count, price)
        if statu:
            self.ware_message.setText('成功修改')
            self.my_view()
        else:
            self.ware_message.setText('修改失败')

    def wareDelete(self):
        nowrow = self.tableWidget.currentRow()
        print("当前行", nowrow)
        oldid = self.data[nowrow][0]
        statu = StoreMysql().delete_goodsinfo(oldid)
        if statu:
            self.ware_message.setText('删除成功')
            self.my_view()
        else:
            self.ware_message.setText('删除失败')
        return True

    # 刷新进货tablewidget

    def my_view(self):
        _translate = QtCore.QCoreApplication.translate
        # self.tableWidget.verticalHeader().setVisible(False)
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("MainWindow", "进货价格"))
        # item = self.tableWidget.item(0, 0)

        self.data = StoreMysql().get_goodsinfo()

        self.tableWidget.setRowCount(len(self.data))
        for x, info in enumerate(self.data):
            print(x, info)
            for y, cell in enumerate(info):
                print(y, cell)
                if y < 8:
                    try:
                        item = QtWidgets.QTableWidgetItem(str(cell))
                        self.tableWidget.setItem(x, y, item)
                        # item = self.tableWidget.item(x, y)
                        # item.setText(_translate("MainWindow",str(cell)))
                    except:
                        pass
                else:
                    pass

    def profitChange(self):
        nowrow = self.tableWidget_2.currentRow()
        print("当前行", nowrow)
        # a,b,c,d,e,f
        id = self.tableWidget_2.item(nowrow, 0).text()
        # ppp=self.tableWidget.item
        bank = self.tableWidget_2.item(nowrow, 1).text()
        goodsname = self.tableWidget_2.item(nowrow, 2).text()
        barcode = self.tableWidget_2.item(nowrow, 3).text()
        salesnumber = self.tableWidget_2.item(nowrow, 4).text()
        remainnumber = self.tableWidget_2.item(nowrow, 5).text()
        profit = self.tableWidget_2.item(nowrow, 6).text()

        oldid = self.data[nowrow][0]

        print(id, bank, goodsname)
        statu = StoreMysql().update_salesinfo(oldid, bank, goodsname, barcode, salesnumber, remainnumber, profit)
        if statu:
            self.ware_message.setText('成功修改')
            self.profitreflash()
        else:
            self.ware_message.setText('修改失败')

    def profitreflash(self):

        self.data = StoreMysql().get_salesinfo()

        self.tableWidget_2.setRowCount(len(self.data))
        for x, info in enumerate(self.data):
            print(x, info)
            for y, cell in enumerate(info):
                print(y, cell)
                if y < 7:
                    try:
                        item = QtWidgets.QTableWidgetItem(str(cell))
                        self.tableWidget_2.setItem(x, y, item)
                        # item = self.tableWidget.item(x, y)
                        # item.setText(_translate("MainWindow",str(cell)))
                    except:
                        pass
                else:
                    pass

    def searchGoods(self):
        print('搜索商品信息')
        barcode = self.search_barcode.text()
        if barcode != '':
            data = StoreMysql().search_goods(barcode=barcode)
            if data:
                data = data[0]
                self.pay += float(data[6] * data[7])
                self.goodsname.setText(data[2])
                self.price.setText("%.2f" % float(data[6] * data[7]))
                self.barcode.setText(data[3])
                self.count.setText(str(data[6] * 100) + "%")
                self.need_pay.setText(str("%.2f" % self.pay))

                # id=data[0]
                # bank=data[1]
                # goodsname=data[2]
                barcode = data[3]
                # orginnumber = data[4]
                purchaseprice = data[5]
                price = data[6] * data[7]

                # 添加信息到销售表
                statu = StoreMysql().sale_goods(barcode, float(price - purchaseprice))

                mylist = QtWidgets.QWidget()
                mylist.setGeometry(QtCore.QRect(90, 700, 820, 30))
                # mylist.setObjectName("mylist")
                listname = QtWidgets.QLabel(mylist)
                listname.setGeometry(QtCore.QRect(0, 0, 151, 30))
                listname.setAlignment(QtCore.Qt.AlignCenter)
                listname.setText(data[2])
                # listname.setObjectName("listname")
                listnum = QtWidgets.QLabel(mylist)
                listnum.setGeometry(QtCore.QRect(300, 0, 151, 30))
                listnum.setAlignment(QtCore.Qt.AlignCenter)
                listnum.setText("1")
                # listnum.setObjectName("listnum")
                listprice = QtWidgets.QLabel(mylist)
                listprice.setGeometry(QtCore.QRect(650, 0, 151, 30))
                listprice.setAlignment(QtCore.Qt.AlignCenter)
                listprice.setText("%.2f" % float(data[6] * data[7]))
                # listprice.setObjectName("listprice")
                # 自定义控件
                item = QtWidgets.QListWidgetItem()
                item.setSizeHint(QtCore.QSize(820, 30))
                # items->setSizeHint(QSize(1000, 32));
                self.listWidget.addItem(item)
                self.listWidget.setItemWidget(item, mylist)
            else:
                self.salemessage.setText("找不到该商品")
                print('找不到？')
        else:
            self.salemessage.setText("请输入条形码")
            print("输入条形码")

    def payOver(self):

        statu = StoreMysql().update_customer_credit(customerid=self.customername.text(), credit=self.need_pay.text())
        if statu:
            self.salemessage.setText("收款成功")
            print("收款成功")
        else:
            self.salemessage.setText("收款失败")
            print("收款失败")
        self.listWidget.clear()
        self.barcode.clear()
        self.price.clear()
        self.search_barcode.clear()
        self.need_pay.clear()
        self.goodsname.clear()
        self.customername.clear()

    def managerUser(self):
        self.adminstacked.setCurrentWidget(self.manager_man)

    def resignMan(self):
        username = self.resigner_name.text()
        password_1 = self.resigner_password_1.text()
        password_2 = self.resigner_password_2.text()
        if (username != '') and (password_1 != '') and (password_2 != '') and password_1 == password_2:
            resigner_type = self.resign_type.currentText()
            pwd = self.calculate_md5(password_2)
            print("加密", pwd)

            statu = StoreMysql().resign_user(username, resigner_type, pwd)
            if statu:
                self.resigner_name.clear()
                self.resigner_password_1.clear()
                self.resigner_password_2.clear()
                self.loginmessage_2.setText('成功添加')
                # self.myview()
            else:
                self.resigner_name.clear()
                self.resigner_password_1.clear()
                self.resigner_password_2.clear()
                self.loginmessage_2.setText('添加失败')
        else:
            # print()
            self.loginmessage_2.setText("错误")

    def deleteMan(self):
        username = self.delete_username.text()
        if username != '':
            statu = StoreMysql().delete_user(username)
            if statu:
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

    def changeStoresAttributes(self):
        self.stackedWidget.setCurrentWidget(self.warewidget)

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
        self.profitreflash()
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

        data = StoreMysql().get_salesinfo()
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
        self.ware_add.clicked.connect(self.wareAdd)
        self.ware_change.clicked.connect(self.wareChange)
        self.ware_delete.clicked.connect(self.wareDelete)
        self.search_and_add.clicked.connect(self.searchGoods)
        self.finish_pay.clicked.connect(self.payOver)
        self.manager_user.clicked.connect(self.managerUser)
        self.resign.clicked.connect(self.resignMan)
        self.delete_man.clicked.connect(self.deleteMan)
        self.change_man.clicked.connect(self.changeUser)
        self.customer_button.clicked.connect(self.customerInfo)
        self.changestoresattributes.clicked.connect(self.changeStoresAttributes)
        # self.changeprofitbutton.clicked.connect(self.changeProfit)
        self.change_logs.clicked.connect(self.press_change_logs)
        self.ware_change_2.clicked.connect(self.profitChange)
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
        self.logoutButton.clicked.connect(self.logout)
        self.ware_query_2.clicked.connect(self.queryGoods)

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

    def queryGoods(self):
        name = self.ware_goodsname.text()
        if name != '':
            print('查询')
            data = StoreMysql().get_goodsinfo()
            for x, info in enumerate(data):
                print(x, info)
                for y, cell in enumerate(info):
                    print(y, cell)
                    if name == cell:
                        self.tableWidget.selectRow(x)
                        self.ware_message.setText("查找成功")
                        break
                    else:
                        pass

        else:
            self.ware_message.setText("查找失败")

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
