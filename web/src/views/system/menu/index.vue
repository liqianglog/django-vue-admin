<template>
	<fs-page>
		<el-row class="s-el-row">
			<el-col :span="6">
				<div class="menu-box menu-left-box">
					<el-input v-model="filterText" :prefix-icon="Search" placeholder="请输入菜单名称" />
					<div class="menu-left-tree">
						<div class="mlt-head">
							<el-icon size="16" color="#606266" class="mlt-head-icon">
								<Menu />
							</el-icon>
							菜单列表
							<el-tooltip effect="dark" placement="right"
								content="1.红色菜单代表状态禁用; 2.添加菜单，如果是目录，组件地址为空即可; 3.添加根节点菜单，父级ID为空即可; 4.支持拖拽菜单;">
								<el-icon size="16" color="var(--el-color-primary)" class="mlt-tooltip">
									<QuestionFilled />
								</el-icon>
							</el-tooltip>
						</div>
						<el-tree ref="treeRef" class="font-mono font-bold leading-6 text-7xl" :data="data" :props="defaultTreeProps"
							:filter-node-method="filterNode" :load="loadNode" @node-drop="nodeDrop" lazy :indent="45"
							@node-click="handleNodeClick" highlight-current default-expand-all>
							<template #default="{ node, data }">
								<element-tree-line :node="node" :showLabelLine="false" :indent="32">
									<span v-if="data.status" class="text-center font-black font-normal">
										<SvgIcon :name="node.data.icon" color="var(--el-color-primary)" />
										&nbsp;{{ node.label }}
									</span>
									<span v-else class="text-center font-black text-red-700 font-normal">
										<SvgIcon :name="node.data.icon" />&nbsp;{{ node.label }}
									</span>
								</element-tree-line>
								<!--  -->
							</template>
						</el-tree>
					</div>

					<div class="menu-left-tags">
						<el-tooltip effect="dark" content="新增">
							<el-icon size="16" @click="handleUpdateMenu('create')" class="mlt-icon">
								<Plus />
							</el-icon>
						</el-tooltip>

						<el-tooltip effect="dark" content="编辑">
							<el-icon size="16" @click="handleUpdateMenu('update')" class="mlt-icon">
								<Edit />
							</el-icon>
						</el-tooltip>

						<el-tooltip effect="dark" content="上移">
							<el-icon size="16" @click="handleSort('up')" class="mlt-icon">
								<Top />
							</el-icon>
						</el-tooltip>

						<el-tooltip effect="dark" content="下移">
							<el-icon size="16" @click="handleSort('down')" class="mlt-icon">
								<Bottom />
							</el-icon>
						</el-tooltip>

						<el-tooltip effect="dark" content="删除">
							<el-icon size="16" @click="handleDeleteMenu()" class="mlt-icon">
								<Delete />
							</el-icon>
						</el-tooltip>
					</div>
				</div>
			</el-col>

			<el-col :span="18">
				<div class="menu-box menu-right-box">
					<menuButton :select-menu="form" />
				</div>
			</el-col>
		</el-row>

		<el-drawer v-model="drawerVisible" title="菜单配置" direction="rtl" size="500px" :close-on-click-modal="false"
			:before-close="handleDrawerClose">
			<div class="menu-box menu-drawer-box">
				<div class="mcb-alert">
					1.红色菜单代表状态禁用;<br />
					2.添加菜单，如果是目录，组件地址为空即可;<br />
					3.添加根节点菜单，父级ID为空即可;<br />
					4.支持拖拽菜单;
				</div>
				<el-form ref="formRef" :rules="rules" :model="form" label-width="80px" label-position="right">
					<el-form-item label="菜单ID" prop="id">
						<el-input v-model="form.id" disabled />
					</el-form-item>
					<el-form-item label="父级ID" prop="parent">
						<el-input v-model="form.parent" />
					</el-form-item>
					<el-form-item required label="菜单名称" prop="name">
						<el-input v-model="form.name" />
					</el-form-item>
					<el-form-item label="组件地址" prop="component">
						<el-autocomplete class="w-full" v-model="form.component" :fetch-suggestions="querySearch"
							:trigger-on-focus="false" clearable :debounce="100" placeholder="输入组件地址" />
					</el-form-item>
					<el-form-item required label="Url" prop="web_path">
						<el-input v-model="form.web_path" />
					</el-form-item>
					<el-form-item label="排序" prop="sort">
						<el-input-number v-model="form.sort" controls-position="right" />
					</el-form-item>
					<el-form-item label="状态">
						<el-radio-group v-model="form.status">
							<el-radio :label="true">启用</el-radio>
							<el-radio :label="false">禁用</el-radio>
						</el-radio-group>
					</el-form-item>
					<el-form-item label="侧边可见">
						<el-radio-group v-model="form.visible">
							<el-radio :label="true">启用</el-radio>
							<el-radio :label="false">禁用</el-radio>
						</el-radio-group>
					</el-form-item>
					<el-form-item label="缓存">
						<el-radio-group v-model="form.cache">
							<el-radio :label="true">启用</el-radio>
							<el-radio :label="false">禁用</el-radio>
						</el-radio-group>
					</el-form-item>
					<el-form-item label="图标" prop="icon">
						<IconSelector clearable v-model="form.icon" />
					</el-form-item>
				</el-form>
				<el-divider></el-divider>
				<div class="menus-btns">
					<el-button @click="saveMenu()" type="primary">保存</el-button>
					<!-- <el-button @click="newMenu()" type="primary" round :disabled="!form.id">新建</el-button>
					<el-button @click="addChildMenu()" type="primary" round :disabled="!form.id">添加子级
					</el-button> -->
					<el-button @click="handleDrawerClose()">取消</el-button>
				</div>
			</div>
		</el-drawer>
	</fs-page>
