import { CrudOptions, AddReq, DelReq, EditReq, dict, CrudExpose, compute } from '@fast-crud/fast-crud';
import _ from 'lodash-es';
import * as api from './api';
import { dictionary } from '/@/utils/dictionary';
import { successMessage } from '../../../utils/message';
interface CreateCrudOptionsTypes {
	crudOptions: CrudOptions;
}

//此处为crudOptions配置
export const createCrudOptions = function ({ crudExpose, rolePermission }: { crudExpose: CrudExpose; rolePermission: any }): CreateCrudOptionsTypes {
	const pageRequest = async (query: any) => {
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
			rowHandle: {
				//固定右侧
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
					custom: {
						text: '权限配置',
						type: 'text',
						tooltip: {
							placement: 'top',
							content: '删除',
						},
						click: (context: any): void => {
							const { row } = context;
							// eslint-disable-next-line no-mixed-spaces-and-tabs
							rolePermission.value.drawer = true;
							rolePermission.value.editedRoleInfo = row;
							rolePermission.value.initGet();
						},
					},
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
						sortable: 'custom',
					},
					form: {
						rules: [{ required: true, message: '角色名称必填' }],
						component: {
							placeholder: '请输入角色名称',
						},
					},
				},
				key: {
					title: '权限标识',
					type: 'text',
					search: { show: false },
					column: {
						width: 120,
						sortable: 'custom',
					},
					form: {
						rules: [{ required: true, message: '权限标识必填' }],
						placeholder: '输入权限标识',
					},
				},
				sort: {
					title: '排序',
					search: { show: false },
					type: 'number',
					column: {
						width: 90,
						sortable: 'custom',
					},
					form: {
						rules: [{ required: true, message: '排序必填' }],
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
						sortable: 'custom',
					},
					form: {
						rules: [{ required: true, message: '是否管理员必填' }],
						value: false,
					},
				},
				status: {
					title: '状态',
					search: { show: true },
					type: 'dict-radio',
					column: {
						width:100,
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
				update_datetime: {
					title: '更新时间',
					type: 'text',
					search: { show: false },
					column: {
						width: 170,
						sortable: 'custom',
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
						sortable: 'custom',
						width: 170,
					},
					form: {
						show: false,
						component: {
							placeholder: '输入关键词搜索',
						},
					},
				},
				// description: {
				//     title: '备注',
				//     type: 'textarea',
				//     search: {show: false},
				//     form: {
				//         component: {
				//             maxlength: 200,
				//             placeholder: '输入备注',
				//         },
				//     },
				// },
			},
		},
	};
};
