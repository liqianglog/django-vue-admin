<template>
	<fs-page>
		<fs-crud ref="crudRef" v-bind="crudBinding">
			<template #cell_url="scope">
				<el-tag size="small">{{ scope.row.url }}</el-tag>
			</template>
		</fs-crud>
		<!-- <permission ref="rolePermission"></permission> -->

		<el-drawer v-model="drawerVisible" title="权限配置" direction="rtl" size="60%" :close-on-click-modal="false" :before-close="handleDrawerClose">
			<template #header>
				<div>当前角色: <el-tag>管理员</el-tag></div>
			</template>
			<PermissionComNew v-if="drawerVisible" @drawerClose="handleDrawerClose" />
		</el-drawer>
	</fs-page>
</template>

<script lang="ts" setup name="role">
import { ref, onMounted } from 'vue';
import { useExpose, useCrud } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
//import permission from './components/PermissionCom/index.vue';
import PermissionComNew from './components/PermissionComNew/index.vue';

let drawerVisible = ref(false);

const rolePermission = ref();

// crud组件的ref
const crudRef = ref();
// crud 配置的ref
const crudBinding = ref();
// 暴露的方法
const { crudExpose } = useExpose({ crudRef, crudBinding });

const handleDrawerOpen = () => {
	drawerVisible.value = true;
};

const handleDrawerClose = () => {
	drawerVisible.value = false;
};

// 你的crud配置
const { crudOptions } = createCrudOptions({ crudExpose, rolePermission, handleDrawerOpen });
//const { crudOptions } = createCrudOptions({ crudExpose, handleDrawerOpen });

// 初始化crud配置
const { resetCrudOptions } = useCrud({
	crudExpose,
	crudOptions,
	context: {},
});
// 页面打开后获取列表数据
onMounted(() => {
	crudExpose.doRefresh();
});

defineExpose(rolePermission);
</script>
