<template>
	<fs-page>
		<fs-crud ref="crudRef" v-bind="crudBinding"> </fs-crud>
	</fs-page>
</template>

<script lang="ts" setup>
import { ref, defineProps, watch } from 'vue';
import { useFs } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
// 当前选择的菜单信息
let selectOptions: any = ref({ name: null });
const props = defineProps<{
	selectMenu: object;
}>();

watch(props.selectMenu, (val: any) => {
	if (!val.is_catalog) {
		selectOptions.value = val;
		doRefresh();
	}
});

const { crudRef, crudBinding, crudExpose, context } = useFs({ createCrudOptions, context: { selectOptions } });
const { doRefresh } = crudExpose;

defineExpose({ selectOptions });
</script>
