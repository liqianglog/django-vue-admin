<template>
	<el-drawer size="70%" v-model="menuButtonDrawer" direction="rtl" destroy-on-close :before-close="handleClose">
		<template #header>
			<div>
				当前菜单:
				<el-tag>{{ selectOptions.name }}</el-tag>
			</div>
		</template>
		<div>
			<fs-page style="margin-top: 60px">
				<fs-crud ref="crudRef" v-bind="crudBinding"> </fs-crud>
			</fs-page>
		</div>
	</el-drawer>
</template>

<script lang="ts" setup>
import { ref, defineProps, defineEmits, watch, toRaw } from 'vue';
import { useExpose, useCrud } from '@fast-crud/fast-crud';
import { createCrudOptions } from './curd';
import { ElMessageBox } from 'element-plus';
// 弹窗是否显示
let menuButtonDrawer = ref(false);
// 当前选择的菜单信息
let selectOptions: any = ref({ name: null });
const props = defineProps<{
	drawerShow: {
		type: boolean;
		default: false;
	};
	selectMenu: object;
}>();
const emit = defineEmits<{
	(e: 'drawer-close', value: boolean): void;
}>();

// 侦听弹窗变量
watch(
	() => props.drawerShow,
	(newVal) => {
		menuButtonDrawer.value = newVal ? true : false;
	}
);

watch(props.selectMenu, (val) => {
	selectOptions.value = val;
	doRefresh();
});

//抽屉关闭确认
const handleClose = (done: () => void) => {
	ElMessageBox.confirm('您确定要关闭?', {
		confirmButtonText: '确定',
		cancelButtonText: '取消',
		type: 'warning',
	})
		.then(() => {
			done();
			// @ts-ignore
			emit('drawer-close', menuButtonDrawer);
		})
		.catch(() => {
			// catch error
		});
};
// crud组件的ref
const crudRef = ref();
// crud 配置的ref
const crudBinding = ref();
// 暴露的方法
const { crudExpose } = useExpose({ crudRef, crudBinding });

const { doRefresh } = crudExpose;
// 你的crud配置
const { crudOptions } = createCrudOptions({ crudExpose, selectOptions });
// 初始化crud配置
// @ts-ignore
const { resetCrudOptions } = useCrud({ crudExpose, crudOptions });
// 你可以调用此方法，重新初始化crud配置
// resetCrudOptions(options)

defineExpose({ menuButtonDrawer, selectOptions });
</script>
