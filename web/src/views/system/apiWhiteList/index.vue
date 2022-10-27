<template>
	<fs-page>
		<fs-crud ref="crudRef" v-bind="crudBinding">
			<template #cell_url="scope">
				<el-tag size="small">{{ scope.row.url }}</el-tag>
			</template>
		</fs-crud>
	</fs-page>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useExpose, useCrud, CrudOptions, AddReq, DelReq, EditReq, dict } from '@fast-crud/fast-crud';
import _ from 'lodash-es';

interface CreateCrudOptionsTypes {
	crudOptions: CrudOptions;
}

//此处为crudOptions配置
const createCrudOptions = function (prop?: CrudOptions): CreateCrudOptionsTypes {
	//本地模拟后台crud接口方法 ----开始
	const records = [
		{
			id: 1,
			modifier_name: '超级管理员',
			creator_name: '超级管理员',
			create_datetime: '2022-05-24 13:43:21',
			update_datetime: '2022-05-31 02:09:01',
			description: 'null1111111',
			modifier: '1',
			dept_belong_id: '1',
			url: '/api/system/dept_lazy_tree/',
			method: 0,
			enable_datasource: true,
			creator: 1,
		},
		{
			id: 2,
			modifier_name: '超级管理员',
			creator_name: '超级管理员',
			create_datetime: '2022-05-24 13:43:21',
			update_datetime: '2022-05-31 02:09:01',
			description: 'null22222',
			modifier: '1',
			dept_belong_id: '1',
			url: '/api/system/dept_lazy_tree/',
			method: 3,
			enable_datasource: false,
			creator: 1,
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
				buttons: {
					view: { show: false },
				},
			},
			form: {
				labelWidth: '120px',
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
					show: false,
					disabled: true,
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
				method: {
					title: '请求方式',
					type: 'dict-select',
					search: { show: true },
					dict: dict({
						data: [
							{
								label: 'GET',
								value: 0,
								color: null,
							},
							{
								label: 'POST',
								value: 1,
								color: null,
							},
							{
								label: 'PUT',
								value: 2,
								color: null,
							},
							{
								label: 'DELETE',
								value: 3,
								color: null,
							},
						],
					}),
					form: {
						component: {
							maxlength: 20,
						},
					},
					column: {
						sortable: true,
					},
				},
				url: {
					title: '接口地址',
					type: 'text',
					search: { show: false },
					form: {
						col: { span: 24 },
						helper: '请正确填写，以免请求时被拦截。匹配单例使用正则,例如:/api/xx/.*?/',
						component: {
							maxlength: 20,
						},
					},
					column: {
						sortable: true,
					},
				},
				enable_datasource: {
					title: '数据权限认证',
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
					form: {
						component: {
							maxlength: 20,
						},
					},
				},
				description: {
					title: '备注',
					type: 'textarea',
					search: { show: false },
					form: {
						col: { span: 24 },
						component: {
							maxlength: 200,
						},
					},
				},
			},
		},
	};
};

// crud组件的ref
const crudRef = ref();
// crud 配置的ref
const crudBinding = ref();
// 暴露的方法
const { crudExpose } = useExpose({ crudRef, crudBinding });
// 你的crud配置
const { crudOptions } = createCrudOptions({ crudExpose });
// 初始化crud配置
const { resetCrudOptions } = useCrud({ crudExpose, crudOptions });
// 你可以调用此方法，重新初始化crud配置
// resetCrudOptions(options)

// 页面打开后获取列表数据
onMounted(() => {
	crudExpose.doRefresh();
});
</script>
