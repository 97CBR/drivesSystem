# -*- coding: utf-8 -*-
# @Time    : 10/23/2019 5:50 PM
# @Author  : HR
# @File    : __init__.py

import pymysql


class StoreMysql:
    def __init__(self):
        self.ip = "127.0.0.1"
        self.port = 3306
        self.username = "root"
        self.password = "root"
        self.database = "drives_management"
        self.charset = "utf8"
        self.db = pymysql.connect(self.ip, self.username, self.password,
                                  self.database, port=self.port, use_unicode=True,
                                  charset=self.charset)

    # 操作数据库
    def operational_data(self, sql):
        print(sql)
        cursor = self.db.cursor()
        # print(sql)
        try:
            cursor.execute(sql)
            print('[+]         Successfully       [+]\n')
            self.db.commit()
            return cursor
        except:
            print('[-]         Failure       [-]\n')
            self.db.rollback()
            return False

    # 获取用户表所有数据
    def get_userinfo(self):
        sql = "SELECT * FROM `users`"
        data = self.operational_data(sql).fetchall()
        # print(data)
        # for x in data:
        #     print(type(x))
        #     print(x)
        return data

    # 获取用户表所有数据
    def get_goodsinfo(self):
        sql = "SELECT * FROM `drives`"
        data = self.operational_data(sql).fetchall()
        # print(data)
        # for x in data:
        #     print(type(x))
        #     print(x)
        return data

    # 获取销售表所有数据
    def get_salesinfo(self):
        sql = "SELECT * FROM `driveinfo`"
        data = self.operational_data(sql).fetchall()
        # print(data)
        # for x in data:
        #     print(type(x))
        #     print(x)
        return data

    def add_ware(self, bank, goods_name, purchase_price, orgin_number, barcode):
        # 获取下一个ID
        SQL = "SELECT goodsid FROM `warehouse`"
        data = self.operational_data(SQL).fetchall()
        print(data)
        id = data[-1][0] + 1
        print("new id", id)
        # 插入warehouse表
        SQL = "INSERT INTO `store`.`warehouse`(`goodsid`,`orginnumber`, `remainnumber`, `barcode`) VALUES ({},{}, {}, '{}')".format(
            id, orgin_number, orgin_number, barcode)
        data = self.operational_data(SQL)
        # 插入goodsinfo表
        SQL = "INSERT INTO `store`.`goodsinfo`(`goodsid`, `bank`, `goodsname`, `barcode`, `purchaseprice`, `orginnumber`) " \
              "VALUES ({}, '{}', '{}', '{}', {}, {})".format(id, bank, goods_name, barcode, purchase_price,
                                                             orgin_number)
        data = self.operational_data(SQL)
        # 插入saleinfo表
        SQL = "INSERT INTO `store`.`salesinfo`(`goodsid`, `name`, `bank`, `barcode`, `salesnumber`, `remainnumber`, `profit`) " \
              "VALUES ({}, '{}', '{}', '{}', 0, {}, 0)".format(id, goods_name, bank, barcode, orgin_number)
        data = self.operational_data(SQL)

        if data:
            return True
        else:
            return False

    def update_goodsinfo(self, id, bank, goodsname, barcode, purchaseprice, orginnumber, count, price):
        # 更新goodsinfo表
        SQL = "UPDATE `store`.`goodsinfo` SET `bank` = '{}', `goodsname` = '{}', `barcode` = '{}'," \
              " `purchaseprice` = {}, `orginnumber` = {} ,`count` = {} ,`price` = {} WHERE `goodsid` = {}".format(bank,
                                                                                                                  goodsname,
                                                                                                                  barcode,
                                                                                                                  purchaseprice,
                                                                                                                  orginnumber,
                                                                                                                  count,
                                                                                                                  price,
                                                                                                                  id)
        data = self.operational_data(SQL)
        # 更新warehouse表
        SQL = "UPDATE `store`.`warehouse` SET `barcode` = '{}', `orginnumber` = {} WHERE `goodsid` = {}".format(barcode,
                                                                                                                orginnumber,
                                                                                                                id)
        data = self.operational_data(SQL)
        if data:
            return True
        else:
            return False

    def delete_goodsinfo(self, id):
        # 删除goodsinfo表
        SQL = "DELETE FROM `store`.`goodsinfo` WHERE `goodsid` = {}".format(id)
        data = self.operational_data(SQL)

        # 删除saleinfo表
        SQL = "DELETE FROM `store`.`salesinfo` WHERE `goodsid` = {}".format(id)
        data = self.operational_data(SQL)

        # 删除warehouse表
        SQL = "DELETE FROM `store`.`warehouse` WHERE `goodsid` = {}".format(id)
        data = self.operational_data(SQL)
        if data:
            return True
        else:
            return False

    def search_goods(self, barcode):
        SQL = "SELECT * FROM `store`.`goodsinfo` WHERE  `barcode` = '{}'".format(barcode)
        # sql = "SELECT * FROM `goodsinfo`"
        data = self.operational_data(SQL).fetchall()
        return data

    def sale_goods(self, barcode, price):
        SQL = "UPDATE `store`.`warehouse` SET `salesnumber` = `salesnumber`+1, `remainnumber` = `remainnumber`-1 WHERE `barcode` = {}".format(
            barcode)
        data = self.operational_data(SQL)

        # SQL="INSERT INTO `store`.`salesinfo`(`goodsid`, `name`, `bank`, `barcode`, `salesnumber`, `remainnumber`, `profit`) VALUES (2, 'a', 'a', 'a', 1, 999, 26)"

        SQL = "UPDATE `store`.`salesinfo` SET `salesnumber` = `salesnumber`+1 , remainnumber=remainnumber-1 ,profit=profit+{} WHERE `barcode` = {}".format(
            price, barcode)
        data = self.operational_data(SQL)
        return data

    def resign_user(self, name, type, pwd):
        SQL = "INSERT INTO `store`.`users`(`name`, `type`, `pwd`) " \
              "VALUES ('{}', '{}', '{}')".format(name, type, pwd)
        data = self.operational_data(SQL)
        return data

    def delete_user(self, name):
        SQL = "DELETE FROM `store`.`users` WHERE `name` = '{}'".format(name)
        data = self.operational_data(SQL)
        return data

    def change_user(self, type, name):
        SQL = "UPDATE `store`.`users` SET `type` = '{}' WHERE `name` = '{}'".format(type, name)
        data = self.operational_data(SQL)
        return data

    def get_customerinfo(self):
        SQL = "SELECT * FROM `customerinfo`"
        data = self.operational_data(SQL).fetchall()
        return data

    def update_salesinfo(self, oldid, bank, goodsname, barcode, salesnumber, remainnumber, profit):
        # 更新salesinfo表
        SQL = "UPDATE `store`.`salesinfo` SET `bank` = '{}', `name` = '{}', `barcode` = '{}'," \
              " `salesnumber` = {}, `remainnumber` = {} , `profit` = {} WHERE `goodsid` = {}".format(bank, goodsname,
                                                                                                     barcode,
                                                                                                     salesnumber,
                                                                                                     remainnumber,
                                                                                                     profit, oldid)
        data = self.operational_data(SQL)
        if data:
            return True
        else:
            return False

    def get_column_name(self, tablename):
        sql = "select COLUMN_NAME,column_comment from INFORMATION_SCHEMA.Columns where table_name='{}' and table_schema='store'".format(
            tablename)
        data = self.operational_data(sql).fetchall()
        return data

    def get_warehouseinfo(self):
        sql = "SELECT * FROM `warehouse`"
        data = self.operational_data(sql).fetchall()
        # print(data)
        # for x in data:
        #     print(type(x))
        #     print(x)
        return data

    def get_top10_bank(self):
        sql = '''SELECT
	salesinfo.goodsid,
	salesinfo.bank,
	salesinfo.profit,
	SUM( profit ) AS bankprofit 
FROM
	salesinfo 
GROUP BY
	salesinfo.bank 
ORDER BY
	salesinfo.bank ASC 
	LIMIT 0,
	1000'''
        data = self.operational_data(sql).fetchall()
        return data

    def get_top100_goods(self):
        sql = '''
SELECT
	salesinfo.goodsid,
	salesinfo.name,
	salesinfo.bank,
	salesinfo.barcode,
	salesinfo.salesnumber
FROM
	salesinfo 
ORDER BY
	salesinfo.salesnumber DESC 
	LIMIT 0,
	100
	        '''
        data = self.operational_data(sql).fetchall()
        return data

    def get_goods_detail_info(self):
        sql = "SELECT * FROM `store`.`allgoodsinfo` ORDER BY `goodsid` LIMIT 0, 1000"
        data = self.operational_data(sql).fetchall()
        return data

    def get_remain_less_than_10(self):
        sql = "SELECT * FROM `store`.`saleview` WHERE `remainnumber` < orginnumber * 0.1 "
        data = self.operational_data(sql).fetchall()
        return data

    def get_suggested_promotional_items(self):
        sql = "SELECT * FROM `store`.`saleview` WHERE `salesnumber` < orginnumber * 0.1  "
        data = self.operational_data(sql).fetchall()
        return data

    def update_customer_credit(self, credit=0, customerid=0):
        sql = "UPDATE `store`.`customerinfo` SET `source` = `source` + {} WHERE `customerid` =  '{}'".format(credit,
                                                                                                             customerid)
        data = self.operational_data(sql)
        return data
