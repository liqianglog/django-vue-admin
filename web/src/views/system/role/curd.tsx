import {CrudOptions, AddReq, DelReq, EditReq, dict,CrudExpose } from '@fast-crud/fast-crud';
import _ from 'lodash-es';

interface CreateCrudOptionsTypes {
	crudOptions: CrudOptions;
}

//此处为crudOptions配置
export const createCrudOptions = function ({crudExpose}: {crudExpose: CrudExpose}): CreateCrudOptionsTypes {
	//本地模拟后台crud接口方法 ----开始
	const records = [
		{
			id: 1,
			modifier_name: '超级管理员',
			creator_name: '超级管理员',
			create_datetime: '2022-04-08 11:02:22',
			update_datetime: '2022-05-31 02:09:00',
			description: null,
			modifier: '1',
			dept_belong_id: '1',
			name: '管理员',
			key: 'admin',
			sort: 1,
			status: true,
			admin: true,
			data_range: 3,
			remark: null,
			creator: 1,
			dept: [],
			menu: [1, 2, 10, 20, 7, 8, 11, 16, 17, 5, 13, 15, 4, 18, 19, 3, 9],
			permission: [
				53, 4, 8, 13, 18, 32, 37, 42, 45, 49, 55, 2, 6, 11, 16, 21, 26, 30, 35, 40, 52, 1, 7, 12, 17, 22, 27, 31, 36, 41, 46, 50, 54, 3, 9, 14, 19,
				23, 25, 33, 38, 43, 47, 48, 5, 10, 15, 20, 24, 28, 34, 39, 44, 51, 29,
			],
		},
	];
	const pageRequest = async (query: any) => {
		return {
			records,
			currentPage: 1,
			pageSize: 20,
			total: records.length,
		};
	};
	const editRequest = async (req: EditReq) => {
		const target = _.find(records, (item) => {
			return req.row.id === item.id;
		});
		_.merge(target, req.form);
		return target;
	};
	const delRequest = async (req: DelReq) => {
		_.remove(records, (item) => {
			return item.id === req.row.id;
		});
	};

	const addRequest = async (req: AddReq) => {
		const maxRecord = _.maxBy(records, (item) => {
			return item.id;
		});
		req.form.id = (maxRecord?.id || 0) + 1;
		records.push(req.form);
		return req.form;
	};
	//本地模拟后台crud接口方法 ----结束
	return {
		crudOptions: {
			request: {
				pageRequest,
				addRequest,
				editRequest,
				delRequest,
			},
			rowHandle: {
				width: 330,
				buttons: {
					edit: {
						size: 'default'
					},
					view: {
						size: 'default'
					},
					remove: {
						size: 'default'
					}
				},
			},
			form: {
				col: { span: 24 },
				labelWidth: '100px',
				wrapper: {
					is: 'el-dialog',
					width: '600px',
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
					column: { show: false },
					type: 'text',
					search: { show: true },
					form: {
						show: false,
						component: {
							placeholder: '输入关键词搜索',
						},
					},
				},
				id: {
					title: 'ID',
					type: 'text',
					column: { show: false },
					search: { show: false },
					form: { show: false },
				},
				name: {
					title: '角色名称',
					type: 'text',
					search: { show: true },
					column: {
						minWidth: 120,
						sortable: true,
					},
					form: {
						rules: [{ required: true, message: '角色名称必填' }],
						component: {
							placeholder: '输入角色名称搜索',
						},
					},
				},
				key: {
					title: '权限标识',
					type: 'text',
					search: { show: false },
					column: {
						width: 120,
						sortable: true,
					},
					form: {
						rules: [{ required: true, message: '权限标识必填' }],
						component: {
							placeholder: '输入权限标识',
						}
					},
				},
				sort: {
					title: '排序',
					search: { show: false },
					type: 'number',
					column: {
						width: 90,
						sortable: true,
					},
					form: {
						value: 1,
					},
				},
				admin: {
					title: '是否管理员',
					search: { show: false },
					type: 'dict-radio',
					dict: dict({
						data: [
							{
								label: '是',
								value: true,
								color: 'success',
							},
							{
								label: '否',
								value: false,
								color: 'danger',
							},
						],
					}),
					column: {
						width: 130,
						sortable: true,
					},
					form: {
						value: false,
					},
				},
				status: {
					title: '状态',
					search: { show: true },
					type: 'dict-radio',
					dict: dict({
						data: [
							{
								label: '启用',
								value: true,
								color: 'success',
							},
							{
								label: '禁用',
								value: false,
								color: 'danger',
							},
						],
					}),
					column: {
						width: 90,
						sortable: true,
					},
					form: {
						value: true,
					},
				},
				update_datetime: {
					title: '更新时间',
					type: 'text',
					search: { show: false },
					column: {
						width: 170,
						sortable: true,
					},
					form: {
						show: false,
						component: {
							placeholder: '输入关键词搜索',
						},
					},
				},
				create_datetime: {
					title: '创建时间',
					type: 'text',
					search: { show: false },
					column: {
						sortable: true,
						width: 170,
					},
					form: {
						show: false,
						component: {
							placeholder: '输入关键词搜索',
						},
					},
				},

				description: {
					title: '备注',
					type: 'textarea',
					search: { show: false },
					form: {
						component: {
							maxlength: 200,
							placeholder: '输入备注',
						},
					},
				},
			},
		},
	};
};