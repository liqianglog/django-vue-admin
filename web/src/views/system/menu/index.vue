<template>
	<fs-page>
		<el-row class="mx-2">
			<el-col :span="4" class="p-1">
				<el-card :body-style="{ height: '100%' }">
					<p class="font-mono font-black text-center text-xl pb-5">
						菜单列表
						<el-tooltip effect="dark" :content="content" placement="right">
							<el-icon> <QuestionFilled /> </el-icon>
						</el-tooltip>
					</p>
					<el-input v-model="filterText" :placeholder="placeholder" />
					<el-tree
						ref="treeRef"
						class="font-mono font-bold leading-6 text-7xl"
						:data="data"
						:props="treeProps"
						:filter-node-method="filterNode"
						@node-click="handleNodeClick"
					>
						<template #default="{ node, data }">
							<span v-if="data.status" class="text-center font-black text-xl">{{ node.label }}</span>
							<span v-else class="text-center font-black text-xl text-red-700">{{ node.label }}</span>
						</template>
					</el-tree>
				</el-card>
			</el-col>
			<el-col :span="20" class="p-1">
				<el-card :body-style="{ height: '100%' }">
					<el-form ref="formRef" :rules="rules" :model="form" label-width="80px" label-position="right">
						<el-divider>
							<strong>菜单配置</strong>
						</el-divider>
						<el-row>
							<el-col :span="10">
								<el-form-item label="菜单ID" prop="id"> <el-input v-model="form.id" disabled /> </el-form-item>
							</el-col>
							<el-col :span="10">
								<el-form-item label="父级ID" prop="parent"> <el-input v-model="form.parent" disabled /> </el-form-item>
							</el-col>
							<el-col :span="10">
								<el-form-item required label="菜单名称" prop="name"> <el-input v-model="form.name" /> </el-form-item>
							</el-col>
							<el-col :span="10">
								<el-form-item label="组件地址" prop="component">
									<el-autocomplete
										class="w-full"
										v-model="form.component"
										:fetch-suggestions="querySearch"
										:trigger-on-focus="false"
										clearable
										debounce="100"
										placeholder="输入组件地址"
									/>
								</el-form-item>
							</el-col>
							<el-col :span="10">
								<el-form-item required label="Url" prop="web_path"> <el-input v-model="form.web_path" /> </el-form-item>
							</el-col>
							<el-col :span="10">
								<el-form-item label="排序" prop="sort">
									<el-input-number v-model="form.sort" controls-position="right" />
								</el-form-item>
							</el-col>
							<el-col :span="10">
								<el-form-item label="状态">
									<el-radio-group v-model="form.status">
										<el-radio :label="true">启用</el-radio>
										<el-radio :label="false">禁用</el-radio>
									</el-radio-group>
								</el-form-item>
							</el-col>
							<el-col :span="20">
								<el-form-item label="权限">
									<el-checkbox-group v-model="form.permission">
										<el-checkbox v-model="form.permission">全选</el-checkbox>
										<el-checkbox label="查询(Search)" />
										<el-checkbox label="新增(Add)" />
										<el-checkbox label="删除(Delete)" />
										<el-checkbox label="编辑(Update)" />
										<el-checkbox label="导入(Import)" />
										<el-checkbox label="导出(Export)" />
									</el-checkbox-group>
								</el-form-item>
							</el-col>
							<el-col :span="20">
								<el-form-item label="图标" prop="icon">
									<IconSelector clearable v-model="form.icon" />
								</el-form-item>
							</el-col>
							<el-col class="center">
								<el-divider>
									<el-button @click="saveMenu()" type="primary" round>保存</el-button>
									<el-button @click="newMenu()" type="success" round>新建</el-button>
									<el-button @click="addChildMenu()" type="info" round>添加子级</el-button>
									<el-button @click="addSameLevelMenu()" type="warning" round>添加同级</el-button>
									<el-button @click="deleteMenu()" type="danger" round>删除菜单</el-button>
								</el-divider>
							</el-col>
						</el-row>
					</el-form>
				</el-card>
			</el-col>
		</el-row>
	</fs-page>
</template>

