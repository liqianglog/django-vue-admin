-- ----------------------------
-- 角色管理 初始化
-- Table structure for permission_role
-- ----------------------------
-- DROP TABLE IF EXISTS `permission_role`;
-- CREATE TABLE `permission_role` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `description` longtext,
--   `creator` varchar(255) DEFAULT NULL,
--   `modifier` varchar(255) DEFAULT NULL,
--   `update_datetime` datetime(6) DEFAULT NULL,
--   `create_datetime` datetime(6) DEFAULT NULL,
--   `roleName` varchar(64) NOT NULL,
--   `roleKey` varchar(64) NOT NULL,
--   `roleSort` int(11) NOT NULL,
--   `status` varchar(8) NOT NULL,
--   `admin` tinyint(1) NOT NULL,
--   `dataScope` varchar(8) NOT NULL,
--   `remark` longtext,
--   PRIMARY KEY (`id`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of permission_role
-- ----------------------------
INSERT INTO `permission_role` VALUES (1, '', 'admin', 'admin', '2021-02-27 08:48:23.225361', '2021-02-27 08:48:08.064911', '超级管理员', 'admin', 1, '1', 1, '2', NULL);
INSERT INTO `permission_role` VALUES (2, '', 'admin', 'admin', '2021-02-27 08:49:05.149632', '2021-02-27 08:48:47.317214', '普通角色', 'common', 2, '1', 0, '2', NULL);

-- ----------------------------
-- Table structure for permission_role_dept
-- ----------------------------
-- DROP TABLE IF EXISTS `permission_role_dept`;
-- CREATE TABLE `permission_role_dept` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `role_id` int(11) NOT NULL,
--   `dept_id` int(11) NOT NULL,
--   PRIMARY KEY (`id`),
--   UNIQUE KEY `permission_role_dept_role_id_dept_id_1d89afeb_uniq` (`role_id`,`dept_id`),
--   KEY `permission_role_dept_role_id_99a9f232` (`role_id`) USING BTREE,
--   KEY `permission_role_dept_dept_id_cbe9076a` (`dept_id`) USING BTREE
-- ) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of permission_role_dept
-- ----------------------------
INSERT INTO `permission_role_dept` VALUES (1, 1, 1);
INSERT INTO `permission_role_dept` VALUES (2, 1, 2);
INSERT INTO `permission_role_dept` VALUES (3, 1, 3);
INSERT INTO `permission_role_dept` VALUES (4, 1, 4);
INSERT INTO `permission_role_dept` VALUES (5, 1, 5);
INSERT INTO `permission_role_dept` VALUES (6, 1, 6);
INSERT INTO `permission_role_dept` VALUES (7, 1, 7);
INSERT INTO `permission_role_dept` VALUES (8, 1, 8);
INSERT INTO `permission_role_dept` VALUES (9, 1, 9);
INSERT INTO `permission_role_dept` VALUES (10, 1, 10);
INSERT INTO `permission_role_dept` VALUES (11, 1, 11);
INSERT INTO `permission_role_dept` VALUES (12, 1, 12);
INSERT INTO `permission_role_dept` VALUES (13, 1, 13);
INSERT INTO `permission_role_dept` VALUES (14, 1, 14);
INSERT INTO `permission_role_dept` VALUES (15, 1, 15);
INSERT INTO `permission_role_dept` VALUES (16, 1, 16);
INSERT INTO `permission_role_dept` VALUES (17, 2, 1);
INSERT INTO `permission_role_dept` VALUES (18, 2, 2);
INSERT INTO `permission_role_dept` VALUES (19, 2, 3);
INSERT INTO `permission_role_dept` VALUES (20, 2, 4);
INSERT INTO `permission_role_dept` VALUES (21, 2, 5);
INSERT INTO `permission_role_dept` VALUES (22, 2, 6);
INSERT INTO `permission_role_dept` VALUES (23, 2, 7);
INSERT INTO `permission_role_dept` VALUES (24, 2, 8);
INSERT INTO `permission_role_dept` VALUES (25, 2, 9);
INSERT INTO `permission_role_dept` VALUES (26, 2, 10);
INSERT INTO `permission_role_dept` VALUES (27, 2, 11);
INSERT INTO `permission_role_dept` VALUES (28, 2, 12);
INSERT INTO `permission_role_dept` VALUES (29, 2, 13);
INSERT INTO `permission_role_dept` VALUES (30, 2, 14);
INSERT INTO `permission_role_dept` VALUES (31, 2, 15);
INSERT INTO `permission_role_dept` VALUES (32, 2, 16);

