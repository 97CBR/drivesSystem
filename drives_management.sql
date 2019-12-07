/*
 Navicat Premium Data Transfer

 Source Server         : 127.0.0.1
 Source Server Type    : MySQL
 Source Server Version : 50553
 Source Host           : localhost:3306
 Source Schema         : drives_management

 Target Server Type    : MySQL
 Target Server Version : 50553
 File Encoding         : 65001

 Date: 07/12/2019 16:23:38
*/

SET NAMES utf8mb4;
SET FOREIGN_KEY_CHECKS = 0;

-- ----------------------------
-- Table structure for driveinfo
-- ----------------------------
DROP TABLE IF EXISTS `driveinfo`;
CREATE TABLE `driveinfo`  (
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `number` int(11) DEFAULT NULL,
  `tpye` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `version` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for drives
-- ----------------------------
DROP TABLE IF EXISTS `drives`;
CREATE TABLE `drives`  (
  `uuid` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `type` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `status` int(1) DEFAULT NULL,
  `version` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `specification` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `product` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `department` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `etpye` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '故障类型',
  `ereason` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL COMMENT '故障原因',
  `ctime` datetime DEFAULT NULL,
  `mtime` timestamp NOT NULL DEFAULT '0000-00-00 00:00:00' ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY (`uuid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of drives
-- ----------------------------
INSERT INTO `drives` VALUES ('123-456', '的高房价', '昂达', 0, '昂达', '大使馆', '发收到货', 'company', '已维修正常', '线路损坏，导致无法启动，更换模块即可', '2019-12-07 11:44:09', '2019-12-07 15:25:00');
INSERT INTO `drives` VALUES ('456-123', '哈萨克打开后发', '萨达', 1, '123', 'big', 'guet', 'company', '0', '0', '2019-12-07 16:03:46', '0000-00-00 00:00:00');
INSERT INTO `drives` VALUES ('456-136', '第三个', '大概', 2, '大法', '的撒发', '那个，五个', 'company', '线路损坏', '更换背板即可', '2019-12-02 11:38:19', '2019-12-07 16:19:55');
INSERT INTO `drives` VALUES ('652', '打扫房间', '闪电发货', 1, '爱生活', '水电费交换机', '史蒂芬霍金', 'company', '线路', '线路老化', '2019-12-07 11:38:08', '2019-12-07 11:38:18');

-- ----------------------------
-- Table structure for fixing
-- ----------------------------
DROP TABLE IF EXISTS `fixing`;
CREATE TABLE `fixing`  (
  `uuid` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci NOT NULL,
  `status` int(1) DEFAULT NULL,
  `fixman` int(11) DEFAULT NULL,
  `fixprocess` int(1) DEFAULT NULL,
  PRIMARY KEY (`uuid`) USING BTREE
) ENGINE = InnoDB CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Table structure for logs
-- ----------------------------
DROP TABLE IF EXISTS `logs`;
CREATE TABLE `logs`  (
  `logid` int(11) NOT NULL AUTO_INCREMENT,
  `uuid` varchar(16) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `record` text CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci,
  `user_id` int(11) DEFAULT NULL,
  PRIMARY KEY (`logid`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 21 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of logs
-- ----------------------------
INSERT INTO `logs` VALUES (20, '456-136', 'user marx 接入 第三个 设备ID:456-136 进行维修，设备当前状态：Fixing', 4);

-- ----------------------------
-- Table structure for users
-- ----------------------------
DROP TABLE IF EXISTS `users`;
CREATE TABLE `users`  (
  `ID` int(11) NOT NULL AUTO_INCREMENT,
  `name` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `pwd` varchar(255) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  `role` varchar(20) CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci DEFAULT NULL,
  PRIMARY KEY (`ID`) USING BTREE
) ENGINE = InnoDB AUTO_INCREMENT = 6 CHARACTER SET = utf8mb4 COLLATE = utf8mb4_general_ci ROW_FORMAT = Compact;

-- ----------------------------
-- Records of users
-- ----------------------------
INSERT INTO `users` VALUES (1, 'hr', 'adab7b701f23bb82014c8506d3dc784e', 'admin');
INSERT INTO `users` VALUES (2, 'cbr', 'adab7b701f23bb82014c8506d3dc784e', 'admin');
INSERT INTO `users` VALUES (4, 'marx', 'adab7b701f23bb82014c8506d3dc784e', 'fixer');
INSERT INTO `users` VALUES (5, 'Tina', 'adab7b701f23bb82014c8506d3dc784e', 'recorder');

-- ----------------------------
-- View structure for log_view
-- ----------------------------
DROP VIEW IF EXISTS `log_view`;
CREATE ALGORITHM = UNDEFINED DEFINER = `root`@`localhost` SQL SECURITY DEFINER VIEW `log_view` AS select `logs`.`logid` AS `logid`,`logs`.`record` AS `record`,`users`.`ID` AS `ID`,`users`.`name` AS `name`,`drives`.`name` AS `drive_name`,`drives`.`uuid` AS `drive_id`,`drives`.`version` AS `version` from ((`logs` join `users`) join `drives`) where ((`logs`.`user_id` = `users`.`ID`) and (`logs`.`uuid` = `drives`.`uuid`));

-- ----------------------------
-- View structure for user_log_view
-- ----------------------------
DROP VIEW IF EXISTS `user_log_view`;
CREATE ALGORITHM = UNDEFINED DEFINER = `root`@`localhost` SQL SECURITY DEFINER VIEW `user_log_view` AS select `logs`.`uuid` AS `log_id`,`logs`.`record` AS `record`,`users`.`ID` AS `ID`,`users`.`name` AS `name`,`drives`.`name` AS `drive_name`,`drives`.`uuid` AS `drive_id`,`drives`.`version` AS `version` from ((`logs` join `users`) join `drives`) where (`logs`.`user_id` = `users`.`ID`);

SET FOREIGN_KEY_CHECKS = 1;