<script lang="ts" setup>
import * as api from './api';
import { ElForm, ElTree, FormInstance, FormRules } from 'element-plus';
import type Node from 'element-plus/es/components/tree/src/model/node';
import { ref, onMounted, computed, watch, reactive, toRaw, defineAsyncComponent, nextTick, shallowRef } from 'vue';
import { useExpose, useCrud } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
import XEUtils from 'xe-utils';
import { errorMessage, successMessage } from '../../../utils/message';

interface Tree {
	id: number;
	name: string;
	status: boolean;
	children?: Tree[];
}
interface APIResponseData {
	code?: number;
	data: [];
	msg?: string;
}
interface Form<T> {
	[key: string]: T;
}
interface ComponentFileItem {
	value: string;
	label: string;
}

// 引入组件
const IconSelector = defineAsyncComponent(() => import('/@/components/iconSelector/index.vue'));
const placeholder = ref('请输入菜单名称');
const filterText = ref('');
const treeRef = ref<InstanceType<typeof ElTree>>();

const treeProps = {
	children: 'children',
	label: 'name',
};

const validateWebPath = (rule: string, value: string, callback: Function) => {
	let pattern = /^\/.*?/;
	if (!pattern.test(value)) {
		callback(new Error('请输入正确的地址'));
	} else {
		callback();
	}
};

watch(filterText, (val) => {
	treeRef.value!.filter(val);
});

const filterNode = (value: string, data: Tree) => {
	if (!value) return true;
	return toRaw(data).name.indexOf(value) !== -1;
};

let data = ref([]);

let isAddNewMenu = ref(false); // 判断当前是新增菜单，还是更新保存当前菜单

const content = `
1.红色菜单代表状态禁用;
2.添加菜单是，如果是目录，组件地址为空即可;
3.添加根节点菜单，父级ID为空即可
`;

let form: Form<string> = reactive({
	id: '',
	parent: '',
	name: '',
	component: '',
	web_path: '',
	sort: '',
	status: '',
	permission: '',
	icon: '',
});
const formRef = ref<InstanceType<typeof ElForm>>();

const querySearch = (queryString: string, cb: any) => {
	const files: any = import.meta.globEager('@views/**/*.vue');
	let fileLists: Array<any> = [];
	Object.keys(files).forEach((queryString: string) => {
		fileLists.push({
			label: queryString.replace(/(\.\/|\.vue)/g, ''),
			value: queryString.replace(/(\.\/|\.vue)/g, ''),
		});
	});
	const results = queryString ? fileLists.filter(createFilter(queryString)) : fileLists;
	cb(results);
};

const createFilter = (queryString: string) => {
	return (file: ComponentFileItem) => {
		return file.value.toLowerCase().indexOf(queryString.toLowerCase()) !== -1;
	};
};

const rules = reactive<FormRules>({
	// @ts-ignore
	web_path: [{ validator: validateWebPath, trigger: 'blur' }],
});

const getData = () => {
	api.GetAllMenu({}).then((ret: APIResponseData) => {
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
				api.UpdateObj(form).then((res: APIResponseData) => {
					successMessage(res.msg as string);
					getData();
				});
			} else {
				// 新增菜单
				api.AddObj(form).then((res: APIResponseData) => {
					successMessage(res.msg as string);
					getData();
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
};
const addChildMenu = () => {
	let parentId = form.id;
	formRef.value?.resetFields();
	form.parent = parentId;
	isAddNewMenu.value = true;
};
const addSameLevelMenu = () => {
	let parentId = form.parent;
	formRef.value?.resetFields();
	form.parent = parentId;
	isAddNewMenu.value = true;
};
const deleteMenu = () => {
	api.DelObj(form).then((res: APIResponseData) => {
		successMessage(res.msg as string);
		getData();
	});
};

const handleNodeClick = (data: any, node: any, prop: any) => {
	Object.keys(toRaw(data)).forEach((key: string) => {
		form[key] = data[key];
	});
	form.id = data.id;
	isAddNewMenu.value = false;
};

// 页面打开后获取列表数据
onMounted(() => {
	getData();
});
</script>

<style lang="scss" scoped>
.el-row {
	height: 100%;

	.el-col {
		height: 100%;
	}
}

.el-card {
	height: 100%;
}
.custom-tree-node {
	flex: 1;
	display: flex;
	align-items: center;
	justify-content: space-between;
	font-size: 14px;
	padding-right: 8px;
}
</style>