-- ----------------------------
-- Table structure for permission_role_menu
-- ----------------------------
-- DROP TABLE IF EXISTS `permission_role_menu`;
-- CREATE TABLE `permission_role_menu` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `role_id` int(11) NOT NULL,
--   `menu_id` int(11) NOT NULL,
--   PRIMARY KEY (`id`),
--   UNIQUE KEY `permission_role_menu_role_id_menu_id_bb9e5441_uniq` (`role_id`,`menu_id`),
--   KEY `permission_role_menu_role_id_33541d2b` (`role_id`) USING BTREE,
--   KEY `permission_role_menu_menu_id_0c24555f` (`menu_id`) USING BTREE
-- ) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of permission_role_menu
-- ----------------------------
INSERT INTO `permission_role_menu` VALUES (1, 1, 1);
INSERT INTO `permission_role_menu` VALUES (2, 1, 2);
INSERT INTO `permission_role_menu` VALUES (3, 1, 3);
INSERT INTO `permission_role_menu` VALUES (4, 1, 4);
INSERT INTO `permission_role_menu` VALUES (5, 1, 5);
INSERT INTO `permission_role_menu` VALUES (6, 1, 6);
INSERT INTO `permission_role_menu` VALUES (7, 1, 7);
INSERT INTO `permission_role_menu` VALUES (8, 1, 8);
INSERT INTO `permission_role_menu` VALUES (9, 1, 9);
INSERT INTO `permission_role_menu` VALUES (10, 1, 10);
INSERT INTO `permission_role_menu` VALUES (21, 1, 11);
INSERT INTO `permission_role_menu` VALUES (22, 1, 13);
INSERT INTO `permission_role_menu` VALUES (23, 1, 14);
INSERT INTO `permission_role_menu` VALUES (24, 1, 15);
INSERT INTO `permission_role_menu` VALUES (25, 1, 16);
INSERT INTO `permission_role_menu` VALUES (26, 1, 17);
INSERT INTO `permission_role_menu` VALUES (27, 1, 18);
INSERT INTO `permission_role_menu` VALUES (28, 1, 19);
INSERT INTO `permission_role_menu` VALUES (29, 1, 20);
INSERT INTO `permission_role_menu` VALUES (30, 1, 21);
INSERT INTO `permission_role_menu` VALUES (31, 1, 22);
INSERT INTO `permission_role_menu` VALUES (32, 1, 23);
INSERT INTO `permission_role_menu` VALUES (33, 1, 24);
INSERT INTO `permission_role_menu` VALUES (34, 1, 25);
INSERT INTO `permission_role_menu` VALUES (35, 1, 26);
INSERT INTO `permission_role_menu` VALUES (36, 1, 27);
INSERT INTO `permission_role_menu` VALUES (37, 1, 28);
INSERT INTO `permission_role_menu` VALUES (38, 1, 29);
INSERT INTO `permission_role_menu` VALUES (39, 1, 30);
INSERT INTO `permission_role_menu` VALUES (40, 1, 31);
INSERT INTO `permission_role_menu` VALUES (41, 1, 32);
INSERT INTO `permission_role_menu` VALUES (42, 1, 33);
INSERT INTO `permission_role_menu` VALUES (43, 1, 34);
INSERT INTO `permission_role_menu` VALUES (44, 1, 35);
INSERT INTO `permission_role_menu` VALUES (45, 1, 36);
INSERT INTO `permission_role_menu` VALUES (46, 1, 37);
INSERT INTO `permission_role_menu` VALUES (47, 1, 38);
INSERT INTO `permission_role_menu` VALUES (48, 1, 39);
INSERT INTO `permission_role_menu` VALUES (49, 1, 40);
INSERT INTO `permission_role_menu` VALUES (50, 1, 41);
INSERT INTO `permission_role_menu` VALUES (51, 1, 42);
INSERT INTO `permission_role_menu` VALUES (52, 1, 43);
INSERT INTO `permission_role_menu` VALUES (53, 1, 44);
INSERT INTO `permission_role_menu` VALUES (54, 1, 45);
INSERT INTO `permission_role_menu` VALUES (55, 1, 46);
INSERT INTO `permission_role_menu` VALUES (11, 2, 1);
INSERT INTO `permission_role_menu` VALUES (12, 2, 2);
INSERT INTO `permission_role_menu` VALUES (13, 2, 3);
INSERT INTO `permission_role_menu` VALUES (14, 2, 4);
INSERT INTO `permission_role_menu` VALUES (15, 2, 5);
INSERT INTO `permission_role_menu` VALUES (16, 2, 6);
INSERT INTO `permission_role_menu` VALUES (17, 2, 7);
INSERT INTO `permission_role_menu` VALUES (18, 2, 8);
INSERT INTO `permission_role_menu` VALUES (19, 2, 9);
INSERT INTO `permission_role_menu` VALUES (20, 2, 10);
