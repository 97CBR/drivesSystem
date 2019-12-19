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
    def get_devices_info(self):
        sql = "SELECT * FROM `drives`"
        data = self.operational_data(sql).fetchall()
        # print(data)
        # for x in data:
        #     print(type(x))
        #     print(x)
        return data

    # 获取销售表所有数据
    def get_logs_records(self):
        sql = "SELECT * FROM `log_view`"
        data = self.operational_data(sql).fetchall()
        # print(data)
        # for x in data:
        #     print(type(x))
        #     print(x)
        return data

    def add_drives2ware(self, drives_uuid, drive_name, drive_type,
                        drive_status, drive_version,
                        drive_specification, drive_product,
                        drive_department,
                        drive_etype, drive_ereason, now):

        SQL = "INSERT INTO `drives_management`.`drives`(`uuid`, `name`, `type`, `status`, `version`, `specification`, " \
              "`product`, `department`, `etpye`, `ereason`,`ctime` ) VALUES ('{}', '{}', '{}', {}, '{}', '{}', '{}', '{}', '{}', '{}','{}')".format(
            drives_uuid, drive_name, drive_type,
            drive_status, drive_version,
            drive_specification, drive_product,
            drive_department,
            drive_etype, drive_ereason, now)

        print(SQL)
        # # 获取下一个ID
        # SQL = "SELECT goodsid FROM `warehouse`"
        # data = self.operational_data(SQL).fetchall()
        # print(data)
        # id = data[-1][0] + 1
        # print("new id", id)
        # # 插入warehouse表
        # SQL = "INSERT INTO `drives_management`.`warehouse`(`goodsid`,`orginnumber`, `remainnumber`, `barcode`) VALUES ({},{}, {}, '{}')".format(
        #     id, orgin_number, orgin_number, barcode)
        # data = self.operational_data(SQL)
        # # 插入goodsinfo表
        # SQL = "INSERT INTO `drives_management`.`goodsinfo`(`goodsid`, `bank`, `goodsname`, `barcode`, `purchaseprice`, `orginnumber`) " \
        #       "VALUES ({}, '{}', '{}', '{}', {}, {})".format(id, bank, goods_name, barcode, purchase_price,
        #                                                      orgin_number)
        # data = self.operational_data(SQL)
        # # 插入saleinfo表
        # SQL = "INSERT INTO `drives_management`.`salesinfo`(`goodsid`, `name`, `bank`, `barcode`, `salesnumber`, `remainnumber`, `profit`) " \
        #       "VALUES ({}, '{}', '{}', '{}', 0, {}, 0)".format(id, goods_name, bank, barcode, orgin_number)
        data = self.operational_data(SQL)

        if data:
            return True
        else:
            return False

    def update_devices_info(self, uuid, name, type, status, version, specification, product, department, etpye,
                            ereason):

        # uuid,        name,        type,        status,        version,        specification,        product,        department,        etpye,        ereason

        # 更新goodsinfo表
        SQL = "UPDATE `drives_management`.`drives` SET  `name` = '{}', `type` = '{}', `status` = {}," \
              " `version` = '{}', `specification` = '{}', `product` = '{}', `department` = '{}'," \
              " `etpye` = '{}', `ereason` = '{}' WHERE `uuid` = '{}'".format(name, type, int(status), version,
                                                                             specification, product, department, etpye,
                                                                             ereason, uuid)
        data = self.operational_data(SQL)
        if data:
            return True
        else:
            return False

    def delete_devices_info(self, id):
        # 删除goodsinfo表
        SQL = "DELETE FROM `drives_management`.`drives` WHERE `uuid` = '{}'".format(id)
        data = self.operational_data(SQL)

        # todo 删除fixing表
        # SQL = "DELETE FROM `drives_management`.`salesinfo` WHERE `goodsid` = {}".format(id)
        # data = self.operational_data(SQL)

        if data:
            return True
        else:
            return False

    def search_devices(self, drives_id):
        SQL = "SELECT * FROM `drives_management`.`drives` WHERE  `uuid` = '{}'".format(drives_id)
        # sql = "SELECT * FROM `goodsinfo`"
        data = self.operational_data(SQL).fetchall()
        return data

    def record_logs(self, uuid, record, user_id):

        SQL = "INSERT INTO `drives_management`.`logs`(`uuid`, `record`, `user_id`) VALUES ('{}', '{}', {})".format(uuid,
                                                                                                                   record,
                                                                                                                   user_id)
        data = self.operational_data(SQL)

        return data

    def registered_user_to_database(self, name, pwd, role):
        SQL = "INSERT INTO `drives_management`.`users`(`name`, `pwd`, `role`) " \
              "VALUES ('{}', '{}', '{}')".format(name, pwd, role)
        data = self.operational_data(SQL)
        return data

    def delete_user(self, name):
        SQL = "DELETE FROM `drives_management`.`users` WHERE `name` = '{}'".format(name)
        data = self.operational_data(SQL)
        return data

    def change_user(self, type, name):
        SQL = "UPDATE `drives_management`.`users` SET `role` = '{}' WHERE `name` = '{}'".format(type, name)
        data = self.operational_data(SQL)
        return data

    def update_admin_log_info(self, log_id, record, user_id, user_name, drive_name, drive_id, version):
        # 更新salesinfo表

        log_sql = "UPDATE `drives_management`.`logs` SET `logid` = {}, `uuid` = '{}', `record` = '{}', `user_id` = {} WHERE `logid` = {}".format(
            log_id, drive_id, record, user_id, log_id)
        data_one = self.operational_data(log_sql)

        drives_sql = "UPDATE `drives_management`.`drives` SET `uuid` = '{}', `name` = '{}', `version` = '{}' WHERE `uuid` = '{}'".format(
            drive_id, drive_name, version, drive_id)
        data_two = self.operational_data(drives_sql)

        if data_one and data_two:
            return True
        else:
            return False

    def get_column_name(self, tablename):
        sql = "select COLUMN_NAME,column_comment from INFORMATION_SCHEMA.Columns where table_name='{}' and table_schema='drives_management'".format(
            tablename)
        data = self.operational_data(sql).fetchall()
        return data

    def get_drive_bad_info(self):
        SQL = "SELECT * FROM `drives_management`.`drives` WHERE `status` <> '1'"
        data = self.operational_data(SQL).fetchall()
        return data

    def get_drive_not_fix_info(self):
        sql = "SELECT * FROM `drives_management`.`drives` WHERE `status` = '0' "
        data = self.operational_data(sql).fetchall()
        return data

    def get_drive_fixing_info(self):
        sql = "SELECT * FROM `drives_management`.`drives` WHERE `status` = '2'"
        data = self.operational_data(sql).fetchall()
        return data

    def get_drive_normal_info(self):
        sql = "SELECT * FROM `drives_management`.`drives` WHERE `status` = '1'"
        data = self.operational_data(sql).fetchall()
        return data

    def get_drive_info_by_prefix_info(self, prefix):
        sql = "SELECT * FROM `drives_management`.`drives` WHERE `uuid` LIKE '%{}-%'".format(prefix)
        data = self.operational_data(sql).fetchall()
        return data

    def get_drive_info_by_time_info(self, start_time, end_time):
        sql = "SELECT * FROM `drives_management`.`drives` WHERE `ctime` > '{}' AND `ctime` < '{}'".format(start_time,
                                                                                                          end_time)
        data = self.operational_data(sql).fetchall()
        return data

    def get_suggested_promotional_items(self):
        sql = "SELECT * FROM `drives_management`.`saleview` WHERE `salesnumber` < orginnumber * 0.1  "
        data = self.operational_data(sql).fetchall()
        return data

    def update_drives_table(self, uuid, etype, eresaon, status):
        sql = "UPDATE `drives_management`.`drives` SET `status` = {} ,`etpye` = '{}', `ereason` = '{}'  WHERE `uuid` =  '{}'".format(
            status, etype, eresaon, uuid)
        data = self.operational_data(sql)
        return data
