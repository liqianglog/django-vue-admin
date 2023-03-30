<template>
	<fs-page>
		<el-row class="mx-2">
			<el-col :span="4" class="p-1">
				<el-card :body-style="{ height: '100%' }">
					<el-input v-model="filterText" :placeholder="placeholder" />

					<el-tree ref="treeRef" class="filter-tree" :data="data" :props="defaultProps" default-expand-all :filter-node-method="filterNode" />
				</el-card>
			</el-col>
			<el-col :span="20" :offset="0" class="p-1">
				<el-card :body-style="{ height: '100%' }">
					<fs-crud class="h-full w-full" ref="crudRef" v-bind="crudBinding"> </fs-crud>
				</el-card>
			</el-col>
		</el-row>
	</fs-page>
</template>

<script lang="ts" setup>
import * as api from './api';
import { ElTree } from 'element-plus';
import { ref, onMounted, computed, watch } from 'vue';
import { useExpose, useCrud } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
import MenuButton from './components/menuButton/index.vue';
import XEUtils from 'xe-utils';
const menuButtonRef = ref();
defineExpose(menuButtonRef);
// crud组件的ref
const crudRef = ref();
// crud 配置的ref
const crudBinding = ref();
// 暴露的方法
const { crudExpose } = useExpose({ crudRef, crudBinding });
// 你的crud配置
const { crudOptions } = createCrudOptions({ crudExpose, menuButtonRef });
// 初始化crud配置
const { resetCrudOptions } = useCrud({ crudExpose, crudOptions });

interface Tree {
	id: number;
	label: string;
	children?: Tree[];
}
const placeholder = ref('请输入用户');
const filterText = ref('');
const treeRef = ref<InstanceType<typeof ElTree>>();

const defaultProps = {
	children: 'children',
	label: 'name',
};

watch(filterText, (val) => {
	treeRef.value!.filter(val);
});

const filterNode = (value: string, data: Tree) => {
	if (!value) return true;
	return data.label.includes(value);
};

let data = ref([]);

interface APIResponseData {
	code?: number;
	data: [];
	msg?: string;
}

const getData = () => {
	api.GetList({}).then((ret: APIResponseData) => {
		const responseData = ret.data;
		const result = XEUtils.toArrayTree(responseData, {
			parentKey: 'parent_id',
			children: 'children',
			strict: true,
		});
		data.value = result;
	});
};

// 页面打开后获取列表数据
onMounted(() => {
	crudExpose.doRefresh();
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
</style>