</template>

<script lang="ts" setup name="menuPages">
import { ref, onMounted, watch, reactive, toRaw, defineAsyncComponent, h } from 'vue';
import XEUtils from 'xe-utils';
import { ElForm, ElTree, FormRules, ElMessageBox } from 'element-plus';
import { getElementLabelLine } from "element-tree-line";
import * as api from './api';
import { Search } from '@element-plus/icons-vue'
import { errorMessage, successMessage, warningMessage } from '../../../utils/message';
import { FormTypes, TreeTypes, APIResponseData, ComponentFileItem } from './types'
import type Node from 'element-plus/es/components/tree/src/model/node'

const menuButton = defineAsyncComponent(() => import('./components/menuButton/index.vue'));
const IconSelector = defineAsyncComponent(() => import('/@/components/iconSelector/index.vue'));
const SvgIcon = defineAsyncComponent(() => import('/@/components/svgIcon/index.vue'));

const ElementTreeLine = getElementLabelLine(h);

const filterText = ref('');
const treeRef = ref<InstanceType<typeof ElTree>>();
let drawerVisible = ref(false)
let treeSelectNode = ref<Node | null>(null)

watch(filterText, (val) => {
	treeRef.value!.filter(val);
});

const defaultTreeProps: any = {
	children: 'children',
	label: 'name',
	icon: 'icon',
	isLeaf: (data: TreeTypes[], node: Node) => {
		if (node.data.is_catalog) {
			return false;
		} else {
			return true;
		}
	},
};

const validateWebPath = (rule: string, value: string, callback: Function) => {
	let pattern = /^\/.*?/;
	if (!pattern.test(value)) {
		callback(new Error('请输入正确的地址'));
	} else {
		callback();
	}
};

const filterNode = (value: string, data: any) => {
	if (!value) return true;
	return toRaw(data).name.indexOf(value) !== -1;
};

// 懒加载
const loadNode = (node: Node, resolve: (data: TreeTypes[]) => void) => {
	// @ts-ignore
	if (node.level !== 0) {
		// @ts-ignore
		api.lazyLoadMenu({ parent: node.data.id }).then((res: APIResponseData) => {
			resolve(res.data);
		});
	}
};

