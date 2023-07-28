<template>
  <fs-crud ref="crudRef" v-bind="crudBinding">
    <template #actionbar-right>
      <importExcel api="api/system/user/">导入 </importExcel>
    </template>
  </fs-crud>
</template>

<script lang="ts" setup name="user">
import { ref, onMounted } from 'vue';
import { useExpose, useCrud } from '@fast-crud/fast-crud';
import { createCrudOptions } from './crud';
import importExcel from '/@/components/importExcel/index.vue'

// crud组件的ref
const crudRef = ref();
// crud 配置的ref
const crudBinding = ref();
// 暴露的方法
const { crudExpose } = useExpose({ crudRef, crudBinding });
// 你的crud配置
const { crudOptions } = createCrudOptions({ crudExpose });
// 初始化crud配置
const { resetCrudOptions } = useCrud({
  crudExpose, crudOptions,
  context: {}
});

/**
 * 部门切换刷新用户列表
 */
const handleDoRefreshUser = (id: string) => {
  crudExpose.doSearch({ form: { dept: id } });
}

onMounted(() => {
  crudExpose.doRefresh();
});

defineExpose({
  handleDoRefreshUser
})
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

.font-normal {
  font-family: Helvetica Neue, Helvetica, PingFang SC, Hiragino Sans GB, Microsoft YaHei, SimSun, sans-serif;
}
</style>
