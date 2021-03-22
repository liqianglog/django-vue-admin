-- ----------------------------
-- 字典管理初始化sql
-- Table structure for system_dictdata
-- ----------------------------
-- DROP TABLE IF EXISTS `system_dictdata`;
-- CREATE TABLE `system_dictdata` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `description` longtext,
--   `creator` varchar(255) DEFAULT NULL,
--   `modifier` varchar(255) DEFAULT NULL,
--   `update_datetime` datetime(6) DEFAULT NULL,
--   `create_datetime` datetime(6) DEFAULT NULL,
--   `dictName` varchar(64) NOT NULL,
--   `dictType` varchar(64) NOT NULL,
--   `status` varchar(8) NOT NULL,
--   `remark` varchar(256) DEFAULT NULL,
--   PRIMARY KEY (`id`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=13 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
-- ----------------------------
-- Records of system_dictdata
-- ----------------------------
INSERT INTO `system_dictdata` (id, description, modifier, update_datetime, create_datetime, dictName, dictType, status, remark, creator_id, dept_belong_id) VALUES (1, '', 'admin', '2021-02-27 06:22:24.215575', '2021-02-27 06:22:24.215617', '用户性别', 'sys_user_sex', '1', '用户性别列表', 1, 1);
INSERT INTO `system_dictdata` (id, description, modifier, update_datetime, create_datetime, dictName, dictType, status, remark, creator_id, dept_belong_id) VALUES (2, '', 'admin', '2021-02-27 06:24:38.126411', '2021-02-27 06:24:38.126456', '菜单状态', 'sys_show_hide', '1', '菜单状态列表', 1, 1);
INSERT INTO `system_dictdata` (id, description, modifier, update_datetime, create_datetime, dictName, dictType, status, remark, creator_id, dept_belong_id) VALUES (3, '', 'admin', '2021-02-27 06:24:54.943462', '2021-02-27 06:24:54.943516', '系统开关', 'sys_normal_disable', '1', '系统开关列表', 1, 1);
INSERT INTO `system_dictdata` (id, description, modifier, update_datetime, create_datetime, dictName, dictType, status, remark, creator_id, dept_belong_id) VALUES (4, '', 'admin', '2021-02-27 06:25:16.667651', '2021-02-27 06:25:16.667697', '任务状态', 'sys_job_status', '1', '任务状态列表', 1, 1);
INSERT INTO `system_dictdata` (id, description, modifier, update_datetime, create_datetime, dictName, dictType, status, remark, creator_id, dept_belong_id) VALUES (5, '', 'admin', '2021-02-27 06:25:34.967768', '2021-02-27 06:25:34.967812', '任务分组', 'sys_job_group', '1', '任务分组列表', 1, 1);
INSERT INTO `system_dictdata` (id, description, modifier, update_datetime, create_datetime, dictName, dictType, status, remark, creator_id, dept_belong_id) VALUES (6, '', 'admin', '2021-02-27 06:26:01.081973', '2021-02-27 06:26:01.082016', '系统是否', 'sys_yes_no', '1', '系统是否列表', 1, 1);
INSERT INTO `system_dictdata` (id, description, modifier, update_datetime, create_datetime, dictName, dictType, status, remark, creator_id, dept_belong_id) VALUES (7, '', 'admin', '2021-02-27 06:26:17.716100', '2021-02-27 06:26:17.716144', '通知类型', 'sys_notice_type', '1', '通知类型列表', 1, 1);
INSERT INTO `system_dictdata` (id, description, modifier, update_datetime, create_datetime, dictName, dictType, status, remark, creator_id, dept_belong_id) VALUES (8, '', 'admin', '2021-02-27 06:26:42.305470', '2021-02-27 06:26:42.305517', '通知状态', 'sys_notice_status', '1', '通知状态列表', 1, 1);
INSERT INTO `system_dictdata` (id, description, modifier, update_datetime, create_datetime, dictName, dictType, status, remark, creator_id, dept_belong_id) VALUES (9, '', 'admin', '2021-02-27 06:26:57.913406', '2021-02-27 06:26:57.913457', '操作类型', 'sys_oper_type', '1', '操作类型列表', 1, 1);
INSERT INTO `system_dictdata` (id, description, modifier, update_datetime, create_datetime, dictName, dictType, status, remark, creator_id, dept_belong_id) VALUES (10, '', 'admin', '2021-02-27 06:27:16.392863', '2021-02-27 06:27:16.392961', '系统状态', 'sys_common_status', '1', '登录状态列表', 1, 1);
INSERT INTO `system_dictdata` (id, description, modifier, update_datetime, create_datetime, dictName, dictType, status, remark, creator_id, dept_belong_id) VALUES (11, '', 'admin', '2021-02-27 07:59:30.310069', '2021-02-27 07:59:30.310115', '菜单类型', 'sys_menu_type', '1', '菜单类型', 1, 1);
INSERT INTO `system_dictdata` (id, description, modifier, update_datetime, create_datetime, dictName, dictType, status, remark, creator_id, dept_belong_id) VALUES (12, '', 'admin', '2021-02-27 07:59:47.677379', '2021-02-27 07:59:47.677423', '接口请求方式', 'sys_interface_method', '1', '接口请求方式', 1, 1);
INSERT INTO `system_dictdata` (id, description, modifier, update_datetime, create_datetime, dictName, dictType, status, remark, creator_id, dept_belong_id) VALUES (13, '', 'admin', '2021-03-07 15:06:34.123188', '2021-03-07 14:27:51.286902', '消息类型', 'sys_message_push_type', '1', '消息通知类型', 1, 1);
INSERT INTO `system_dictdata` (id, description, modifier, update_datetime, create_datetime, dictName, dictType, status, remark, creator_id, dept_belong_id) VALUES (14, '', 'admin', '2021-03-07 15:06:38.891604', '2021-03-07 15:06:00.930057', '消息状态', 'sys_message_push_status', '1', '消息通知状态', 1, 1);
