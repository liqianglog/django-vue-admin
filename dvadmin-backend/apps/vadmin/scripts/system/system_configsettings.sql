-- ----------------------------
-- 参数设置 初始化sql
-- Table structure for system_configsettings
-- ----------------------------
-- DROP TABLE IF EXISTS `system_configsettings`;
-- CREATE TABLE `system_configsettings` (
--   `id` int(11) NOT NULL AUTO_INCREMENT,
--   `description` longtext,
--   `creator` varchar(255) DEFAULT NULL,
--   `modifier` varchar(255) DEFAULT NULL,
--   `update_datetime` datetime(6) DEFAULT NULL,
--   `create_datetime` datetime(6) DEFAULT NULL,
--   `configName` varchar(64) NOT NULL,
--   `configKey` varchar(256) NOT NULL,
--   `configValue` varchar(256) NOT NULL,
--   `configType` varchar(8) NOT NULL,
--   `status` varchar(8) NOT NULL,
--   `remark` varchar(256) DEFAULT NULL,
--   PRIMARY KEY (`id`)
-- ) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

-- ----------------------------
-- Records of system_configsettings
-- ----------------------------
INSERT INTO `system_configsettings` (id, description, modifier, update_datetime, create_datetime, configName, configKey, configValue, configType, status, remark, creator_id, dept_belong_id) VALUES (1, '', 'admin', '2021-02-27 07:14:48.935587', '2021-02-27 07:14:48.935634', '主框架页-默认皮肤样式名称', 'sys.index.skinName', 'skin-blue', 'Y', '1', '蓝色 skin-blue、绿色 skin-green、紫色 skin-purple、红色 skin-red、黄色 skin-yellow', 1, 1);
INSERT INTO `system_configsettings` (id, description, modifier, update_datetime, create_datetime, configName, configKey, configValue, configType, status, remark, creator_id, dept_belong_id) VALUES (2, '', 'admin', '2021-02-27 07:15:14.039924', '2021-02-27 07:15:14.039967', '用户管理-账号初始密码', 'sys.user.initPassword', '123456', 'Y', '1', '初始化密码 123456', 1, 1);
INSERT INTO `system_configsettings` (id, description, modifier, update_datetime, create_datetime, configName, configKey, configValue, configType, status, remark, creator_id, dept_belong_id) VALUES (3, '', 'admin', '2021-02-27 07:15:36.091655', '2021-02-27 07:15:36.091694', '主框架页-侧边栏主题', 'sys.index.sideTheme', 'theme-dark', 'Y', '1', '深色主题theme-dark，浅色主题theme-light', 1, 1);
