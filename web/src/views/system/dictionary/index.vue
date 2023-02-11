<template>
	<fs-page>
		<fs-crud ref="crudRef" v-bind="crudBinding"> </fs-crud>
		<subDict ref="subDictRef" :row-id="rowId"></subDict>
	</fs-page>
</template>

<script lang="ts" setup>
import { ref, onMounted, watch } from 'vue';
import type { Ref } from 'vue';
import { useExpose, useCrud } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
import subDict from './subDict/index.vue';

//字典配置ref
const subDictRef = ref();

const rowId: Ref<number> = ref(0);

defineExpose({ subDictRef, rowId });
// crud组件的ref
const crudRef = ref();
// crud 配置的ref
const crudBinding = ref();
// 暴露的方法
const { crudExpose } = useExpose({ crudRef, crudBinding });
// 你的crud配置
const { crudOptions } = createCrudOptions({ crudExpose, subDictRef });
// 初始化crud配置
const { resetCrudOptions } = useCrud({ crudExpose, crudOptions });

// 页面打开后获取列表数据
onMounted(() => {
	crudExpose.doRefresh();
});
</script>
