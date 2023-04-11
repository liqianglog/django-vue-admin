import { defineStore } from 'pinia';
import Cookies from 'js-cookie';
import { UserInfosStates } from './interface';
import { Session } from '/@/utils/storage';
import { request } from '../utils/service';

/**
 * 用户信息
 * @methods setUserInfos 设置用户信息
 */
export const useUserInfo = defineStore('userInfo', {
	state: (): UserInfosStates => ({
		userInfos: {
			avatar: '',
			userName: '',
			name: '',
			email: '',
			mobile: '',
			gender: '',
			dept_info: {
				dept_id: 0,
				dept_name: '',
			},
			role_info: [
				{
					id: 0,
					name: '',
				},
			],
		},
	}),
	actions: {
		async setUserInfos() {
			// 存储用户信息到浏览器缓存
			if (Session.get('userInfo')) {
				this.userInfos = Session.get('userInfo');
			} else {
				let userInfos: any = await this.getApiUserInfo();
				this.userInfos.userName = userInfos.data.name;
				this.userInfos.avatar =
					userInfos.data.avatar || 'https://img2.baidu.com/it/u=1978192862,2048448374&fm=253&fmt=auto&app=138&f=JPEG?w=504&h=500';
				this.userInfos.name = userInfos.data.name;
				this.userInfos.email = userInfos.data.email;
				this.userInfos.mobile = userInfos.data.mobile;
				this.userInfos.gender = userInfos.data.gender;
				this.userInfos.dept_info = userInfos.data.dept_info;
				this.userInfos.role_info = userInfos.data.role_info;
				Session.set('userInfo', this.userInfos);
			}
		},
		async getApiUserInfo() {
			return request({
				url: '/api/system/user/user_info/',
				method: 'get',
			});
		},
	},
});
