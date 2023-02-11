import * as api from './api';
import { dict, PageQuery, AddReq, DelReq, EditReq, CrudExpose, CrudOptions } from '@fast-crud/fast-crud';
import { request } from '/@/utils/service';
import { dictionary } from '/@/utils/dictionary';
interface CreateCrudOptionsTypes {
	crudOptions: CrudOptions;
}

export const createCrudOptions = function ({ crudExpose }: { crudExpose: CrudExpose }): CreateCrudOptionsTypes {
	const pageRequest = async (query: PageQuery) => {
		return await api.GetList(query);
	};
	const editRequest = async ({ form, row }: EditReq) => {
		form.id = row.id;
		return await api.UpdateObj(form);
	};
	const delRequest = async ({ row }: DelReq) => {
		return await api.DelObj(row.id);
	};
	const addRequest = async ({ form }: AddReq) => {
		return await api.AddObj(form);
	};
	return {
		crudOptions: {
			request: {
				pageRequest,
				addRequest,
				editRequest,
				delRequest,
			},
			actionbar: {
				buttons: {
					add: {
						show: false,
					},
				},
			},
			rowHandle: {
				buttons: {
					edit: {
						show: false,
					},
					remove: {
						show: false,
					},
				},
			},
			columns: {
				_index: {
					title: '序号',
					form: { show: false },
					column: {
						//type: 'index',
						align: 'center',
						width: '70px',
						columnSetDisabled: true, //禁止在列设置中选择
						formatter: (context) => {
							//计算序号,你可以自定义计算规则，此处为翻页累加
							let index = context.index ?? 1;
							let pagination = crudExpose.crudBinding.value.pagination;
							return ((pagination.currentPage ?? 1) - 1) * pagination.pageSize + index + 1;
						},
					},
				},
				search: {
					title: '关键词',
					column: {
						show: false,
					},
					search: {
						show: true,
						component: {
							props: {
								clearable: true,
							},
							placeholder: '请输入关键词',
						},
					},
					form: {
						show: false,
						component: {
							props: {
								clearable: true,
							},
						},
					},
				},
				username: {
					title: '登录用户名',
					search: {
						disabled: false,
					},
					width: 140,
					type: 'input',
					form: {
						disabled: true,
						component: {
							placeholder: '请输入登录用户名',
						},
					},
				},
				ip: {
					title: '登录ip',
					search: {
						disabled: false,
					},
					width: 130,
					type: 'input',
					form: {
						disabled: true,
						component: {
							placeholder: '请输入登录ip',
						},
					},
				},
				isp: {
					title: '运营商',
					search: {
						disabled: true,
					},
					disabled: true,
					width: 180,
					type: 'input',
					form: {
						component: {
							placeholder: '请输入运营商',
						},
					},
				},
				continent: {
					title: '大州',
					width: 80,
					type: 'input',
					form: {
						disabled: true,
						component: {
							placeholder: '请输入大州',
						},
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				country: {
					title: '国家',
					width: 80,
					type: 'input',
					form: {
						component: {
							placeholder: '请输入国家',
						},
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				province: {
					title: '省份',
					width: 80,
					type: 'input',
					form: {
						component: {
							placeholder: '请输入省份',
						},
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				city: {
					title: '城市',
					width: 80,
					type: 'input',
					form: {
						component: {
							placeholder: '请输入城市',
						},
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				district: {
					title: '县区',
					key: '',
					width: 80,
					type: 'input',
					form: {
						component: {
							placeholder: '请输入县区',
						},
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				area_code: {
					title: '区域代码',
					type: 'input',
					form: {
						component: {
							placeholder: '请输入区域代码',
						},
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				country_english: {
					title: '英文全称',
					width: 120,
					type: 'input',
					form: {
						component: {
							placeholder: '请输入英文全称',
						},
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				country_code: {
					title: '简称',
					type: 'input',
					form: {
						component: {
							placeholder: '请输入简称',
						},
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				longitude: {
					title: '经度',
					type: 'input',
					disabled: true,
					form: {
						component: {
							placeholder: '请输入经度',
						},
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				latitude: {
					title: '纬度',
					type: 'input',
					disabled: true,
					form: {
						component: {
							placeholder: '请输入纬度',
						},
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				login_type: {
					title: '登录类型',
					type: 'select',
					search: {
						disabled: false,
					},
					dict: {
						data: [
							{ label: '普通登录', value: 1 },
							{ label: '微信扫码登录', value: 2 },
						],
					},
					form: {
						component: {
							placeholder: '请选择登录类型',
						},
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				os: {
					title: '操作系统',
					type: 'input',
					form: {
						component: {
							placeholder: '请输入操作系统',
						},
					},
				},
				browser: {
					title: '浏览器名',
					type: 'input',
					form: {
						component: {
							placeholder: '请输入浏览器名',
						},
					},
				},
				agent: {
					title: 'agent信息',
					disabled: true,
					type: 'input',
					form: {
						component: {
							placeholder: '请输入agent信息',
						},
					},
				},
			},
		},
	};
};
