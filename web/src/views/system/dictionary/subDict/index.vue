<template>
	<el-drawer size="70%"   v-model="drawer" direction="rtl" destroy-on-close :before-close="handleClose">
		<fs-page>
			<fs-crud ref="crudRef" v-bind="crudBinding"> </fs-crud>
		</fs-page>
	</el-drawer>
</template>

<script lang="ts" setup>
import {ref, onMounted, defineProps, computed, watch} from 'vue';
import { useExpose, useCrud } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
import { ElMessageBox } from 'element-plus';
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

//抽屉是否显示
const drawer = ref(false);

//抽屉关闭确认
const handleClose = (done: () => void) => {

	ElMessageBox.confirm('您确定要关闭?', {
		confirmButtonText: '确定',
		cancelButtonText: '取消',
		type: 'warning',
	})
		.then(() => {
			done();
		})
		.catch(() => {
			// catch error
		});
};
const {setSearchFormData,doRefresh} = crudExpose
defineExpose({ drawer,setSearchFormData,doRefresh });
// 页面打开后获取列表数据
onMounted(() => {
  // console.log(48,currentRow)
	crudExpose.doRefresh();
});
</script>
