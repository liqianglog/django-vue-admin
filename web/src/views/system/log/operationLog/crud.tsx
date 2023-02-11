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
				request_modular: {
					title: '请求模块',
					search: {
						disabled: false,
					},
					type: 'input',
					form: {
						disabled: true,
						component: {
							placeholder: '请输入请求模块',
						},
					},
				},
				request_path: {
					title: '请求地址',
					search: {
						disabled: false,
					},
					type: 'input',
					form: {
						disabled: true,
						component: {
							placeholder: '请输入请求地址',
						},
					},
				},
				request_body: {
					column: {
						showOverflowTooltip: true,
						width: 200, //列宽
						minWidth: 100, //最小列宽
					},
					title: '请求参数',
					search: {
						disabled: true,
					},
					disabled: true,
					type: 'textarea',
					form: {
						component: {
							props: {
								type: 'textarea',
							},
							autosize: {
								minRows: 2,
								maxRows: 8,
							},
							placeholder: '请输入关键词',
						},
					},
				},
				request_method: {
					title: '请求方法',
					type: 'input',
					search: {
						disabled: false,
					},
					form: {
						disabled: true,
						component: {
							placeholder: '请输入请求方法',
						},
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				request_msg: {
					title: '操作说明',
					disabled: true,
					form: {
						component: {
							span: 12,
						},
					},
				},
				request_ip: {
					title: 'IP地址',
					search: {
						disabled: false,
					},
					type: 'input',
					form: {
						disabled: true,
						component: {
							placeholder: '请输入IP地址',
						},
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				request_browser: {
					title: '请求浏览器',
					type: 'input',
					form: {
						disabled: true,
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				response_code: {
					title: '响应码',
					search: {
						disabled: true,
					},
					type: 'input',
					form: {
						disabled: true,
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				request_os: {
					title: '操作系统',
					disabled: true,
					search: {
						disabled: true,
					},
					type: 'input',
					form: {
						disabled: true,
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				json_result: {
					title: '返回信息',
					search: {
						disabled: true,
					},
					type: 'input',
					form: {
						disabled: true,
					},
					component: { props: { color: 'auto' } }, // 自动染色
				},
				creator_name: {
					title: '操作人',
					form: {
						disabled: true,
					},
				},
			},
		},
	};
};