const nodeDrop = (draggingNode: Node, dropNode: Node) => {
	// @ts-ignore
	if (!dropNode.isLeaf) {
		// @ts-ignore
		api.dragMenu({ menu_id: draggingNode.data.id, parent_id: dropNode.data.id }).then((res: APIResponseData) => {
			successMessage(res.msg as string);
		});
	}
};

let data = ref([]);

let isAddNewMenu = ref(false); // 判断当前是新增菜单，还是更新保存当前菜单

let form: FormTypes<any> = reactive({
	id: '',
	parent: '',
	name: '',
	component: '',
	web_path: '',
	sort: 0,
	status: true,
	is_catalog: false,
	permission: '',
	icon: '',
	visible: true,
	cache: true,
});
const rules = reactive<FormRules>({
	// @ts-ignore
	web_path: [{ validator: validateWebPath, trigger: 'blur' }],
});

const formRef = ref<InstanceType<typeof ElForm>>();

const querySearch = (queryString: string, cb: any) => {
	const files: any = import.meta.glob('@views/**/*.vue');
	let fileLists: Array<any> = [];
	Object.keys(files).forEach((queryString: string) => {
		fileLists.push({
			label: queryString.replace(/(\.\/|\.vue)/g, ''),
			value: queryString.replace(/(\.\/|\.vue)/g, ''),
		});
	});
	const results = queryString ? fileLists.filter(createFilter(queryString)) : fileLists;
	// 统一去掉/src/views/前缀
	results.forEach((val) => {
		val.label = val.label.replace('/src/views/', '');
		val.value = val.value.replace('/src/views/', '');
	});
	cb(results);
};

const createFilter = (queryString: string) => {
	return (file: ComponentFileItem) => {
		return file.value.toLowerCase().indexOf(queryString.toLowerCase()) !== -1;
	};
};

const getData = () => {
	api.GetList({}).then((ret: APIResponseData) => {
		const responseData = ret.data;
		const result = XEUtils.toArrayTree(responseData, {
			parentKey: 'parent',
			children: 'children',
			strict: true,
		});
		data.value = result;
	});
};

const saveMenu = () => {
	formRef.value?.validate((valid, fields) => {
		if (valid) {
			if (!isAddNewMenu.value) {
				// 保存菜单

				form.component == '' ? (form.is_catalog = true) : (form.is_catalog = false);
				api.UpdateObj(form).then((res: APIResponseData) => {
					successMessage(res.msg as string);
					getData();
					handleDrawerClose()
				});
			} else {
				// 新增菜单
				form.component == '' ? (form.is_catalog = true) : (form.is_catalog = false);
				api.AddObj(form).then((res: APIResponseData) => {
					successMessage(res.msg as string);
					getData();
					handleDrawerClose()
				});
			}
		} else {
			errorMessage('请填写检查表单');
		}
	});
};

const newMenu = () => {
	formRef.value?.resetFields();
	isAddNewMenu.value = true;
	handleDrawerClose()
};

const addChildMenu = () => {
	let parentId = form.id;
	formRef.value?.resetFields();
	form.parent = parentId;
	isAddNewMenu.value = true;
	handleDrawerClose();
};

const handleNodeClick = (record: any, node: Node) => {
	treeSelectNode.value = node;
	Object.keys(toRaw(data)).forEach((key: string) => {
		form[key] = record[key];
	});
	delete form.component_name;
	form.id = record.id;
	isAddNewMenu.value = false;
};

/**
 * 点击左侧编辑按钮
 */
const handleUpdateMenu = (type: string) => {
	if (type === 'create') {
		drawerVisible.value = true
		return
	}
	if (!form.id) {
		warningMessage('请选择菜单！')
		return
	}
	drawerVisible.value = true
}
const handleDrawerClose = () => {
	drawerVisible.value = false
}

/**
 * 删除菜单
 */
const handleDeleteMenu = () => {
	if (!form.id) {
		warningMessage('请选择菜单！')
		return
	}
	ElMessageBox.confirm(
		'您确认删除该菜单项吗?',
		'温馨提示',
		{
			confirmButtonText: '确认',
			cancelButtonText: '取消',
			type: 'warning',
		}
	).then(() => {
		api.DelObj(form).then((res: APIResponseData) => {
			successMessage(res.msg as string);
			getData();
			handleDrawerClose();
		});
	})
};

