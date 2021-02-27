-- ----------------------------
-- 菜单管理初始化sql
-- Table structure for permission_menu
-- ----------------------------
-- DROP TABLE IF EXISTS `permission_menu`;
-- CREATE TABLE `permission_menu` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `description` longtext,
--   `creator` varchar(255) DEFAULT NULL,
--   `modifier` varchar(255) DEFAULT NULL,
--   `update_datetime` datetime(6) DEFAULT NULL,
--   `create_datetime` datetime(6) DEFAULT NULL,
--   `menuType` varchar(8) NOT NULL,
--   `icon` varchar(64) DEFAULT NULL,
--   `name` varchar(64) NOT NULL,
--   `orderNum` int(11) NOT NULL,
--   `isFrame` varchar(8) NOT NULL,
--   `web_path` varchar(128) DEFAULT NULL,
--   `component_path` varchar(128) DEFAULT NULL,
--   `interface_path` varchar(256) DEFAULT NULL,
--   `interface_method` varchar(16) NOT NULL,
--   `perms` varchar(256) DEFAULT NULL,
--   `status` varchar(8) NOT NULL,
--   `visible` varchar(8) NOT NULL,
--   `isCache` varchar(8) NOT NULL,
--   `parentId_id` int(11) DEFAULT NULL,
--   PRIMARY KEY (`id`),
--   KEY `permission_menu_parentId_id_df49c7ef_fk_permission_menu_id` (`parentId_id`),
--   CONSTRAINT `permission_menu_parentId_id_df49c7ef_fk_permission_menu_id` FOREIGN KEY (`parentId_id`) REFERENCES `permission_menu` (`id`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=11 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of permission_menu
-- ----------------------------
INSERT INTO `permission_menu` VALUES (1, '', 'admin', 'admin', '2021-02-27 07:50:00.410101', '2021-02-27 07:41:28.660364', '0', 'system', '系统管理', 1, '1', '/system', '', '', 'GET', NULL, '1', '1', '1', NULL);
INSERT INTO `permission_menu` VALUES (2, '', 'admin', 'admin', '2021-02-27 07:51:14.500722', '2021-02-27 07:51:14.500768', '0', 'peoples', '权限管理', 2, '1', '/permission', '', '', 'GET', NULL, '1', '1', '1', NULL);
INSERT INTO `permission_menu` VALUES (3, '', 'admin', 'admin', '2021-02-27 08:20:40.164651', '2021-02-27 07:54:38.630670', '1', 'dict', '字典管理', 1, '1', '/system/dict', 'system/dict/index', 'system/dict/type', 'GET', 'system:dict:type:get', '1', '1', '1', 1);
INSERT INTO `permission_menu` VALUES (4, '', 'admin', 'admin', '2021-02-27 08:24:03.776515', '2021-02-27 08:06:51.019173', '1', 'edit', '参数管理', 2, '1', '/system/config', 'system/config/index', 'system/config/', 'GET', 'system:config:get', '1', '1', '1', 1);
INSERT INTO `permission_menu` VALUES (5, '', 'admin', 'admin', '2021-02-27 08:26:56.407590', '2021-02-27 08:25:37.339270', '1', 'post', '岗位管理', 1, '1', '/permission/post', 'permission/post/index', 'permission/post', 'GET', 'permission:post:get', '1', '1', '1', 2);
INSERT INTO `permission_menu` VALUES (6, '', 'admin', 'admin', '2021-02-27 08:26:48.454509', '2021-02-27 08:26:48.454553', '1', 'tree', '部门管理', 2, '1', '/permission/dept', 'permission/dept/index', 'permission/dept', 'GET', 'permission:dept:get', '1', '1', '1', 2);
INSERT INTO `permission_menu` VALUES (7, '', 'admin', 'admin', '2021-02-27 08:28:20.411115', '2021-02-27 08:28:20.411164', '1', 'tree-table', '菜单管理', 3, '1', '/permission/menu', 'permission/menu/index', 'permission/menus', 'GET', 'permission:menus:get', '1', '1', '1', 2);
INSERT INTO `permission_menu` VALUES (8, '', 'admin', 'admin', '2021-02-27 08:29:30.153322', '2021-02-27 08:29:30.153361', '1', 'peoples', '角色管理', 4, '1', '/permission/role', 'permission/role/index', 'permission/role', 'GET', 'permission:role:get', '1', '1', '1', 2);
INSERT INTO `permission_menu` VALUES (9, '', 'admin', 'admin', '2021-02-27 08:30:14.030845', '2021-02-27 08:30:14.030888', '1', 'user', '用户管理', 5, '1', '/permission/user', 'permission/user/index', 'permission/user', 'GET', 'permission:user:get', '1', '1', '1', 2);
INSERT INTO `permission_menu` VALUES (10, '', 'admin', 'admin', '2021-02-27 08:37:24.948235', '2021-02-27 08:36:04.824117', '0', 'guide', 'dvAdmin官网', 9, '0', 'https://django-vue-admin.com', '', NULL, 'GET', NULL, '1', '1', '1', NULL);
