<template>
	<fs-page>
		<fs-crud ref="crudRef" v-bind="crudBinding">
			<template #cell-rowHandle-right="scope">
				<el-button class="row-handle-btn" type="warning" size="default" @click="handleOpenRoleDrawer(scope.row.id, scope.row.name)"
					>权限管理</el-button
				>
			</template>
		</fs-crud>
		<el-drawer v-model="state.roleVisible" direction="rtl" destroy-on-close size="65%">
			<template #header="{ close, titleId, titleClass }">
				当前角色
				<div>
					<el-tag size="default">{{ state.roleDrawerTitle }}</el-tag>
				</div>
			</template>
			<span>Hi, there!</span>
		</el-drawer>
	</fs-page>
</template>

<script lang="ts" setup>
import { ref, reactive, onMounted } from 'vue';
import { useExpose, useCrud } from '@fast-crud/fast-crud';
import { createCrudOptions } from './curd';

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

const state = reactive({
	roleVisible: false,
	roleDrawerTitle: '',
});

const handleOpenRoleDrawer = (sign: string, title: string) => {
	state.roleDrawerTitle = title;
	state.roleVisible = true;
};

// 页面打开后获取列表数据
onMounted(() => {
	crudExpose.doRefresh();
});
</script>
