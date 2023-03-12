import * as api from './api';
import { dict, PageQuery, AddReq, DelReq, EditReq, CrudExpose, CrudOptions } from '@fast-crud/fast-crud';
import { dictionary } from '/@/utils/dictionary';
import { eIconPicker, eIcon } from 'e-icon-picker';
import { useCompute } from '@fast-crud/fast-crud';
import { inject } from 'vue';
import { functions } from 'lodash-es';
import { apiPrefix as menuPrefix } from './api';
import XEUtils from 'xe-utils';
import { request } from '/@/utils/service';
const { compute } = useCompute();
interface CreateCrudOptionsTypes {
	crudOptions: CrudOptions;
}

export const createCrudOptions = function ({ crudExpose, menuButtonRef }: { crudExpose: CrudExpose; menuButtonRef: any }): CreateCrudOptionsTypes {
	const hasPermissions: any = inject('$hasPermissions');
	//验证路由地址
	const validateWebPath = (rule: string, value: string, callback: Function) => {
		const isLink = JSON.parse(crudExpose.getFormData().is_link);
		console.log(isLink);
		let pattern = /^\/.*?/;
		if (isLink) {
			pattern = /^((https|http|ftp|rtsp|mms)?:\/\/)[^\s]+/g;
		} else {
			pattern = /^\/.*?/;
		}
		// console.log('isLink', isLink, 'pattern', pattern, pattern.test(value));
		if (!pattern.test(value)) {
			callback(new Error('请正确的地址'));
		} else {
			callback();
		}
	};

	const pageRequest = async (query: PageQuery) => {
		return await api.GetList({});
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
			actionbar: {
				buttons: {
					add: {
						show: hasPermissions('menu:Create'),
					},
				},
			},
			rowHandle: {
				width: 310,
				buttons: {
					custom: {
						text: '按钮配置',
						type: 'warning',
						tooltip: {
							placement: 'top',
							content: '按钮配置',
						},
						show: compute(({ row }: any) => {
							if (row.web_path && !row.is_link) {
								return true && hasPermissions();
							}
							return false;
						}),
						click: (context: any): void => {
							const { row } = context;
							menuButtonRef.value.drawer = true;
							menuButtonRef.value.selectOptions = row;
							menuButtonRef.value.initGet();
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
						width: '80px',
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
				parent: {
					title: '父级菜单',
					column: {
						show: false,
					},
					type: 'dict-cascader',
					dict: dict({
						url: menuPrefix,
						value: 'id',
						label: 'name',
						children: 'children',
						isTree: true,
						getData: async ({ url }: { url: string }) => {
							return request({
								url: url,
								params: { limit: 100, status: 1, is_catalog: 1 },
							}).then((ret: any) => {
								const responseData = ret.data;
								const result = XEUtils.toArrayTree(responseData, {
									parentKey: 'parent',
									strict: true,
								});
								return [{ id: null, name: '根节点', children: result }];
							});
						},
					}),
					form: {
						component: {
							filterable: true,
							placeholder: '请选择父级菜单',
							props: {
								props: {
									checkStrictly: true,
									value: 'id',
									label: 'name',
								},
							},
						},
					},
				},
				name: {
					title: '菜单名称',
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
							{ required: true, message: '菜单名称必填项' },
						],
						component: {
							props: {
								clearable: true,
							},
							placeholder: '请输入菜单名称',
						},
					},
					column: {
						width: 180,
					},
				},
				icon: {
					title: '图标',
					form: {
						component: {
							name: eIconPicker,
							vModel: 'modelValue',
						},
					},
					column: {
						component: {
							name: eIcon,
							vModel: 'modelValue',
							style: 'font-size:18px',
						},
					},
				},
				sort: {
					title: '排序',
					column: {
						width: 60,
					},
					type: 'number',
					form: {
						value: 1,
						component: {
							placeholder: '请输入排序',
						},
					},
				},
				is_catalog: {
					title: '是否目录',
					column: {
						width: 60,
					},
					type: 'dict-switch',
					dict: dict({
						data: dictionary('button_whether_bool'),
					}),
					form: {
						component: {
							placeholder: '请选择是否目录',
						},
						// valueChange(key, value, form, { getColumn, mode, component, immediate, getComponent }) {
						//     if (!value) {
						//         form.web_path = undefined
						//         form.component = undefined
						//         form.component_name = undefined
						//         form.cache = false
						//         form.is_link = false
						//     }
						// }
					},
				},
				is_link: {
					title: '外链接',
					type: 'dict-switch',
					dict: dict({
						data: dictionary('button_whether_bool'),
					}),
					form: {
						value: false,
						component: {
							/* show(context) {
                                const { form } = context
                                return !form.is_catalog
                            }, */
							placeholder: '请选择是否外链接',
						},
						/*  valueChange(key, value, form, { getColumn, mode, component, immediate, getComponent }) {
                             form.web_path = undefined
                             form.component = undefined
                             form.component_name = undefined
                             if (value) {
                                 getColumn('web_path').title = '外链接地址'
                                 getColumn('web_path').component.placeholder = '请输入外链接地址'
                                 getColumn('web_path').helper = {
                                     render(h) {
                                         return (< el-alert title="外链接地址,请以https|http|ftp|rtsp|mms开头" type="warning" />
                                         )
                                     }
                                 }
                             } else {
                                 getColumn('web_path').title = '路由地址'
                                 getColumn('web_path').component.placeholder = '请输入路由地址'
                                 getColumn('web_path').helper = {
                                     render(h) {
                                         return (< el-alert title="浏览器中url的地址,请以/开头" type="warning" />
                                         )
                                     }
                                 }
                             }
                         } */
					},
				},
				web_path: {
					title: '路由地址',
					width: 150,
					column: {
						show: false,
					},
					form: {
						rules: [
							{ required: true, message: '请输入正确的路由地址' },
							{ validator: validateWebPath, trigger: 'change' },
						],
						component: {
							show(context: any) {
								const { form } = context;
								return !form.is_catalog;
							},
							props: {
								clearable: true,
							},
							placeholder: '请输入路由地址',
						},
						helper: {
							render(h) {
								return <el-alert title="浏览器中url的地址,请以/开头" type="warning" />;
							},
						},
					},
				},
				component: {
					title: '组件地址',
					type: 'dict-select',
					show: false,
					dict: dict({
						getData: () => {
							const files: any = import.meta.globEager('@views/**/*.vue');
							let result: Array<any> = [];
							Object.keys(files).forEach((key: string) => {
								result.push({
									label: key.replace(/(\.\/|\.vue)/g, ''),
									value: key.replace(/(\.\/|\.vue)/g, ''),
								});
							});
							return result;
						},
					}),
					column: {
						show: false,
					},
					form: {
						rules: [{ required: true, message: '请选择组件地址' }],
						component: {
							props: {
								clearable: true,
								filterable: true, // 可过滤选择项
							},
							placeholder: '请输入组件地址',
						},
						helper: {
							render(h) {
								return <el-alert title="src/views下的文件夹地址" type="warning" />;
							},
						},
					},
				},
				component_name: {
					title: '组件名称',
					column: {
						width: 140,
					},
					form: {
						rules: [{ required: true, message: '请输入组件名称' }],
						component: {
							show(context: any) {
								const { form } = context;
								return !form.is_catalog && !form.is_link;
							},
							props: {
								clearable: true,
							},
							placeholder: '请输入组件名称',
						},
						helper: {
							render(h) {
								return <el-alert title="xx.vue文件中的name" type="warning" />;
							},
						},
					},
				},
				menuPermission: {
					title: '拥有权限',
					type: 'dict-select',
					form: {
						show: false,
						component: {
							elProps: {
								// el-select的配置项，https://element.eleme.cn/#/zh-CN/component/select
								filterable: true,
								multiple: true,
								clearable: true,
							},
						},
					},
					column: {
						width: 260,
					},
				},
				cache: {
					title: '缓存',
					column: {
						width: 60,
					},
					search: {
						show: true,
					},
					type: 'dict-switch',
					dict: dict({
						data: dictionary('button_whether_bool'),
					}),
					form: {
						value: false,
						component: {
							// show(context) {
							//     const { form } = context
							//     return !form.is_catalog
							// },
							placeholder: '请选择是否缓存',
						},
						helper: {
							render(h) {
								return <el-alert title="是否开启页面缓存,需要组件名称和xx.vue页面的name一致" type="warning" />;
							},
						},
					},
				},
				visible: {
					title: '侧边可见',
					column: {
						width: 60,
					},
					search: {
						show: true,
					},
					type: 'dict-switch',
					dict: dict({
						data: dictionary('button_whether_bool'),
					}),
					form: {
						value: true,
						component: {
							placeholder: '请选择侧边可见',
						},
						rules: [
							// 表单校验规则
							{ required: true, message: '侧边可见必填项' },
						],
						helper: {
							render(h) {
								return <el-alert title="是否显示在侧边菜单中" type="warning" />;
							},
						},
					},
				},
				status: {
					title: '状态',
					sortable: true,
					search: {
						show: true,
					},
					column: {
						width: 80,
					},
					type: 'dict-switch',
					dict: dict({
						data: dictionary('button_status_bool'),
					}),
					form: {
						value: true,
						component: {
							placeholder: '请选择状态',
						},
						rules: [
							// 表单校验规则
							{ required: true, message: '状态必填项' },
						],
					},
				},
			},
		},
	};
};
