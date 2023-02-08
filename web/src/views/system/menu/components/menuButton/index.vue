<template>
  <el-drawer
      size="70%"
      v-model="drawer"
      direction="rtl"
      destroy-on-close
      :before-close="handleClose"
  >
    <template #header>
      <div>当前菜单:
        <el-tag>{{ selectOptions.name }}</el-tag>
      </div>
    </template>
    <div style="position: relative">
      <fs-page>
        <fs-crud ref="crudRef" v-bind="crudBinding">
        </fs-crud>
      </fs-page>
    </div>
  </el-drawer>
</template>

<script lang="ts" setup>
import {ref, onMounted} from 'vue';
import {useExpose, useCrud} from '@fast-crud/fast-crud';
import {createCrudOptions} from './curd';
import {ElMessageBox} from "element-plus";
import * as api from './api'
// 弹窗是否显示
const drawer = ref(false)
// 当前选择的菜单信息
const selectOptions = ref({name:null})

//抽屉关闭确认
const handleClose = (done: () => void) => {
  ElMessageBox.confirm('您确定要关闭?', {
    confirmButtonText: '确定',
    cancelButtonText: '取消',
    type: 'warning',
  })
      .then(() => {
        done()
      })
      .catch(() => {
        // catch error
      })
}
// crud组件的ref
const crudRef = ref();
// crud 配置的ref
const crudBinding = ref();
// 暴露的方法
const {crudExpose} = useExpose({crudRef, crudBinding});
// 你的crud配置
const {crudOptions} = createCrudOptions({crudExpose, selectOptions});
// 初始化crud配置
const {resetCrudOptions} = useCrud({crudExpose, crudOptions});
// 你可以调用此方法，重新初始化crud配置
// resetCrudOptions(options)
const initGet = ()=>{
  api.GetList({menu:selectOptions.value.id}).then((res:any)=>{
    const {data} = res
    crudExpose.crudBinding.value.data=data
  })
}

defineExpose({drawer, selectOptions,initGet})
</script>
