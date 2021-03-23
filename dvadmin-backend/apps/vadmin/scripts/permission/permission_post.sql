-- ----------------------------
-- 岗位管理初始化sql
-- Table structure for permission_post
-- ----------------------------
-- DROP TABLE IF EXISTS `permission_post`;
-- CREATE TABLE `permission_post` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `description` longtext,
--   `creator` varchar(255) DEFAULT NULL,
--   `modifier` varchar(255) DEFAULT NULL,
--   `update_datetime` datetime(6) DEFAULT NULL,
--   `create_datetime` datetime(6) DEFAULT NULL,
--   `postName` varchar(64) NOT NULL,
--   `postCode` varchar(32) NOT NULL,
--   `postSort` int(11) NOT NULL,
--   `status` varchar(8) NOT NULL,
--   `remark` longtext,
--   PRIMARY KEY (`id`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of permission_post
-- ----------------------------
INSERT INTO `permission_post` (id, description, modifier, update_datetime, create_datetime, postName, postCode, postSort, status, remark, creator_id, dept_belong_id) VALUES (1, '', 'admin', '2021-02-27 07:16:10.725970', '2021-02-27 07:16:10.726016', '董事长', 'ceo', 1, '1', NULL, 1, 1);
INSERT INTO `permission_post` (id, description, modifier, update_datetime, create_datetime, postName, postCode, postSort, status, remark, creator_id, dept_belong_id) VALUES (2, '', 'admin', '2021-02-27 07:16:28.139648', '2021-02-27 07:16:28.139689', '项目经理', 'ce', 2, '1', NULL, 1, 1);
INSERT INTO `permission_post` (id, description, modifier, update_datetime, create_datetime, postName, postCode, postSort, status, remark, creator_id, dept_belong_id) VALUES (3, '', 'admin', '2021-02-27 07:16:39.843069', '2021-02-27 07:16:39.843114', '人力资源', 'hr', 3, '1', NULL, 1, 1);
INSERT INTO `permission_post` (id, description, modifier, update_datetime, create_datetime, postName, postCode, postSort, status, remark, creator_id, dept_belong_id) VALUES (4, '', 'admin', '2021-02-27 07:16:51.082769', '2021-02-27 07:16:51.082813', '普通员工', 'user', 4, '1', NULL, 1, 1);
