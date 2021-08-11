-- ----------------------------
-- 用户管理 初始化sql
-- Table structure for permission_userprofile
-- ----------------------------
-- DROP TABLE IF EXISTS `permission_userprofile`;
-- CREATE TABLE `permission_userprofile` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `password` varchar(128) NOT NULL,
--   `last_login` datetime(6) DEFAULT NULL,
--   `is_superuser` tinyint(1) NOT NULL,
--   `first_name` varchar(30) NOT NULL,
--   `last_name` varchar(150) NOT NULL,
--   `is_staff` tinyint(1) NOT NULL,
--   `is_active` tinyint(1) NOT NULL,
--   `date_joined` datetime(6) NOT NULL,
--   `username` varchar(150) NOT NULL,
--   `secret` varchar(255) NOT NULL,
--   `email` varchar(255) DEFAULT NULL,
--   `mobile` varchar(255) DEFAULT NULL,
--   `avatar` longtext,
--   `name` varchar(40) NOT NULL,
--   `gender` varchar(8) CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci DEFAULT NULL,
--   `remark` longtext,
--   `user_type` int(11) NOT NULL,
--   `create_datetime` datetime(6) DEFAULT NULL,
--   `update_datetime` datetime(6) DEFAULT NULL,
--   `dept_id` int(11) DEFAULT NULL,
--   PRIMARY KEY (`id`),
--   UNIQUE KEY `username` (`username`),
--   KEY `permission_userprofile_dept_id_bd5c7976` (`dept_id`) USING BTREE
-- ) ENGINE=InnoDB AUTO_INCREMENT=2 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of permission_userprofile
-- ----------------------------
INSERT INTO `permission_userprofile` (id, password, last_login, is_superuser, first_name, last_name, is_staff, is_active, date_joined, username, secret, email, mobile, avatar, name, gender, remark, user_type, create_datetime, update_datetime, dept_id, dept_belong_id, creator_id) VALUES (1, 'pbkdf2_sha256$150000$X0RG2idBumnn$TaMaXFquGzyDtytL3ofZG/sSN+1VR521A9xLkUPxYI4=', '2021-02-27 06:20:28.214775', 1, '', '', 1, 1, '2021-02-27 06:20:09.188689', 'admin', '3704adf3-380f-4c27-a8da-60420e8cb4ab', 'admin@qq.com', NULL, NULL, '管理员', '2', '1', 2, '2021-02-27 06:20:09.263192', '2021-02-27 09:14:30.009998', 1, 1, 1);
INSERT INTO `permission_userprofile` (id, password, last_login, is_superuser, first_name, last_name, is_staff, is_active, date_joined, username, secret, email, mobile, avatar, name, gender, remark, user_type, create_datetime, update_datetime, dept_id, dept_belong_id, creator_id) VALUES (2, 'pbkdf2_sha256$150000$vWY1VIn7rEJz$qq2iiADgcGumy9kNU1FSBhktcimaudYICviCcOKzfKY=', NULL, 0, '', '', 0, 1, '2021-03-03 15:38:27.009893', 'dvadmin', 'b4c5d79a-f01c-4244-92f8-b5288eca1d50', NULL, NULL, NULL, '普通用户', '2', NULL, 0, '2021-03-03 15:38:27.010771', '2021-03-03 15:38:27.086069', 1, 1, 1);
-- ----------------------------
-- Table structure for permission_userprofile_post
-- ----------------------------
-- DROP TABLE IF EXISTS `permission_userprofile_post`;
-- CREATE TABLE `permission_userprofile_post` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `userprofile_id` int(11) NOT NULL,
--   `post_id` int(11) NOT NULL,
--   PRIMARY KEY (`id`),
--   UNIQUE KEY `permission_userprofile_post_userprofile_id_post_id_b9fb91e9_uniq` (`userprofile_id`,`post_id`),
--   KEY `permission_userprofile_post_userprofile_id_229fe756` (`userprofile_id`) USING BTREE,
--   KEY `permission_userprofile_post_post_id_dda441c3` (`post_id`) USING BTREE
-- ) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of permission_userprofile_post
-- ----------------------------
INSERT INTO `permission_userprofile_post` (id, userprofile_id, post_id) VALUES (1, 1, 1);
INSERT INTO `permission_userprofile_post` (id, userprofile_id, post_id) VALUES (2, 2, 4);

-- ----------------------------
-- Table structure for permission_userprofile_role
-- ----------------------------
-- DROP TABLE IF EXISTS `permission_userprofile_role`;
-- CREATE TABLE `permission_userprofile_role` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `userprofile_id` int(11) NOT NULL,
--   `role_id` int(11) NOT NULL,
--   PRIMARY KEY (`id`),
--   UNIQUE KEY `permission_userprofile_role_userprofile_id_role_id_70affc5e_uniq` (`userprofile_id`,`role_id`),
--   KEY `permission_userprofile_role_userprofile_id_66835002` (`userprofile_id`) USING BTREE,
--   KEY `permission_userprofile_role_role_id_e91fd02e` (`role_id`) USING BTREE
-- ) ENGINE=InnoDB AUTO_INCREMENT=3 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of permission_userprofile_role
-- ----------------------------
INSERT INTO `permission_userprofile_role` (id, userprofile_id, role_id) VALUES (1, 1, 1);
INSERT INTO `permission_userprofile_role` (id, userprofile_id, role_id) VALUES (2, 2, 2);
