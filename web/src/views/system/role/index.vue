<template>
	<fs-page>
		<fs-crud ref="crudRef" v-bind="crudBinding">
			<template #cell_url="scope">
				<el-tag size="small">{{ scope.row.url }}</el-tag>
			</template>
		</fs-crud>

		<permission ref="rolePermission"></permission>


			<PermissionComNew  v-model:drawerVisible="drawerVisible" :roleId="roleId" :roleName="roleName"  @drawerClose="handleDrawerClose" />

	</fs-page>
</template>

<script lang="ts" setup name="role">
import { ref, onMounted } from 'vue';
import { useExpose, useCrud } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
import permission from './components/PermissionCom/index.vue';
import PermissionComNew from './components/PermissionComNew/index.vue';

let drawerVisible = ref(false);
let roleId = ref(null);
let roleName = ref(null);

const rolePermission = ref();
// crud组件的ref
const crudRef = ref();
// crud 配置的ref
const crudBinding = ref();
// 暴露的方法
const { crudExpose } = useExpose({ crudRef, crudBinding });

const handleDrawerOpen = (row:any) => {
  roleId.value = row.id
  roleName.value = row.name
	drawerVisible.value = true;
};

const handleDrawerClose = () => {
	drawerVisible.value = false;
};

// 你的crud配置
const { crudOptions } = createCrudOptions({ crudExpose, rolePermission, handleDrawerOpen });

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
