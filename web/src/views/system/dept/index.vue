<template>
	<fs-page>
		<el-row class="mx-2">
			<el-col :span="4" class="p-1">
				<el-card :body-style="{ height: '100%' }">
					<p class="font-mono font-black text-center text-xl pb-5">
						部门列表
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
						:load="loadNode"
						lazy
						icon="ArrowRightBold"
						:indent="12"
					>
						<template #default="{ node, data }">
							<span class="text-center font-black text-xl">{{ node.label }}</span>
						</template>
					</el-tree>
				</el-card>
			</el-col>
			<el-col :span="20" class="p-1">
				<el-card :body-style="{ height: '100%' }">
					<fs-crud ref="crudRef" v-bind="crudBinding"> </fs-crud>
				</el-card>
			</el-col>
		</el-row>
	</fs-page>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch, toRaw } from 'vue';
import { useFs } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
import * as api from './api';
import { ElTree } from 'element-plus';
import XEUtils from 'xe-utils';

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

// 引入组件
const placeholder = ref('请输入部门名称');
const filterText = ref('');
const treeRef = ref<InstanceType<typeof ElTree>>();

const treeProps = {
	children: 'children',
	label: 'name',
	icon: 'icon',
	isLeaf: (data: Tree[], node: Node) => {
		// @ts-ignore
		if (node.data.hasChild) {
			return false;
		} else {
			return true;
		}
	},
};

watch(filterText, (val) => {
	treeRef.value!.filter(val);
});

const filterNode = (value: string, data: Tree) => {
	if (!value) return true;
	return toRaw(data).name.indexOf(value) !== -1;
};

// 懒加载
const loadNode = (node: Node, resolve: (data: Tree[]) => void) => {
	// @ts-ignore
	if (node.level !== 0) {
		// @ts-ignore
		api.GetList({ parent: node.data.id }).then((res: APIResponseData) => {
			resolve(res.data);
			console.log(res.data);
		});
	}
};

let data = ref([]);

const content = `
1.部门数据支持懒加载;
`;

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

const { crudBinding, crudRef, crudExpose } = useFs({ createCrudOptions });

// 页面打开后获取列表数据
onMounted(() => {
	getData();
	crudExpose.doRefresh();
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
</style>
