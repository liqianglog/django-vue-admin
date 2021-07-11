-- ----------------------------
-- 部门管理 初始化sql
-- Table structure for permission_dept
-- ----------------------------
-- DROP TABLE IF EXISTS `permission_dept`;
-- CREATE TABLE `permission_dept` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `description` longtext,
--   `creator` varchar(255) DEFAULT NULL,
--   `modifier` varchar(255) DEFAULT NULL,
--   `update_datetime` datetime(6) DEFAULT NULL,
--   `create_datetime` datetime(6) DEFAULT NULL,
--   `deptName` varchar(64) NOT NULL,
--   `orderNum` int(11) NOT NULL,
--   `owner` varchar(32) DEFAULT NULL,
--   `phone` varchar(32) DEFAULT NULL,
--   `email` varchar(32) DEFAULT NULL,
--   `status` varchar(8) DEFAULT NULL,
--   `parentId_id` int(11) DEFAULT NULL,
--   PRIMARY KEY (`id`),
--   KEY `permission_dept_parentId_id_43a4fd49` (`parentId_id`) USING BTREE
-- ) ENGINE=InnoDB AUTO_INCREMENT=17 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of permission_dept
-- ----------------------------
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (1, '', 'admin', '2021-02-27 07:26:20.518695', '2021-02-27 15:18:39.000000', 'XX创新科技', 1, NULL, '15888888888', 'cxkj@qq.com', '1', 1,NULL, 1);
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (2, '', 'admin', '2021-02-27 07:25:09.041807', '2021-02-27 07:25:09.041853', '北京总公司', 1, NULL, NULL, NULL, '1', 1, 1, 2);
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (3, '', 'admin', '2021-02-27 07:26:14.418894', '2021-02-27 07:25:25.195849', '上海分公司', 2, NULL, NULL, NULL, '1', 1, 1, 3);
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (4, '', 'admin', '2021-02-27 07:26:01.993095', '2021-02-27 07:25:38.904644', '杭州分公司', 4, NULL, NULL, NULL, '1', 1, 1, 4);
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (5, '', 'admin', '2021-02-27 07:28:15.854856', '2021-02-27 07:25:54.379081', '深圳分公司', 3, NULL, NULL, NULL, '0', 1, 1, 5);
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (6, '', 'admin', '2021-02-27 07:26:37.589741', '2021-02-27 07:26:37.589780', '研发部门', 1, NULL, NULL, NULL, '1', 1, 2, 6);
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (7, '', 'admin', '2021-02-27 07:26:47.781467', '2021-02-27 07:26:47.781511', '市场部门', 2, NULL, NULL, NULL, '1', 1, 2, 7);
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (8, '', 'admin', '2021-02-27 07:26:57.059878', '2021-02-27 07:26:57.059923', '测试部门', 3, NULL, NULL, NULL, '1', 1, 2, 8);
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (9, '', 'admin', '2021-02-27 07:27:06.088134', '2021-02-27 07:27:06.088178', '财务部门', 4, NULL, NULL, NULL, '1', 1, 2, 9);
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (10, '', 'admin', '2021-02-27 07:27:15.287731', '2021-02-27 07:27:15.287772', '运维部门', 5, NULL, NULL, NULL, '1', 1, 2, 10);
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (11, '', 'admin', '2021-02-27 07:27:24.834369', '2021-02-27 07:27:24.834413', '市场部门', 1, NULL, NULL, NULL, '1', 1, 3, 11);
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (12, '', 'admin', '2021-02-27 07:27:34.161898', '2021-02-27 07:27:34.161944', '财务部门', 2, NULL, NULL, NULL, '1', 1, 3, 12);
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (13, '', 'admin', '2021-02-27 07:28:20.474025', '2021-02-27 07:27:47.938676', '市场部门', 1, NULL, NULL, NULL, '0', 1, 5, 13);
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (14, '', 'admin', '2021-02-27 07:28:23.394188', '2021-02-27 07:27:53.794331', '财务部门', 2, NULL, NULL, NULL, '0', 1, 5, 14);
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (15, '', 'admin', '2021-02-27 07:28:03.368497', '2021-02-27 07:28:03.368540', '市场部门', 1, NULL, NULL, NULL, '1', 1, 4, 15);
INSERT INTO `permission_dept` (id, description, modifier, update_datetime, create_datetime, deptName, orderNum, owner, phone, email, status, creator_id, parentId_id, dept_belong_id) VALUES (16, '', 'admin', '2021-02-27 07:28:10.532392', '2021-02-27 07:28:10.532436', '财务部门', 2, NULL, NULL, NULL, '1', 1, 4, 16);
