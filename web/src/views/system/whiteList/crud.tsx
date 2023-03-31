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
							let pagination: any = crudExpose.crudBinding.value.pagination;
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
				method: {
					title: '请求方式',
					sortable: true,
					search: {
						disabled: false,
					},
					type: 'dict-select',
					dict: dict({
						data: [
							{
								label: 'GET',
								value: 0,
							},
							{
								label: 'POST',
								value: 1,
							},
							{
								label: 'PUT',
								value: 2,
							},
							{
								label: 'DELETE',
								value: 3,
							},
						],
					}),
					form: {
						rules: [
							// 表单校验规则
							{
								required: true,
								message: '必填项',
							},
						],
						component: {
							span: 12,
						},
						itemProps: {
							class: { yxtInput: true },
						},
					},
				},
				url: {
					title: '接口地址',
					sortable: true,
					search: {
						disabled: true,
					},
					type: 'dict-select',
					dict: dict({
						async getData(dict: any) {
							return request('/swagger.json').then((ret: any) => {
								const res = Object.keys(ret.paths);
								const data = [];
								for (const item of res) {
									const obj = { label: '', value: '' };
									obj.label = item;
									obj.value = item;
									data.push(obj);
								}
								return data;
							});
						},
					}),
					form: {
						rules: [
							// 表单校验规则
							{
								required: true,
								message: '必填项',
							},
						],
						component: {
							span: 24,
							props: {
								elProps: {
									allowCreate: true,
									filterable: true,
									clearable: true,
								},
							},
						},
						itemProps: {
							class: { yxtInput: true },
						},
						helper: {
							render(h) {
								return <el-alert title="请正确填写，以免请求时被拦截。匹配单例使用正则,例如:/api/xx/.*?/" type="warning" />;
							},
						},
					},
				},
				enable_datasource: {
					title: '数据权限认证',
					search: {
						disabled: false,
					},
					width: 150,
					type: 'dict-radio',
					dict: dict({
						data: dictionary('button_status_bool'),
					}),
					form: {
						value: true,
						component: {
							span: 12,
						},
					},
				},
			},
		},
	};
};
