import * as api from './api';
import { dict, PageQuery, AddReq, DelReq, EditReq, CrudExpose, CrudOptions } from '@fast-crud/fast-crud';
import { dictionary } from '/@/utils/dictionary';
import {nextTick, ref} from 'vue';

interface CreateCrudOptionsTypes {
	crudOptions: CrudOptions;
}

export const createCrudOptions = function ({ crudExpose, subDictRef }: { crudExpose: CrudExpose; subDictRef: any }): CreateCrudOptionsTypes {
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
			rowHandle: {
				width: 360,
				buttons: {
					custom: {
						text: '字典配置',
						type: 'success',
						tooltip: {
							placement: 'top',
							content: '字典配置',
						},
						//@ts-ignore
						click: (context: any) => {
							const {row} = context
							subDictRef.value.drawer = true;
							nextTick(()=>{
								subDictRef.value.setSearchFormData({ form: { parent: row.id } });
								subDictRef.value.doRefresh();
							})


						},
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
							// @ts-ignore
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
				label: {
					title: '字典名称',
					search: {
						show: true,
						component: {
							props: {
								clearable: true,
							},
						},
					},
					type: 'input',
					form: {
						rules: [
							// 表单校验规则
							{ required: true, message: '字典名称必填项' },
						],
						component: {
							props: {
								clearable: true,
							},
							placeholder: '请输入字典名称',
						},
					},
				},
				value: {
					title: '字典编号',
					search: {
						disabled: true,
						component: {
							props: {
								clearable: true,
							},
						},
					},
					type: 'input',
					form: {
						rules: [
							// 表单校验规则
							{ required: true, message: '字典编号必填项' },
						],
						component: {
							props: {
								clearable: true,
							},
							placeholder: '请输入字典编号',
						},
						helper: {
							render(h) {
								return <el-alert title="使用方法：dictionary('字典编号')" type="warning" />;
							},
						},
					},
				},
				status: {
					title: '状态',
					width: 90,
					search: {
						show: true,
					},
					type: 'dict-radio',
					dict: dict({
						data: dictionary('button_status_bool'),
					}),
					component: {
						props: {
							options: [],
						},
					},
					form: {
						rules: [
							// 表单校验规则
							{ required: true, message: '状态必填项' },
						],
						value: true,
						component: {
							placeholder: '请选择状态',
						},
					},
				},
				sort: {
					title: '排序',
					width: 90,
					type: 'number',
					form: {
						value: 1,
					},
				},
			},
		},
	};
};
