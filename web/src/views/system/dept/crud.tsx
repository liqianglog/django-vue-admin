import * as api from './api';
import { dict, UserPageQuery, AddReq, DelReq, EditReq, compute, CreateCrudOptionsProps, CreateCrudOptionsRet } from '@fast-crud/fast-crud';
import { verifyPhone } from '/@/utils/toolsValidate';
import { dictionary } from '/@/utils/dictionary';
import { successMessage } from '/@/utils/message';

export const createCrudOptions = function ({ crudExpose }: CreateCrudOptionsProps): CreateCrudOptionsRet {
	const pageRequest = async (query: UserPageQuery) => {
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

	const validatePhone = async (rule: any, value: any, callback: any) => {
		if (value === '') {
			throw new Error('请输入手机号码');
		}
		if (verifyPhone(value)) {
			callback();
		} else {
			throw new Error('手机号码格式有误');
		}
	};

	/**
	 * 懒加载
	 * @param row
	 * @returns {Promise<unknown>}
	 */
	const loadContentMethod = (tree: any, treeNode: any, resolve: any) => {
		api.GetList({ parent: tree.id }).then((res: any) => {
			resolve(res.data);
		});
	};

	return {
		crudOptions: {
			request: {
				pageRequest,
				addRequest,
				editRequest,
				delRequest,
			},
			pagination: {
				show: false,
			},
			table: {
				rowKey: 'id',
				lazy: true,
				load: loadContentMethod,
				treeProps: { children: 'children', hasChildren: 'hasChild' },
			},
			rowHandle: {
				fiexd: 'right',
				fixed: 'right',
				width: 200,
				buttons: {
					view: {
						show: false,
					},
					edit: {
						iconRight: 'Edit',
						type: 'text',
					},
					remove: {
						iconRight: 'Delete',
						type: 'text',
					},
					addChildren: {
						text: '添加子级',
						type: 'text',
						click(context) {
							const rowId = context.row.id;
							crudExpose!.openAdd({ row: { parent: rowId } });
						},
					},
				},
			},
			columns: {
				_index: {
					title: '序号',
					form: { show: false },
					column: {
						type: 'index',
						align: 'center',
						width: '70px',
						columnSetDisabled: true, //禁止在列设置中选择
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
				name: {
					title: '部门名称',
					sortable: true,
					treeNode: true, // 设置为树形列
					search: {
						disabled: false,
						component: {
							props: {
								clearable: true,
							},
						},
					},
					width: 180,
					type: 'input',
					form: {
						rules: [
							// 表单校验规则
							{ required: true, message: '部门名称必填项' },
						],
						component: {
							span: 12,
							props: {
								clearable: true,
							},
							placeholder: '请输入部门名称',
						},
					},
				},
				key: {
					title: '部门标识',
					sortable: true,
					form: {
						component: {
							props: {
								clearable: true,
							},
							placeholder: '请输入标识字符',
						},
					},
				},
				owner: {
					title: '负责人',
					sortable: true,
					form: {
						component: {
							span: 12,
							props: {
								clearable: true,
							},
							placeholder: '请输入负责人',
						},
					},
				},
				phone: {
					title: '联系电话',
					sortable: true,
					form: {
						rules: [{ validator: validatePhone, trigger: 'blur' }],
						component: {
							span: 12,
							props: {
								clearable: true,
							},
							placeholder: '请输入联系电话',
						},
					},
				},
				email: {
					title: '邮箱',
					sortable: true,
					form: {
						component: {
							span: 12,
							props: {
								clearable: true,
							},
							placeholder: '请输入邮箱',
						},
						rules: [
							{
								type: 'email',
								message: '请输入正确的邮箱地址',
								// @ts-ignore
								trigger: ['blur', 'change'],
							},
						],
					},
				},
				sort: {
					title: '排序',
					sortable: true,
					width: 80,
					type: 'number',
					form: {
						value: 1,
						component: {
							span: 12,
							placeholder: '请选择序号',
						},
					},
				},
				status: {
					title: '状态',
					sortable: true,
					search: {
						disabled: false,
					},
					type: 'dict-radio',
					column: {
						component: {
							name: 'fs-dict-switch',
							activeText: '',
							inactiveText: '',
							style: '--el-switch-on-color: #409eff; --el-switch-off-color: #dcdfe6',
							onChange: compute((context) => {
								return () => {
									api.UpdateObj(context.row).then((res: APIResponseData) => {
										successMessage(res.msg as string);
									});
								};
							}),
						},
					},
					dict: dict({
						data: dictionary('button_status_bool'),
					}),
				},
			},
		},
	};
};
