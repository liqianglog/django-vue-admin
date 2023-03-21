import { defineStore } from 'pinia';
import { ConfigStates } from './interface';
import { request } from '../utils/service';

export const urlPrefix = '/api/system/system_config/';

/**
 * 系统配置数据
 * @methods getSystemConfig 获取系统配置数据
 */
export const SystemConfigStore = defineStore('SystemConfig', {
	state: (): ConfigStates => ({
		systemConfig: {},
	}),
	actions: {
		async getSystemConfigs() {
			request({
				url: urlPrefix,
				method: 'get',
			}).then((ret: { data: [] }) => {
				// 转换数据格式并保存到pinia
				let dataList = ret.data;
				dataList.forEach((item: any) => {
					let childrens = item.children;
					if (childrens.length > 1) {
						this.systemConfig[item.key] = childrens;
					} else {
						this.systemConfig[item.key] = item.value;
					}
				});
			});
		},
	},
	persist: {
		enabled: true,
	},
});