/**
 * 移动操作
 */
const handleSort = (type: string) => {
	if (!form.id && treeSelectNode.value) {
		warningMessage('请选择菜单！')
		return
	}
	const parentList = treeSelectNode.value?.parent.childNodes || [];
	const index = parentList.findIndex(i => i.data.id === form.id)
	const record = parentList.find(i => i.data.id === form.id)

	if (type === 'up') {
		if (index === 0) return
		parentList.splice(index - 1, 0, record as any)
		parentList.splice(index + 1, 1)
	}
	if (type === 'down') {
		parentList.splice(index + 2, 0, record as any)
		parentList.splice(index, 1)
	}
}

// 页面打开后获取列表数据
onMounted(() => {
	getData();
});
</script>

<style lang="scss" scoped>
.s-el-row {
	height: 100%;
	overflow: hidden;

	.el-col {
		height: 100%;
		padding: 10px 0;
		box-sizing: border-box;
	}
}

.menu-box {
	height: 100%;
	padding: 10px;
	background-color: #fff;
	box-sizing: border-box;
}

.menu-left-box {
	position: relative;
	border-radius: 0 8px 8px 0;
	margin-right: 10px;

	.mlt-head {
		display: flex;
		align-items: center;
		margin-left: -8px;
		color: #606266;
		font-weight: 600;

		.mlt-head-icon {
			margin-right: 8px;
			position: relative;
			top: -1px;
		}

		.mlt-tooltip {
			margin-left: 5px;
			position: relative;
			top: -1px;
		}
	}

	.menu-left-tags {
		height: 40px;
		position: absolute;
		bottom: 0;
		left: 0;
		right: 0;
		padding: 0 20px;
		display: flex;
		align-items: center;
		justify-content: space-around;
		box-sizing: border-box;

		.mlt-icon {
			cursor: pointer;
			color: var(--el-color-primary);
		}
	}
}

.menu-right-box {
	border-radius: 8px 0 0 8px;
}

.menus-btns {
	padding-bottom: 10px;
	box-sizing: border-box;
}

.menu-drawer-box {
	border-radius: 8px;
	margin: 0 10px;
	overflow-y: auto;

	.mcb-alert {
		color: #fff;
		line-height: 24px;
		padding: 8px 16px;
		margin-bottom: 20px;
		border-radius: 4px;
		background-color: var(--el-color-primary);
	}
}

.font-normal {
	font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB, Microsoft YaHei, SimSun, sans-serif;
}
</style>

<style lang="scss">
.menu-left-tree {
	height: calc(100% - 60px);
	padding: 20px;
	box-sizing: border-box;
	overflow-y: auto;

	.el-tree-node__content {
		height: 32px !important;
	}

	.el-tree .el-tree-node__expand-icon svg {
		display: none !important;
		height: 0;
		width: 0;
	}

	.el-tree-node__expand-icon {
		font-size: 16px;
	}

	.el-tree-node__content>.el-tree-node__expand-icon {
		padding: 0;
		box-sizing: border-box;
		margin-right: 5px;
		margin-left: 24px;
	}

	.el-tree .el-tree-node__expand-icon.expanded {
		-webkit-transform: rotate(0deg);
		transform: rotate(0deg);
	}

	.el-tree .el-tree-node__expand-icon.is-leaf {
		margin-left: 0
	}

	.el-tree .el-tree-node__expand-icon:before {
		background: url("../../../assets/img/menu-tree-show-icon.png") no-repeat center / 100%;
		content: '';
		display: block;
		width: 24px;
		height: 24px;
	}

	.el-tree .el-tree-node__expand-icon.expanded:before {
		background: url("../../../assets/img/menu-tree-hidden-icon.png") no-repeat center / 100%;
		content: '';
		display: block;
		width: 24px;
		height: 24px;
	}

	.el-tree .is-leaf.el-tree-node__expand-icon::before {
		display: block;
		background: none !important;
		content: '';
		width: 18px;
		height: 18px;
		border: none;
	}
}
</style>
