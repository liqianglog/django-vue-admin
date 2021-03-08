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
INSERT INTO `permission_menu` VALUES (1, '', 'admin', '2021-02-27 07:50:00.410101', '2021-02-27 07:41:28.660364', '0', 'system', '系统管理', 1, '1', '/system', '', '', 'GET', NULL, '1', '1', '1', 1, NULL);
INSERT INTO `permission_menu` VALUES (2, '', 'admin', '2021-02-27 07:51:14.500722', '2021-02-27 07:51:14.500768', '0', 'peoples', '权限管理', 2, '1', '/permission', '', '', 'GET', NULL, '1', '1', '1', 1, NULL);
INSERT INTO `permission_menu` VALUES (3, '', 'admin', '2021-02-27 08:20:40.164651', '2021-02-27 07:54:38.630670', '1', 'dict', '字典管理', 1, '1', '/system/dict', 'system/dict/index', 'system/dict/type', 'GET', 'system:dict:type:get', '1', '1', '1', 1, 1);
INSERT INTO `permission_menu` VALUES (4, '', 'admin', '2021-02-27 08:24:03.776515', '2021-02-27 08:06:51.019173', '1', 'edit', '参数管理', 2, '1', '/system/config', 'system/config/index', 'system/config/', 'GET', 'system:config:get', '1', '1', '1', 1, 1);
INSERT INTO `permission_menu` VALUES (5, '', 'admin', '2021-02-27 08:26:56.407590', '2021-02-27 08:25:37.339270', '1', 'post', '岗位管理', 1, '1', '/permission/post', 'permission/post/index', 'permission/post', 'GET', 'permission:post:get', '1', '1', '1', 1, 2);
INSERT INTO `permission_menu` VALUES (6, '', 'admin', '2021-02-27 08:26:48.454509', '2021-02-27 08:26:48.454553', '1', 'tree', '部门管理', 2, '1', '/permission/dept', 'permission/dept/index', 'permission/dept', 'GET', 'permission:dept:get', '1', '1', '1', 1, 2);
INSERT INTO `permission_menu` VALUES (7, '', 'admin', '2021-02-27 08:28:20.411115', '2021-02-27 08:28:20.411164', '1', 'tree-table', '菜单管理', 3, '1', '/permission/menu', 'permission/menu/index', 'permission/menus', 'GET', 'permission:menus:get', '1', '1', '1', 1, 2);
INSERT INTO `permission_menu` VALUES (8, '', 'admin', '2021-02-27 08:29:30.153322', '2021-02-27 08:29:30.153361', '1', 'peoples', '角色管理', 4, '1', '/permission/role', 'permission/role/index', 'permission/role', 'GET', 'permission:role:get', '1', '1', '1', 1, 2);
INSERT INTO `permission_menu` VALUES (9, '', 'admin', '2021-02-27 08:30:14.030845', '2021-02-27 08:30:14.030888', '1', 'user', '用户管理', 5, '1', '/permission/user', 'permission/user/index', 'permission/user', 'GET', 'permission:user:get', '1', '1', '1', 1, 2);
INSERT INTO `permission_menu` VALUES (10, '', 'admin', '2021-02-27 08:37:24.948235', '2021-02-27 08:36:04.824117', '0', 'guide', 'dvAdmin官网', 9, '0', 'https://django-vue-admin.com', '', NULL, 'GET', NULL, '1', '1', '1', 1, NULL);
INSERT INTO `permission_menu` VALUES (11, '', 'admin', '2021-02-27 16:19:21.529666', '2021-02-27 16:17:36.685174', '1', 'job', '文件管理', 3, '1', '/system/savefile', 'system/savefile/index', '/system/savefile', 'GET', 'system:savefile:get', '1', '1', '1', 1, 1);
INSERT INTO `permission_menu` VALUES (13, '', 'admin', '2021-03-03 14:41:08.227821', '2021-03-03 14:18:52.530449', '2', NULL, '用户新增', 1, '1', NULL, NULL, '/permission/user/', 'POST', 'permission:user:post', '1', '1', '1', 1, 9);
INSERT INTO `permission_menu` VALUES (14, '', 'admin', '2021-03-03 14:43:34.207938', '2021-03-03 14:43:34.208093', '2', NULL, '用户修改', 2, '1', NULL, NULL, '/permission/user/{id}/', 'PUT', 'permission:user:{id}:put', '1', '1', '1', 1, 9);
INSERT INTO `permission_menu` VALUES (15, '', 'admin', '2021-03-03 14:44:58.006289', '2021-03-03 14:44:58.006338', '2', NULL, '用户删除', 3, '1', '', NULL, '/permission/user/{id}/', 'DELETE', 'permission:user:{id}:delete', '1', '1', '1', 1, 9);
INSERT INTO `permission_menu` VALUES (16, '', 'admin', '2021-03-03 14:45:50.575443', '2021-03-03 14:45:50.575507', '2', NULL, '用户导出', 4, '1', NULL, NULL, '/permission/user/export/', 'GET', 'permission:user:export:get', '1', '1', '1', 1, 9);
INSERT INTO `permission_menu` VALUES (17, '', 'admin', '2021-03-03 14:51:14.157310', '2021-03-03 14:51:14.157447', '2', NULL, '用户导入', 5, '1', NULL, NULL, '/permission/user/import/', 'POST', 'permission:user:import:post', '1', '1', '1', 1, 9);
INSERT INTO `permission_menu` VALUES (18, '', 'admin', '2021-03-03 14:51:51.220886', '2021-03-03 14:51:51.220933', '2', NULL, '重置密码', 6, '1', NULL, NULL, '/permission/user/resetPwd/', 'PUT', 'permission:user:resetpwd:put', '1', '1', '1', 1, 9);
INSERT INTO `permission_menu` VALUES (19, '', 'admin', '2021-03-03 14:53:47.877063', '2021-03-03 14:53:47.877116', '2', NULL, '角色新增', 1, '1', NULL, NULL, '/permission/role/', 'POST', 'permission:role:post', '1', '1', '1', 1, 8);
INSERT INTO `permission_menu` VALUES (20, '', 'admin', '2021-03-03 14:54:28.794968', '2021-03-03 14:54:28.795015', '2', NULL, '角色修改', 2, '1', NULL, NULL, '/permission/role/{id}/', 'PUT', 'permission:role:{id}:put', '1', '1', '1', 1, 8);
INSERT INTO `permission_menu` VALUES (21, '', 'admin', '2021-03-03 14:58:00.798718', '2021-03-03 14:58:00.798813', '2', NULL, '删除角色', 3, '1', NULL, NULL, '/permission/role/{id}/', 'DELETE', 'permission:role:{id}:delete', '1', '1', '1', 1, 8);
INSERT INTO `permission_menu` VALUES (22, '', 'admin', '2021-03-03 14:58:28.940577', '2021-03-03 14:58:28.940625', '2', NULL, '角色导出', 4, '1', NULL, NULL, '/permission/role/export/', 'GET', 'permission:role:export:get', '1', '1', '1', 1, 8);
INSERT INTO `permission_menu` VALUES (23, '', 'admin', '2021-03-03 15:00:41.081771', '2021-03-03 15:00:41.081832', '2', NULL, '菜单新增', 1, '1', NULL, NULL, '/permission/menus/', 'POST', 'permission:menus:post', '1', '1', '1', 1, 7);
INSERT INTO `permission_menu` VALUES (24, '', 'admin', '2021-03-03 15:01:03.178824', '2021-03-03 15:01:03.178874', '2', NULL, '菜单修改', 2, '1', NULL, NULL, '/permission/menus/{id}/', 'PUT', 'permission:menus:{id}:put', '1', '1', '1', 1, 7);
INSERT INTO `permission_menu` VALUES (25, '', 'admin', '2021-03-03 15:02:56.123525', '2021-03-03 15:02:56.123571', '2', NULL, '菜单删除', 3, '1', NULL, NULL, '/permission/menus/{id}/', 'DELETE', 'permission:menus:{id}:delete', '1', '1', '1', 1, 7);
INSERT INTO `permission_menu` VALUES (26, '', 'admin', '2021-03-03 15:04:35.191774', '2021-03-03 15:04:35.191856', '2', NULL, '部门新增', 1, '1', NULL, NULL, '/permission/dept/', 'POST', 'permission:dept:post', '1', '1', '1', 1, 6);
INSERT INTO `permission_menu` VALUES (27, '', 'admin', '2021-03-03 15:04:56.963168', '2021-03-03 15:04:56.963214', '2', NULL, '部门修改', 2, '1', NULL, NULL, '/permission/dept/{id}/', 'PUT', 'permission:dept:{id}:put', '1', '1', '1', 1, 6);
INSERT INTO `permission_menu` VALUES (28, '', 'admin', '2021-03-03 15:05:39.602577', '2021-03-03 15:05:39.602622', '2', NULL, '部门删除', 3, '1', NULL, NULL, '/permission/dept/{id}/', 'DELETE', 'permission:dept:{id}:delete', '1', '1', '1', 1, 6);
INSERT INTO `permission_menu` VALUES (29, '', 'admin', '2021-03-03 15:06:50.095341', '2021-03-03 15:06:50.095388', '2', NULL, '岗位新增', 1, '1', NULL, NULL, '/permission/post/', 'POST', 'permission:post:post', '1', '1', '1', 1, 5);
INSERT INTO `permission_menu` VALUES (30, '', 'admin', '2021-03-03 15:07:36.013313', '2021-03-03 15:07:36.013358', '2', NULL, '岗位修改', 2, '1', NULL, NULL, '/permission/post/{id}/', 'PUT', 'permission:post:{id}:put', '1', '1', '1', 1, 5);
INSERT INTO `permission_menu` VALUES (31, '', 'admin', '2021-03-03 15:08:10.371530', '2021-03-03 15:08:10.371575', '2', NULL, '岗位删除', 3, '1', NULL, NULL, '/permission/post/{id}/', 'DELETE', 'permission:post:{id}:delete', '1', '1', '1', 1, 5);
INSERT INTO `permission_menu` VALUES (32, '', 'admin', '2021-03-03 15:09:02.213084', '2021-03-03 15:09:02.213131', '2', NULL, '岗位导出', 4, '1', NULL, NULL, '/permission/post/export/', 'GET', 'permission:post:export:get', '1', '1', '1', 1, 5);
INSERT INTO `permission_menu` VALUES (33, '', 'admin', '2021-03-03 15:11:37.616329', '2021-03-03 15:11:37.616415', '2', NULL, '字典新增', 1, '1', NULL, NULL, '/system/dict/type/', 'POST', 'system:dict:type:post', '1', '1', '1', 1, 3);
INSERT INTO `permission_menu` VALUES (34, '', 'admin', '2021-03-03 15:12:47.237658', '2021-03-03 15:12:47.237713', '2', NULL, '字典修改', 2, '1', NULL, NULL, '/system/dict/type/{id}/', 'PUT', 'system:dict:type:{id}:put', '1', '1', '1', 1, 3);
INSERT INTO `permission_menu` VALUES (35, '', 'admin', '2021-03-03 15:13:40.185174', '2021-03-03 15:13:40.185230', '2', NULL, '字典删除', 3, '1', NULL, NULL, '/system/dict/type/{id}/', 'DELETE', 'system:dict:type:{id}:delete', '1', '1', '1', 1, 3);
INSERT INTO `permission_menu` VALUES (36, '', 'admin', '2021-03-03 15:15:12.950584', '2021-03-03 15:15:12.950684', '2', NULL, '字典导出', 4, '1', NULL, NULL, '/system/dict/type/export/', 'GET', 'system:dict:type:export:get', '1', '1', '1', 1, 3);
INSERT INTO `permission_menu` VALUES (37, '', 'admin', '2021-03-03 15:16:54.709780', '2021-03-03 15:16:20.868146', '2', NULL, '清理缓存', 5, '1', NULL, NULL, '/system/dict/type/clearCache/', 'DELETE', 'system:dict:type:clearcache:delete', '1', '1', '1', 1, 3);
INSERT INTO `permission_menu` VALUES (38, '', 'admin', '2021-03-03 15:17:54.232085', '2021-03-03 15:17:54.232166', '2', NULL, '参数新增', 1, '1', NULL, NULL, '/system/config/', 'POST', 'system:config:post', '1', '1', '1', 1, 4);
INSERT INTO `permission_menu` VALUES (39, '', 'admin', '2021-03-03 15:18:37.088187', '2021-03-03 15:18:37.088237', '2', NULL, '参数修改', 2, '1', NULL, NULL, '/system/config/{id}/', 'PUT', 'system:config:{id}:put', '1', '1', '1', 1, 4);
INSERT INTO `permission_menu` VALUES (40, '', 'admin', '2021-03-03 15:19:05.532556', '2021-03-03 15:19:05.532616', '2', NULL, '参数删除', 3, '1', NULL, NULL, '/system/config/{id}/', 'DELETE', 'system:config:{id}:delete', '1', '1', '1', 1, 4);
INSERT INTO `permission_menu` VALUES (41, '', 'admin', '2021-03-03 15:19:49.576174', '2021-03-03 15:19:49.576221', '2', NULL, '参数导出', 4, '1', NULL, NULL, '/system/config/export/', 'GET', 'system:config:export:get', '1', '1', '1', 1, 4);
INSERT INTO `permission_menu` VALUES (42, '', 'admin', '2021-03-03 15:21:20.098250', '2021-03-03 15:21:20.098345', '2', NULL, '清理缓存', 5, '1', NULL, NULL, '/system/config/clearCache/', 'DELETE', 'system:config:clearcache:delete', '1', '1', '1', 1,4);
INSERT INTO `permission_menu` VALUES (43, '', 'admin', '2021-03-03 15:22:48.492613', '2021-03-03 15:22:48.492666', '2', NULL, '文件上传', 1, '1', NULL, NULL, '/system/savefile/', 'POST', 'system:savefile:post', '1', '1', '1', 1, 11);
INSERT INTO `permission_menu` VALUES (44, '', 'admin', '2021-03-03 15:23:58.219105', '2021-03-03 15:23:58.219155', '2', NULL, '文件删除', 2, '1', NULL, NULL, '/system/savefile/{id}/', 'DELETE', 'system:savefile:{id}:delete', '1', '1', '1', 1, 11);
INSERT INTO `permission_menu` VALUES (45, '', 'admin', '2021-03-03 15:25:15.224971', '2021-03-03 15:25:15.225018', '2', NULL, '清理废弃文件', 3, '1', NULL, NULL, '/system/clearsavefile/', 'POST', 'system:clearsavefile:post', '1', '1', '1', 1, 11);
INSERT INTO `permission_menu` VALUES (46, '', 'admin', '2021-03-03 15:28:30.061632', '2021-03-03 15:27:19.945663', '2', NULL, '文件下载', 4, '1', NULL, NULL, NULL, 'GET', 'system:clearsavefile:download:post', '1', '1', '1', 1, 11);
INSERT INTO `permission_menu` VALUES (47, '', 'admin', '2021-03-07 14:35:34.237127', '2021-03-07 14:32:06.754815', '1', 'message', '消息通知', 4, '1', 'system/message', 'system/message/index', '/system/message/', 'GET', 'system:message:get', '1', '1', '1', 1, 1);
INSERT INTO `permission_menu` VALUES (48, '', 'admin', '2021-03-07 14:35:06.718432', '2021-03-07 14:35:06.718463', '2', NULL, '发布通知', 1, '1', NULL, NULL, '/system/message/', 'POST', 'system:message:post', '1', '1', '1', 1, 47);
INSERT INTO `permission_menu` VALUES (49, '', 'admin', '2021-03-07 14:36:47.675806', '2021-03-07 14:36:47.675837', '2', NULL, '修改通知', 2, '1', NULL, NULL, '/system/message/', 'PUT', 'system:message:put', '1', '1', '1', 1, 47);
INSERT INTO `permission_menu` VALUES (50, '', 'admin', '2021-03-07 14:37:52.130536', '2021-03-07 14:37:52.130567', '2', NULL, '删除通知', 3, '1', NULL, NULL, '/permission/menu/', 'DELETE', 'permission:menu:delete', '1', '1', '1', 1, 47);
INSERT INTO `permission_menu` VALUES (51, '', 'admin', '2021-03-07 14:42:37.410336', '2021-03-07 14:42:37.410366', '2', NULL, '通知导出', 4, '1', NULL, NULL, '/system/message/export/', 'GET', 'system:message:export:get', '1', '1', '1', 1, 47);
